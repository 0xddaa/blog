title: GiTs 2014 Reverse 150 papsmear
date: 2014-1-20 19:58
category: reverse
tags: GiTsCTF
slug: gits_2014_reverse_150_papsmear

這題很慢才打開  
解出來的時後竟然超過時間了阿阿阿  
悲劇 看來還是對 python 不夠熟  
* * *

根據說明用 nc 連至目標後  
隨便輸入一些字串  
得到錯誤訊息 :  

>  Serial: asd  
> Bzzt. Wrong!  

直接打開檔案發現是一個 python 的 code  
最後有兩行:  

```
with open('flag.txt','r') as f:
    print f.read()
```

看來這題的目的很明顯了  
需要找出一個正確 Serial 滿足所有條件  
Server 就會把 key 給噴出來  
剩下的就是 trace code...  
首先，程式將 Serial 以 *-* 分開 變成 6 個數字  
每次取 1 對數字 `(num1, num2)` 做判斷  

先解釋一下每個函數代表的意思:  

1. `_a()` : 得到數個質數，大小為 2~x ，每次呼叫後都會改變下一次呼叫的值
2. `__a(n)` : 為 `_a()` 所得到的質數做過濾，如果是 n 的因數，則過濾此質數
3. `___a(n)` : 將 `__a()` 過濾後的質數做 (1 - 1.0 / p) 取整數後相乘
4. `____a(n)` : `___(num1 * num2) == ___a(num1) * ___a(num2)`
5. `_____a(num1, num2)` : 限制 num1 介於10001~100000，num2 介於100~999

程式有幾條限制 任何一條沒滿足都會發生 exception 並結束:  

1. `_____a()` 回傳 True
2. `___a(num1) == num1 - 1`
3. `____a()` 回傳 True
4. 3個(num1,num2)組合不能相同
5. 最後一個條件有點複雜，直接看 code

```
for k in range(7,10):
  a,b = int(c.pop()),int(c.pop())
  for x in [a+b*n for n in range(k)]:
    y = [p for p in __a(x)]
    if not (len(y)==1 and y[0]==x):raise
```

看似條件很多  
但是其實 *條件 1* 是限制 input size  
*條件 3* 很容易滿足  
所以暫時不用考慮  
我們先找出滿足 *條件 2* 的所有 `num1`  
再用暴力解去找出滿足 *條件 5* 的解  
最後再用 *條件 3* 來檢查是不是正確的解  

只有三組 k 滿足以上條件  
**k = 7 or 8 or 9** 
分別對應到 3 組 num  
有些解是共同的  
因為 *條件 4* 的限制所以要挑不一樣的解  
隨便選一組送過去就拿到key了  

> Serial:  
> 10243-420-11003-630-10859-210  
> The flag is: ThesePrimesAreNotIllegal  

flag: `ThesePrimesAreNotIllegal`  
