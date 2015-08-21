title: ACTF 2014 Crypto 老大哥aay的秘密
date: 2014-4-14 21:19
category: forensic
tags: XCTF
slug: actf_forensic_100_aay_secret

期中考完了來補一下 ACTF write up  
打完 plaidctf 覺得自己跟 學長 Orange 217 等大大  
差距十分之大 Orz  
要花更多時間練習才行 QQ  
* * *

這題給了一個 rar 的檔案  
裡面包含 7 個檔案，每個 5 byte  
猜測應該是可以從 CRC32 brute-force 出結果  
測試一下  
`echo -ne 'ACTF' > tmp; crc32 tmp; cat tmp`  
> 76f37a57  

跟 rar 的檔案吻合  
應該可以確認猜測無誤  

接著要去 survey CRC32 的算法  
結果就找到現成的 code  
[http://www.opensource.apple.com/source/xnu/xnu-1456.1.26/bsd/libkern/crc32.c]  
open source 所以可以隨便改 XD  
改成 linux 的版本以後就可以開始跑了  
因為是 flag 所以應該只有 printable  
測試 32 ~ 126  
約 5 分鐘跑出結果  

flag: `ACTF{ch3ck5um_l34k_y0ur_1nf0m4710n}`  
