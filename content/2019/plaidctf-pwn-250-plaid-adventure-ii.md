title: Plaid CTF 2019 Pwn 250 Plaid Adventure II
date: 2019-4-16 03:05
category: pwn
tags: PlaidCTF, Out-of-bound
slug: plaidctf_pwn_250_plaid_adventure_ii

這題約結束前 10 分鐘跟 angelboy 一起寫完 exploit  
已經確認在 local 可以打, 結果 remote server 壞掉 = =  
不然應該有機會 AK 的...QQ  

* * *

## Overview

跟去年 [Plaid Adventure](https://ddaa.tw/plaidctf_reverse_200_plaid_adventure.html) 一樣是由 [inform 7](http://inform7.com/) 寫成的互動式文字遊戲  
題目敘述說要讀取 `flag.glksave`, 但沒辦法使用 `restore` 這個指令  
目的還算滿明確, 要用題目中的漏洞想辦法繞開限制執行 `restore`

## Analysis

逆向的方式請參考去年的 write up, 逆完之後大致可以知道遊戲是:

- 只有一個場景, 場景上只有 `machine` 和 `blackboard` 兩個物件
- `look machine` 可以從結果得知 `dial`, `slider`, `button` 三個物件
    - `set dial to $flavor` (`select $flavor`) 可以選擇飲料的口味
        - 一共有 18 個口味: apple, apricot, blackberry, cherry, cranberry, cola, grape, guava, lemon, lime, orange, pickle, peach, pear, pineapple, raspberry, strawberry and watermelon
        - `set slider to $num` (`set $num`) 可以設定將 slider 設成 -2147483648 ~ 2147483647 之間的數字
    - `push button` 會掉一瓶飲料出來, 飲料會印上 `$index:$slider` 的 symbol
        - 背包最多只能擺 6 瓶飲料
        - 不能重複購買飲料
- `drink $flavor` 可以把飲料喝掉, 喝完背包的空間會清出來
    - `pickle` 因為太難喝沒辦法喝掉...XD
- `look blackboard` 會印出以下內容:
> A blackboard. On it is written:  
> The flag will be here after restoring!
- `(write|erase) blackboard` 可以在 blackboard 上寫字或清除, 最多不能超過 35 個字
- `restore`, `save` 之類的系統指令都被禁用了

## Solving

這題的困難點就是在逆向和找洞...  
經過一番波折後，發現這題的漏洞在 `pickle` 雖然沒辦法喝掉  
但還是會將背包飲料的數量 - 1, 因此可以突破背包 6 瓶飲料的限制  
飲料在印 symbol 時會存在 `479074_soda_sliders`  
超過 6 瓶會 out of bound write, 蓋到後面 `479098_soda_func` 的內容  
而 `479098_soda_func` 是一個 func ptr array ... XD  

到這邊已經可以自由控 $pc 到任意位置  
很開心地想說跳 `restore` 就可以結束了, 但發現可以跳 `save` 卻不能跳 `restore`  
因為...  

```
[ routine7331_restore local0 local4 ;
    @nop;
    @nop;
    @nop;
    ...
    return 1;
];
```

◢▆▅▄▃ 崩╰(〒皿〒)╯潰 ▃▄▅▆◣

比對了 asm 確定是沒有其他的 `@restore` 指令集可以使用  
接下來很明確必須自行寫入 shellcode, 並跳過去執行 (glulx vm 不存在 NX 保護)  
原本想透過黑板的 write 指令來寫 bytecode  
但發現 write 指令沒辦法讀 null byte  
而要將 shellcode 偽造成 routine 一定得包含 null byte... orz  
BTW, 如果直接跳到非 routine 開頭的位置, glulx 會直接發生 exception 終止程式  

卡了一陣子才想到可以利用前面 `479074_soda_sliders` 來放 shellcode  
`479074_soda_sliders` 是一個 big endien 的 int 陣列  
只要重複 `set slider to $num` 和 `push button` 就可以寫入 shellcode  

這邊原本想把去年題目的 restore bytecode 送過去  
但發現因為遊戲檔案格式和版本不同, 沒辦法直接參考  
花了一點時間弄出最新版的 `.ulx` 檔案  
又發現完整的 restore 長度會超過可用的空間 = =  
最後透過 try and error 確定只需要留以下 asm 就可以達到 restore 的功能:

```
@callfiii routine763 1 2 0 -> local4;
@callfiii routine589 local4 2 301 -> mem450124;
@restore mem450124 -> local0;
return -1;
```

最後只要把超出背包的某瓶飲料 slider 設到放 shellcode 的位置  
執行 `drink $flavor` 就可以觸發 restore, 輸入 `flag` 讀取 `flag.glksave`  
再回來看 blackboard 上的內容就有 flag 了  

此時就很悲劇的發現 remote server 壞掉  
就此跟 AK 無緣 QQ  

不過後來修好之後, 還發現有一點小問題  
remote 因為 terminal 不同的關係, 觸發 `restore` 時 input buffer 是髒的  
不能直接輸入檔名, 要先送一些 `/b` 清掉 buffer 之後  
再送 `flag` (or `flag.glksave`) 才會是正確的檔名  

## Note

其實發現 pickle 不能喝有一段時間  
但我竟然沒有馬上意識到漏洞有相關...Orz  
也沒有馬上提出來討論  
不然可能可以省下 2 hr 的找漏洞時間來寫 exploit  
絕對是戰犯無誤 QQ  
還好沒有錯失 DEFCON 的資格...  

flag: `PCTF{pWn_4dv3ntUrE_IF_3d1ti0n}`  
exploit: [plaid-adventure-ii.py]({filename}/exp/plaid-adventure-ii.py)  
