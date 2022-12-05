# Challenge expected solve
1. Look at each character as binary
2. Notice that the last byte looks similar to an ASCII character. For example, we know `s` ends with `110011`, and so does `걳`.
3. Derive the following binary transformations by looking at the first four characters (which are known to be `sun{`):
```sed
s/11101010 10110001 10/01/g
s/11101010 10110000 10/00/g
```
4. Re-encode the binary as ASCII (or UTF-8).

# Alternative solve
Re-implement base64 by hand and tweak a few settings to work with the base128 algorithm. This is what happens in `solve.py`.