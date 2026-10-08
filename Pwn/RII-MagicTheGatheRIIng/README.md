# [Pwn] Simplified Magic the GatheRIIng

## Deployment
Custom PwnableHarness, removing 32-bit support and using an Ubuntu 20.04 base
* Build regularly with Pwnable harness via `make clean docker-clean docker-build docker-start publish`
  * If you have to build the challenge binary again, it must be done on Ubuntu 20.04

## Maintenance

Solver is `solution.py` and will try to reach localhost on port 22002.

See [writeup.md](writeup.md) for the solution.
