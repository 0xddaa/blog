title: 0CTF 2018 Pwnable 478 Zer0 FS
date: 2018-4-6 22:51
category: pwn
tags: 0CTF, Linux kernel
slug: 0ctf_pwnable_478_zer0fs

The problem was solved with **jeffxx**, **atdog** and **lays**  
Most of exploit was written by **atdog** during the competition and I rewrote the exploit for the write-up.  

* * *

## Analysis

We will enter a shell that building by KVM after ssh connection enbalished. The discription said the flag is `sha256(/root/flag)`, but we had no permisson to read it. As other Linux kernel challenge, our target is obtaining the root priviledge, then we can calculate the hash of `/root/flag`.  
There are two setuid programs under the root directory. One of them is `/mount`. Try to execute `/mount` but the error message is as below:

> mount: mounting /tmp/zerofs.img on /mnt failed: No such file or directory

After created `/tmp/zerofs.img`, we got another error message:

> mount: mounting /dev/loop0 on /mnt failed: Device or resource busy

Well, maybe we should make a normal image at first. Aside from creating image, let's see what files the challenge gave.

```
-rw-r--r-- yoghur7/yoghur7 7173904 2018-03-29 03:42 public/bzImage
-rw-rw-r-- yoghur7/yoghur7 3229184 2018-03-30 01:13 public/rootfs.cpio
-rw-r--r-- yoghur7/yoghur7  326664 2018-03-29 03:42 public/zerofs.ko
-rwxrwxr-x yoghur7/yoghur7     240 2018-03-29 03:42 public/run.sh
```

`run.sh` is a shellscript to start the challege environment by kvm (or qemu). Notice, the arguments include `-initrd`. It means the rootfs is made by ramdisk and files will be stored in memory. I used the feature for exploit this challenge.  

Obviously, we should analysis `zerofs.ko` at first. **jeffxx** found a repository called [simplefs](https://github.com/psankar/simplefs) which is very similar with zerofs.ko, but a little difference still exists, such as the inode structure and super block. We made a little [modification]({filename}/exp/0001-make-zerofs-image.patch) after reversing `zerofs.ko` and we could make a legal image thourgh `mkfs-simplefs`. By the way, I didn't attend the reverse stage ... I was stucking in **Might dragon** at that time. Orz  

## Vulnerability

1. `zerofs_write`: There was a buffer overflow when using `copy_from_user` but it didn't check the boundary. This vulnerabiliy wouldn't be use in my exploit.
2. `zerofs_read`: It checked that the length must be smaller than file size. However, because we could control the full file system, we could make an illegal file which file size is not equal to the real size (see [patch2]({filename}/exp/0002-illegal-size.patch)). After that, it will leak extra data in kernel memory when reading the file.
3. `zerofs_lleek`: Exist the same problem that mention in `zerofs_read`. We could call `lseek` to control the position of the file.

We could combine `llseek` with `zerofs_read` to leak the data more easier or `zerofs_write` to avoid breaking some important sturcture.  


## Exploit

Our target is getting the root priviledge and reading `/root/flag`. As above mentioned, the rootfs was on kernel memory, so we could modify the file throught arbitrary write in `zerofs_write`. I also noticed that both `/mount` and `/umount` are setuid programs. We could replace a part of file content to our shellcode. I think it is the easiest way to reach our target.  

Now, we almost had an arbitrary read or write on kernel memory, but we could not confirm the offset because the randomization of kernel heap mechanism. Thus, we must to identify the distance between the overflowed buffer and the rootfs.  

I disabled KASLR and use gdb to watch the kernel memory. It looks like below:

```
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
    0x7ffe4e844000     0x7ffe4e847000 rwxp     3000 0          <=== user space program
0xffff880002dbd000 0xffff8800035bd000 rwxp   800000 0          <=== overflowed buffer
0xffff880003614000 0xffff880003e14000 rwxp   800000 0          <=== rootfs
0xffffc900001c2000 0xffffffff82203000 rwxp 36ff82041000 0      [stack]
0xffffffff8143a000 0xffffffff81c3a000 rwxp   800000 0
0xffffffffbffff000 0xffffffffc0004000 rwxp     5000 0
```

I noticed that the offset of rootfs is fixed, but the offset of overflowed buffer would change. I'm not sure the reason, maybe it was generated dynamicly by `__bread_gfp`? Despite sometime it would be the same, I wanted to make a stable exploit because it was annoying to upload file to the remote environment.  

We could write a program that keeps adjust the position by `lseek` and leaking memory by `read`, then checking if the leaked data contains the specified pattern. I chose a string **/bin/mount** to be the pattern because it occurs in rootfs once and it is used by `/mount`. After finding the pattern, we could add or minus the offset to modify any file on rootfs. The proof-of-concept is as below:

```
for (int i = start; i < end; i++) {
    lseek(fd, i * 0x1000, SEEK_SET);
    read(fd, buf, 0x1000);
    if (search(buf, PATTERN)) {
        printf("offset = %d\n", i);
        off = i * 0x1000  - 0x94000 + 0x1081;
        break;
    }
}
```

Finally, adjust the file position to the calculated offsetand and write a shellcode to execute `/bin/sh`. After that, execute `/mount` again. We could get a shell with the root priviledge. :)

## Note

There are some detail about making the exploit.

1. For local testing, I wrote a script to repack rootfs into a cpio file. The image and exploit will in the file system after rebooting.
2. Adding `-s` into the arguments when starting qemu and using gdb remote attach to debug my exploit.
3. Modify `/init` to initialize something, such as mount /tmp/zerofs.img and set priviledge to root.
4. The environment linked most of binary to busybox. Thus, I uploaded the image and exploit by copy-paste base64 string and decode them back to the binary. Is there a better way?
5. I needed to keep the size of exploit small because using copy-paste to upload, but there is no glibc in the environment. Thus, I compiled my exploit with [dietlibc](https://www.fefe.de/dietlibc/).
6. As our expectation, we could not find the pattern like `flag{` directly, because `/root/flag` is a pure binary file.

flag: `flag{600291f9a05a1e78215aa48c9ff6a4b1bb207c2b4ffa66223fcc67c04281397f}`  

exploit: [exp.c]({filename}/exp/zerofs.c)  
