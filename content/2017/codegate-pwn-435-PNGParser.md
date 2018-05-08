title: Codegate CTF 2017 prequals web+pwn 435 PNGParser 
date: 2017-2-13 11:34
category: web
tags: Codegate CTF, Stack Overflow, LFI
slug: codegate_web+pwn_435_pngparser

The challenges is more interesting than last year.  
However, why held the CTF on Friday? :(  
* * *

The problem description provided some website links for us. All of them are the same.  
There are two tags on the website. One of them is named `FILE UPLOAD`, Another one is named `INTERNET`.  
We could upload a PNG file from local or through internet.  
My teammate, **jeffxx** found there is a LFI vulnerability in `INTERNET` page.  
It can read any file after modified the protocol to `file://`.  
However, the flag doesn't located on the general path.  
We could not read the flag directly, but we could download the source.  
After reading source, we could find a elf file named `PNGParser` will be executed when the website handled the uploaded PNG file.  

`PNGPareser` must be executed with one argument `file_name`.  
It will parse the file and dump each entry in the file if the file is a legal PNG file.  
I decided to fuzz the binary after openen it wit **IDA Pro** because the parser is a little complicated.  
Luckily, the binary crashed easily and the error message was:

> \*\*\* Error in `./pngparser': double free or corruption (out): 0x089f0598 \*\*\*

Now, we knowed the crashed point at `0x089f0598`, but why it crashed ?.  
With the program slicing skill that I learned from Software Debugging, I found the fault is happened on `0x0804946d`.  
Heap overflow happened after the program called `memcpy()` and the buffer that stored the PNG content overwrote the top chunk.  
In order to understand what happened, we need to take a look on PNG stcucture before going on.  

```
/* Some members may not be exactly. Sorry for my indolence. */
struct PNG
{
  int status;
  char header[8];
  char next[4];
  int chunk_size;
  void *data_ptr;
  int size1;
  int size2;
  char *buf;
  char entry[80];
};
```

And here is a piece of pseudocode nearby `memcpy()`:

```
int parse_png(PNG *png, char *buf, size_t len)
{
  ...
  while ( i < len )
  {
    if ( len - i >= png->s1 - png->s2 )
      v4 = png->s1 - png->s2;
    else
      v4 = 2000;
    cmp_header(&png->header[4], "PLTE");
    memcpy(&png->buf[png->s2], &buf[i], v4);
    png->s2 += v4;
    i += v4;
    if ( png->s2 >= png->s1 )
    {
      v5 = parse_entry(png);
      if ( !v5 )
        return 0;
    }
  }
}
```


`len` is the return value of `fread()` in main function.   
Its maximum value is `0x10000` because the third argument of `fread()` is equal to 0x10000.  
We can control the value of `len` easily through cutting the PNG files.  
`parse_png()` will parse from the start entry (`png->header` == "\x89PDF\x0d\x0a\x1a\x0a") at first.  
Next, calulate the offset of next entry and parse each by each until reach `IEND` entry.  
We can construct a PNG file, which has a entry that the real size is smaller than the size field.  
And then, the condition `len - i >= png->s1 - png->s2` will be satisfied and `v4` will be set to 2000.  
Overflow will happened because the size of `png->buf` is determined by `png->chunk_size`.  

Sounds great. However, we still need to overcome a little trouble.  
First, each PNG entry has a crc field, so we cannot modify the PNG file directly.  
We must calulate the correct crc checksum for each entry in PNG file after modified.  
Second, `PNGParser` is a non-interactive program, it means ASLR will become a knotty problem.  
Most of heap exploitation skills need to know the memory layout.  
In fact, I didn't think out a efficient method to exploit this challenge through heap exploitation.  
However, at the same line, `memcpy()` is possible to trigger stack overflow !  

```
int parse_entry(PNG *a1)
{
...
    case 0xD:
LABEL_12:
      a1->status = 0xE;
      a1->s1 = 4;
      a1->s2 = 0;
      a1->buf = a1->next;
      goto LABEL_17;
...
}
```

There is a switch case in `parse_entry()`. Accoring to `png->status`, entry will be handle by different ways.  
In the most case, `png->buf` will store the address of malloc buffer, except `png->status` is equal 0xd.  
In this case, `png->buf` will point to the address of `png->next` and `png->status` become 0xe.  
Let's see where is the varaible `png` ... It is a local variable in `main()`.  
Thus, if the entry which status is equal to 0xe happened overflow, we can control the partial stack of `main()`.   

It seems to be left to do the ROP and shell out ... Not yet! O__Q  
Although we have overwriten the stack of `main()`, but we cannot go well to reach `return`.  
The segmentation fault will still happen in `feof()` because the file descriptor was overwritten.  
We must forge a fake FILE structure to prevent the program crashed.  
But, where can we forge the sturcture? Remember, we don't know the memory layout.  
I stucked at here for a while, then I found `tEXt` entry can help us!.   
The content of `tEXt` entry will be copy to the bss section whose address is `0x0804e4de`.  
Notice, null byte cannot appear in the `tEXt` entry, so we cannot forge it completely.  
Our goal is just that let `feof()` return gracefully. Luckily, the binary is x86 architecutre.  
Thus, we can reach the goal and forge the vtable in the FILE structure incidentally.  
I made one of vtable function to `add esp, 0xd8` and it will be used in `fread()`.  
After that, the control flow will enter our rop payload when executing `fread()`.  
Finally, we can do ROP easily and shell out! :)

exploit: [exp.py]({filename}/exp/pngparser.py)  

flag: `FLAG{sh3_1s_b3t1fu1_#$%}`
