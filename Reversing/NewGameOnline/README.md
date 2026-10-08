# [REV] NewGameOnline

Just build w/ PwnableHarness and share the published files.

Code of interest is in [main.grsf.c](main.grsf.c). This file is processed
in-place by the build system. Strings from comments are converted to the
obfuscated format using [grsf.py](grsf.py) and stored directly in this source
file. This is done primarily to speed up subsequent compilations, as a new
compile (such as after `pwnmake grsf-remove`) can take over a minute to generate
all of the GRSF strings.

> **NOTE**: Changing the flag is not as simple as just changing the contents of
> the [flag.txt](flag.txt) file. After changing it, you must regenerate the
> encrypted flag. See the `#ifdef PREPARE_ENCRYPTED_FLAG` section of
> [main.grsf.c](main.grsf.c) for info.

See [writeup.md](writeup.md) for the solution.
