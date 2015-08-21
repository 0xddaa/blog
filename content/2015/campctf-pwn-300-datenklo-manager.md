title: CAMPCTF 2015 Pwn 300 datenklo manager
date:
category: pwn
tags: CAMPCTF, hof
slug: campctf_pwn_300_dkm

這次的 pwn 題型都很和善  
這題應該是裡面最難的一題 (?  
至少對我來說 heap 還是很難解 OTZ  
* * *
題目跟一般 heap 題差不多  
一個選單有數樣功能:

1. List DK
2. Add DK
3. Edit DK
4. Delete DK
5. exit

DK 又分成兩種類型: `with wifi`, `without wifi`  
這個程式用到的結構如下:

```
struct DK_base {
    long lg;
    long la;
    void *show_ptr;
    void *edit_ptr;
};

struct DK_with_wifi {
    DK_base base;
    char* ssid[32];
    char comment[1024];
};

struct DK_without_wifi {
    DK_base base;
    char comment[1024];
};
```

`show_ptr` 和 `edit_ptr` 會在 `List DK` 和 `Edit DK` 的功能用到  
在 add 之後就會根據 DK 種類填入對應的函式位置  
程式根據目前 DK 的數量動態配置一個陣列來記錄 DK  
兩種 DK 用同一個陣列去記錄  
因此會根據 DK 種類不同呼叫不同的函式處理 DK  

程式的漏洞是
先 add 一個 `DK_with_wifi`  
接著 edit dk 將種類改成 `DK_without_wifi`  
程式會在同一個位置將 chunk 重新 realloc 0x420 byte  
但是 edit 有一個選項是 `do not change`  
會用一開始宣告時分配的 func 去處理 DK  
因此我們可以用處理 `DK_with_wifi` 的 edit function 去處理 `DK_without_wifi`  
由於兩者大小相差 0x100 byte  
因此會導致 `heap overflow` 的問題  

這題我的利用方式是 [The Malloc Maleficarum](https://dl.packetstormsecurity.net/papers/attack/MallocMaleficarum.txt) 提到的 `The House of Lord`  
原理是 overflow 以後把 freed chunk 的 BK 改成我們偽造的 chunk  
這樣下次 malloc 的時候就會得到所偽造 chunk 的位置  
詳細步驟如下:

1. 新增兩個 `DK_with_wifi`, 利用 `comment` 的 1024 byte 偽造兩個 freed chunk  
2. 用 edit 將第一個 DK 的類型改成 `DK_without_wifi`  
3. 再 edit 一次, 這次選 `Do Not Change`, 在 edit comment 的時候會超出 0x100 bytes  
4. 利用超出的 0x100 byte 把 BK 改成 第一個 chunk 的位置
5. 隨便 add 一個 DK, 這個 DK malloc 得到的位置會和第一個 DK 的 comment 重疊
6. 用 `Do Not Change` 編輯第一個 DK, 修改 comment 時可以改到第三個 DK 的 func ptr, 把 `edit_ptr` 改成 system  
7. 用 `Do Not Change` 編輯第三個 DK, 由於 `edit_ptr` 已經被改掉, 會變成執行 system  

libc address 和 heap address 可以利用 `list DK` 取得  
system 的參數剛好會落於第一個 DK comment 的位置  
所以可以直接 `system("/bin/sh")` 取得 shell  
完整 exploit: [exp.py]({filename}/exp/dkm.py)

* * *
btw, 後來 **angelboy** 說只要 edit 的時候 SSID 設 0  
下次 add 的 DK 可以直接被 overflow 蓋 func ptr 了...  
這題是我想太難了 OTZ  
