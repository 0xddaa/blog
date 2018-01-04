title: Trend Micro CTF 2017 write-ups 
date: 2017-6-25 20:01
category: misc
tags: engima, wireshark, frequency analysis, Other CTF
slug: tmctf_misc_2400_write_ups

Our team `phddaa` (what the f...) got 2400 points and 19th rank this year.  
We didn't spend too much time on this game because we think the competition is 48 hours. O\_\_O  
There are several categories of challenges but I don't know how they distinguish.  
Almost of challenges need to analyze and guess... Thus, I put this write up in **misc** category.  
* * *

### Analysis-Offensive 100

The problem provided a binary named `Forensic_Encyption`. The file type is `MS-DOS` but it's not a real MS-DOS executable. After a liitle guessing, I found the binary is a zip file. We can get two files, `file_1` and `file_2` after extracted `Forensic_Encyption`.  

- `file_1`  
    - An image with jpeg format hide a string `VHVyaW5nX01hY2hpbmVfYXV0b21hdG9u` in exif information.
    - Decode the string with base64 and get `Turing_Machine_automaton`.
- `file_2`  
    - Another zip file.
    - We can extract a text file `key.txt` with the password `Turing_Machine_automaton`.

`key.txt` is a file which recorded the information about `ipsec`. I spent some time at this stage to find more clues. Finally, I found another file `file_3` hidden in `Forensic_Encyption`. We can modify the header back to `PK` and extract `file_3`.  
`file_3` is a pcap which recorded the traffic contained `ESP` protocol. We can decrypt the traffic with `key.txt` then get a html file.  

```
Reflector:C Thin, beta, I, IV, II (T M J F), Plugboard: L-X/A-C/B-Y

TMCTF{APZTQQHYCKDLQZRG}

APZTQQHYCKDLQZRG is encrypted.
```

The cipher is encrypted by `enigma`, but the website contained the encrypted key. Thus, we can decrypt the cipher easily.  
I use [this](http://summersidemakerspace.ca/projects/enigma-machine/) to encrypt and get the real flag.  
The flag is: `TMCTF{RISINGSUNANDMOON}`  

### Analysis-Offensive 200

`cracktheflag.exe` is a simple passcode validator which received a number and judge if the number is a valid passcode.  
Surprisingly, this challege can be solved without any guessing.  

The condition of the valid passcode is as below:

```
x1 = passcode / 10000 % 100
x2 = passcode / 100 % 100
x3 = passcode % 100

1. len(passcode) == 6 
2. `passcode` is primes
3. x1 is primes
4. x2 is primes
5. (x3 * x3 ^ x1) >> 8 == 0
6 sum(ascii(d) for d in passcode) - 288 is primes
```

At first, I tried to solve it with **z3**. However, it will spend a lot of time when checking prime. I decided to write a script to filter all possible solutions.  
We can list all of the primes which satisified condition 1 and 2, then filter them with condition 3 to 6.  
I found 7 solutions to satisify all conditions, and the biggest one is `236749`:

- 20509
- 24109
- 24709
- 25309
- 234149
- 234749
- 236749

The program description said there are 8 possible solutions. I have no idea where is wrong.  
Anyway, the biggest passcode is the same.  

flag: `TMCTF{236749}`  

### Forensic 100

The pcap is a DNS traffic. According the description, there are some messages hidden in the traffic. The hostnames are very suspicious because the last one is shorter than others. I concated them and decode it with base64, but getting nothing. I stuck in this stage until organizers posted a hint which said the cipher is `base` but not `base64`.  
I tried to decode with familiar base familiy blindly, such as `base128`, `base32`. Obviously, it's wrong. Our teammate **jeffxx** found only 58 charcaters appeared in the cipher, then I tried `base58` and success to decode the cipher. The plaintext is an article and the flag is at the end.   

flag: `TMCTF{DNSTunnelExfil}`

### MISC 100

I could not analyze the pcap with *wireshark* at first because the header was corruption. However, I saw there are some strings begin with `CLIENT_RANDOM` in the pcap. After googled, I known `CLIENT_RANDOM` is encrypted keys used in HTTP2 traffic. Thus, I tried to repair the pcap. `file` command said the pcap file is big-endien, but I compared with the other pacp file and found only the order of first 4 bytes is wrong. After fixed it, **wireshark** could open the pcap normally and I could dump the object in HTTP2 traffic manually. I'm not sure if the latest wireshark support to dump HTTP2 object.  

The traffic is someone access a website about **visual cryptgraphy**. There are some pictures hidden in traffic and css. I stack at here then my teammate **atdog** found a methond to overlap the iamges and get the flag. <(\_ \_)>.  

flag: `TMCTF{CanYouSeeThis?}`
