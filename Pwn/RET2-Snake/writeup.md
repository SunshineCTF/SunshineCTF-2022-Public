## Functional Overview

The game is a basic implementation of snake. In this version, you "wrap" through walls (i.e. going right and hitting the wall places the snake head back at column 0). There is also a "chaos" mode where the snake continuously grows longer and apples shorten it.

Various globals keep track of the game state, some relevant ones are:
- `head_r`, `head_c`, `head_dir`: current row/column/direction of the snake head
- `snake`, `apple`: bitmaps indicating the presence of the snake or an apple at each point
- `g_rand`: the rand implementation is a simple LCG (used to spawn apples)
- `move_snake`: a function pointer that differs between normal and chaos mode

## The Bug

Apples are spawned at the start of a game or whenver an apple is consumed:
```c
void spawn_apple() {
    int loc;
    do {
        loc = rand();

        // ensure the index is not negative before the signed modulo
        if (loc < 0)
            loc = -loc;

        loc = loc % (NROWS*NCOLS);
    } while (_GETBIT(snake, loc) || _GETBIT(apple, loc));
    _SETBIT(apple, loc);
}
```
This is a classic `-INT_MIN == INT_MIN` bug, which will leave `loc` negative after the modulo. This will set a bit at a negative index in the `apple` bitmap.

In terms of manipulating the LCG to output `INT_MIN`, the LCG is seeded at the beginning of each game by interpreting the first 4 bytes of the `snake` bitmap as an integer (which will contain the previous game's bitmap at game-over state). Controlling the seed then becomes the task of "drawing" a certain pattern in the first few rows with the snake, then ending the game.

## Exploitation

When it goes to set the negatively-indexed bit, it ends up bitwise or-ing `head_r` with 8. The board has 15 rows (i.e. the last row has index 14). If the head is at row 7 (which is the starting row for a new game) when the corruption occurs, the head will be "transported" out-of-bounds to row 15. The way the logic is written, immediately moving down to row 16 will avoid wrapping the head back to row 0.

With the snake head now out-of-bounds, the primitive we gain is the ability to set bits out-of-bounds by moving the snake.

The corruption target will be the `move_snake` function pointer. For context, the binary is a single rwx blob, so redirecting the function pointer to shellcode is possible. By setting one of the bits in the function pointer, it is possible to jump into the bss section between the `snake` bitmap and the `move_snake` function pointer. Writing into this region of the bss can be done using the out-of-bounds snake movement to write individual bits.

Barring any unintended solutions, the challenge now becomes crafting "drawable" shellcode. That is, shellcode with a bit pattern that when "visualized" as rows/columns can be drawn with the snake. This can potentially be done across multiple games. Since the shellcode resides out-of-bounds of the `snake` bitmap, it will not be zero-initialized each new game.

## Shellcode

Finding useful drawable shellcode is intended to be the hard part of the challenge, and will probably take some time/iterations. For me, a guiding observation was that bytes with more bits set were more likely to be drawable. Using something like MS Paint was also pretty helpful to determine the actual paths :)

The shellcode I ended up with was a very short stub that JOPs into a call to `read`, such that it reads into the text section where the call will return. This allows executing unconstrained shellcode that can execve /bin/sh.