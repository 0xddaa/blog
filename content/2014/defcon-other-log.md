title: DEFCON 22 CTF final log
date: 2014-8-13 18:34
category: other
tags: DEFCON CTF
slug: defcon_other_log

**===WARNING===**
這篇文章廢話超多......  
若要看比賽細節請直接跳至 **8/8**  
* * *

## 8/5
* * *
必須說這次的出國真的很刺激  
首先是 orange 的簽證填錯護照號碼 XD  
過安檢的時候 jery 背包的一堆給溪都被丟掉了  
到 SFO 之後 sean 和 jery 過海關時不知為何被攔下  
好險長榮的工作人員去解圍  
經過一番波折終於抵達 las vegas  
在搭機場到飯店的接駁車上  
深深為 strip 的夜景感到驚豔  
> TT: 就是 unix 那個 strip  

可惜相機還放在行李箱裡 Orz  
抵達飯店 RIO 以後跟 GD 會合  
在等待 checkin 的時間把一樓賭場逛了逛  
有種劉姥姥進大觀園的感覺~  
回飯店放完行李就出發覓食  
最後吃了漢堡王...好貴  
不過份量也很大  
大家對蘑菇醬很有話題...XDD  
![IMG_1733.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/WBrjgcYzQoSJ7dOIROZK_IMG_1733.JPG)

吃完去賭場逛逛  
大家玩了幾次吃角子老虎  
輸一點小錢就回房間洗洗睡  
因為網路要另外收錢 = =  
順便抱怨飯店的提供的肥皂和洗髮精真的很難用  
我有點皮膚過敏的反應 orz  
![IMG_1734.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/lE6XqYfnTeuUtH8tPf4Y_IMG_1734.JPG)  


## 8/6
* * *
如果不算昨天，今天是到 las vegas 的第一天  
其實感覺不到什麼時差  
睡到大約九點  
發現 jeffxx 等人早就起床去吃過早餐了  
其他人也就集合下去吃  
一部分的人吃 starbucks  
其他人又去吃漢堡王 XDD  
starbucks 好貴 ...  
$11 ... 應該是我生平吃過最貴的早餐了  

吃完早餐有些人就回去調時差  
其他人各自做自己的事情  
等到下午大家開始整合事前準備  
由於賽前無法得知規則及環境  
大家盡可能的推演各種狀況  
並分成 **wrapper** 和 **script** 兩組  
分配工作給大家  
兩組的工作主要有：  

- wrapper (seau jery peter shik lucas)
 - pty
 - socket
 - ld\_preload 
 - ptrace
- script (orange jeffxx atdog dm4 and me)
 - backdoor
 - backup token & log
 - monitor dir, port, ... etc
 - parse pcap

除此之外還有模擬 gamebox 環境  
由 orange 和 jery 負責  
討論完後大家就各自工作  
其餘的時間除了吃 buffet 以外  
就是各自工作  
buffet 味道還不錯  
不過柳橙汁超酸  
中途大家要發表一下賽前心得...  
超難的 我已經不記得自己講什麼了 = =  
吃完原本打算去賭場浪費 $$  
結果才坐下來就被保安檢查  
我沒帶證件就被趕回房間了 QQ  
把一些 script 做細微修改  
剩下的時間研究去年 blue-lotus 的心得和去年 defcon 規則  
![IMG_1757.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/IJ1AfSDFRduOKnyl14Je_IMG_1757.JPG)  

## 8/7
* * *
早上 alan 幫大家準備的早點  
吃一吃不知道誰提議要吃泡麵  
我帶的熱水壺就派上用場 XD  
吃完原本以為是要去樓下聽規則  
結果只是領取 badge 和一些大會贈品  
badge 是一塊...開發板 ?  
裡面似乎可以編寫自己的功能  
還有一些奇怪的模組 XD  
我對硬體不熟就沒研究了  
沒多久 alan 買完其他人的 badge  
大概有 20 幾個 ... 超扯 XD  
![IMG_1766.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/Q6WB6yoSSTSIpK7eFW7y_IMG_1766.JPG)  

接著我們下去買紀念 t-shirt 的攤位  
一路上都是排隊買票的隊伍  
長度快要突破天際啦~~~  
![IMG_1770.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/0xO4c4xRQzWTtBvcJCrq_IMG_1770.JPG)  
到攤位才知道原來 t-shirt 有很多種  
樣式還滿好看的 不輸西門町一些潮T  
最有看頭的是白色醫生袍 XDDD  
穿上去實在很酷  
不過如果平常穿可能恥力要夠 XD  
因為帶的錢不夠  
只好先買了一件外套和 t-shirt  
外套要 $60 樣式很普通  
材質感覺不錯 穿起來很舒服  
![IMG_1773.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/MDiHWTHESwispnHRXdCM_IMG_1773.JPG)  

下午去逛 outlet  
orange & alan & me 搭導演的車  
其他人就搭車前往  
逛了半天結果我只買一隻冰淇淋來吃 XD  
其他人都各自有收穫  
回程順便去中國超市幫忙採購明天的早餐  
看到很多台灣的商品  
結帳時店員也是來自台灣  
還跟 alan 要電話 XD  
![IMG_1804.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/aMIkfF4QESjWNzS6DltI_IMG_1804.JPG)  

等大家都回到飯店後  
對明天比賽的戰術最後討論  
基本上有：  

- 檢查 gamebox 能用上的 wrapper
- 上 wrapper
- 上 script
- 與外場 sync 資訊
- 錯誤狀況 & SOP 

討論持續到晚上一點多大家才休息  
主要是 wrapper 組要做的事情真的很多  
他們甚至省下 outlet 的行程趕工  
太強大了 <(\_ \_)>  

# 8/8
* * *
大家一大早就到樓下等著比賽開始  
看到很多之前只會在網路看到的隊伍  
感覺還滿奇妙的 XD  
大家進場後場外組和後援組就待在隔壁間  
透過事先建好的 ssh tunnel 操作  
我這邊負責建置的 script 沒遇到什麼問題  
ptrace 如預期的不能用  
wrapper 大部分都接了上去  
10 點正式開始  
開放兩個服務：`eliza` and `wdub`  
`eliza` 簡單的說就是大航海時代宇宙版  
可以買賣東西賺錢這樣  
`wdup` 是一個 http server  
不過由於只能透過 ctf.tw 存取  
沒有 browser 可用  
暫時就沒看這邊  

一開始就不太順利  
**wrapper 沒辦法通過主辦方的 service check**  
一開始就墊底 OTZ  
更慘的是 開賽兩小時後對外網路 gg  
**帶來的 switch 對 vlan 999 的支援有問題**  
場內暫時用 4G 上網  
場外則完全無法連線  
還好 `eliza` 是用 qemu 模擬 x86 的服務  
暫時還可以做離線分析  
這邊我試到可以控制 eip  
要開始寫 ROP 時  
場內也是進行到這步驟  
為了避免工作重疊就交給 sean 來寫 exploit  
在這邊我們場外組犯了一個錯誤  
**看到 `wdup` 有 html ， 一直以為`wdup`是 web 題......**  
網路問題導至內外的資訊傳遞一直很緩慢  
一直到第二天快結束才反應過來  
超虧... `wdup` 可能是我們掉最多分的一題  

後來 GD 拿 thinkpad 接無線網卡暫時做為 router 使用  
讓場外組可以 access 內網 不過延遲很高...  
途中還有幾個突發狀況：  

- 內外網全死，疑似是有隊伍做 dos，應該是透過 `eliza`，cpu 使用率很高
- peter 和 shik 嘗試解 badge 題，結果在燒一次版子要兩分鐘，中間剛好 service check XDD
- lucas 透過分析封包時發現 `eliza` 根本沒有 DEP，不過此時 sean 也差不多完成 ROP exploit 了

過一段時間又開了一題 `imap`  
顧名思義就是可以做 imap protocol 的各種操作  
這題的 flag 位置跟其他題都不同  
猜測是 owner 為 root 資料夾底下有個特殊的檔案  
此外資料夾底下還有登入用的 password  
由於 tunnel 實在很 lag  
我只好在手機上用 gdb 去 reverse 這題  
lucas 有發現可疑的流量  
有其他隊伍直接就登入、讀 flag 並結束連線  
前面完全沒有獲得帳密的過程  
由於沒有備份 flag 很難確認到底是不是被攻擊了  
但我猜測應該並沒有被攻陷  
因為此流量的來源隊伍名次較後  
如果有成功拿 flag 不應該如此  
這流量的產生有兩個可能：  

1. 此主辦方的 service check
2. 此為其他隊伍混淆視聽的假流量

現在想想應該是第二個可能  
畢竟主辦方在有切 vlan 的情況下  
應該不會提供 service check 的流量  

正當場外在研究 `imap`時  
場內似乎發現有其他隊伍用 `eliza` 的新漏洞來攻擊我們  
這個沒辦法透過 replay exploit 去獲得分數  
發生 exploit 需要遊戲金額到一定數量才能觸發  
物品和星球都是隨機生成  
所以必須先寫個自動賺錢外掛 XDD  
這邊就給 217 的 acm 大大去搞定  

回到飯店後吃晚餐順便討論今天的戰況  
抱歉我完全不記得午餐和晚餐吃什麼.......OTZ  
比賽期間我們的名次在 4~8 名徘徊  
第一名由_韓國 ASRT_ 遙遙領先  
沒意外 `eliza` 最早的 exploit 就是由他們寫出  
第二名則由 _men in blackhats_ 迎頭趕上  
第三名是 _ppp_  
第四名 _blue-lotus_  
我們暫居第五  

討論完以後大家又繼續離線分析  
但是實在太累大家相繼睡去  
直到半夜又醒來解題 XDD  
dm4 給我了一個 `imap` 可疑流量  
這次是真的可以 work !  
發現執行完 payload 以後  
可以用 `list` 指令做任意路徑存取  
也就是可以得知使用者帳戶名稱及存放密碼的檔案  
由於密碼存放的資料夾和目錄是 666  
我瞬間念頭是可以透過其他 service 來存取這些檔案  
這個 payload 應該也只做到目前這樣  
後來 atdog 睡醒之後加入分析的行列  
眼尖的發現 payload 的檔名是用 `aaaaaaaaaaaaaaaaaaaaaaaaaaa../`  
但是這樣的路徑根本不會 work XD  
原來這邊是一個 BOF 造成的邏輯漏洞  
突破盲點後很快我們找出 exploit 的位置  
並由 dm4 寫出攻擊的 script  
另一邊 `eliza` 也成功賺到足夠的 $$ 並寫出 exploit  

##8/9
* * *
第二天一早要進場但是被擋在外面要排隊  
最後要由隊長拿 token 讓 8 個人進去  
因此外場組就只能在外面等  
今天 GD 嘗試解決 vlan 999 的問題  
可惜還是無解  

今天得知主辦方計分方面有問題  
重算我們的排名上升到第二！  
後來記分板就關閉了 只顯示排名  
中午開了新題目 `justify`  
_dragon sector_ 有送可疑流量過來  
但是仔細檢查後根本與程式流程無關  
而且流出的 flag 也 match 不上備份的  
差不多這時間我們突然第一名了 XD  
應該要歸功於前面成功攻擊放的後門  

兩點左右發現 `justify` 被打了  
不過內場後來說已經 patch  
但是這邊又有溝通上的問題 QQ  
外場大概很早有發現漏洞的確切位置  
但是以為內場已經 patch 而沒有告知  
回飯店才知道內場的 patch 是其他問題  
靠 wrapper 一開始有守下幾波  
不過 _ppp_ 的 payload 也一直進化  
五點的時候 `justify` 突然爛掉  
還原成最初版本也沒用  
後來確認是主辦方的問題 XD  

差不多三點左右 `wdup` 換新版本  
由於沒人分析 又是一陣手忙腳亂  
只 wrapper 擋在前面避免大量失分  
靠著 replay 從弱隊獲得一些分數  
好像還有隊伍用其他 service 在 tmp 建 link  
來繞過 `wdup` 的限制  

接近六點的時候 `eliza` 換成 arm 的版本  
不過程式似乎沒有做改動  
我們很快就把 jump 的漏洞給補上  
btw, patch 的部分都是靠 jery 負責  
真的很強大 <(\_ \_)>  
6:37 `imap` 也放出了第二個版本  
外場第一時間把檔案抓下來比對  
由於 ctf.tw 無法連外  
只能轉成 hex 再用 copy & paste 的方式拉出來 ...  
這次有小部分功能都改過  
不過 diff 過後很快就找到問題點在一個 decode base64 的 function  
lucas 說第一個版本也又這個 function  
但是沒有被呼叫到  
接下來到結束時間都在研究如何觸發這個漏洞  

內場其實發生很多事情外場都不清楚 ><  
比如說  

- 主要得分來自前面種的後門
- `justify` 持續掉分
- 其他隊伍也有很多 wrapper 和 defense script，必須想辦法繞過

這些場外其實都第一時間沒得到消息...  
很多狀況都是回飯店討論時才知道的  
即使用 skype 還是有些不方便  

晚上大家實在太累了  
吃完飯都決定回去小寐一會兒才陸續起來解題  
我睡到凌晨 1 點...鬧鐘沒設完就睡著了 = =  
好險沒睡到隔天  
醒來 lucas 和 atdog 已經讓 `imapv2` 會 stack smash  
但是似乎沒辦法繞過 stack guard  
jery 則是說已經還原數個 `justify` struct  
可以分工去 reverse 程式  
此時我們才開始交流內外場對這題的進度  
知道這題是吃 DIMACS CNF format 格式的文件後  
分析進度開始加速了起來  
> 217: 這就是一題 hrms  

jery 則把漏洞給補上  
用一種很巧秒的方式 XD  
將整個 stack 移到 environment variable 的位置  
這樣即使 overflow 也只會蓋到環境變數  
> _blue-lotus_: 神思路! 太猥瑣了!  

這題 patch 有一定難度  
很多隊伍只是把長度加大來騙人  
實際上只要改過 padding 長度依然可以 overflow  
可惜直到比賽我們最後還是沒有成功分析出 `justify` 的演算法  
只能靠 replay 的方式重送  
也沒拿到什麼分數  

至於其他兩題的進度  
sean 和 jeffxx 把 arm 版本的 `eliza` 第二個漏洞給做出來  
`imapv2` 可以對任意地址寫 1 byte  
但是找不到 memory leak 和可以利用的地方 OTZ  

## 8/10
* * *
第三天大家莫名其妙又要排隊  
這次我們決定直接坐在沙發  
用無線網路存取內網 XD  
果然操作效率大幅提升阿!!!  
只可惜第三天真的太累了......  
沒辦法專注在分析 0 day  
分析 _ppp_ 的流量只看到一堆假流量毫無稍獲  
不過分析 _binja_ 、 _blue-lotus_  
似乎都有嘗試對 `justify` 發動攻擊  
另外 第三天 `wdup` 還是有被攻擊成功  
由於第二天後半開始幾乎都是挨打的狀態  
不過修補及時 應該也沒有太大損害  
第三天沒有攻擊流量、也沒有分數排名  
(我看了螢幕三分鐘才發現是 replay ....  

比賽就這樣平淡的結束了  
大家留下來拍照和聽主辦單位宣布一些事情  
也有跟其他隊伍稍微交流一下心得  
就回飯店休息了......實在是很累 = =  
睡到 4:30 以為是頒獎開始了 結果還沒  
只好回比賽場地繼續 social  
值得一提的是 _ghost in the shellcode_ 的成員來跟我們分享一些 CTF 的經驗  
他說自己已經比了 9 年  
隊伍花五年去弄出一套 framework 來幫助 CTF 競賽  
我們也跟他們提到 HITCON CTF  
說題目還沒出完  
他也回說完全了解出題的痛苦 XD  
![IMG_1813.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/KTP0zJmeRyezvahV3trC_IMG_1813.JPG)  

最後閉幕式在半夢半醒中度過  
聽到 _dragon sector_ 的名字我嚇了一大跳  
想說如果他們反超到第一名 那我們就死定啦  
第三天很多都是他們對我們發動攻擊 = =  
還好他們是第三 我們第二 _ppp_ 還是保持在第一  
跟第二天的名次完全一樣 XD  
插曲是因為宣布名次時攝影大哥剛好去上廁所  
在後面罵一聲 **幹!!!** XDDD  
![IMG_1815.JPG](http://user-image.logdown.io/user/6149/blog/6156/post/220500/BHzsEqRruLGYt3kQUZ3A_IMG_1815.JPG)  

晚餐吃了奇怪的中式合菜  
除了那道青菜以外吃起來都不錯  
吃完大家都回去休息了  
sean & jeffxx & peter & me 四個人開始玩世紀二 XDD  
中間還發生 virtual box 跟 guest os 和 host 無縫接軌的神奇畫面...  
不過我真的玩得很爛 = =  
被改強的電腦打爆兩次  
最後一場改打塔快和城快結果電腦瞬間被虐爆....  
> sean: 怎麼差這麼多? 遊戲做壞了吧  

之後改玩小遊戲...打了 40 幾分鐘  
打到兩邊都不想玩了 = =  
最後吃一碗泡麵做為一天的結束  

## 8/11
* * *
最後一天早上在飯店聊天  
因為沒有微波爐可以熱昨天的炒飯  
只好很克難的吹風機加熱 XDDD  
親眼見證了 lucas 被 GD + dm4 的聯手推坑  
買完大家就在飯店裡玩 boss 耳機 XDD  
後來 alan 也買了一個  

下午的行程大致就是...  
逛街逛到腿軟  
死觀光客模式快門按不停  
溫蒂漢堡很難吃  
搭飛機回家  
就不詳細贅述細節了  

幹  
原本要傳 defcon 閉幕式的照片做結尾  
可是免費帳號不能傳照片了 = =  
