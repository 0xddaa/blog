title: CSAW CTF 2015 pwn 500 rhinoxorus 
date: 2015-9-21 21:23
category: pwn
tags: CSAWCTF, bof
slug: csawctf_pwn_500_rhinoxorus

想說這次 CSAW 從比較難的題目開始解  
結果 ida 打開一分鐘就看到洞了 囧  
不過 exploit 還是寫個 3 小時左右吧  
挺煩人的...
* * *

這題的程式行為就是不斷的做 function call  
有 256 個不同的 function  
buf 大小不太一樣, 行為卻都類似  
毫無意義可言....
程式碼大概長這樣:  

```
void func_2a(char *a1, int a2)
{
    char buf[100];
    int len = a2 - 1;
    ...
    if (len) {
        for (i = 0; i < len; i++)
            buf ^= a1[i];
        func_array[buf[0]](&buf[1], len);
    }
}

void process_connection(int fd)
{
    char buf[256];
    int len;

    memset(buf, 0, 256);
    len = recv(fd, buf, 256, 0));
    if (len > 0)
        func_array[buf[0]](buf, len);
}
```

這邊先定義一次 stack frame 的層數  
後面會比較好說明  

1. layer0: `process_connetion` 的 stack frame  
2. layer1: 第一次的 function call  
3. layer2: 第二次的 function call, 後以此類推  

很明顯的 overflow  
下一層的 buffer 一定比 `layer0` 的 256 小  
做 xor 時就會蓋到超出 stack frame 的範圍  
而且還不是直接 copy 過去  
是做 xor 寫值 ... 所以什麼 stack guard 根本可以無視 XDD  

那思路其實就滿明確的  
**先 bof, 然後做 rop**  
先隨便送個 256 字元試試...  
*Segmentation fault*  
表示漏洞的確存在, 但是跟我的預期不太相符  
我原本是預計會發生 _\*\*\* stack smashing detected \*\*\*_  
gdb 實際追一下發現在做 xor 的時候存取到 stack 以外的範圍了  
仔細看一下是因為 `len` 在 buffer 的後面...  
bof 會順便被改掉的關係  

仔細想一下 `len` 這邊也要好好設才行  
因為這個程式會一直 call 一直 call  
就算正常結束的話也會做 256 次之後才觸發 return  
這樣 payload 早就被 xor 得不成人形了...  
但是也不能再 `layer1` 就改成 0  
不然這樣改完 `len` 就不會繼續蓋後面的 return address 了  
所以理想的狀況是:  

* 在 layer1 寫好 rop chain  
* 在 layer2 改掉 `len` 觸發 return  

所以 `layer1`, `layer2` 是哪一個 function 就要好好考慮一下 XD  
挑對 function exploit 會比較好寫一點  
`layer1` 的 buffer 要大一點, 不然 xor 會蓋到 `layer0` 的 buffer  
`layer2` 的 buffer 要小一點, 第二層 overflow 會蓋不到 `len`  
我不幸挑錯 `layer2` function ...  
會進入到 `layer3` Orz ...  
變成要讓兩次 stack guard 都不能被更動才行  

可以觸發 return 後  
就用 pop 之類的先把未知的垃圾跳開  
讓 rop chain 可以完整地落在 buffer 上  
接下來我是把 stack 先移到 bss 段  
再跳一次 recv 接第二次 rop  
這樣就不會一直被 xor 弄壞了  

exploit: [rhinoxorus.py]({filename}/exp/rhinoxorus.py)  
