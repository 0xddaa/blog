title: BCTF 2016 crypto 200 Special RSA
date: 2016-3-21 20:13 
category: crypto
tags: XCTF, rsa
slug: bctf_crypto_200_special_rsa

這題是很基本的 crypto 題目
從有 94 隊解就知道了...= =  
不過我還是想了好久 QQ  
對現代密碼學實在不太擅長  
這次一邊解一邊研究模運算  
趁記憶深刻趕快寫這篇 write-up  
* * *

題目雖然叫 **Special RSA** 但是這題跟 RSA 其實沒有很大關連...  
還比較像 ElGamel encryption = =  
害我還跑去看 ElGamel 有什麼弱點 囧  

題目給了四個檔案:

 - special\_rsa.py
 - msg.txt
 - msg.enc
 - flag.enc

`special_rsa.py` 有 usage, 真好心 XD 
> dada@ubuntu:~/bctf/special\_rsa$ ./special\_rsa.py  
> usage: ./special\_rsa.py enc|dec input.file output.file  

加密會把 input 切成很多個 block, 每個 256 byte  
每個 block 轉成 數字在用以下公式加密:  

 1. `c = (pow(k, r, N) * m) % N`  

c = cipher, m = plain, m < N  
r = random number, N = big prime  
r 會跟 c 包在一起再用 msgpack 打包  
k 沒有給...給了這題就不用解了 XD  

解密有兩步驟:  

 1. `k_inv = modinv(k, N)`  
 2. `m = pow(k_inv, r, N) * c % N`  

`k_inv` 是 k 的模反元素   
 
解密的原理是:   

```
    pow(k_inv, r, N) * c % N
=   pow(k_inv, r, N) * ((pow(k, r, N) * m) % N) % N
=   (pow(k_inv, r, N) % N) * ((pow(k, r, N) * m) % N) % N   // pow(k_inv, r, N) = pow(k_inv, r, N) % N
=   pow(k_inv, r, N) * (pow(k, r, N) * m) % N               // (a % N * b % N) % N = a * b % N
=   pow(k_inv * k, r, N) * m % N                            // (a * b) ^ r % N = (a ^ r % N) * (b ^ r % N) % N
=   pow(1, r, N) * m % N                                    // k * k_inv % N = 1
=   m % N                                                   // m < N
=   m
```

模運算有幾個重要的特性:  

  1. % 運算子優先度最後  
  2. 滿足加法律  
    - `a + b % N = (a % N + b % N) % N`
  3. 減法等同加上倒數, 因此也滿足減法  
    - `a - b % N = (a % N - b % N) % N`
  4. 乘法等於連加, 因此滿足乘法  
    - `a * b % N = (a % N * b % N) % N`  
  5. 除法等同乘上倒數, 倒數就是模反元素  
    - `a * b_inv % N = (a % N / b % N) % N`  
  6. 指數等於連乘, 因此滿足指數律 (`^` 表示平方)  
    - `(a * b) ^ r % N = (a ^ r % N) * (b ^ r % N) % N`  
    - `(a - b) ^ r % N = (a ^ r % N) / (b ^ r % N) % N`  
    - `g ^ (a + b) % N = (g ^ a % N) * (g ^ b % N) % N`  
  7. 任何數乘上模反元素的餘數會是 1
    - `a * a_inv % N = 1` 

我們已知 `m`, `r`, `N`, 利用模運算的特性  
我們可以反推出 `k` 的值  

  1. 求 m 的模反元素  
    - `m_inv = modinv(m, N)`  
  2. 將 c 乘上模反元素得到 pow(k, r, N)  
    - `c * m_inv % N = pow(k, r, N) % N = pow(k, r, N)`  
  3. `msg.enc` 有兩個 block, 重複兩次得到 pow(k, r1, N), pow(k, r2, N)  
    - `p1 = c1 * m_inv % N = pow(k, r1, N) % N = pow(k, r1, N)`  
    - `p2 = c2 * m_inv % N = pow(k, r2, N) % N = pow(k, r2, N)`  
  4. 由於底數相同, p1 & p2 可以做指數的加減法, 目標是求出 pow(k, 1, N)  
    - `pow(k, 1, N) = k`  
    - 問題變成: `r1 * z1 + r2 * z2 = 1`, 解 z1 & z2  
  5. **Extended Euclid Algorithm** 可以解此問題
    - `egcd(r1, r2) = [gcd(r1, r2), z1, r2]`  
    - 剛好 gcd(r1, r2) = 1  
  6. 把 z1, z2 代回解 `pow(k, r1 * z1 + r2 * z2, N)` 即可求得 k  

[POC]({filename}/exp/special_rsa.py)  

flag: `BCTF{q0000000000b3333333333-ju57-w0n-pwn20wn!!!!!!!!!!!!}`
