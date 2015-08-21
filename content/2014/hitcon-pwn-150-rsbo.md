title: HITCON CTF 2014 pwn 150 rsbo  
date: 2014-8-18 23:01
category: pwn
tags: HITCON CTF
slug: hitcon_pwn_150_rsbo 

這題是 32 bit 的 elf  
程式規模很小  
很容易就看完了  
* * *

試一下超長字串就發現程式會 crash  
仔細看是因為 `read_80_bytes()` buffer overflow  
buffer 長度 80 實際讀入 0x80 ...  
我一開始的確沒注意 XDD  

crash 的原因是因為 ret 被蓋掉  
蓋完 ret 以後還有 16 byte 的長度可以利用  
這題有 dep + ASLR 的保護  
所以沒辦法知道要跳到哪  
此外，輸入的內容會隨機被打亂  
我們沒辦法讓 ret 正確變成我們希望的內容  

```
size = read_80_bytes(buf);
for ( i = 0; i < size; ++i )
{
    v3 = rand();
    v7 = v3 % (i + 1);
  v6 = buf[i];
  buf[i] = buf[v3 % (i + 1)];
  buf[v7] = v6;
}
```

前面還有一個 `init()` 去讀 flag 並隨機做 xor 後當成 rand seed  
不過最後計算過程中的 buf 會被清空  
完全無法利用  

後來無意間發現 `size` 和 `i` 的值會被覆蓋  
但是有做初始化所以用不上  
可是如果我們將所有 buffer 都塞成 `\x00` 會發生什麼事呢?  
如果在交換過程中 `size` 與其他 byte 做交換  
只要 `size` 所代表的 4 個 byte 都被換掉  
`size` 的值就會變成 0  
迴圈因此中止  
扣掉 `size` 和 `i` 以後  
因此我們會有 20 byte 可以利用  
此時就可以開始利用 ROP 做點事情  

如果沒有 ASLR 的保護我們可以直接透過 `return to libc` 去拿到 shell  
**可惜世界上總是很多事情沒有如果...**  
所以我們必須先想辦法讓程式 memory leak  
這樣一來 20 byte 就完全不夠用了...  
所以我們可以 ret 到 `read_80_bytes` 來讀取更多的內容  
不直接跳到 `read` 是為了省下參數空間  

btw, 因為暫存的 `ebp` 會被覆蓋  
執行到 `leave` 時會改變 `esp`  
在讀完額外的 80 byte 時  
我們將內容讀到 bss segment 上  
並且將 `ebp` 蓋成 bss 的位置  
第二階段的 rop chain 都改放在 bss 上  

最後只要隨便找個 got 上有的 function  
把內容改成 `system` 的位置  
在 cat flag 就得到結果了  

flag: `HITCON{Y0ur rand0m pay1oad s33ms w0rk, 1uckv 9uy}`
