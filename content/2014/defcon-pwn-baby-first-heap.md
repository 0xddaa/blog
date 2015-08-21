title: Defcon 22 Quals Baby's First heap 
date: 2014-5-20 1:31
category: pwn
tags: DEFCON CTF, hof
slug: defcon_pwn_baby_first_heap 

這題是第一天在看的  
在嘗試做 payload 時 **jeffxx** 就解完啦 XD  
不過還是厚著臉皮寫一下 write up  
* * *

連上去環境後得到這樣的訊息：
> Welcome to your first heap overflow...  
> I am going to allocate 20 objects...  
> Using Dougle Lee Allocator 2.6.1...  
> Goodluck!  
> Exit function pointer is at 804C8AC address.  
> [ALLOC][loc=9DE4008][size=1246]  
> [ALLOC][loc=9DE44F0][size=1121]  
> ...  
> Write to object [size=260]:  
> 123  
> Copied 4 bytes.  
> [FREE][address=9DE4008]  
> [FREE][address=9DE44F0]  
> ...  
> [FREE][address=9DE84B0]  
> Did you forget to read the flag with your shellcode?  
> Exiting  

好像就只是個簡單的 heap overflow ?  
一開始以為要用舊的環境才能測  
就用 2.6.32 在 debug  
後來發現 `free()` 好像是程式自帶的  
我在 3.8.0-29 測試也沒問題  
(有錯請告知 QQ)  

這題會 allocate 20 次空間  
接著讓我們輸入一個字串  
把字串 copy 到 第 10 個空間  
再把 20 個空間給 free  
隨便輸入一下 發現 >=260 個 byte 就會 crash  
直接開 gdb 去看原因  
是死在這一行  

```
0x80493f6 <free+273>:        mov    DWORD PTR [eax+0x8],ed
eax            0x61616161  
edx            0x61616161  
```

看起來這邊可以任意寫入記憶體  
嘗試一下把題目的 `exit_func` 改掉  

```
0x80493ff <free+282>:        mov    DWORD PTR [eax+0x4],edx
eax            0x61616161
edx            0x804c8a4 
x/xw 0x804c8ac
0x804c8ac <exit_func>:  0x61616161
```

喔喔 成功改掉了 但是依然 crash  
所以要 jmp 的位置也要可寫入才行  
不過 heap 本來就能寫所以沒啥問題  
就正式來一次吧  

```
0x80493f6 <free+273>:        mov    DWORD PTR [eax+0x8],edx
eax            0x0
edx            0x0
0x804c8ac <exit_func>:  0x0804f350
```

WTF? 還是 crash  
原本以為是 overwrite 失敗  
但是仔細一看問題是出在下一次 call free 才 crash  
我卡在這時 jeffxx 就解完了 XD  
原本是打算去改 `free()` 的 GOT  
才發現 `free()` 寫死了沒辦法改  
不過還有個 `printf()` 可以改  
`printf()` 的位置在 0x0804c004  
要跳轉出來的位置就是他 print 出的第 10 個位置 XDDD  
最後的 payload 是：  
`[jmp addr][0x0804c000][nop][addr]`  

剩下就是寫 shellcode 了  
因為會 write 兩次  
我是第二次才 overwrite GOT  
由於第一次會把 jmp addr +8 的地方改成 `0x0804c000`  
要記得被改爛的這 4 byte 給跳開  
這樣就成功拿到 shell 了  
