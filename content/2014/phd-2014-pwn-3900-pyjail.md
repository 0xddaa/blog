title: phd CTF 2014 Pwn 3900 pyjail
date: 2014-1-28 21:31
category: pwn
tags: phdCTF
slug: phd_2014_pwn_3900_pyjail

這題解超久 = = 好險有解出來  
但是知道關鍵又覺得這題好像沒什麼 Orz  
就好像變魔術一樣  
謎底揭曉就不好玩了 QQ  
* * *

這題給了 py 的 source code  
我們可以輸入一些指令  
pyjail 會利用 `exec` 去執行  
但是有做一些限制:  
  
1) 以下關鍵字都被過濾了...  
```
sanitize = re.compile(  
  r'(?:__|import|globals|locals|exec|eval|join|format|replace|translate|try|except|with|content|frame|back)'  
  ).sub  
```
2) 僅接受以下字元  
```
alphabet = ' \n\r0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ(),.:;<=>[]_{}'  
```
3) 只留下 trusted built-in function  
```
trusted_builtins = """  
  True False type int  
  """.split()  
```

這題的目的很明確，直接看 code :   
```
def exec_in_context(ctx):  
  exec code in ctx  
  print 'Flag is',  
  try:  
    assert FLAG != part1_of_flag  
  except:  
    print '********************'  
```

`exec code in ctx` 執行我們輸入的程式碼  
接著只要 `FLAG != part1_of_flag` == True  
就會把 FLAG 印出來  
不然就會印出一堆星星  
至於 FLAG 的值  
是由以下兩個 function 去決定:  
```  
def we_must_be_sure_flag_part1_is_ready():  
    global FLAG  
    FLAG = part1_of_flag  
  
def we_must_be_sure_flag_part2_is_ready():  
    global FLAG  
    FLAG += part2_of_flag  
```  
  
由於 `exec code in ctx`  
closure 被限制了  
我們只能執行 `ctx = {'div': divider}` 中所定義的的 function :  
```  
def divider(v1):  
    a = "You are lucky!"  
    b = "Try again!"  
  
    def divider(v2):  
        i,t,s,  n,o,t,  s,o,  h,a,r,d  
        if int(v1) / int(v2) == EXPECTED:  
            print a  
            we_must_be_sure_flag_part2_is_ready()  
        else:  
            print b  
    we_must_be_sure_flag_part1_is_ready()  
    return divider  
```  

part1 的部分很簡單  
我們直接呼叫 div(1) 就會執行到了  
但是 part2 的部分  
`EXPECTED = 13.37`  
兩個int相除不可能會是float Orz  
因此需要想辦法繞過那條限制  
  
最直覺想法是改 `EXPECT` 的值  
但是測試後發現 `EXPECT` 不是 free variable  
怎麼改都沒效 XD  
後來想透過 overload `int()`  
傳入自訂的 class  
令即使是用 `int()` 結果依然是 *float*  
可惜也失敗了  
因為 *__* 被過濾 而且 *__name__* 也被拿掉了 = =  
  
後來仔細想  
會留下 `type()` 一定有他的原因  
以此作為突破點  
發現可以用 function 中有一個 attribute `func_code`  
這個參數是 python 的 byte code  
可以替換這個屬性來執行其他的 function  
但是我在替換時  
遇上了 free variable 數目不符的訊息  
對 python 不夠熟 ... 不知道怎麼解決 QQ  
只好另尋他法  
就發現還有一個屬性 `func_closure`  
裡面定義了函式中  
屬於其 closure 的變數或函式  
`print div(1).func_closure`  
列出了一堆local variavle  
最後一項為:  
> <cell at 0x801858520: function object at 0x80185cd70>  
  
這個物件其實就是 `we_must_be_sure_flag_part2_is_ready()`  
理論上可以用 `cell_contents` 將 cell 中的 object 拿出來  
但是 **content** 被過濾 ...  
這時可以利用 type 新增物件的方式  
來得到 cell 的值  
```  
def get_cell_value(cell):  
    return type(lambda: 0)(  
        (lambda x: lambda: x)(0).func_code, {}, None, None, (cell,)  
    )()  
```  

原理是:  
  
1. `type(function)(func_code, func_global, func_name, func_default, func_closure)`  
用這樣的方式定出一個 *print cell* 的 function  
2. `(lambda x: lambda: x)(0)`  
定義這個 function 會把第一個參數的值回傳  
3. 最後把 cell 包裝成 closure 的形式  
原本的 closure 被換成我們傳入的 cell  
所以參數就變成 cell 中的 value  
  
如此一來就可以執行 `we_must_be_sure_flag_part2_is_ready()` 了  
btw, 前面想的利用替換 *func_code* 也是可行的  
這題還有彩蛋，是要想辦法 read 檔案  
我沒有解出來 QQ  
後來才知道利用替換 func_code 的方式  
只要新增一行 `print type(stdout)(egg).read()`  
就可以讀檔案了  
  
flag: `7hE_0w15_4R3_n07_wh47_7h3Y_533m--7hEr3_15_4_m4n_1n_a_5m111n9_649`  
