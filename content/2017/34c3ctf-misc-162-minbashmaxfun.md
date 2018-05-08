title: 34C3CTF 2017 MISC 162 minbashmaxfun
date: 2018-1-4 01:05
category: misc
tags: 3XC3CTF, Bash, CMD Injection
slug: 34c3ctf_2017_misc_162_minbashmaxfun

34C3 跟去年一樣是在上班時間舉辦  
沒什麼時間打，第二天的下班時間幾乎都在解這題  
這題應該是至今解過限制最多的 cmd injection 題目了...  

* * *

題目會把我們的 input 丟到 `execl("/bin/bash", "/bin/bash", "-c", input, NULL)` 執行  
但 input 只能包含以下字元：`$ ( ) # ! { } < \ '`  
而且執行前會把 stdin 先關掉，無法交互執行指令  
（後面會說明這有多靠北 = =）  
原本以為是類似 [pwnable.kr](http://pwnable.kr) 的 **cmd3**  
可以拿以前的 payload 來用...果然是太天真了 QQ  
這題比起 **cmd3** 更困難的地方在於連路徑都無法使用  
不過，解題思路還是有相似之處  

**cmd3** 也限制了輸入英數字，但可以用 `$((a+b))` 的方式做出各種數字  
這題連運算符號也限制了...不過原理大同小異  

1. `$#` => 0  
    - `$#` 的意思是參數的個數，這題沒有其餘的參數所以會是 0   
2. `$(($#<$$))` => 1
    - `$$` 代表的是目前的 pid ，pid 會 > 0 所以可以得到 1
    - 後來看 write-up 學到 `${##}` 就能得到 1 
    - 大括號前面加 `#` 的用意是取得變數的長度
3. `$((1<<1))` => 2  
    - shift 運算，bj4
4. `$((2#bbb))` => 任意數字
    - 將 bbb 以二進制轉換成數字

接著就卡關了好一陣子，大概花了兩三小時 RTFM  
推薦超詳細的 bash 文件 [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/abs-guide.html)  
這題因為可用的字元超少，所以目標是先弄懂每個字元的功能  
早些時候 freetsubasa 提出了從 `$0` 的得到 `bash` 的思路  
但透過變數取得的數字會喪失原本的功能  
原本以為無法，結果在翻文件的過程發現 `${!#}` 這個東西  
效果等同於 `$BASH_ARGV`，其值會執行目前 script 的名稱  
前面提到這題的執行環境是 `/bin/bash -c input`  
因此透過 `${!#}` 我們可以取得 `/bin/bash` 的字串  

在正常的環境下，搞出 `/bin/bash` 就可以執行 shell 了  
但這題因為把 stdin 給關了  
即使執行 `/bin/bash` 也會立刻結束程序  
因此要能執行任意指令才能解這一題...  
透過 $ 編碼的數字無法在同一層 shell 解析  
但是可以將編碼餵給再次執行的 bash  
由第二層的 bash 來解析編碼  
這部分可以透過 pipe 來達成  
`<<<` 的用途是將任意字串交由前面的指令執行  
bash 可以用 `$'\ooo'` 的形式來表達任意字元（ooo 是字元轉 ascii 的八進制）  
結合這兩者，我們就可以執行任意指令  
到目前為止，不算數字編碼的部分，payload 會長的像這樣：  
`${!#}<<<$'\154\163'`

上述的做法雖然已經可以執行任意指令，但不能給參數...  
原因將空白 pipe 進前面的指令，會被當成同一個參數內的東西  
沒辦法作為第二層 bash 分隔符號  
這邊的解決方式是傳入 `{a,b}` 的語法  
會被 bash 自動擴展成兩個不同的參數 `a b`  
也就是說， shell 裡輸入 `{ls,-al}`  
效果等同於輸入 `ls -al`  
至此，我們已經可以做到執行任意指令  
接下來就只要 `cat /flag` 就可以拿到 flag 了~  

...並不是  
flag 的權限是 root:root 400  
題目還準備了一個 setuid 的 `/get_flag`  
要執行才能拿到 flag  ，但執行下去的結果是：

> Please solve this little captcha:  
> 4202242116 + 2217953831 + 1255076993 + 3775205480 + 2795260270  
> 14245738690 != 0 :(  

不知道各位看官是不是還記得 stdin 已經被關閉了  
以目前的情況而言，我們必須在執行前就輸入好答案  
所以這個看似簡單的 captcha ，實際上是超靠北的問題  
為此我還將 `get_flag` dump 出來分析看 captcha 有沒有辦法預測 XD  

發現這個問題後，第一個想法是打 reverse shell 出來  
這樣就可以無視 stdin 被關掉的問題  
但發現目前的 payload 沒辦法在第二層 bash 裡面處理 pipe 符號   
為了做到 fd 重導向，必須在第二層 bash 再次執行 `bash -c <cmd>`  
結果解完 pipe 的問題才發現 sandbox 裡面沒有網路環境 囧  
因此 captcha 唯一的解法是透過 pipe 得到 `/get_flag` 的 output  
計算完結果後在導回 `/get_flag` 的 stdin  

這部分解法就很多種了  
我想到的是透過 `tail` 和 `tee` 來達成：

1. `tail -F /tmp/log | /get_flag | tee /tmp/result &`
2. `echo $answer > /tmp/log`
3. `cat /tmp/result`

不過 mike 大概早我五分鐘先解出來了 XD  
作法是上傳 elf，透過 elf 處理 pipe 的問題   
官方的解法是用 `exec` 和 pid 做 fd 重導向  
個人覺得 **LosFuzzys** 的[解法](https://losfuzzys.github.io/writeup/2017/12/30/34c3ctf-minbashmaxfun/)最漂亮  
可以在一行指令搞定  

flag: `34C3_HAHAHA_you_bashed_it_You_truly_are_a_god_of_BASH`

exploit: [exp.py]({filename}/exp/minbashmaxfun.py)
