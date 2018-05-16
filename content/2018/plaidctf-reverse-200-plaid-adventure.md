title: Plaid CTF 2018 Reverse 200 Plaid Adventure
date: 2018-5-17 04:04
category: reverse
tags: PlaidCTF
slug: plaidctf_reverse_200_plaid_adventure

這題困難的地方都被 **lucas** 逆完了 <(\_ \_)>  
不過有個小地方讓我們卡關超久...  
BTW，我覺得這題分數 200 分有點太少...  

* * *

## Overview

將題目給的檔案解開後，發現竟然是個 web service = =  
不過只是個靜態網頁，可以隨便用個 python http server 跑起來  
用 broswer 連上可以發現是個文字解謎的遊戲  
這種遊戲模式被稱為 [Interactive fiction](https://en.wikipedia.org/wiki/Interactive_fiction)  

遊戲開始後會進入一個迷宮  
迷宮不算複雜，正常的遊玩就可以把所有場景走一遍  
可以入手的道具有：

1. 紅、藍、黃、綠 四色寶石各一顆
2. 大門鑰匙

獲得所有道具後前往某個有大門的場景  
用鑰匙打開門後，會有一台機器可以放置四色寶石  
依序放上後，出現 ... 的訊息  
猜測是要根據某個順序觸碰寶石  
到這邊就無法用正常的繼續遊戲，開始需要逆向遊戲的邏輯  
我大概花一個小時就過到這邊，接下來卡了十幾個小時...Orz  

```
>put red
(the red orb in the red slot)
The red orb clicks into place, and lights up with a subtle glow.

>put blue
(the blue orb in the blue slot)
The blue orb clicks into place, and lights up with a subtle glow.

>put yellow
(the yellow orb in the yellow slot)
The yellow orb clicks into place, and lights up with a subtle glow.

>put green
(the green orb in the green slot)
The green orb clicks into place, and lights up with a subtle glow.
The machine whirs to life, and the orbs get brighter. Perhaps you could try touching them?

> 
```

## Analysis

一開始有些困惑這題的目的是什麼  
因為 web 並不會去讀取 gblorb  
研究了一陣子發現 web 是透過 interpreter 執行 `Plaid Adventure.gblorb.js`  
也可以用其他的媒介載入 gblorb 執行遊戲，兩者沒有差別  

用 file 查看 gblorb 會得到以下結果：
> IFF data, Blorb Interactive Fiction with executable chunk

丟給 google 搜尋得知和 [Inform 7](https://en.wikipedia.org/wiki/Inform#Inform_7) 有關  
Inform 7 是拿來開發 IF 的一種 framework  
可以讓開發者用自然語言來撰寫 IF 遊戲   
寫好的遊戲會以 [Glulx](https://en.wikipedia.org/wiki/Glulx) 運行   
Glulx 是一種專門用來執行 IF 的虛擬機  
[https://www.eblong.com/zarf/glulx/](https://www.eblong.com/zarf/glulx/) 收集了各種 Glulx 的實做  
我後來是選擇用純 cmdline 操作的 **glulxe** 來執行遊戲  
比較方便透過 script 操作  
不用每次重新手動走迷宮 XD  

## Reversing

上述的網站也有 Glulx 的完整 spec  
原先以為要看懂他的實作自己 parsing gblorb 的內容  
但搜尋一下發現已經有寫的 decompiler [mrifk](https://hackage.haskell.org/package/mrifk)   
可以將 gblorb 轉成 human readable 的 pseudo code  
片段如下：

```
[ routine221097 local0 ;
    local0 = 0;
  .label221105:
    if (local0 < 16) {
        478466->local0 = 0;
        local0 = local0 + 1;
        jump label221105;
    }
    return 1;
];

```

pseudo code 中有幾種比較重要的語法

1. Object
    - Object 會定義遊戲中的各種場景和物件，並且描述他們之間的關聯性
    - e.g. 房間 A 可以往西走到房間 B，這樣 Object 就會定義 A 和 B 的關聯性
2. Routine
    - Routine 像是執行了某個指令後要觸發的行為，基本上跟 function 十分類似
    - e.g. 輸入 `open door`，觸發開門的 Routine，但因為門是上鎖的，檢查某個變數沒有被設置後，就印出對應訊息然後結束 routine，輸入 `unlock door with key` 之後，觸發開鎖的 Routine 並設置變數，再次輸入 `open door` 就可以順利開門
3. local0, local4, local8, ...
    - 類似 local varible 的概念，從命名規則可以推測變數的大小
    - 宣告在 routine 名稱後面的代表是 caller 傳來的參數
4. 478466->local0
    - 類似全域變數，此例 `478466` 是個長度為 16 的一維陣列，local0 是 index


但光靜態分析 psedo code 還是難以完全理解程式邏輯  
需要一邊執行遊戲，一邊猜測運行到 pseudo code 的哪一段  
使用 **glulxe** 進行遊戲還有另一個原因  
**glulxe** 支援簡單的 debug 功能  
但由於我們沒有遊戲產生時的 debug info  
沒辦法直接存取遊戲裡的數值，只能簡單的下斷點來看程式運行到哪個階段  
斷點還只能設在 routine 的開頭...  

透過比對 object 在那些 routine 被使用，及透過 breakpoint 耐心的 try and error  
可以追到有兩個 routine 是解這題的關鍵：

- `routine221131`
    - 處理 touch 礦石的 Routine
    - 做的事情是把每三次觸碰的寶石顏色轉成一個數字，再存入一個長度 16 的矩陣
        - red: 0b01
        - blue: 0b10
        - green: 0b10
        - yellow: 0b11
    - e.g. 觸碰紅色三次就代表 `0b010101 = 21`
- `routine220666`
    - 判斷觸碰的順序是否正確，正確則進入 `routine221211` 印 flag
    - 將 `routine221131` 得到的矩陣與位於 `478802` 的二維陣列相乘，得到的結果要與 `478482` 的陣列相同

不過前面有提到 debugger 沒辦法存取數值  
但我們可以對 glulxe 稍做修改，印出 Glulx 裡面 `478802` 和 `478482` 位址上的資料  

## Solving

由於陣列的大小都是 1 byte  
`routine220666` 其實就是 ring 在 0 ~ 255 的矩陣乘法  
`routine221131` 得到的矩陣 A 乘上位於 `478802` 的矩陣 B 等於位於 `478482` 的矩陣 X  
問題簡化為：**AB=X, 已知 B 和 X，求 A 的值?**  
因此只要求出 B 的反矩陣與 X 相乘就可以得到結果  
將結果根據 `routine221131` 的規則做基底為 4 的因式分解就可以推回觸碰的順序  
聽起來很完美，但實際上並不是 Orz  

解出來的 A 是 `[188, 185, 130, 28, 247, 150, 58, 227, 106, 0, 116, 197, 113, 25, 178, 70]`  
根本無法用 `routine221131` 的規則推回對應的顏色  
這邊一開始是先用 z3 求解，為了避免是 z3 規則寫錯，後來改用 sage 做矩陣運算，也是得到相同的結果  
就這樣卡了一陣子，後來發現 `478482` 除了 `routine220666` 以外  
還有一個 `routine221185` 會把 478482[15] + 1 ...  
重算一次得到正確的結果：`[48, 7, 46, 15, 21, 25, 11, 24, 49, 16, 55, 12, 40, 41, 48, 47]`  
轉換為顏色後，順序是：
`B B Y Y R B G Y G Y Y B R R R R G R Y G B B G R R B Y B B R Y R Y B Y B B G G R G G B B Y Y Y G`  
但我們因為不知道如何觸發 `routine221185`  
做法是直接修改 gblorb 上對應到 478482 的位址  
在按照上面的順序觸摸寶石，flag 就會噴出來了  

```
The four orbs get brighter and brighter, as the machine starts violently whirring and clicking. You close your eyes as blinding light fills the room. When you finally open your eyes, you find yourself outside of the cavern, holding the flag in your hands:

PCTF{Tw1styL1ttl3Fl4g}


    *** The End ***
```

## Note

比賽結束後，irc 上出題者說，要發現隱藏的指令 `xyzzy`  
輸入這個指令就會觸發 `routine221185`  
應該有不少人也是卡死在這邊 XD  


flag: `PCTF{Tw1styL1ttl3Fl4g}`  
exploit: [solve.sage]({filename}/exp/plaid-adventure.sage)  
