title: BCTF 2014 PPC & CRYPTO 100 混沌密碼鎖
date: 2014-3-12 2:26 
category: crypto
tags: XCTF, Collision
slug: bctf_crypto_100_password_lockstitch

百度 CTF blue-lotus 辦的  
個人覺得題目還滿有趣的  
不過到處都是置入性行銷 XD  
* * *

環境是用 python 寫的一個伺服器  
先試試看要我們幹嘛：  

> Welcome to Secure Passcode System  
> First, please choose function combination:  
> f1: 1  
> f2: 2  
> f3: 3  
> f4: 4  
> Wrong function combination, you bad guy!  

trace 原始碼得知  
輸入的四個數字會對應到四個 function  
並以輸入的順序將 answer 解密  

```
f['fun1']=reverse
f['fun2']=base64.b64decode
f['fun3']=zlib.decompress
f['fun4']=dec2hex
f['fun5']=binascii.unhexlify
f['fun6']=gb2312
f['fun7']=bin2dec
f['fun8']=hex2bin
f['fun9']=hex2dec

answer = 78864179732635837913920409948348078659913609452869425042153399132863903834522
3652502504296451635172283566227769786379106795384189279098815026542757070698107378508
0761091619256306959366409460515974044867013206561595622472701295421839060280657753745
6281222826375
answer_hash = f['fun6'](f['fun2'](f[f1](f[f2](f[f3](f[f4](answer))))))
```

answer 都是數字，大膽猜測 f4 是`dec2hex`  
且 `fun6` 和 `fun2` 已經被使用，剩下的只有6種  
而且後面三種看起來很像來亂的  
所以就先試前三種做排列組合  
結果就找到順序是 `3 5 1 4`  

但是這只是第一關而已  
麻煩的在後面  
接著要求我們輸入 passcode  
程式會將 passcode 以相同的順序作解密  
比對結果是否與 `answer_hash` 相同  
若相同則會將 flag 印出  
但是 passcode 不能與 answer 相等  
也就是說要找到另一組數字才行  

仔細觀察前面用到的四個 functio  n
`reverse` 肯定是 1-to-1  
`base64` 和 `dec2hex` 也是  
那就只有 `zlib.decompress` 可以做文章了  
試了一下在 zlib.decompress 的參數後面加料後對結果不影響 XD  

```
x = ((f[f2](f[f3](f[f4](answer)))))
y = binascii.hexlify(x)+"01"
x = y.decode('hex')
test = f['fun6'](f['fun2'](f['fun3'](x)))
if test == answer_hash:
    print 'same'
```

此時 `fun9` 就有用了  
我們可以用他們來生一組新的 passcode  

```
print  f['fun9'](f['fun1'](y))
```

> Your passcode: 2046914671302815174999479572879926709311623516344310480161044657024943192185778242098416328741805906729519967582134066703522565680955045139113850683617281109011304982006585757796402695817434740126949224951202731646556997125542758488503105749434074546856689060231  
> Welcome back! The door always open for you, your majesty!

flag: `BCTF{py7h0n-l1b-func7i0ns-re4lly-str4nge}`
