title: Codegate CTF 2015 pwn 1000 sokoban 
date: 2015-3-24 12:55
category: pwn 
tags: Codegate CTF, Off-by-one
slug: codegate_pwn_1000_sokoban

The challenge is a game that called **sokoban**. lol  
After we passed the first levels, we entered a menu and were able to choose the game mode.  
* * *

The menu looked like:  

> 1. Go to random infinite challenge mode  
> 2. Go to next stage  

Next, we opened IDA pro and reversed the binary.  
We could easily find the code like:  

```
if (playgame() == 1)
    get_flag();
puts(s);
return;
```

Then we traced how is the return value assigned......  

```
// just pseudo code
if (win)
  passed++;
return (passed == 228) ? 2 : 0;
```

228 is the amount of all levels.  
It seems impossible to arrive `get_flag()`. XD  
But our goal is very clear, **control the EIP and go to `get_flag()`**.  

We accidentally found the game sometimes generates a blank map in random mode then checks the rule of movement, it restricts the character by the element in the map, not the size of map.  
Therefore, once we could get the blank map, we were able to move the character to anyware in **bss segment** and **GOT segment**.  

There is the defination of elements:  

- \x00: nothing
- \x01: destination of box
- \x02: wall
- other: it's not important.

According to the rule of sokoban, we could push a byte onto `\x00` or `\x01`.  
It's very difficult to use......  
I tried to move the content of GOT at first, but I found GOT looks like:  

> <time@got.plt>:        0xf7ffafa0      0x00007fff      0x00400dd6      0x00000000  
> <wgetch@got.plt>:      0xf7bc2f90      0x00007fff      0x00400df6      0x00000000  
> <noecho@got.plt>:      0xf7bc0a50      0x00007fff      0x00400e16      0x00000000  
> <wmove@got.plt>:       0xf7bc4e40      0x00007fff      0xf799de70      0x00007fff  
> <mvprintw@got.plt>:    0xf7bc7db0      0x00007fff      0xf7bc0ad0      0x00007fff  

Almost all bytes are adjacent to each other.  
Therefore, we couldn't change the GOT area at most situation except ASLR was enable.  
For example, it's possible to make a libc address likes **0x7fffff00xx**.  
So we could modify a byte on GOT to somewhere in libc.  

Still seem useless....  
But after I checked all possible gadgets, I found a magic gadget at **0x3e260**.  
That is `add rsp, 0x28; (pop XX)*6; ret`.  
Furthermore, the address of `rand()` is **0x3d060**.  
If we modify `rand()` to that magic gadget, the return address is **0x401a9a** after we execute `rand()` again.  
Luckily, there are a hidden function in the game.  
If we press `v`, it will add 0x12 on **0x60c120**.  
And, 0x3e260 - 0x3d060 = 0x12......  

So, hence we had already bypassed the action of assign value to `EAX`.  
If we could control `EAX` and set `EAX = 1`, we entered the function `get_flag()`.  
Lucklily, if the argument of wgetch is \x00, the return value will be 1.  
On x86 architecture, the return value will be stored in `EAX`.  
`EAX` won't be modified until we call `rand()`.  
Finally, the program will print the flag. :)  

flag: `WH0n in OOme, ZZ as 12e RolanS`  
