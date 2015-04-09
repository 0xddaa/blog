title: CSAW CTF 2014 pwn 300 ish
date: 2014-9-23 9:23
category: pwn
tags: CSAWCTF, memory leak
slug: csawctf_2014_pwn_300_ish

接觸 CTF 一年整了...  
好像進步很多 卻又好像什麼都一樣 (嘆  
最後 400 分體力不支了  
隔天才解出有點可惜 QQ  
* * *

*ish* 是一個模擬 shell 的程式  
有以下幾個指令：  

- *ls*
- *cat*
- *ping*
- *admin*
- *login*
- *run*
- *sleep*
- *lotto*
- *quote*
- *run*
- *exit*

把程式都看過一遍以後  
比較可疑的有 *cat*、*run*、*login*、*lotto*  
其他都毫無意義  

*cat* 會去開一個檔案  
但是開啟參數有問題  
檔案不存在就會生一個出來...已存在就會回傳錯誤直接 return  

*run* 是把指令切割後  
第一個參數丟到 `system` 呼叫  
不過第一個參數一定是 *run*...  
依然無法利用  

*login* 會再開一次 shell  
檢查帳號是不是 *root*  
是的話就會要求密碼  
並從 *key* 這個檔案讀 64 byte 後並比對  
但是如果密碼長度超過 64 byte  
`memset` 不會被觸發到  
密碼會被留在 stack 中  

*lotto* 有 **uninitial varaible** 造成的 memory leak  
可惜是用 `%u` 去印  
沒辦法自由調整位置  

這樣看完思路就很明確了  
利用 *login* + *lotto* 去 leak 出 flag  
而且出題者還很好心在這兩個 function 一開始 print 出 variable 的位置 = =  

雖然很快就找到方向  
這題還是卡了一段時間.....  
如果照正常的順序開一個 shell 再執行 `lotto`  
能 leak 的位置剛好在 `flag[64]` 結束  
剛好是 **stack guard** ...  
試了各種指令的組合也沒辦法調整 `esp`  
一度以為這題是 bof = =  

最後逐步比對 assembly  
才發現問題出在 *alloca* 這個 function  
一開始以為這個指令是和 `malloc` 類似  
但 `alloca` 是會在 stack 中把 esp 的位置向上拉來增加空間  
再把新的 esp 回傳  
因此可以利用這個指令來調整 *lotto* 所 leak 出的位置  

所以只要透過調整 `uname` 的長度來控制 stack  
就可以 leak *lotto* 之前的任意 address 了  
觸發順序如下:  

1. *login with short uname*
2. *login with root*
3. *exit*
4. *login with long uname*
5. *lotto*

flag: `AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMOOOOXX`  
