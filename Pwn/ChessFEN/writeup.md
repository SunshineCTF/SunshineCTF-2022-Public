# [PWN TBD] ChessFEN

Challenge built around a real-world bug that used to be present in the
built-in Chess app on macOS back in 2017 (for Apple-internal folks,
rdar://problem/33459037). The parser for FEN (Forsyth-Edwards Notation) chess
board states has a vulnerability where you can arbitrarily move a pointer
forwards and backwards in memory and write a few unique byte values whenever
you wish.

There are a few constraints:

1. The pointer cannot move before the beginning of the board array in memory.
   This has the impact of limiting the corruption targets. Specifically for
   the implementation in this challenge, the board is on the stack for `main`,
   so you cannot corrupt the stack frames of functions called by `main`.
2. You can only move the pointer by a maximum of 8 bytes at a time in each
   direction. This has the impact of making it unrealistic to jump extreme
   distances through memory such as from the stack to the heap.
3. You can only write 12 different byte values: one for each piece (or pawn).

When I was first creating this challenge, I was thinking about corrupting the
return address of main such that it would jump to a section of code already in
the binary that did `system("/bin/sh")`, but sadly, constraint #3 above makes
that extremely difficult. Therefore, the intended exploitation path is to move
the pointer to the `hasHaxx` variable (which is set to `true` in `main` ONLY
when the `HAXX` environment variable is set at the start of the program,
meaning it will never normally be set on the server) and corrupt it by writing
any piece value to that byte of memory. Then it's just a matter of bringing
the pointer back to the bottom of the chess board and passing the rest of the
FEN format checks. After this, you're able to use the hidden menu option 1337.

Menu option 1337 asks you for an address to jump to. The challenge binary has
ASLR enabled, so this means players will need an info-leak to pick a target.
The board is uninitialized, so if you display the board before loading FEN
data, it will use uninitialized stack memory when printing the board out.
However, the memory isn't printed out directly. Rather, it's used to index
into a string constant that holds the Unicode characters for the chess pieces.
Therefore, to get the leaked data, players will need to find the printed
string chunks in the program binary and calculate the offset from the start of
the chess pieces string (to find the index value used).

In the leaked data, there is a pointer to the `.text` section of the challenge
binary. This can be used to find the ASLR slide and therefore pick any address
within the challenge binary to jump to. The target should be the call to
`system("cat flag.txt")` at the beginning of `main`.
