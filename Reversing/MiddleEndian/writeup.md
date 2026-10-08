# Middle Endian Writeup

## Solution

1. Notice that the bytes are scrambled in a deterministic way (see: magic number)
- Every *odd* byte is swapped with a byte equidistant from the other side.
2. Write a script to un-scramble it (i.e. `middle_endian.py`).
3. Run the script to re-order the bytes.
4. Open the file and reveal the flag.
