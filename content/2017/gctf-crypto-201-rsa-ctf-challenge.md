title: Google CTF 2017 Crypto 201 RSA CTF Challenge
date: 2017-6-26 11:38
category: crypto 
tags: PKCS#1 v1.5, RSA, CVE, Google CTF
slug: gctf_crypto_201_rsa_ctf_challenge

這題沒有解出來...不過學到很多關於 **PKCS#1 v1.5** 的攻擊方式  
還是厚著臉皮寫了一篇 write up  

* * *

PKCS#1 v1.5 是 RSA 的一種實際應用方式，詳細內容可以參考 RFC 2313[^rfc2313]  
目的是將訊息 padding 後構造成數位簽章或數位信封使用的格式，大概會長得這樣：

```
EB: Encryption block 
BT: Block type, 00, 01, 02
PS: Padding string
D:  Data

EB = 00 || BT || PS || 00 || D
```

本題是要找出是簽署 `challenge` 這個字串的 signature   
因此接下來只看 BT = 01 的情況  
簽署 signature PS 會是 n 個 ff  
Data 會由兩部分組成，分別是 `ASN.1`[^asn1] 和 `hash(m)`  
`ASN.1` 取決於後面用哪一種 hash 演算法  
可以把他想像成 hash 演算法的特徵碼  

PKCS#1 v1.5 本身沒有問題  
但是在兩個條件存在時，可以任意偽造任意訊息的 signature  

1. RSA 產生 key pair 時使用了過小的 e (exponent)
2. 用了不正確的方式解析 signature

RSA 的加密方式是 `c = m ** e % N`  
如果 e 太小，導致 `m ** e < N` 成立，解密就可以化簡成:
```
已知 m、N、e，求 c 的 e 次方根  
```

對 PKCS#1 v1.5 而言也有類似的問題，由於格式固定  
如果知道 public key 的長度和 message，我們可以推出 RSA 加密後的 signature 會是：  
```
EB = 0001 + ff * n + 00 + ASN.1 + hash(m)
```
n 取決於 public key 的長度，假設長度是 1024，就要 padding 91 個 ff  
如果 e 太小而且`EB` 剛好是 e 次方數，signature 就是 `EB` 開 e 次方根  
(不太確定在正確 padding 的情況下，`EB` 是不是不可能會是 e 次方數)  

本題在原始碼中附上了 public key  
N = 1024 bit，e = 3  
想當然，這題的 `EB` 不是一個立方數 XD  
因此還需要條件 2 才有辦法成功偽造 `challenge` 的 signature  

關於 PKCS#1 v1.5 的攻擊最早由 **Bleichenbacher** 提出[^Bleichenbacher] (疑似是這題的出題者)  
其中一種方式是 **Chosen Cipher Attacks**  
後來有人把各種因為實作上的缺陷而產生的攻擊方式整理成一篇論文[^sigflaw]  

由於本題沒有給 server 端的 source code  
因此我們不曉得條件 2 是因為如何實作而導致的  
準確地說，我們甚至不能確定條件 2 是否存在  
因此只能靠猜測的方式，亂送各種因為實作上缺陷而可以偽造的 signature 給 server  

以下是可能的幾種實作缺陷：

### 1. Bleichenbacher’s Low-Exponent Attack  
此方式是最早提出的攻擊手段  
原因是實作時沒有驗證是否有額外的資料在 `hash(m)` 之後  
假設題目是此種實作缺陷，可以送這種格式讓 server 解密：  
`0001 + ff*91 + 00 + ASN.1 + hash(m) + evil`  
由於 evil 是在放在 payload 的最後，有很大的機率可以將 payload 補成一個立方數  
不過此題不是這種實作缺陷  
這種攻擊方式要在 key 長度在 3072 以上才保證一定成功  
1024 會有無法成功補成立方數的可能  

### 2. Variants for Smaller RSA Moduli  
此方式是因為沒有正確檢查 `EB` 的長度  
由於 `ASN.1` 長度不固定的原因  
有些實作方式不會正確檢查 ff 的個數  
只檢查總長度為 8 的倍數  
因此我們有機會透過調整 ff 的個數把 payload 控制成一個立方數  
不過這題也不是考這種利用方式  
試了一下在此題結尾必須是 `md5("challenge")` 的情況下  
不管怎麼刪減都沒辦法做出有效的 payload  

### 3. Exploiting the Algorithm Parameters Field
最早被提出是在 CVE-2006-4339[^cve-2006-4339]，GnuTLS 的實作缺陷  
GnuTLS 在某段程式碼中假設傳進來的 payload 一定是用 md5 做 hash 的 `EB`  
完全沒有檢查 `ASN.1` 的內容是否正確  
因此可以透過調整 `ASN.1` 欄位的內容讓 EB 變成一個立方數  
論文中衍伸了 CVE-2006-4339 提到的攻擊手法  
並將條件改成有分段檢查 `ASN.1` 的欄位  
問題變成可以用不同的 hash 算法混淆判斷來製造立方數  
這題我嘗試了 `CVE-2006-4339` 的實作缺陷，也不成功  
論文提到的衍伸方式利用條件太嚴謹了，看起來這題就做不到 XD  

### 4. Attack Variant against the Netscape Security Services
這個實作缺陷最早是發現在 NSS 的原始碼  
原因跟 2. 有點類似，但是變成完全不檢查 ff  
由於 PKCS#1 v1.5 是向右對齊  
NSS 的實作方式從右邊檢查完 `hash(m)`、`ASN.1` 以後  
就檢查是否用 `00` 分隔和 `0001` 結尾  
因此可以送以下格式的 payload 來偽造：  
`0001 + 00 + evil + hash(m)`  
**python-rsa** 也有發生過類似的問題 CVE-2016-1494[^cve-2016-1494]  
差別是有多檢查 `ASN.1`，因此要改成送這樣的格式：  
`0001 + 00 + evil + ASN.1 + hash(m)`  


本題考的是 CVE-2016-1494  
比賽中我也有嘗試這種做法...不過我是拿別人的 code 來改的
不確定是原本就寫錯了，還是我改壞了  
我沒辦法在 message 是 `challenge` 的情況找出一組成功的解 Orz  
我就以為不是考這個了...  
比賽完自己重寫一遍，就有成功解出 flag 了 = =  

在實作時有很重要的一點是，由於數字很大  
基本上不可能一個一個數字去試是不是立方數  
要透過 bit 枚舉的方式快速找出後綴符合 `ASN.1 + hash(m)` 的數字  
然後用二分法找前綴符合 `000100` 開頭的數字  
就可以解出 flag 了  
解完後往 server 送，server 就會吐 flag 在網頁上了  

flag: `CTF{zx2fn265ll7}`


[^rfc2313]: PKCS #1: RSA Encryption, <https://tools.ietf.org/html/rfc2313>
[^asn1]: Abstract Syntax Notation One，定義於 X.208
[^Bleichenbacher]: <http://archiv.infsec.ethz.ch/education/fs08/secsem/bleichenbacher98.pdf>
[^sigflaw]: <https://www.cdc.informatik.tu-darmstadt.de/reports/reports/sigflaw.pdf>
[^cve-2006-4339]: <https://lists.gnupg.org/pipermail/gnutls-dev/2006-September/001240.html>
[^cve-2016-1494]: <https://blog.filippo.io/bleichenbacher-06-signature-forgery-in-python-rsa/>
