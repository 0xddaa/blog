title: GiTs 2014 Trivia 150 lugkist
date: 2014-1-20 19:04
category: forensic
tags: GiTsCTF
slug: gits_2014_trivia_150_lugkist

這次的CTF全名是 : ghost in the shell code  
超級長 所以縮寫成 GiTs  
* * *

將xz檔解壓縮以後得到的是一個純文字的文件  
前面兩行是 Find the key  
後面開始是好幾行的大寫英文字母 每行有六個字  

> GVZSNG
> AXZIOG
> YNAISG
> ASAIUG
> ....

第一時間以為是 **ADFGVX** 加密  
但是仔細看並不是這麼回事  
先寫個簡單的小程式來統計出現的字母  
發現文中只出現 **AEGIKLNOPSTUVXYZ**  
於是就把這一串拿去 google  
找得到的討論串不多  
其中一個標題是 *SMB1 Game Genie thread of epic winness*  
看完討論得知 **AEGIKLNOPSTUVXYZ** 是某個遊戲機金手指的輸入字元  
![game_genie.png]({filename}/images/gits_2014_lugkist_1.png)

於是以 **Game Genie** 為關鍵字下去搜尋  
得知每一個 **AEGIKLNOPSTUVXYZ** 的字串  
都可以對應到一個 hex address  
所以我們要做的事情是  
把每一行的 ciphertext 轉換成 hex string  

理論上應該是要研究他們轉換的算法  
不過我不小心 google 到別人寫好的 perl code XD  
轉換出來會得到兩段 hex string  
前半段是類似 **ddab** 這種格式  
後半段則是一個 ASCII code  
用一開始的順序解出來的結果是  
`d   w P m   a   ?   d   i r c i e l m y w n c a a v p a h s i k v   t s n h t e n c e h o B g s a   o r   e   d e . y o e`  

完全看不出來是三小 XD  
所以推測前面的 hex string 應該是用來排序  
果然排序後就得到key了  
`P o w e r   o v e r w h e l m i n g ?   B a c k   i n   m y   d a y   c h e a t s   d i d   n o t   h a v e   s p a c e s .`  

key : `Power overwhelming? Back in my day cheats did not have spaces.`  
