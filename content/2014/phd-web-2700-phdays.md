title: phd CTF 2014 Web 2700 PHDays 
date: 2014-1-28 20:05
category: web
tags: Other CTF, SQL Injection, Frequency Analysis
slug: phd_web_2700_phdays

其實題目全名是  
*stand back, we have PHDays!*  
我去翻以前上課的投影片才發現關鍵  
好險以前有好好上課 XDD  
* * *

連到網頁經過檢查以後  
會發現存在 `index.php~` 這種暫存檔  
裡面有著登入的 source code  

裡面有一行：  
`$query = "SELECT username FROM users WHERE id='$uid'";`  
uid 並沒有做過濾，我們可以做 **SQL injection**  
但是...  

```
if(isset($_COOKIE['uid'])) {
  $uid = openssl_decrypt ($_COOKIE['uid'], $method, $key, false, $iv);
}
else {
  $uid = generateRandomString(32);
  setcookie("uid",openssl_encrypt ($uid, $method, $key, false, $iv));
}
```

uid 是從 *$_COOKIE* 得來  
但是被加密過了...  
加密的方式是 `$method = 'aes-256-ofb';`  
到這看似無解了  
AES 256 目前還沒有一個很有效率的演算法來破解  
但是仔細研究 ofb 這種 stream cipher  
![ofb.png]({filename}/images/phd_2014_phdays_1.png)  

在 key 和 iv 重複使用的情況下  
每次 encrypt 出來的 xor key 都會相同  
因此只要蒐集到夠多的 cipher  
就可以透過**頻率分析**的方式去解出 xor key  

由於密文長度只有 32  
蒐集的 cookie 其實不用太多 雖然越多會越準確  
我後來測試只要蒐集 100 個就足以解出 xor key 了  
將 cookie 做 urldecode 再做 base64 解碼  
才是正確的 cipher  
最後解出的 xor key 是: `8fd8392de73d15c49b7188ad91cdcad8cc7978e304d4acd2f336b275b18bcd32`  
有了這一串 xor key  
我們就可以把 payload 加密成正確的形式  
再做 **SQL injection**  

測試一下 `' or 1=1 or ''='`  
可以成功得到訊息變成 *Welcome, admin!*  
再做幾個測試  
發現存在 `password` 欄位  
所以把密碼給猜出來應該就是 key 了  
先試試長度: `' or length(password)=46 or '`  
發現密碼共 46 位  
接著寫 script 一個一個踹出正確的字元  
一開始用的 payload 是 `' or mid(password,pos,1)='a' xor'`  
但是會大小寫不分...而且不知道為什麼 *Y* 測試不出來 = =  
CTF 結束後我又試了一下  
原來直接用 `' or mid(password,1,1)='a`  
就可以試出來了 Orz  

> pos 1 is [5]  
> pos 2 is [0]  
> pos 3 is [M]  
> pos 4 is [3]  
> pos 5 is [7]  
> pos 6 is [I]  
> pos 7 is [M]  
> pos 8 is [3]  
> ...  

flag: `50M37IM35_Y0U_D0_N07_N33D_A_K3Y_70_D3CRYP7_AES`  
