title: CSAW CTF 2015 web 500 Weebdate
date: 2015-9-22 0:24
category: web
tags: CSAWCTF, LFI, sqli
slug: csawctf_web_500_weebdate

這題能解出來要歸功於  
**ding**, **happyholic1203**, **mangoking**, **jpeanut**  
已經把前面的問題都找出了  
我其實只是撿尾刀而已...  
* * *
不過還是厚著臉皮寫一下 write up  
不然這邊 web 分類文章都空空蕩蕩...  

這題的背景故事是  
有一個叫做 **Donald Trump** 的傢伙在這個交友網站註冊了帳號  
用來當作販毒的聯絡管道云云  
需要破出他的二段式認證 (`password` + `TOTPKEY`) 登入他的帳號  
這題的 `flag = md5(TOTPKEY + password)`  

這個交友網站除了一般的帳號密碼以外  
還需要填入 oauth 解 `TOTPKEY` 的結果才能成功登入  
可以用以下指令來解:  
`oathtool --base32 --totp AAAAAAAAAAAA`  
得到的結果是一個 6 位數字  
會隨時間改變, 所以要趕快登入 XDD  
註冊的時候試了一下如果帳號前四碼相同  
`TOTPKEY` 得到的結果都一樣  
一開始以為只要註冊前面開頭一樣的帳號  
就可以拿到 `TOTPKEY`了 (後來才發現事情沒這麼簡單 Orz)  
所以把目標先鎖定在拿到 `password`  
登入之後有幾個功能:

- Edit Profile
- Search User
- Send Message

...沒有登出, 想換帳號都要刪 cookie 超麻煩 = =  
cookie 的格式是 `username_timestamp_sha1ofsomething`  
原本在猜後面的 sha1 可能跟密碼有關  
打算試試看能不能偷到 **Donald Trump** 的 cookie  
`Send Message` 其實沒有對特殊字元作過濾  
可以完整個插入 `<script>alert(1);</script>` 到網頁裡面  
但是, _*沒有任何反應*_ ......  
仔細研究了一下, 發現網站的 header 有加入 CSP  
CSP 可以限定那些才是合法的 js 來源  
這個網站的設定只有源自 [https://api.google.com]() 才可以被執行  
因此插入的 XSS 這招是無效的...  
查了很久都沒有可以繞過的方式 Orz  

不過也不是毫無所獲  
從 CSP header 發現了一個 uri: `report-uri /csp/violate`  
接著追到 [http://54.210.118.179/csp/view]() 這個頁面  
有趣的是...這個頁面存在 **SQL injection** 的問題  
把所有欄位拉出來之後, 發現存在 `user_password` 這個欄位  
`user_password` 的結果是 sha256 hash  
做幾個實驗後, 發現應該是加入 username 當成 salt  
結果會是 `user_password = sha256(username+password)`  
把結果拿去爆一下 得到密碼是 `6`  
(這邊我們弄錯帳號名稱了, 所以真正的密碼不是這組 XDD)  
搭配剛剛用開頭相頭所得到的 `TOTPKEY`  
拿去做 md5 再送記分板就得到.... _Wrong flag_  

事實上根據剛剛的 `TOTPKEY` & `password` 也沒辦法成功登入  
後來討論時某人發現昨天和今天註冊的 `TOTPKEY` 不一樣  
原本在想是不是加入時間因素下去算  
但是又有人說昨天和今天註冊的帳號 `TOTPKEY` 都一樣...XD  
後來想想應該不是時間, 可能是 ip 之類的因子  
但是我們還是不知道 `TOTPKEY` 是怎麼拿到的...  
只好尋找其他的方向  

那這個網站除了 sqli 以外  
其實還有 LFI 的問題  
`Edit Profile` 的功能有一個設定頭像的功能  
會讀外部的 url, 並檢查是不是圖片  
如果是的話設定成頭像  
如果不是圖片就會跳 Exception  
然後把檔案內容當成錯誤資訊印出來  
在這邊做了各種嘗試  
像是去撈 apache 的設定檔  
還有 `settings.py` 以後  
最後猜到網頁是寫在 `/var/html/weeb/server.py`  
閱讀原始碼後, 發現 `TOTPKEY` 的算法如下:

```
 34 def generate_seed(username, ip_address):
 35     return int(struct.unpack('I', socket.inet_aton(ip_address))[0]) + struct.unpack('I', username[:4].ljust(4,'0'))[0]
 36
 37 def get_totp_key(seed):
 38     random.seed(seed)
 39     return pyotp.random_base32(16, random)
```

的確如我們所推測是靠 `username` + `ip` 去算的  
但只是當成 seed 接著還要取 random XD  
到這邊幾乎就已經解出來了...可以成功登入  
只是送 flag 還是發現不對  
原因是弄錯帳號啦~~~
正確的帳號應該是 `donaldtrump` 才對 = =  
那密碼用 `rockyou.txt` 就可以破出來了~ 結果是 `zebra`  
最後做 `md5("6OIMTPLHSQ6JUKYPzebra")` 就是這題的 flag 了 XD  

flag: `a8815ecd3c2b6d8e2e884e5eb6916900`  

