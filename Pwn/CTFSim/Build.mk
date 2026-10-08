UBUNTU_VERSION := 16.04

TARGETS := ctf-simulator guess

BITS := 64

NX := 1
ASLR := 1
RELRO := 1
CANARY := 1
STRIP := 1

ctf-simulator_SRCS := sim.c
guess_SRCS := guess.c

DOCKER_IMAGE := sun22-ctf-simulator
DOCKER_PORTS := 22000
DOCKER_TIMELIMIT := 30

# The original handout was just the ctf-simulator binary
PUBLISH_BUILD := ctf-simulator

# `pwnmake check`: run the solver and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
