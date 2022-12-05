Multi-part question and answer style challenge.


### Password

The easiest way to get the password is a breakpoint at the `strcmp()`. You could
also decode the GRSF-encoded password string.

Password: `supercalifragilisticexpialidocious`


### Name of first pet

Input line is modified by adding one to the ASCII value of each character. It is
then compared to a GRSF-encoded string (using `strcmp()`). This time, adding a
breakpoint on the `strcmp()` is not enough, as you need to input a different
string than what you see being compared to.

Answer: `Mister Sprinkles`


### Mother's maiden name

This one is a bit trickier. The expected answer is double-encoded using GRSF.
Additionally, after the first layer of GRSF is decoded, a translation is applied
to the string by replacing digits `[0-9]` with letters `[a-j]` and vice-versa.
Furthermore, this function doesn't use something like `strcmp()` to make it
harder to solve with a breakpoint. Instead, each character of the input string
is compared to each decoded character from the GRSF-encoded answer on the fly as
it is being decoded. This means that the decoded version of the GRSF-encoded
answer is never fully loaded into memory at any point. Also, the comparison is
performed using subtraction and a rolling difference accumulator, and it does
not short-circuit the comparison when a non-matching character is reached. This
avoids a side-channel timing (or inscount) attack. Therefore, the player is
required to figure out how the translation works and decoding GRSF strings.

Answer: `McCormick`


### Master override code

This is the final part of the challenge. This time, the player needs to supply
a string that can be GRSF-decoded to a specific answer string. This answer
string, after being passed through the libc `memfrob()` function, should equal
`Shibboleet` (XKCD reference). Additionally, both the `strdup` and `memfrob`
functions are dynamically referenced using `dlsym()` just for fun. Obviously a
breakpoint on `dlsym()` will reveal which functions are being used here. This
was just to make it _slightly_ trickier, and add a little spice to the level.

To actually generate the GRSF string, players could simply use the hex-encoding
part of the GRSF format. That way, they don't need to figure out how to select
the values for the random string generation part.

Possible answer: `f20.9x4d4c47474a49404051`
Answer (after GRSF-decoding): `yBCHHEFOO^`


### Conclusion

By entering in all of these answers, such as by piping the contents of
[solution.txt](solution.txt) to the program, the flag will be printed.
