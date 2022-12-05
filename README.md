SunshineCTF 2022 Challenges
-----

This is the public release of the challenges from SunshineCTF 2022. Unless otherwise specified, all challenges are released under the MIT license.

## How to build/deploy Reversing and Pwn challenges

Install the `pwnmake` command by following the instructions located at https://github.com/C0deH4cker/PwnableHarness.

* To compile all binaries: `pwnmake`
* To build Docker images for all server-based challenges: `pwnmake docker-build`
* To run Docker containers for all server-based challenges: `pwnmake docker-start`
* To publish all build artifacts that should be distributed to players to the `publish` folder: `pwnmake publish`

Most of the server-based challenges will be migrated to https://ctf.hackucf.org eventually.
