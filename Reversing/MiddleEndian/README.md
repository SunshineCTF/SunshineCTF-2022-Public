# [Crypto] Middle Endian

## Deployment

1. Prepare a file to re-encode. Make sure it has a noticable magic number header.
2. Run `python3 middle_endian.py`
3. Type in the file name to middle-endian-ify, then click Enter.
4. Distribute the outputted file. It has a `.me` extension.

## Solver

1. `middle_endian.py` also acts as a solver.

## Solution

1. Notice that the bytes are scrambled in a deterministic way (see: magic number)
- Every *odd* byte is swapped with a byte equidistant from the other side.
2. Write a script to un-scramble it (i.e. `middle_endian.py`).
3. Run the script to re-order the bytes.
4. Open the file and reveal the flag.