title: Olympic CTF 2014 10 point summary 
date: 2014-2-10 21:22
category: other
tags: Other CTF
slug: olympic_other_10_summary 

這次的戰績只有慘不忍睹....  
除了 web200 以外  
其他解出的題目都只有 10 分 Orz  
Web200 Orange 大大的 [write up](http://blog.orange.tw/2014/02/olympic-ctf-2014-curling-200-write-up.html) 已經很詳細了  
就不想再寫一份了 XD  
* * *

# Freestyle 10
## Trivial
> Hack the Planet\_

這題 hitcon 也有出過 XD  
google 一下就知道是驚嘆號了  
btw, 這題原出處好像是 defcon  

# CURLing 10
## Out there
> Flag is out there:  
> http://[2a02:6b8:0:141f:fea9:d5ff:fed5:XX01]/  
> Flag format: CTF{..32 hexes..}  

這題難點是ipv6...  
由於我的機器沒辦法設定ipv6 route  
所以一開始沒辦法解 XD  
後來是到學校以後才發現學校有辦法瀏覽ipv6的web  
寫個批次檔一次開啟一堆網頁 (chrome 超強!)  
結果只有這個有畫面：  
`http://[2a02:6b8:0:141f:fea9:d5ff:fed5:6901]/`  
看 source code 就找到flag了  


# Binathlon 10
## Just No One
> Here's your binary: setup.exe

這題是最白爛的一題 XD  
附檔是一個利用 inno setup 包裝起來的一個安裝套件  
有密碼!  
用 ollydbg bypass 密碼以後可以正確安裝  
點擊程式...只會看到無限迴圈一直印  
`You already saw the flag`  
一開始以為 flag 是安裝密碼  
但是 survey 以後發現 inno 比對的是 hash 過後的密碼  
所以 flag 應該不會在這  
隔天突然想通印出來的 msg 是提示  
然後把安裝前的 EULA 看一遍  
發現 flag 果然藏在那邊 XDD  
人生第一次認真看完 EULA....  

# Figure Crypting 10
## Crypting
> 43wdxz 4edcvgt5 65rdcvb 6tfcgh8uhb 9ijn

一開始以為是加密後的文字  
所以嘗試過 shift、substitution  
都解不出來.....  
後來自己打一遍發現這個string在鍵盤上的排列好像不太對勁...  
所以這五段代表的是五個英文字母...  
`sochi`  

# Nopsleigh 10
## As seen on DEFCON
> EBFE is to x86 as \_\_\_\_ is to ARM64  

這題我沒解出來 :(  
survey以後發現 `EBFE` 對於x86來說  
代表的是 `jmp 0x00`  
所以就會變成無窮迴圈  
對於 arm64 來說 指令就是  
`b 0` = `1400000`  
我到這邊為止就卡住了  
後來才知道 arm64 要 little-endian  
所以是 `00000014`.....
* * *
這次打完覺得自己還是太弱了 = =
比較需要技術性的都解到一半就解不下去
看來還需要多多加油 Orz
