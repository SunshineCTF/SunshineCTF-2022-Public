from pwn import *

REMOTE = 1

context.log_level = "warning"

exe = ELF("ctf-simulator")
context(binary=exe)

if REMOTE:
	r = remote("127.0.0.1", 22000)
else:
	r = exe.process()

r.recvuntil(b"What's the name of your CTF team?\n[>] ")
name = b"A" * 20
r.sendline(name)

r.recvuntil(b"Okay %s" % name)

seed_leak = r.recv(4)
seed = u32(seed_leak)

info("Seed is %d" % seed)

guesses = []
helper = ELF("guess", checksec=False)
hproc = helper.process([str(seed)])
try:
	while True:
		guesses.append(int(hproc.recvline()))
except:
	pass

info("Answers will be: %r" % guesses)

for guess in guesses:
	r.recvuntil("What is it?\n[>] ")
	r.sendline(str(guess))

r.recvuntil(b"Here's a reward for you: ")
print(r.recvline().decode("utf8").strip())
