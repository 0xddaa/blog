title: Codegate CTF Preliminary 2014 200 dodoCrackme
date: 2014-2-24 1:53
category: reverse
tags: CodegateCTF
slug: codegate_2014_reverse_200_dodocrackme

這是應該是我玩過的 CTF 裡面最硬的一次 ORZ  
大量的 pwn 和 reversing  
根本破壞遊戲體驗....= =  
這次跟 217 和 chroot 還有 sqlab 學長一起參加  
跟大大們學到很多招數 :)  
希望下次別這麼醬油了 Orz  
* * *

這題是 **ELF 64-bit LSB executable**  
先觀察一下行為:  
> root@localhost's password: 1234  
> Permission denied (password).  

感覺就要先把 root password 弄到手  
先把分析看看 binary  
用ida打開會嚇一跳  
因為是用組語寫的 Orz  
function 只有一個start  
出現很多 syscall  

查一下資料發現 syscall 會把 call number 放在 `rax`   
用 interrupt 處理動作  
```  
 mov    $0x1,%eax  
 mov    $0x1,%edi  
 mov    %rbp,%rsi  
 mov    $0x1,%edx  
 syscall  
```  
  
上面組語的行為是 `write(1, rbp, 1);`  
過程中是用 inc / dec 控制輸出的 byte  
直接看 code 看不出密碼  
輸出 *root@localhost's password:* 後  
接著是一些用途不明的 code  
然後才是 syscall read  
在 syscall 的地方下 breakpoint  
接著把 `rbp` 附近的 memory dump 出來  
發現從 `0x7ffff7ff8b58` 開始  
每隔 16 byte 就會有奇怪的字元:  
> 0x7ffff7ff8b58: 72 'H'    
> 0x7ffff7ff8b60: 0 '\000'  
> 0x7ffff7ff8b68: 52 '4'    
> 0x7ffff7ff8b70: 0 '\000'  
> 0x7ffff7ff8b78: 80 'P'    
> 0x7ffff7ff8b80: 0 '\000'  
> 0x7ffff7ff8b88: 80 'P'    
> 0x7ffff7ff8b90: 0 '\000'  
> 0x7ffff7ff8b98: 89 'Y'    
> ...  

所以推測剛剛那段意義不明的 code 是用來生成 password  
不過到這已經可以知道 flag 了  
我就沒有去回去研究到底是不是如我猜想的了  

flag: `H4PPY_C0DEGaTE_2014_CU_1N_K0RE4`  
