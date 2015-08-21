title: 9447 CTF 2014 pwn 420 classy 
date: 2014-12-4 14:22
category: pwn
tags: Other CTF
slug: 9447ctf_pwn_420_classy 

這題看了十個小時多卻沒解出來  
實在是很挫敗......  
不過還是覺得這題該寫個 write up 紀錄  
下次才不會一樣進入思維誤區  
* * *

這題是 binary 是用 C++ 寫的  
還包含了一些 libary function  
程式規模非常大 要每個 function 都看過不太可能  

`main` 非常簡單  
進行 io redirect 和一些參數的檢查  
接著就進入兩個關鍵的 function  
`parse_file_or_die()` 以及 `gogo()`  

這兩個 function 都十分複雜  
而且又用了不少動態跳躍  
即使用 ida pro 翻成 pseudo code 也不完整  
很難完全看懂  
用動態分析其行為得到結果是：

- `parse_file_or_die()`
    讀入一個 java class，如果格式有誤或者使用了不允許的動作都會發生 exception 並結束
- `gogo()`
    逐步執行 bytecode，如果使用沒有實作的指令或是使用 mnemonic 有問題，就跳出 exception 並結束

所以這題是個 java emulator  
一開始以為這題是 jailbreak 的類型  
一直在想辦法繞過 `parse_file_or_die()` 的限制去讀 flag  
但是這個方向顯然是錯的  
直到官方放出了 `libc-2.19.so` 才把方向轉為尋找漏洞...  
這邊犯下了第一個錯誤－－太執著於靜態分析  
花了很多時間在看 `parse_file_or_die()`  
直到 Lays 發現寫 bytecode 使用數個 `ldc` 會導致程式 smash tht stack  
才確定 vuln 在 `gogo()` =\_\_=  

有了 crash 點就很輕易能找出程式是哪裡出問題 (fault localization?)  
逐步追蹤可以找到 crash 的原因在呼叫 `Stack::push()` 會 overflow  
後來又發現 istore 算好 offset 可以改到 eip 的 value  
但由於一次寫入會是 16 byte (tag + value)  
tag 值無法控制...也就是說無法控制連續的 stack  
只能做一次 return  
沒有辦法成功構造出 rop 去 leak information 再跳到 system  
嘗試找 gadget 來解決 stack layout 的問題  
經過三小時的嘗試後宣告這方向似乎是錯的....  
開始把方向轉到尋找可用的 bytecode  
但是時間已經不夠了 Q\_\_Q  

後來花點時間把程式完全看懂  
這題的問題是這樣子的.....  
(後面 **小寫 stack** 表示 elf 的 stack、**大寫 Stack** 表示 jvm 模擬的 stack)  

這題在初始化 jvm 的環境後  
將一些參數 push 進 Stack  
就開始執行 java main function 的 bytecode  
接著可以使用 bytecode 操作 Stack 的指令去控制 stack  
這題的 Stack 並不是使用 C++ 的 standard library 寫的  
而是出題者自已寫的 Stack 物件  
導致可以 overflow 以及修改 stack 的內容  
push 的單位是一個 `StackItem` = 16 byte  
但也造成前面提到的不能連續控制記憶體的問題  

```
struct StackItem
{
    int tag;
    int value;
};
```

- `ldc [value or str]`
- `sipush [value]`  
    兩個指令類似，在 Stack push StackItem
- `istore [offset]`
    在 Stack + offset 的位置寫 StackItem
- `iload [offset]`
    在 Stack + offset 的位置 pop StackItem，檢查 StackItem.tag 的值是不是 0x2f，如果是就 push 進 Stack
  
理論上 `iload` 做 `0x2f` 的檢查以後沒辦法任意讀取記憶體內容  
但是這邊其實是有問題的  
原因是 Stack 的內容並沒有對齊 16 byte  

```
0xffffd020:     0x0000005e      0x08065188      0xffffd034      0x0805305c
0xffffd030:     0x080650f8      0x0000002f      0x0000002f      0x0000002f
0xffffd040:     0x0000002f      0x0000002f      0x0000002f      0x0000002f
0xffffd050:     0x0000002f      0x0000002f      0x0000002f      0x0000002f
0xffffd060:     0x0000002f      0x0000002f      0x0000002f      0x0eceea00      <-- stack guard
0xffffd070:     0xffffd080      0x00000000      0xffffd128      0x08054180
```

`ldc 0x2f` push 大量的 0x2f 進入 Stack  
`iload` 是按照 `[Stack + offset\*8]` 的方式去存取 Stack  
如果把 push 的內容就是 0x2f 就可以 bypass `iload` 的 檢查  
因此我們可以順利得到 stack 上的內容  
以此例來說，`iload` 得到的結果是 stack guard  
用同樣的方式可以得到出 `libc` 的位置  

嚴格來說，這樣並沒有成功 leak memory  
因為不會 print 出來，我們也沒辦法再接 io  
但是這題也不需要  
用 `iload` 得到 libc 以後可以直接用 bytecode 提供的指令做運算  
算出 `system` 的位置，再用 `istore` 重新寫回 stack  

總結這題的做法如下：

1. `iload` 得到 stack guard  
2. `iload` 得到 libc address  
3. 利用 `sipush`、`iadd`、`isub` 等做運算得到 `system`、`/bin/sh`  
4. `istore` 改寫 ret address 以及參數  
5. `istore` 將被更動的 stack guard 寫回  

* * *

經過這題才發現自己的思維很狹隘  
執著於過去學到的 rop 走入誤區  
一直想著如何 leak address  
卻沒想到可以利用 java 本身做運算  
紀錄此篇 write up  
希望以後不會犯下同樣的錯誤  
