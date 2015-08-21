title: Pwnium CTF 2014 pwn 200 Be a robot 
date: 2014-7-11 22:59
category: pwn
tags: Other CTF, uninit
slug: pwnium_pwn_200_be_a_robot

Pwnium CTF....but there is only one pwn problem. lol  
(pwn100 was down.)  
* * *

The problem gave us a host that we can login by ssh and do something.  
Our goal is using the executable named `pwn200` to get the content of file named `flag` under the same directory.  

After using IDA to reverse the elf, we can find the vulnerability is in the fucntion `atExit()`.  

```
int __cdecl atExit(signed int age){
  int (*v2)(void); // [sp+Ch] [bp-Ch]@0

  if ( age <= 25 ){
    if ( age 0 ){
      v2 = kid;
    }
    else{
      v2 = adult;
    }
  }
  else{
    v2 = man;
  }
  return v2();
}
```

If we input a negative number, the elf won't initialize the variable `v2`.  
Therefore, we can control eax and execute arbitrary code.  

We can't jump to shellcode easily because of ASLR protection.  
However, the program provide a magic function `test()` which call `system()` and just print `hacked`.  
We can use ROP to do something to read flag.  
With no difficulty, I found the ROP chain to call system and controll `esp` to change the argument.  
But where can I put the command to get flag ? I stuck in tis problem for a while.  
Finally, I used the environment variable to solve the problem.  
Set an environment variable as `cat flag` with a lot of blanks. Like that:  
> DDAA=" "\*130000 + "cat flag"

Then we can guess the address of our environment variable.   
It must be between `cat` and `=`.  
Once it was right in our guess, we can see the flag of pwn200.  
