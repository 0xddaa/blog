title: Cyber Readiness Challenge 2014 Level 1 Summary
date: 2014-4-2 22:51
category: other
tags: Other CTF
slug: cyber_readiness_challenge_level1_summary

今天跟 **jeffxx** 和 **atdog** 參加賽門鐵克主辦的 CTF  
見識到好多平常只有在網路上看過 id 的 大大 (worship)  
題目還滿有趣的~ 從中學到不少東西  
希望以後還會有機會參加 XD  
* * *

故事背景是一個因為咖啡廳漲價而心生不滿的中二顧客  
決定黑咖啡廳的網路當作報復 (誤  

題目環境給了一個 ip *10.1.1.10*  
連過去會到咖啡廳的網站  
(因為題目環境是封閉的 所以只能稍微記錄一下做法了 ><)  

##Problem 1 300  
這題敘述是要找出咖啡廳是用什麼軟體架設的  
點開 source code 就看到註解裡面有記錄了  
flag: 忘了  

##Problem 2 500  
這題是要找到一個還沒使用過的優惠券  
點到網頁 *deals* 的分類會看到兩個優惠券  
當然都不是 flag  
url 大概長這樣 `http://10.1.1.10/xxxx/deals/1`  
很直覺的去改一下後面的參數  
改成 0 就發現多噴一個優惠券  
也就是此題的 flag  
flag: 忘了  

##Problem 3 1000  
這題是要我們找出隱藏的菜單或 *shopadmin* 的 password  
上一題的 url 有 `SQLi` 的漏洞  
但是我用 **sqlmap** 爆不出來 QQ  
在用掉一個有等於沒有的提示後 (try sql syntax in url ... 類似這樣)  
確定是 SQli 的漏洞  
手動塞 payload  
得到 *shopadmin* 的 `md5(password)`  
拿去反查後得到 flag  
flag: `brewster`  

##Problem 4 500
某個 file 記錄著可以存取 WIFI 的 **access code**  
flag 是 file 的完整路徑  
這題也是在網頁上找了很久  
結果用了提示才知道是要用 ssh 連進去 .\_.  
file 就在家目錄下  
flag: 忘了  

##Problem 5 300  
要求 WIFI **access code**  
就在剛剛的檔案裡 送分題  
flag: 忘了  

##Problem 6 500
前面一堆描述忘記是啥了  
總之要找出 *10.1.2.15* 的 hostname  
原本以為是用剛剛 ssh 進的主機去反解  
結果不是 =.=  
這台有開 **netbios** 的 port  
google 一下可以用 **netscan** 去掃  
就得到 hostname 了  
flag: 忘了  

##Problem 7 1000  
打進去就對了 bj4  
這題用到的漏洞是 **MS08-067**  
第一次用 **metasploit** XD  
還好這題沒更動什麼  
照著教學做就過了  
可是我前面不小心按到這題的 hint ... 悲劇  
flag: `emploees.zip`  

##Problem 8 300  
該題環境還有另一個帳號  
**metasploit** 開啟 shell 以後  
用 `net user` 列出所有使用者  
flag: `manager`  

##Problem 9 1000  
第 8 題得到的帳戶似乎密碼可以被破解  
flag 就是密碼  
用 **metasploit** 內建的 `hashdump` 得到密碼的 shadow  
這題我用網路上的方式爆不出 **NTLM** 的密碼  
改用提示的 **John The Ripper** 就爆出來了  
flag: `COFFEE123`  

##Problem 10 1000  
第 7 題的 zip 有加密  
要想辦法破出密碼  
用 **metasploit** 內建的 download 得到 zip 檔  
嘗試使用 **fcrackzip** 去破解...但是跑不出來  
因為時間不太夠只好打開 hint  
提示要用 dictionary  
上網找的字典檔要 4G 來不及下載了  
在開一個提示才知道原來 kali 已經自帶字典檔了  
用 `rockyou.txt` 成功解出壓縮檔密碼 `blingbling`  
flag 在檔案裏面  
flag: 忘了  

* * *
LEVEL 2 是賽門鐵克的產品  
根本沒人想去試...  
給個 24 小時再說吧 XD  
* * *
LEVEL 3  
我開了一個 hint 但是登不進去環境 Q\_Q  
最後把 hint 全開照著指示還是進不去 WTF~~~  
結果是主辦方那邊的 bug ORZ  
在分秒必爭之際...我發呆了半小時 囧rz  
最後 LEVEL3 只解兩題  so sad  
早知道學 atdog 大大 直接找漏洞打 (誤  
* * *
結束前 scoreboard 就關閉了  
不知道自己確切的名次  
估計應該在 10 名上下吧 ><  
還有很大的努力空間呀~~  
這次的題目類型跟平常打的 CTF 相差滿大的  
不過也學到很多工具的使用方式  
感謝**賽門鐵克**主辦這次活動  
以及 **TDOH** 的宣傳 讓我有渠道可以參加這次活動~  
