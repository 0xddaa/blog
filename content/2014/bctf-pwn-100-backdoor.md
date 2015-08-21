title: BCTF 2014 PWN 100 後門程序
date: 2014-3-12 18:12 
category: pwn
tags: XCTF
slug: bctf_pwn_100_backdoor

這題算是很基本的 pwn  
但是可能因為中間有點小陷阱  
所以解出來的人不多 (?  
* * *

連到目標環境後會印出一堆歌詞 (?  
輸入 n 就離開程式，不然會在印一次歌詞  

> ...  
> Drink all the booze  
> Hack all the things  
>  
> Replay?(y/n)  

檢查程式以後  
程式有故意留下的 backdoor  
只要 input 符合條件  
就會跳轉到 buf 執行 shellcode  
行為如下：

1. 判斷 input 第一個字是否為 'n' or 'N'，是則終止程式  
2. 將 input 與 `<baidu-rocks,froM-china-with-love>` 做 xor 加密  
3. 如果 xor 後前面 10 byte == 'n0b4CKd00r' 就轉到 buf + 1  

所以我們要計算 `n0b4CKd00r` + `shellcode` xor 後的值
但是陷阱在於 scanf 讀到某些字元就會終止 `ex: \x00`  
導致 shellcode 沒有完全被載入  
還好這題沒有對 shell code 長度做限制  
可以靠塞 nop 調整 shellcode 的 offset 來避開特殊字元  
接著就發現 `/home/ctf/flag.txt` 底下有答案了  

flag: `BCTF{H4v3-4-n1C3-pWn1ng-f3sT1v4l!!}`  
