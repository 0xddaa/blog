title: Boston Key Party CTF 2016 Reverse 3 Harvard Jit in my pants
date: 2016-03-15 23:00
category: reverse
tags: BKPCTF, 
slug: bkpctf_reverse_3_jit_in_my_pants

剛從成功嶺出來就撞上這場 CTF ... XD  
果然是醬油到爆  
雖然去成功嶺之前大概也差不多吧 囧  
* * *

題目給了一個 elf 超混亂 看不懂  
但是包含了一些奇怪的字串  
丟去 google 可以發現這個 elf 是由 **MyJIT** 寫成的程式  
[MyJIt]()  
其實從題目名稱大概就猜得到這題是 just in time 生成的程式  
所以直接逆 elf 是很難看出程式邏輯的  

第一件事情就是 dump 出程式實際在執行的 code  
先用 `ltrace` 稍微看一下程式在幹麻  
經過一連串不知所云的 `malloc` & `free` 之後  
發現最後會用 `puts` 印出 _NOPE._  
可以直接在 puts 下斷點  
會發現有一塊 rwx 的 memory 在 `0x778000`  
dump 出來就會是 runtime 實際在運作的程式了  

轉回 asm 會發覺整段只有一個 function  
不知道能不能丟回 ida 轉 pseudo code...  
如果有人知道怎麼做麻煩教我一下 QQ  
這段 code 跳來跳去而且用了很多不常見的指令  
靜態分析看不太懂  
追一追就掉到 loop 裡了  
loop 裡會一直 call 那堆不知所云的 `malloc`  
> 0000000000778144 ff95f8feffff     call qword [rbp-0x108]  

在這邊卡了一陣子  
後來回去追 elf 的流程發現 `0x4473ef` 在處理 output 訊息  
字串不是直接放在 rodata  
而是一個 byte 一個 byte 處理  
做出字串再丟到 `puts`  
所以一開始沒有發現這個 function ...  
`0x4473ef` 會根據第一個參數的內容是 0 or 1 or 2  
決定要印出哪個字串 (Nope/Congraz.../Usage)  
往回追是什麼地方會 call `0x4473ef`  
結果發現跟 call malloc 的是同一行...囧  
繼續往回追 rdi 是怎麼來的  
跟蹤一連串的 jmp 以後  
大概三四次吧 其實沒有很多  
可以找到比對 flag 的關鍵點 而且是線性比對  
所以可以用爆破的方式一個一個 byte 爆出 flag
 `0x77827f` 會將正確的長度放在 rcx  
因此只要看目前正確的長度數量  
就可以判斷有沒有猜對了  
後面生成 flag 的部分我就懶得看了  
直接用爆破的方式爆出 flag  

順帶一提 我一直以為 bostonkeyparty 的縮寫是 BKT  
前面先打好 prefix 結果怎麼爆都不對...

flag: `BKPCTF{S1de_Ch4nnel_att4cks_are_s0_1338}`  

