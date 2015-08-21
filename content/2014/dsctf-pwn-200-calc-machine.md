title: Dragon Sector CTF 2014 Pwnable200 
date: 2014-4-29 3:15
category: pwn
tags: Other CTF, fmt str vuln
slug: dsctf_pwn_200_calc_machine

I almost forget how to use format string vulnerability attack......  
* * *

After connecting the server, we can get the message like that:  
> Welcome to Multipurpose Calculation Machine!  
> Menu:  
>   add:  Addition  
>   sub:  Subtraction  
>   mul:  Multiplication  
>   div:  Division  
>   pow:  Power  
>   mod:  Modulo  
>   sin:  Sinus  
>   cos:  Cosinus  
>   tan:  Tangens  
>   cot:  Cotangens  
>   quit  
> Choice: add  
> [add] Choose the number of parameters: 1  
> [add] Provide parameter 1: 1  
> [add] Message of the day: Don't cry because it's over, smile because it happened. -- Dr. Seuss, operands: [1]  
> [add] The sum of provided numbers is 1  

Expect the choice, the problem uses `scanf("%u")` to get users input.  So there hasn't bof to overwrite memorys. In each choice, the programe uses `printf(format)` to print "Message of day" and "operands". The length of `format` is 308 bytes. And the problem runs a for loop which counts to 308 and checks whether `foramt` has `%` symbol.  

```
strncpy(format,unk_3bc0,n);
for(j=0;j<n;j++){ //n=308
    if(format[j]=='%')
    format[j]='_';
}
```

It seems to prevent the format string attack. However, if the length of "Message of day" + "operand" + others is bigger than 308, it will cause the end of string `\0` be overwrite. Luckily, the input of choice is behind of `format`. Thus, we can bypass the filter of `%` symbol and use the format string vulnerability.  

Then we use `%x` to leak the memory, and notice the program uses ASLR protection. We must calculate the base by subtracting `0x3b00`. Then using `%n` to overwrite memory. I try to overwrite return address at first, but it's not work. I use GDB to trace the program , it execute `system('/bin/sh')` indeed. However it doesn't open shell. So I decide to try another way.  

The `main` function will dynamic execute the function that maps to each choice. The function table is started at 0x3b00. I decide to overwrite `quit` choice, it is at 0x3b80 and its value is 0x1fea. After overwriting it to 0x0d20,we can type `quit` and get the shell.  

flag: `DSCTF_d7b9926c37e5e6b1f796abaf8a3ae7a26050ddb78c4685985321f03d6fd273ba`
