title: 32C3CTF 2015 PWN 200 readme
date: 2015-12-31 18:21
category: pwn
tags: 3XC3CTF, bof, trick
slug: 32c3ctf_2015_pwn_200_readme

這題被安博給攔胡了 T\_T  
沒發現 rodata 有 flag 可以 leak XD  
* * *

這題一開始打開來看沒什麼頭緒  
然後一堆隊伍都秒解出來 = =  
嘗試塞很長的 payload 結果發生奇怪的 crash  
`__GI_getenv (name=0x7ffff7b9c26b "BC_FATAL_STDERR_",...`  
於是把 `LIBC_FATAL_STDERR` 當成關鍵字丟進 google  
找到一篇韓國 conference *inc0gnito* 的 [pdf](http://inc0gnito.com/Inc0gnito/ssp.pdf)  
裡面有提到觸發 stack guard 以後  
可以透過覆蓋環境變數 leak memory  

```
# sysdeps/unix/sysv/linux/libc_fatal.c
/* Open a descriptor for /dev/ttyunless the user explicitly
     requests errors on standard error.  */
  constchar *on_2 = __secure_getenv("LIBC_FATAL_STDERR_");
  if (on_2 == NULL || *on_2 == '\0')
    fd= open_not_cancel_2 (_PATH_TTY, O_RDWR | O_NOCTTY | O_NDELAY);
  if (fd == -1)
    fd= STDERR_FILENO;
```

只要把 `LIBC_FATAL_STDERR` 隨便設一個值  
程式就會被 stderr 的訊息給噴回來了  
開啟 stack guard 後如果發生 bof 會噴出像這樣的錯誤訊息：
> \*\*\* stack smashing detected \*\*\*: ./readme.bin terminated  
> Aborted (core dumped)  

pdf 提到透過覆蓋 `__libc_argv[0]`  
把內容改成我們想要 leak 的 address  
就可以達成 infomation leak  

```
# debug/fortify_fail.c
__libc_message(2, "*** %s ***: %s terminated\n",msg, __libc_argv[0] ?: "<unknown>");
```

這題很好心也很壞心的讓我們可以在 `0x600d20` 寫值  
但是那邊也是 flag 的位置...囧  
我們可以把內容設成 `LIBC_FATAL_STDERR=xxx`  
在 overflow 的時候在 552 offset 的位置蓋上 `0x600d20`  
就可以控制 `LIBC_FATAL_STDERR` 的值了  
這樣就可以把 stderr 噴回來  
剩下的問題就是 leak 什麼內容  
這題雖然看似在 `0x600d20` 會把 flag 內容覆蓋掉  
但是在 elf 初始化時會把字串留在 `0x400d20` rodata 段上面  
因此這題把 `0x400d20` 的內容 leak 出來  
就可以獲得 flag 了  

> Hello!  
> What's your name? Nice to meet you, .  
> Please overwrite the flag: Thank you, bye!  
> `*** stack smashing detected ***: 32C3_ELF_caN_b3_pre7ty_we!rd... terminated`  

exploit: [meh.py]({filename}/exp/readme.py)  

flag: `32C3_ELF_caN_b3_pre7ty_we!rd`  
