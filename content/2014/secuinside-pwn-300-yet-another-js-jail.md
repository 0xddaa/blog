title: Secuinside ctf 2014 pwn 300 yet-another-javascript-jail
date: 2014-6-6 3:33
category: pwn
tags: OtherCTF
slug: secuinside_pwn_300_yet_another_js_jail 

這題沒解出來 QQ  
找錯 CVE 真是太囧了  
如果找對個應該是有機會可以解出來吧...  
* * *

這題是一個 javascipt 的 jail 環境  
可以任意執行一些 js 的指令  
part1 dm4 秒殺了 XD  
做法是 overwrite `Array.prototype.toString`  
過 part1 以後得到一個 elf  
不看還好...reverse 以後嚇一跳  
根本就是一個 v8 engine = =  

比對 `RunShell()` 和 example code 以後  
沒看到什麼能利用的地方  
初步判定洞是在 v8 裡面  
而且上一題的 jsjail 版本比較新  
就猜這題的解法應該跟 cve 有關  
結果找錯個 e04...  
[http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-1705]  
這個才是正確的 = =  
被分類在 chrome 裡面 之前用 v8 下去找沒看到  
這是一個可以任意讀寫記憶體位置的漏洞  
[poc](https://code.google.com/p/v8/source/browse/branches/3.24/test/mjsunit/regress/regress-crbug-351787.js)

```
var ab4 = new ArrayBuffer(8);
ab4.__defineGetter__("byteLength", function() { return 0xFFFFFFFC; });
var aaaa = new Uint32Array(ab4);
```

關鍵代碼是這三行  
執行這三行以後就可以透過 `aaaa` 的 pointer 去任意讀寫 memory  
原理我實在是找不到說明 也 trace 不出來 Orz  
不負責任猜測是將 array 的長度設成超大  

執行 poc 後在 `ExecuteString()` 的地方確認 memory 的狀態  
會發現 heap 中有大量的區塊都被改成 `aaaaaaaa`  
一直往上爬就可以推算出 `aaaa` 的 pointer 位於 `0x09196eb8`  
所以我們透過 `aaaa[i] = 0xAAAAAAAA` 的方式就可以改寫記憶體了  
但是要 overwrite 哪裡 ... ?  
仔細觀察後發現讀取指令的部分是利用 `fgets()` 去得到 input  
got table 也是可以被 overwrite 的區域  
因此目標應該就是將 `fgets()` 換成我們要的區域了  
(不過在這邊我沒有看到 system() 之類的 function 好利用...)  
(別人的 write up 寫有 system 可以跳)  
(在想是否因為題目環境是 ubuntu 14.04 的關係...)  

but `fget()` 在 got table 的位置是 `0x091680a8`  
欸...嘗試一下 index 好像不能用負數  
這樣豈不是改不到嗎...?  
卡關很久才發現這邊有 interger overflow 的情況  
這邊取得 dst pointer 的做法是 `*aaaa + index*4`  
因此只要 index 夠大  
就會被當成負數做判斷  
如此一來就能任意跳轉記憶體位置了  

btw 聽說這個 cve 是 tomcr00se 舉報的 XDDD  
