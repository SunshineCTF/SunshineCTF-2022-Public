# [RE] Let's-a-Go!

## Deployment

1. XOR-encrypt a flag with `2357111317192329313741434753` and put it in the `message` variable. Avoid l33tspeak; it breaks my XOR logic.
2. Compile the Go binary (`go build`).
3. Use [UPX](https://github.com/upx/upx) to pack the binary: `upx -9 compile_go`
4. Distribute `compile_go` as a different name (e.g. `plumber_game`).

## Solution

1. Decompress the binary using UPX (note the `UPX!` strings!)
2. Run `strings`, such as:
```bash
strings -n 8 compile_go | grep -v "\." | grep Alphabet
```
3. Find the password.
4. Type in the password by running the binary.
5. Get the flag!