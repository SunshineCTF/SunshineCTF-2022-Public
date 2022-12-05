# [Pwn] Simplified Magic the GatheRIIng

## Vulnerability
No bounds checking in the `Load cards` functionality which allows an
out-of-bounds write on the stack. The program only allows the loading of two
cards, and thus the overwriting of two values.

## Exploitation
Stack variables are (mis)aligned in such a way that 1) a `char *` in the CPU's
deck of cards can be overwritten and 2) the return address of `main` can be
overwritten with completely controlled values. Because ASLR is on but PIE is
off, we don't know where libc is but do know what address portions of the
binary reside at. This allows us to overwrite the CPU card's `char *` with the
address of `puts@GOT`, resulting in a `puts(puts)` when playing the game and
leaking a libc address. With that done, we can then use the given libc to
calculate an offset to a magic gadget. Once the return address of `main` is
overwritten with the address of the magic gadget, we simply exit the game and
are given a shell to `cat` the flag. A specific side effect of zeroing out some
registers is done before the exit so that the magic gadget at `0xe3b34` works
as expected.

## Gotchas

* RBP is not necessarily `0x0` when executing the magic gadget, but it overlaps the a card's `type` and `cost` field, which can be controlled and forced to be `0x0`.
* Due to ASLR, the libc address may contain an unexpected NULL or newline character, which may break exploit scripts or not leak enough information. Restarting the challenge multiple times may be necessary to get a valid leak back.
* Winning the game against the CPU really is irrelevant to solving the challenge, which should be clear from reversing, the challenge description, and the categorization in the pwn section.

## Deployment
Custom PwnableHarness, removing 32-bit support and using an Ubuntu 20.04 base
* Build regularly with Pwnable harness via `make clean docker-clean docker-build docker-start publish`
  * If you have to build the challenge binary again, it must be done on Ubuntu 20.04

## Maintenance

Solution is in `solution.py` and will try to reach localhost on port 22002.
Intended solution will drop you into a shell where you can cat the flag.txt
file.
