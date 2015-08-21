title: Secuinside ctf 2014 reverse 100 find key
date: 2014-6-9 2:46
category: reverse
tags: OtherCTF
slug: secuinside_reverse_100_find_the_key

這題是快要結束才開出來的一題 reverse  
到結束也沒人解出來 ORZ  
稱假日有點時間還是把它解出來了...  
* * *

題目是一個 32 bit 的 elf  
執行需要輸入兩個參數  
題目會先對第一個參數做檢查  
> ./findkey 123 123  
> key 1 = 123  
> 0 is differnce  
> Wrong password  

很快找到檢查第一個參數的 function 在 `0x0804b76d`  
trace 完後這個 func 的演算法是：  

```
def sub_804b76d(arg1,n=0x31):
    for i in range(56):
        v7 = 0
        v4 = len(sentence[i])
        v2 = smaller(n,v4)

        for j in range(v2):
            v7 += (ord(sentence[i][j]) * ord(arg1[j]))
            j+=1

        if v7 != dword_804F180[i]:
            print "%d is difference" % i
            return
```

程式中存了 56 個字串  
會依序取得每個字元與 `argv[1]` 相乘並加總  
並檢查結果是否如預期  
看起來很複雜  
其實就是國中的數學 多元一次方程式 XD  
給 56 個方程式解 49 個未知數這樣  
但是這邊一開始卡關了  
逐一檢查後才發現  
由於字串中有幾個 byte 是特殊字元  
那邊在程式中的加總結果與我模擬的不同  
原因我沒有深究~ 反正只要有 49 個方程式就能解了  
把那幾個扣掉後依然可以得到解  
`3 lroea5 r tfmh0wl1y15on 3y! 4n 50r,30wv3r !4kwi`  
也就是第一個參數  

通過第一階段以後  
剩下的頗複雜 Orz  
很多 function 亂 call  
還有很多根本沒做事情 = =  
只好用動態分析的方式檢查 function 在做啥  
`sub_8048A32` 和 `sub_8048A58` 作用不明  
不負責任猜測可能是類似 `malloc` 和 `free` 的動作  
程式流程如下：  

```
sub_8048A32(src,0);
strtobigint(src,argv[2]);
memcpy(dst,src,sizeof(dst));
v3 = check_key2(argv[1],n,dst)^1;
sub_8048A58(dst);
if (v3) {
  puts("Wrongpassword");
  v2=1;
}
else {
  printf("Theflagis:'%s'\n",argv[1]);
  v2=0;
}
```

第二部分會先將 `argv[2]` 轉換成一個 struct  
架構大概長這樣：  

```
struct bigint{
  int signed;
  unsigned int length[2];
  unsigned int value[2000];
}
```

接著進入到 `check_key2()` 裡面  
程式流程如下：  

```
memcpy(&_bigint,bigint,8008u);
sub_804b330(digits,&_bigint,n);
sub_8048A58(&_bigint);
_0x31=n;
for (i=0;i<_0x31;++i){
  v12=0;
  for (j=0;j<i;++j){
    v3=*next_digit(digits,j);
    if (v3>*next_digit(digits,i))
      ++v12;
  }
  if (dword_804F280[i]!=v12){
    v4=0;
    gotoLABEL_15;
  }
}
```

首先是 `sub_804b330` 這個 function  
會將 `argv[2]` 所輸入的數字  
轉變成一個 mod 49 的多項式  
像是 `a48 * x^48 + a47 * x^47 + ... + a1 * x + a0` 這樣子  
此外還會確認 a0 ~ a48 是否全部不相同  
如果有任兩個相同會直接印出 `Wrong password` 並結束程式  

接下來程式會用兩個 for loop 去檢查分解出來的係數  
如果第 n 個係數 an < 前面的任一係數 ai  
v12 的值就會 +1  
接著對 v12 的值與保存於 `dword_804F280` 做比較  
其值依序為   
> 0 1 0 1 1 1 2 4 1 3 1 6 2 4 5 2 16 17 0 16 2 14 9 1 15 9 10 14 0 15 17 27 4 17 14 10 5 7 13 21 35 9 28 25 42 23 8 45 27

因為係數的值彼此不同  
比較係數大小可以確保係數的順序是正確  
接著要從 `dword_804F280` 去推算出正確的順序是多少  
觀察了一下發現到一件很重要的事情：  
**最晚出現的 0 代表其係數為 48**  
可以用反證法來推論其正確：  

1. 如果更前面有係數為 48 ， dword_804F280[i] 不會是 0
2. 如果更後面的係數為 48 ， dword_804F280[i] 不會是最後一個出現的 0

最後一個 0 在 index = 23 的位置  
因此 a23 = 48  
接著我們把 48 扣掉  
並且把 `dword_804F280` 所有 index > 23 的值 -1  
現在最後一個 0 所代表的值就是 47  
以此類推 我們可以得到所有的係數  
最後將所有係數透過多項式算出的大數為 `28367585747398446017812492718893415428463369378432457345198085366128794480569061784`  
也就是第二個參數  
兩個參數都正確 flag 也就噴出來了  
> ./exec  
> key 1 = 3 lroea5 r  tfmh0wl1y15on 3y! 4n 50r,30wv3r !4kwi  
> The flag is : 'w0w! 1nv3r51on arr4y i5 4we50m3 f0r th3 k3y, lol!'  

flag: `w0w! 1nv3r51on arr4y i5 4we50m3 f0r th3 k3y, lol!`
