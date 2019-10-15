title: 35C3CTF 2018 zajebiste 290 logrotate 
date: 2019-1-9 20:23
category: misc
tags: 3XC3CTF, Bash, Race Condition 
slug: 35c3ctf_2018_zajebiste_290_logrotate

35C3 今年的題目也是超難 = =  
各種 browser 和 sandbox escape 題  
現在的 CTF 真的越來越 real world 啦  
BTW，`zajebiste` 的分類聽說就是 zero day 的意思 XD  

* * *

在星期五還在上班的時候，有人就敲我說有 `logrotate` 這題  
> 有 log 題欸 你不是 log 大王嗎  

ok, challenge accepted. = =+  
結果從星期五晚上開始看，一直到星期六晚上才想到作法 QQ  
(雖然中間去幫忙看了一下 `collection`)  

簡單介紹一下這題的環境  
nc 連上通過 pow 的考驗之後  
會初始化一個 docker container 然後進入 chroot  
得到的權限會是 `uid=1000(user) gid=1000(user) groups=1000(user),0(root)`  
要想辦法讀到只有 root 可以存取的 `/flag`  

一開始想嘗試直接 escape chroot 的限制，不過失敗了 QQ  
原因應該是 debain 不允許非 root 去 ptrace 別人的 process  
只好認真看題目的結構  
題目給了一個 setuid 的 binary `run_cron`  
允許我們以 root 的權限觸發 logrotate  
同時故意放了一個有問題的設定檔 `/etc/logrotate.d/pwnme`  

```
/tmp/log/pwnme.log {
    daily
    rotate 12
    missing ok
    notifempty
    size 1K
}
```

嘗試自行建立 `/tmp/log/pwmne.log`  
(`/tmp/log` 的權限必須是 700 否則會噴 error)  
可以成功觸發 logrotate  
但要如何利用呢...?  

第一個直覺就是 symbolic link 會出問題 XD  
嘗試了一下...什麼時都沒發生  
開 debug mode 來看可以得知原因是有 symlink 做檢查  
> log /tmp/log/pwnme.log is symbolic link. Rotation of symbolic links is not allowed to avoid security issues -- skipping.  

```
1125     if ((sb.st_mode & S_IFMT) == S_IFLNK) {
1126         message(MESS_DEBUG, "  log %s is symbolic link. Rotation of symbolic"
1127             " links is not allowed to avoid security issues -- skipping.\n",
1128             log->files[logNum]);
1129         return 0;
1130     }
```

但顯然存在 [TOCTOU](https://cwe.mitre.org/data/definitions/367.html) 的問題  
只要透過 while loop 不斷的讓 pwnme.log 在 symlink 和 normal file 之間切換  
就有機會 bypass 掉這個檢查  
但因為題目給的 logrotate 設定檔只是單純把 log 做 `rename`  
因此完全沒有用...XDD

> ls -l  
> total 0  
> lrwxrwxrwx 1 user user 11 Jan  8 09:25 pwnme.log.1 -> /etc/passwd  

雖然沒有用，不過這帶給我一個思路是：  
**logrotate 其他地方會不會也存在 TOCTOU 的問題呢 ?**  

因此就開始了 logrotate 的 code review 之路  
BTW，比賽環境使用的版本是 3.11.0  
比賽過程有稍微走錯路去確認是不是考 CVE issue  
後來才發現原來 CentOS 9 現行的版本就是 3.11.0 ... Orz  

code review 完發現還有一個地方 "乍看之下" 有類似的問題  
在 logrotate 設定檔包含 `create` 的情況  
最後會呼叫 `createOutputFile` 產生目前最新的 log 檔案  
`createOutputFile` 會先檢查目前 output 的位置是否存在檔案  
如果存在會強制 rename 成 `filename-%Y%m%d%H.backup`  
(重試兩次，兩次都失敗會放棄建立檔案)  
然後用 `fchmod` 將檔案改成原本 log 的權限  

原本看到這個想法是，一樣透過 race condition 的方式  
如果能在更改權限的時候觸發到，就可以把 `/flag` 的權限改成 user  
仔細思考之後是不可能做得到的  
因為這邊用的是 `open` + `fchmod` 而不是 `stat` + `chmod`  

後來又想是不是可以在 `rename` 的過程中做到 race condition ?  
但據我了解 `rename` 會是由 [syscall](https://code.woboq.org/userspace/glibc/sysdeps/unix/sysv/linux/rename.c.html) 來完成  
算是 atomic 的操作，不太可能達成  
只好思索其他的方式  

最後發現問題還是出在 `createOutputFile` 身上  
用 verbose mode 可以得知完整的 logrotate 的流程會是：

```
renaming /tmp/log/pwnme.log.12 to /tmp/log/pwnme.log.13 (rotatecount 12, logstart 1, i 12),
renaming /tmp/log/pwnme.log.11 to /tmp/log/pwnme.log.12 (rotatecount 12, logstart 1, i 11),
renaming /tmp/log/pwnme.log.10 to /tmp/log/pwnme.log.11 (rotatecount 12, logstart 1, i 10),
renaming /tmp/log/pwnme.log.9 to /tmp/log/pwnme.log.10 (rotatecount 12, logstart 1, i 9),
renaming /tmp/log/pwnme.log.8 to /tmp/log/pwnme.log.9 (rotatecount 12, logstart 1, i 8),
renaming /tmp/log/pwnme.log.7 to /tmp/log/pwnme.log.8 (rotatecount 12, logstart 1, i 7),
renaming /tmp/log/pwnme.log.6 to /tmp/log/pwnme.log.7 (rotatecount 12, logstart 1, i 6),
renaming /tmp/log/pwnme.log.5 to /tmp/log/pwnme.log.6 (rotatecount 12, logstart 1, i 5),
renaming /tmp/log/pwnme.log.4 to /tmp/log/pwnme.log.5 (rotatecount 12, logstart 1, i 4),
renaming /tmp/log/pwnme.log.3 to /tmp/log/pwnme.log.4 (rotatecount 12, logstart 1, i 3),
renaming /tmp/log/pwnme.log.2 to /tmp/log/pwnme.log.3 (rotatecount 12, logstart 1, i 2),
renaming /tmp/log/pwnme.log.1 to /tmp/log/pwnme.log.2 (rotatecount 12, logstart 1, i 1),
renaming /tmp/log/pwnme.log.0 to /tmp/log/pwnme.log.1 (rotatecount 12, logstart 1, i 0),
old log /tmp/log/pwnme.log.0 does not exist
renaming /tmp/log/pwnme.log to /tmp/log/pwnme.log.1
creating new /tmp/log/pwnme.log mode = 0644 uid = 1000 gid = 1000
removing old log /tmp/log/pwnme.log.13
```

在 `findNeedRotating` 執行完之後 (也就是前面檢查 folder 700 和 symlink 的地方)  
就不會再對 log 的儲存位置做檢查了  
後面會用 rename 進行 logrotate，但如前述應該沒辦法利用  
最後 creating 時會用 `open` 創建新的檔案  
在這之前沒有再進行一次路徑檢查，也存在 TOCTOU 的問題  
因此有機會透過 symlink race codition 的方式  
達成在任意路徑創造出可讀寫的 `pwnme.log` 檔案  

由於有 `run_cron` 的存在，我選擇建 symlink 的目標是 `/etc/cron.d`  
`run_cron` 做的事情其實是 `execl("/bin/run-parts", "run-parts", "--regex", ".*", "/etc/cron.d", NULL);`  
成功將 symlink 建成 `/etc/cron.d` 後  
透過編輯 `/etc/cron.d/pwnme.log` 就可以以 root 執行任意指令  

剩下的問題就是如何剛好在 call `open` 的時候達成 race condition 了  
一開始單純用 while loop 切換 symlink 和 folder  
但跑了幾萬輪之後還是沒有成功...Orz  
後來做了些修改，多跑了一個 while loop 重複 `touch /tmp/log/pwnme.log`  
前面有提到 `createOutputFile` 會在 log 存在時進行備份  
利用這個行為增加 race condition 成功的機會  
最後大約放著跑了一個小時後  
成功拿到建立 `/etc/cron.d/pwnme.log` 並拿到 root shell  

這題雖然分類在 `zajebiste` 底下  
除了有問題的設定檔，的確也幾乎是 real world 的環境配置  
但實際上發生問題的機率實在是太低了 = =  
這題如果沒有辦法用 while loop 去重複執行 `run_cron` 根本沒辦法觸發問題...囧rz  
我猜也是因為這樣出題者才懶得回報問題吧 (茶  

flag: `35C3_rotating_as_intended`

exploit: [exp.sh]({filename}/exp/logrotate.sh)
