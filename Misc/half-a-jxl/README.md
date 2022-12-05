# [Misc] Half A JXL

## Deployment
1. Run `python3 gen.py`
2. Type in desired flag, then click Enter.
3. Visit [https://jxl-art.surma.technology/](https://jxl-art.surma.technology/) and put in the contents of your clipboard (the output)
4. Edit the `Width` argument in the copied text with something that just *barely* reveals the flag.
4. Click `▶ Run`.
5. Host the generated JXL (`half.jxl`) *somewhere*.

Provided sample has flag `sun{jp3gs_l1k3_b1n_tr33s}` and merely requires byte changes. Compare with `full.jxl.SOLUTION` and ensure only a few bytes in the upper parts of the file have changed for sanity checking.

To make the challenge easier, make sure the output file with the original width and the shrunken width have the same file size.

## Solution
Refer to `file_format.pdf` or the JXL spec for assistance.

The goal is to change the Width argument to that that reveals the flag in full. The exact location of this byte will vary, but knowing where the bits are is the point of the challenge.

Alternatively, you can export the MA Tree stored in the file and re-generate an image with it.

Note: Windows and many Linux image viewers that are *up-to-date* can natively view JXL files, as can Chromium and Firefox with a certain flag asserted.