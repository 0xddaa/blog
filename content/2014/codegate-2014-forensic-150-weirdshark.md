title: Codegate CTF Preliminary 2014 150 WeirdShark
date: 2014-2-25 0:20
category: forensic
tags: CodegateCTF
slug: codegate_2014_forensic_150_weirdshark

這題是這次 CTF 唯一的一題 Forensics ......  
* * *

題目是一個 pcap 檔  
用 **wireshark** 開啟卻出現錯誤訊息  
![weirdshark1.PNG]({filename}/images/codegate_2014_weirdshark_1.png)  

看來是毀損了  
只好想辦法修復  
找到一個線上修復 pcap 的網站  
[pcapfix](http://f00l.de/pcapfix/)  

修復後再開一次檔案...fail again  
![weirdshark2.PNG]({filename}/images/codegate_2014_weirdshark_2.png)  
至少 *cap\_len* 變小了  
這次只好自己手動修復了 QQ  
`62 = 0x3E, 64 = 0x40`  
搜尋一下 0x40  
嘗試改成 0x3E  
![weirdshark3.PNG]({filename}/images/codegate_2014_weirdshark_3.png)  
然後就 work 了... =.=  

除了一般 tcp 就只出現 http了  
看到有 *GET /xxx.jpg* 的可疑封包  
把檔案解開來看看  
`file -> extract object -> http`  
將所有檔案檢查過以後  
發現在 pdf 檔裡面有 flag XD  
![flag.PNG]({filename}/images/codegate_2014_weirdshark_flag.png)  
  
flag: `FORENSICS_WITH_HAXORS`  
