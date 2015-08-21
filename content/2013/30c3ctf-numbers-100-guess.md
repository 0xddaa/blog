title: 30C3CTF 2013 Number 100 Guess
date: 2013-12-30 22:56
category: crypto
tags: 3XC3CTF, PRNG
slug: 30c3ctf_2013_number_100_guess

第一次玩的 wargame --- 程式安全的作業1  
也是猜數字...不過  
這題好難 Orz...  
* * *

先 nc 連過去看看情況  
>Welcome to this little guessing game!  
>You have 0/10 right guesses, whats your next guess? 123  
>Nope, that was wrong, correct would have been 8309891200023509866...  
>You have 0/10 right guesses, whats your next guess? 456  
>Nope, that was wrong, correct would have been 14393411043272556995...  
>You have 0/10 right guesses, whats your next guess?  

大概就是要我們猜對 10 次吧  
看看程式碼是如何寫的：  

```
if guess != answer:
  guess_right = 0
  c.sendall("Nope, that was wrong, correct would have been %s...\n" % answer)
  continue
guess_right += 1
if guess_right < guess_limit:
  c.sendall("Yes! That was correct, awesome...\n")
  continue
c.sendall("You did it! The flag is: %s" % flag)
```

結果不只要猜對 10 次 還要連續猜對 10 次 XD  
以前作業是用 bof 去 overwrite 判斷的變數  
不過 python 是沒有什麼 bof 之類的可以用吧...  

只好研究一下答案是如何產生的：  

```
r = random.Random()
r.seed(os.urandom(16))
...
while 1:
  answer = str(r.getrandbits(64)
  ....
```

看起來沒有破綻，每次連線 seed 的值都由 `os.urandom(16)` 決定  
不過在 **連線後** seed 的值就固定了  
當下我是想了幾種做法：  

1. 破解出 `os.urandom()` 的算法，知道下次seed之後就可以得知每次產生的answer
2. 暴力破解試出seed的值，然後就可以推出後面 `getrandbits(64)` 的結果
3. 破解出 `getrandbits(64)` 的算法，得到後面 `getrandbits(64)` 的結果

google一下 `os.random()` 的作法，得知是看系統的 */dev/urandom* 是怎麼實作，感覺在遠端是無法破解吧 XD  
然後當時不知道哪根筋不對，竟然會覺得 2 是可行的，程式寫完開始 run 就去睡覺  
後來想想 seed 的可能性是... 16byte = 2^8^16 = 2^128   
幹...跑到 4012 年都跑不出結果吧 XD  
還一度想用平行運算...後來想想 ctf 應該不會出這種需要暴力破解的題目  

最後考慮方案(3)....開始 google `Random.getrandbits()` 的作法  
最後找到一篇  
[http://jazzy.id.au/default/2010/09/22/cracking_random_number_generators_part_3.html]  

`Random.getrandbits()` 是 PRNG (偽隨機數生成器)  
所用到的演算法是 **Mersenne Twister**  
MT 會產生 624 個 state
每個 state 代表一個 32 bit 的數字  
每一個 state 可以產生出一個 32 bit 的亂數  
計算的方式如下：  

```
int tmp = state[currentIndex];
tmp ^= (tmp >>> 11);
tmp ^= (tmp << 7) & 0x9d2c5680;
tmp ^= (tmp << 15) & 0xefc60000;
tmp ^= (tmp >>> 18);
ran_num = tmp
```

624個 state 用完，再計算新的 state value  
所以我們接著需要做的是....  

1. 隨便猜一個數字，並記錄傳回的 answer
2. 將 answer 拆成前半 a1 和後半 a2，分別是兩次 state 產生出來的亂數
3. 用 a1, a2 反推出 state 代表的結果 s1, s2
4. 重複 312 次，共得到 624 個state

得到 624 個 state 後，可以產生每個 state 下一次的value  

```
int[] state;
for (i = 0; i < 624; i++) {
  int y = (state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7fffffff);
  int next = y >>> 1;
  next ^= state[(i + 397) % 624];
  if ((y & 1L) == 1L)
    next ^= 0x9908b0df;
  state[i] = next;
}
```

用新的 state 套上前面計算的方式，就是下次的 answer  
![flag.png]({filename}/images/30c3CTF_2013_guess_flag.png)  

flag: `30C3_b9b1579866cccd28b1918302382c9107`
