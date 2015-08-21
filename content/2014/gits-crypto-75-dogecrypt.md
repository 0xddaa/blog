title: GiTs 2014 Crypto 75 Dogecrypt
date: 2014-1-20 23:46
category: crypto
tags: GiTsCTF
slug: gits_crypto_75_dogecrypt

老實說我覺得這題出滿爛的  
害我花最長時間解結果沒解出來  
因為最關鍵的資訊是在 IRC 上提示的 ORZ  
* * *

這題給的檔案是一個加密過後的文件  
前面的標頭是 **VimCrypt~01!**  
google 以後我才知道原來 *vim* 可以用 `:X` 或 `-x` 加密文件 =.=  
加密方式又有分較舊版的 **PKZIP (VimCrypt~01)** 和新版的 **blowfish (VimCrypt~02)**  
這題是舊版的 **PKZIP**  

一開始 google 尋找解法  
發現有人寫了 **vimzipper**  
用途是將加密過的 vim 文件重新包裝成 zip 的格式  
包完可以用 **pkcrack** 或其他破解 zip 的軟體去分析  
但是測試後重新封裝的 zip 沒辦法用 brute-force 去得到 key  
**pkcrack** 則需要先知道明文才有辦法分析  
在網站上逛來逛去也沒看到 size = 402 byte 的文件  
我就卡死在這邊了 ORZ  
後來看別人的 write up  
才得知原來這題有 hint:  

> "Solveable in <5m. Much attack very wamerican-small."

**wamerican-small** 是一個字典檔  
可以用 `apt-get install wamerican-small` 下載安裝  
裝完檔案會在 `/usr/share/dict/wamerican-small`  
於是乎 我們就用字典破解來解這題...  
我用 python 開 vim 再踹密碼  
大約是一秒一個的速度 = =  
五萬多行跑完天都黑了  
所以用 `split` 把檔案切成 10 個  
大概跑一小時就跑出結果了  
解出來的密碼是: *parliament*  
可以用 vim 並輸入密碼開啟原本的檔案  
就得到結果了~  

write up 提供的解法打開 vim source code  
用裡面的 function 來 decrypt 文件  
過程也是用字典檔下去試  
不過用這種做法五分鐘就跑完了 <(\_ \_)>  

flag: `ShibeSuchDictionaryAttacksWow`  
