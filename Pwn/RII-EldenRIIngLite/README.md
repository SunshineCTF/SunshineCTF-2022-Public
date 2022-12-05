# [Pwn] Elden RIIng Lite #

## Vulnerability ##

Use-after-free caused by freeing the chunk of memory associated with `Unpolished *player` after the NG+ state is reached.

## Exploitation ##

Three global variables are declared that represent the amount of "runes" that each user will obtain by defeating each boss. In each boss fight function, a local `long int *` is declared that points to the respective boss's rune variable. Upon defeating each boss, the pointer is dereferenced in order to print the amount of runes the user has received. In `second_boss`, two locals (`char taunt[16]` and `long int *dropped_runes`) are ordered in such a manner that when `read` is called later in the program, it facilitates a buffer overflow from `taunt` to `dropped_runes`, meaning that `dropped_runes` can be overwritten. Because the binary is not position-independent, the user can find the address of some libc symbol in the GOT (e.g., `puts`), and write it to `dropped_runes`, so when the user beats the boss, the address of the chosen libc symbol will be printed, leaking libc. Using this address, the user should be able to locate the address of `__free_hook` and a magic gadget present in libc-2.31 by using offsets.

After the libc leak is obtained, the user must then beat the final boss, prompting the user with the choice to start NG+. If the user answers yes, `Unpolished *player` is freed, but then the game begins anew. Via the departing message that the user must give "Malloca", the user is then able to dereference the `key` entry for the recently freed `Unpolished *`, allowing the user to write to the tcache's bin counts and bin entries. With the `__free_hook`  address retrieved from earlier, the user should be able to identify the correct bin to modify in order to write the address of `__free_hook` to its head.

The final requirement is to return the address of `__free_hook` to the user and write to it. This is achieved by a code snippet in `first_boss` that allows the user to allocate a buffer of size `0x80` in order to "leave a message" for other players after defeating the boss. This is the only instance in the program where a chunk of memory of size `0x80` is allocated, so this should serve as a guide as to which bin to modify. After agreeing to leaving a message, the user will be returned the address of `__free_hook` and can write the address of the magic gadget to it, resulting in the execution of a shell and the ability to `cat flag.txt`. 

## Enabled Mitigations ##

- ASLR
- Stack Cookie
- Full RELRO
- NX

## Files to Publish ##

- `EldenRIIngLite`
- `libc.so.6 (2.31)`
- `ld-linux-x86-64.so.2`
