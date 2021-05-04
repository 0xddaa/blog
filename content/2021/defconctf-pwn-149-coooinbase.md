title: DEF CON CTF 29 Pwn 149 coooinbase 
date: 2021-05-04 15:19
category: pwn
tags: DEFCON CTF, Stack Overflow, ARMv8, Shellcode
slug: defconctf_pwn_149_coooinbase

2020 一整年都沒發文 XD，去年只有打 DEF CON 初賽決賽而已，今年年初只打了 RealWorld CTF，現在比較少打 CTF，除了健康和體力不太能負荷，總覺得題目也沒有以前有趣了，大部分題目要花大量時間逆向，技術含量卻有限，常常辛苦逆向完或寫好工具，但解完這題之後就用不太上...不如把時間拿去挖 real world 的漏洞更有價值 QQ 這題在漏洞部分是比較簡單的題目，但利用這個漏洞需要發揮創意思考，如果沒有非預期的爛洞的話會是有趣的 pwn 題

* * *

題目連上後會是一個信用卡付款的 web 頁面，前端 post data 送到 ruby 寫的後端處理  
ruby 端會先檢查一下 card number 是否格式正確，然後將 post data 轉換成 **bson** 格式後用 base64 編碼透過 stdin 丟給 `x.sh` 執行  
`x.sh` 會跑 qemu arm64 kernel，kernel 再運行 userspase 的程式處理 base64 input，最後將 output 回傳給 web 顯示  
userspace 和 kernel 各有一把 flag，kernel 的部分是另一題 cooinbase-kernel，這篇 write-up 不會提到 kernel 部分   

這題的 kernel 部分不是 Linux Kernel，syscall 是自己定義的，userspace 也不是 ELF format，因此丟進 ida pro 沒辦法直接認出來  
需要自己標出 entry 再讓 ida pro 去解，userspace 的程式如果先看 kernel 應該可以很輕易找出來，但沒看可以更輕易找出來，因為 entry 就在 0 而已 XD  
接著是逆向的部分，userspace 是一個很小的 binary 叫做 `run`，沒有 library call，syscall 也跟正常 Linux Kernel 的不同，程式有自己包幾個常見 function，像是 `strcpy`、`memcpy` 之類的，有點像 IoT 上會跑的程式  

經過一番逆向之後可以看出程式的行為是：

1. 透過 getchar 的 syscall 跑 loop 讀 512 byte 進來再補 \0 做結尾
2. 將 input 做 base64 decode，得到 raw bson
3. 將 raw bson 進行初步處理成 bson object
4. 從 bson object 拿到 post data 中的 `CVC`, `MON`, `YR`, `CC`
    - 其中 `CC` 是透過 `bson_get_string` 取出，其他的是透過 `bson_get_int` 取出
5. 依序印出 **PROCESSED CC: **、**$CC**、**\n**

程式的漏洞在 `bson_get_string`，裡面會發生 stack overflow  
bson string 的格式是：`"\x02" + ename + "\x00" + p32(size) + data + "\x00"`  
`bson_get_string` 會先取得 size，再用類似 alloca 的行為將 stack 往上拉，然後用 `strcpy` 將 data 複製到 buffer 上  
因為沒有檢查 size 和 data 的長度是否一致，因此再 strcpy 時會發生 overflow，可以蓋掉 ret 控制 $pc   
但有個問題是，bson 是由 web 端的 ruby 構造出來的，我們沒辦法直接構造出 size 和 data 不一致的 bson  

嘗試解決這個問題時，發現送超長的 input 時 output 會多噴一次 **PROCESSED CC:**  
原因是程式其實會一直重複執行直到 `x.sh` 裡面的 `timeout 1` 中止 qemu 才停止  
我們送的長度如果在 base64 編碼後超過 512 byte，超出的部分就會到程式下次執行才被處理  
所以我們可以在控制 card number 的長度，讓 card number 的後半段變成下次執行的 input，就可以用後半段構造任意 bson  

由於 kernel 沒有實作 **ASLR** 和 **DEP** 的保護，因此接下來將 $pc 控到我們 input 的地方跑 shellcode 就可以 RCE 了  
...才怪，上面只是我天真的想法 = =  
要控 $pc 到 stack 上的時候發現 input 如果包含 `0x80` 以上的字元就沒辦法順利餵 input  
追蹤了一陣發現是在餵給 binary 之前 ruby 會用 regex 做檢查 card number  
如果 input 包含 `0x80` 以上的字元會發生 utf8 decode 的 exception，binary 從 input 拿到的只是 exception 的字串而已  
只要傳合法的 utf8 字串就可以了嗎 ? 但唯一能放 shellcode 的 buffer 只有 stack 上，會落在 **0xf000 ~ 0x10000** 之間  
而 `0xf0` ~ `0xff` 不可能在 utf8 的結尾出現，也就是說在 string-based 的 overflow 中我們沒辦法把 ret 蓋成 stack 上的 address  

我在這邊卡關了好一陣子沒想法，只好請求隊友的支援 QQ 大家努力一陣子之後，幾乎在同時間發現三個可行的做法：

1. 透過 SSRF 構造任意的 bson
    web 端的 ruby 是將 post form 轉送給 `http://#{env['HTTP_HOST']}/gen-bson"`，但 HTTP_HOST 是從 HTTP header 的 HOST 欄位可以控制，可以架一個 web server 直接在 /gen-bson 頁面回傳任意的 bson，連前面控制 card number 的長度都不需要 ... XD 因為不會過原本的 /gen-bson，也不會遇到 utf8 字元的問題，所以真的是超簡單蓋 ret 跳 stack 跑 shellcode 就結束了
2. 透過 alloca 將 `strcpy` 的內容蓋掉原本 codebase
    - 前面有提到 0 是這個 binary 的 entry point，由於 bson string 的 size 是我們可以任意控制的，因此有機會將 alloca 後的 buffer 拉到 codebase 的位置，這樣程式下一次執行時跑到 codebase 時就會跑我們的 code
    - 這個思路沒有實際嘗試，我把改掉 size 之後就沒有好好的跑到 `bson_get_string` 裡面，應該是弄壞了偽造的 bson 結構，要重新構造一下才有機會，另外 `strcpy` 寫的 shellcode 要避開 null byte 和 utf8 char 的問題，不是很好利用
3. 透過 `bson_get_int` 寫 4 byte shellcode
    - `bson_get_int` 可以讀 4 byte 到 x2 指到的位置上，而 overflow 完 x2 剛好是 bson 中 `CC` 結構的大小 (= size + 11)，我們可以跳到原本程式拿出 `YR` 的地方，將 YR 的值取出當成 4 byte 的 shellcode 到 `size + 11` 的位置，下次 overflow 再跳到 `size + 11` 跑 4 byte shellcode，跳到完整 shellcode 的位置
    - 由於 `bson_get_string` 已經先 parse 了 size 錯誤的 CC，因此我們需要在 CC 內部構造一個假的 bson object 讓拿完 size 之後，讓繼續爬 YR 的時候不會壞掉，細節請參考 exploit
    - size + 11 沒有對齊 4 byte，但不知道是 qemu 還是 kernel 沒有檢查要 alignment，所以直接跳過去就可以執行
    - 4 byte shellcode 和 full shellcode 都要避開 invalid utf8 char

比賽中是用 SSRF 拿到 flag，後續 kernel 題就可以寫一個超過長度的 read shellcode 來拿到 kernel flag  
賽後試了一下透過第三個思路也是可以達成目的，但 shellcode 就比較難寫一點，要閃掉 invalid utf8 char，kernel 的部分理論上也沒問題，但就懶得寫了 XD   

最後講一下寫 utf8 的 shellcode：
 
1. 透過類似 `add w0, w0, $imm` 的指令當成 `mov` 來控制 reg
    - 建議不要用 x 系列的 reg 否則會出現 invalid char
    - 裡面只有 $imm 有機會出現 0x80 以上的 char，遇上時可以 add 多次來閃
2. `svc 0` 結尾會包含 0xd4，因此下一條要是 0x80 以上的 instruction
    - 可以從 [arm developer](https://developer.arm.com/documentation/ddi0596/2021-03/Base-Instructions/B-cond--Branch-conditionally-?lang=en) 的文件中找隨便一條低位的 8 bit 可以任意控制、高位不包含 invalid char、而且不影響 shellcode 行為的指令
    - `beq 0x0030` = `\x80\x01\x00\x54` 可以滿足條件

exp: [coooinbase.py]({filename}/exp/coooinbase.py)
