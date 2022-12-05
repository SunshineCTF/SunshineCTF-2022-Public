# Build instructions
There is one Dockerfile in challenge-1

Build it as you would any other Dockerfile.

The docker container installs a rootless user and launches the tasks as them. The rootless user has read-only access to the flag file named "key" for each challenge.

## Example build command script
An example build command is included in the shell script `build_and_run_containers.sh` at the root of this folder.

## autosolver
There's an autosolver in `./autosolver`. You can run it at the command-line as a python script.
Will print out debug info, and if it passes the flag and generates the correct flag, optionally returns 0 with the `--no-repeat` flag, or continues looping until it detects an error and exits with error code 1.