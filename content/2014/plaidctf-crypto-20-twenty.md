title: Plaid CTF 2014 Crypto 20 twenty 
date: 2014-4-15 0:34
category: crypto
tags: PlaidCTF, Substitution Cipher
slug: plaidctf_crypto_20_twenty 

Try using English to write the solution down.  
However, my English is not so good.  
I hope to improve it through this method. :)  
* * *

The problem gave us a bzip2 file. We get the cipher in `twenty.txt` after extracting it.  
> fvoxoxfvwdepagxmwxfpukleofxhwevefuygzepfvexwfvufgeyfryedojhwffoyhxcwgmlxeylawfxfurwfvoxecfezfvwbecpfpeejuygoyfefvwxfpwwfxojumwuxfuffvwawuxflecaazubwjwoyfvwyepfvwuxfhwfjlopwckaohvfjlzopwoaahevupgwpfvuywjoywjdwyfufjupouvbuaajwuaoupkecygjwoyfvwuxxdofvyeacmwbvuzoyhlecpwzcbroyhdofvfvwgcgwdveheffvwrwlxfelecpxuzwuygfvexwfvufbuyfgempoyhxcofxbplfelecpcybawxujfexwffawgoxkcfwxfvechvflecgfubrawfvoxdofvuaoffawjepwfubfmcffvwyuhuoyzcghwkubrwpxogeyfryediubroxvwgufwupwswplfojwofvoyrezaorxuyhmcfxvofjuyfvwlpwubepkepufoeyuygojukwpxeyozobufoeyezzpwwgejzepuaaleczoaagebrwfxaorwfvufxubeybwkfzepwohyfeluaadvoawaudlwpxjcggldufwpuygfpexxfuaaecfezmcxoywxxoxiuoazepjwuyglecpwxcoyhjwbosoaalwnvomoffvoxoyfvwbecpfpeejheeygeofogupwlecbeyhpufcaufoeyxfvwzauhoxxoybwywdbplkfejohvfvuswyxumubrgeepxocxweagbplkfe

I didn't notice this text is encrypted by replacing at first because there are not blanks or other symbols. I had no idea to solve it until jeffxx tell me `fvox` = `this`.  

The usual way to break **Substitution cipher** is find some repeat patterns in cipher. The patterns usually present a word in natual language, such as `the`,`this`, `in` ... etc. The more pattern we can find, the more character we get.  

However, this cipher does not have any blank or other symbols. It is hard to identify which pattern is the word. Therefore, I used a regular expression dictionary to assist me find a word that match the pattern.  

For example, after we substituted 'fvoxw' to `thise`, we could get a part of plain as below: (The capital letters were substituted.)  
> THISISTHEdepagSmESTpukleITShEeHeTuygzepTHeSETHuTgeyTryedIjhETTIyhScEgmlSeylaETSTurETHISecTe  
> zTHEbecpTpeejuygIyTeTHESTpEETSIjumEuSTuTTHEaEuSTlecaazubEjEIyTHEyepTHEuSThETjlIpEckaIhHTjlzI  
> pEIaaheHupgEpTHuyEjIyEjdEyTuTjupIuHbuaajEuaIupkecygjEIyTHEuSSdITHyeacmEbHuzIyhlecpEzcbrIyhdI  
> ....  

Observing the text, we could find some duplicate patterns, like `THeSE`, `STpEET`. I guessed that means `those`, `street`. If not sure which words match the pattern, we can use dictionary to search possible words. We could get `o` and `r`, and substitute them to cipher again.  

We could use **google** to search sentences after some characters were substiuted. Finally, I found the plaintext was a lyrics of rap from youtube ([https://www.youtube.com/watch?v=9iUvuaChDEg]). And the last sentence is **CONGRATULATIONSTHEFLAGISSINCENEWCRYPTOMIGHTHAVENSABACKDOORSIUSEOLDCRYPTO**.  

flag: `sincenewcryptomighthavensabackdoorsiuseoldcrypto`
