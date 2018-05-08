title: SECCON 2016 Binary+Crypto 200 Lost Decryption
date: 2016-12-13 2:43
category: crypto
tags: SECCON CTF, Feistel Cipher
slug: seccon_re+crypto_200_lostdecryption

這題是 pwn 題被大家掃光之後  
不得以之下只好來看的題目...  
Crypto is so difficult. Orz
* * *

題目給了三個檔案 **cipher**, **libencrypt.so**, **flag.enc**  
cipher 沒辦法執行, 會噴出以下 error:
> ./cipher: error while loading shared libraries: libdecrypt.so: cannot open shared object file: No such file or directory

把 cipher 丟到 ida pro 以後可以大致分析出行為:

1. Usage: cipher (encrypt|decrypt) key input output
2. 可以藉由第二個參數選擇要加密還是解密, 分別會 call `encrypt(buf, key)` 或 `decrypt(buf, key)`
3. 加密的方式是 block cipher, block size = key length = 16 byte
4. 依序將加密或解密後的結果寫進 output file
5. 如果 input 不是 16 的倍數, 最後會補上 padding

這題的關鍵還是在 libencrypt.so 上, 裡面只有一個加密 function  
encrypt 會做 14 次 xor, xor key 由一個亂七八糟的 function 產生  
xor 完會將 block 的前半和後半做交換  

```
258 void __fastcall encrypt(char *buf, char *key)
...
273   do
274   {
275     v5 = sub_8a0(b1, k1);
276     b0 ^= v5;
277     k1 = sub_8a0(k1, 0x9104F95DE694DC50LL);
278     xchg(&b0);
279     xchg(&k0);
280     --i;
281   }
282   while ( i );
...
286 }
```

如果有修過密碼學, 應該一眼就可以感覺出這是典型的 **feistel cipher**  
feistel cipher 的特徵就是解密就是加密的倒過來  
所以這題其實不用看懂 `sub_8a0` 到底在做什麼  
直接拿來用就可以了  
k1 就是 feistel cipher 的 round key, 用來產生 xor 用的 key  
round key 不受 cipher 影響, 可以跑 14 round 得到所有的 round key  
可以用 ida pro decompile `sub_8a0` 寫一個解密的 function:

```
void decrypt(int *buf)
{
    __int64 k1[14] = {0x7071370944faa683, 0xc936fe92f5be592, 0xfb865e2b2a6216f, 0x89745418b4f3701d, 0xfa8b683d8876468f, 0xe2185b1aa6ace4c2, 0xf6f840cc5548b290, 0xeb42f12db34bcecc, 0xe3459923a1fadfda, 0x3ac1150762625475, 0xccb7b4ad260cfb29, 0xb2007c75f4bad138, 0x8850ec377c7449b6 , 0x1ba31bdc8631ecd6};

    int b[2] = {buf[0], buf[1]};
    xchg(&b);
    for (int i = 13; i >= 0; i--) {
        xchg(&b);
        b[0] ^= sub_8a0(b[1], k1[i]);
    }
    xchg(&b);
    buf[0] = b[0];
    buf[1] = b[1];
 }
```

編譯成執行檔後, 就可以拿來 decrypt flag.enc 的內容了  

flag: `SECCON{Decryption_Of_Feistel_is_EASY!}`
