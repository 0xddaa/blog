title: HITCON CTF 2016 crypto 150 OTP
date: 2016-10-13 20:13 
category: crypto
tags: PRNG 
slug: hitcon_crypto_150_otp

Sovled: 12 / 1024

今年是第一次以出題方的身分參加 HITCON CTF  
一直很擔心自己的題目不夠水準  
有一點低估自己的題目難度了  
以解題人數來看, 這題應該可以加到 200 分  
* * *

otp 的行為是接收使用者的明文  
隨機產生一組長度等於 明文 + flag 的 xor key  
透過 xor 加密 明文 + flag 並回傳給使用者  
並且可以選擇透過何種方式產生 xor key  

這題主要考的是 **CVE-2016-6316**  
libgcrypt 實作 PRNG 有缺陷  
導致每獲得 580 byte 之後, 就可以算出接下來的 20 byte  
在取得 random number 以後, 都會取目前 random pool 的部分內容做 hash  
再存回 random pool 打亂 entropy  
原本演算法的設計是取 `pool[L-40:L+44]`  
但 libgcrypt 在實作時卻取了 `pool[L-40:L-20] + pool[L:L+44]`  
中間漏掉了一個 block, 導致在不需知道全部的 pool 的情況下  
就可以算出 next state  
詳細的原理在這篇: [Entropy Loss and Output Predictability in theLibgcrypt PRNG](http://formal.iti.kit.edu/~klebanov/pubs/libgcrypt-cve-2016-6313.pdf)  

文章中沒有詳細描述 libgcrypt 的 hash method  
需要自行 trace libgcrypt source code  
根據文件指出的 `mix_pool`, 會發現以下的程式碼

```
 603   gcry_assert (pool_is_locked);
 604   _gcry_sha1_mixblock_init (&md);
```

因此可以得知實作時是用 sha1 做 hash  
並且是透過 update 的方式取得 sha1 的結果  
我一開始沒看仔細, 實作 poc 的時候一直以為是每次取新的 sha1  
卡了一小段時間 Orz

得知以上幾點之後, 就可以開始解這題了  
步驟如下:

1. 加密時輸入長度為 580 byte 的明文, 接收到 580 + n byte 的密文
2. 將明文和密文的前 580 byte xor, 得到 xor key 的前 580 byte, 也就是加密第 29 個 block 時, random pool 的 state
3. 計算 `sha1_update(xorkey[560:580] + xorkey[0:44])`, 結果即是第 30 個 block 的 state
  - 由於我們不知道 random pool 最早的狀態, 不能每個 block 陸續做 `sha1_update` 得到目前的 state
  - 要利用類似 length extension attack 的手法, 將初始的常數換成上一次 sha1 的結果, 也就是 `xorkey[560:580]`
4. 將計算出的結果與密文 xor, 可以得到 flag 的前 20 byte
5. 再次加密, 這次長度輸入 560 byte, 由於我們已經知道 flag 的前 20 byte, 因此一樣可以算出 580 byte 的 xor key
6. 重做 2 ~ 4 步驟就可以得到 flag 剩下的部分

[otp.py]({filename}/exp/otp.py)

flag: `hitcon{N0_n33d_t0_rev0k3_pr1v4te_k3y}`
