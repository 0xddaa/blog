title: Boston Key Party CTF 2014 Pwn 100 risc_emu 
date: 2014-3-2 23:50 
category: pwn
tags: BKTCTF, Out-of-bound
slug: bktctf_pwn_100_risc_emu

這次為期36小時  
題目很多 而且有些感覺很有趣  
可惜周六有點事情 這次沒辦法全程參與  
最後只拿到500分 好弱 ORZ  
* * *

這題是模擬 RISC CPU 的程式  
類型是 Pwning , ELF x64  
能執行類似 ARM 語法的模擬器  
> RISC CPU Emulator BkP 2014  
> Give me your bytecode!  
> Please give me your bytecode base64'd:  
> aaaa  
> Got it, executing aaaa now!  
> I don't recognize opcode 0x69  

我們可以給它一個 bytecode (須加密成 base64)  
格式為 \[opcode\] \[dst\] \[src\] \[value\] (會依據指令不同有所分別)  
dst 就是模擬的 register  
位於程式 heap 的某些區段  
能接受的指令有 9 種：  
`add`,`addi`,`sub`,`subi`,`xor`,`and`,`mul`,`div`,`term`  

reverse 以後發現處理指令的方式位於 `0x401c66`  
是以一個 function table 儲存每個指令的 address  
再由 `call eax` 的方式去執行  
接著繼續 trace 發現一個有趣的事情  
大部分的指令在 dst 都有做過濾  
如果 **>=8** 就會回傳 `ERROR!`  
只有 `addi` 和 `subi` 不會!  
這邊可以任意竄改 `0x604b50+0xff` 範圍之內的的值  
`0x604b50`~`0x604b70` 是模擬器中 register 的值  
而 0x604c10 開始就是 function table  
我們可以竄改 function table 到我們要的 eip  

到這邊為止都是正確的思路  
接下來我浪費了將近5小時在做 exploit...  
我發現不管輸入多長的字串  
emu 會切割成好幾個 4 byte 的指令並執行  
後面可以塞shellcode  
接著我企圖透過 `addi` 將其中一個 function 的值  
由 `0x40xxxx` 覆寫成 `0x60xxxx` 也就是 buf 的位置  
但是由於 emu 每次執行完指令後回將 return value 存在 heap 中  
執行超過12個指令將會蓋到題目的 heap guard  
將會出現：
> \*\*\* HEAP FUCKERY DETECTED \*\*\*: /home/dada/wargame/risc\_emu/emu terminated \*  
> Obtained 4 stack frames.  
> /home/dada/wargame/risc\_emu/emu() [0x4025f6]  
> /home/dada/wargame/risc\_emu/emu() [0x401bb2]  
> /lib/x86\_64-linux-gnu/libc.so.6(\_\_libc\_start\_main+0xed) [0x7ffff722976d]  
> /home/dada/wargame/risc\_emu/emu() [0x401379]  

但是如果我們輸入不只 4 byte  
後面的指令會繼續被執行  
並不會馬上將 return value 存到 heap  
於是還是可以將 function table 寫成 buf 的位置  
一切都就緒後我發現還是無法成功  
why? 因為這題有 DEP 囧!!!!!!!  
所以這一段基本上都是白費工夫  
因為所有能塞 shellcode 的區段根本沒辦法執行 Orz  

到這邊我就很賭爛的去睡覺了  
隔天起來突然發現這題原來got裡有一個 `system()` ...  
而且很剛好 在 `call eax` 到 emu function 的時候  
剛好 rdi 指向的是 buf 的位置.....OTZ (x64 參數指標是放在 rdi)  
所以這題只要：  

1. 用 addi 去改 function table 中一個 function 的值 ex: `term`
2. 第一個 byte 放 \x09 (`term` 的 opcode) 後面接 system 的參數

就可以任意執行指令了 ORZ  
此外這題已經把 stdout dup 到socket  
所以只要 `system("cat key")` 以後就有 key 了  

flag: `stupid_boston_leprechauns_and_geohots`  
