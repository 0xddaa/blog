title: Plaid CTF 2014 Crypto 250 Parlor 
date: 2014-4-17 10:37
category: crypto
tags: PlaidCTF, Length Extension Attack
slug: plaidctf_crypto_250_parlor

這題是 217 的大大們解出來的  
我知道關鍵後  
隔天才自己做一遍  
寫程式太慢了.........  
* * *

這題連到目標環境後敘述如下：  

```
/------------------------------------------------------------------------------\
| Welcome to the betting parlor!                                               |
|                                                                              |
| We implement State of the Art cryptography to give you the fairest and most  |
| exciting betting experience!                                                 |
|                                                                              |
| Here's how it works: we both pick a nonce, you tell us odds, and you give us |
| some money.                                                                  |
| If md5(our number + your number) % odds == 0, you win bet amount*odds.       |
| UPDATE: IF YOU DIDN'T REALIZE IT, WE DO INCLUDE A NEWLINE AT THE END OF YOUR |
| NUMBER. SORRY FOR THE INCONVENIENCE. THANK YOU FOR USING PARLOR              |
| Otherwise, we get your money! We're even so nice, we gave you $1000 to start.|
|                                                                              |
| If you don't trust us, we will generate a new nonce, and reveal the old nonce|
| to you, so you can verify all of our results!                                |
|                                                                              |
| (Oh, and if you win a billion dollars, we'll give you a flag.)               |
\______________________________________________________________________________/

====================
  1) set your odds
  2) set your bet
  3) play a round
  4) get balance
  5) reveal nonce
  6) quit
====================
```

規則總結如下：

1. 設定一個模數 odds
2. 下注 bet
3. 猜一個數字 your num (之後簡稱num)
4. 如果滿足 `md5(our num + your num) % odds == 0`, 則獲得 odds * bet 的金額
5. 贏得 100w 

雖然題目說要我們猜一個數字並與 nonce 相加  
但是將 nonce reveal 出來  
會是一段 hex  
轉為 byte 以後，與 num 相加，做 md5 再 % odds  
可以到相同的結果  
所以其實是字串相加，而不是數字  

這題如果能預先算出 md5 的結果  
就能輕鬆獲勝了  
有一種 hash 的攻擊方式叫做 **Length Extension Attack** (後簡稱 LEA)  
適用於大部分的 hash，如 md5 sha1 sha256  
可以在不知道 text，只知道 hash 過的結果的情況下  
預測 `hash(text + padding + suffix)` 的結果  

這邊研究了一下 md5 hash 的過程  
首先會切成數個 64 byte 的 block  
最後一個 block 如果不是 56 byte 會做 padding  
padding 的方式是第一個 byte 為 `\x80`  
接著填充 `\x00`  
最後 8 byte 補上原始長度 (bit)  
接著 md5 會有 4 個初始量  

```
a=0x67452301
b=0xEFCDAB89
c=0x98BADCFE 
d=0x10325476
```

接著會以 a b c d 以及 block[i] 為參數  
做一系列的運算  
會得到另外四個值 aa bb cc dd  
並且將 a b c d 與 aa bb cc dd 做相加  
這個過程視為一個 round  

```
aa,bb,cc,dd = f(a,b,c,d,block[i])
a += aa
b += bb
c += cc
d += dd
```

如果後面還有 block 就繼續做運算  
直到沒有 block 為止  
a b c d 的最終值合併後就是 md5 的結果  

如果 a b c d 的初始值改變的結果會如何 ?  
LEA 就是利用這點  
如果我們現在已知 `md5(nonce + num)` 的結果  
將其結果還原為 a b c d  
並當作 function f 中 a b c d 的初始值  
做一次 `f(a,b,c,d,msg)` 的運算  
結果等同於 `md5(nonce + num + padding + msg)`   
所以即使不知道 `nonce + num`  
也可以預測出結果  

Talk is cheap, 先 reveal nonce 判斷是否可行：  

```
nonce = "760c4a0f8ec61bec304ed4d8d8abeb98".decode('hex')
num = 'a\n'
md5(nonce + num) = '5b356daa0313063af25f8da01922128d'
a,b,c,d = md5tonum(md5(nonce + num))
# nonce = 16, a\n = 2, 所以填充\x80+\x00*37 + len 8, total = 64
padding = "\x80"+"\x00"*37 + "\x90"+"\x00"*7
print md5('a\n'+padding+'b\n')
block = [256511094 3961243278 3637792304 2565581784 8391265 0 0 0 0 0 0 0 0 0 144 0 8391266 0 0 0 0 0 0 0 0 0 0 0 0 0 528 0]
md5: 12b74d8200ff1c84500b1e55ada2ce7e 
print guess('b\n',a,b,c,d,66) # 新的長度是 66 byte
block = [8391266 0 0 0 0 0 0 0 0 0 0 0 0 0 16 0]
md5: 12b74d8200ff1c84500b1e55ada2ce7e 
```

剩下的難題就是怎麼樣得到 md5 的結果了  
把 odds 設成 100  
第一次送 'a\n' 得到 r1  
r1 = `md5 % 2\*\*100`  
第二次送 'a\n' + padding + 'b\n' 得到 r2  
用 r1 推出 a b c d 並用 LEA 預測結果  
(a 用 brute-force 的方式去試)  
如果結果與 r2 相同  
就代表 a 的值是正確的  
也就得到完整的 md5 了  

flag: `i_dunno_i_ran_out_of_clever_keys`
