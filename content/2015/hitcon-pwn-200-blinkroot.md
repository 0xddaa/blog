title: HITCON 2015 PWN 200 blinkroot
date: 2015-10-20 1:23
category: pwn
tags: HITCON CTF, dl_resolve
slug: hitcon_pwn_200_blinkroot

這次也是一題都沒解出來  
大概是沒天份吧  
不過其實後來知道怎麼偽造 link\_map 以後  
比賽期間寫的 payload 一度已經很接近了...  
只是後來方向錯了 Orz...   
* * *
這題的程式非常簡單  
pseudo code 長這樣:  

```
char data[1024];
int main()
{
    if (recvlen(0, data, 1024) == 1024) {
        close(0);
        close(1);
        close(1);
        data[(int)data] = (int128)(0x1000000000 | data[8]);
        puts(data[16]);
    }
    exit(0);
}
```

前八個 byte 可以任意控制  
所以會造成任意寫值的問題
這題不知道用什麼方式  
組合語言是透過 xmm0 寫值  
能寫的位置一定要對齊 16 byte (addr & 0xf == 0)  
而且前 8 byte 還固定成 0x10  
所以不能單純靠改 `.dynamic` 來解這題  
那這題的作法是偽造 *link_map* 以後做 *dl_resolve*  
目標讓呼叫 `puts(data[16])` 變成解出 `system[data[16]]`  

*dl_resolve* 是 ELF 有做 lazy binding 的時候  
function call 不會直接跳進 libc  
而是透過 got.plt 得到 function 的 index 後  
跳到 PLT0 才解析出 function 在 libc 中的位置  
簡單來說大概就是做這樣的事情  
`dl_runtime_resolve (link_map,index)`  
*dl_resolve* 裡面還會 call `_dl_fixup`  
`_dl_fixup` 才是真正去查 libc address 的地方  

以前考過的 *dl_resolve* 的做法  
是透過偽造 index  
讓 `__fix_up` 去解 symbol 時落在我們偽造的 *SYMTAB* 上面  
再讓查 `st_name` 時落在我們想要執行的 function 名稱  
這題的沒辦法去控制 index  
所以變成只能從偽造 *link_map* 下手  

根據我比賽時的整整 12 個小時的嘗試...  
完整的偽造 *link_map* 是不可能做到的 T\_\_T  
原因是 *link_map* 中有一個 `l_scope` 的 member  
在 `_dl_fixup` 內部的 `_dl_lookup_symbol_x` 會用上  
`l_scope` 會指向 *link_map* 本身  
*link_map* 的結構是一個 linked\_list  
每個 node 保存 elf 和有使用到的 shared library symbol  
`_dl_lookup_symbol_x` 比對所有 shared library 的 symbol  
試著找出目前 function call 的這個 symbol  
我們無法得知 glibc 的 *link_map* ... 所以不可能偽造成功 QQ  

那 *dl_resolve* 還有一個利用方式是:  
如果 function 已經被解析過  
[dl-runtime.c:90](https://github.com/lattera/glibc/blob/master/elf/dl-runtime.c#L90)  
> `if (__builtin_expect (ELFW(ST_VISIBILITY) (sym->st_other), 0) == 0) { ... }`  
> `else { ... }`

會直接進入 else, 不會進入 `_dl_lookup_symbols_x`  
直接透過 `link_map->l_addr + sym->st_value` 得到結果  
這兩個值都可以透過偽造 *link_map* 來控制  
如果在已知 libc 版本的情況下  
我們可以讓 `l_addr` 或 `st_value` 其中一個是以解析過的 function  
另一個則透過 libc 算出適當的 offset  
就可以跳到任意函式了  
還有一個要注意的是  
原本 *dl_resolve* 解析完會將結果寫回 GOT 上  
但是 offset 亂掉了結果可能會是一個不能寫的區段  
所以還要偽造 *JMPREL* 結果能寫回去才行  
至於要寫到哪裡就隨意了 反正之後不會用上  

這題我先嘗試讓 *link_map* 落在 `__libc_start_main` 的 GOT  
這樣 `l_addr` 就會是 `__libc_start_main` 的 address  
再偽造 `STMTAB` 和 *JMPREL* 得到 `st_value` 並算出 system 的位置  
結果是成功的...但是這題有個問題是  
如果這樣子偽造, *link_map* 會在 `data - 0x48` 的位置  
但是 *SYMTAB* 的位置在 `link_map + 0x68 == data + 0x20`  
`puts` 的參數卻是 `data[0x10]`...  
所以能執行的指令就變成不能超過 16 byte XD  
對於一般的題目倒也沒差  
但是這題把 fd 都關了所以只能把執行結果送回來而已  
16 byte 根本不夠用 Orz  

第二次的做法就變成讓 *link_map* 完整的落在 data[512] 上  
`l_addr` 可以隨意控制  
再將 *SYMTAB* 偽造到 GOT 上  
滿足 `st_other != 0` 且 `st_value == libc address`  
一樣要偽造 *JMPREL* 讓結果可以寫回去  
就可以解出任意的 libc function 了  
後來想想第二種的做法似乎限制比較少  
更好利用  

總結一下透過 `st_other` 的利用條件:  

1. 已經有 glibc 可以算 offset
2. 有大約 0x140 以上的 buffer 可以偽造 *link_map*
 - 取決於 function index, 越後面所需空間越大
3. 可以 return 到 plt 上, 或是可以改 got 上的 *link_map*
4. 要已知可寫的 address ... 所以開 PIE 這招大概還是不能用 Orz

flag: `hitcon{81inkr0Qt I$ #B|InK1n9#}`
