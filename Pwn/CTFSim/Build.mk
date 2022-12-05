TARGETS := ctf-simulator guess

BITS := 64

NX := 1
ASLR := 1
RELRO := 1
CANARY := 1
STRIP := 1

ctf-simulator_SRCS := sim.c
guess_SRCS := guess.c

DOCKER_IMAGE := ctf-simulator
DOCKER_PORTS := 22000
DOCKER_TIMELIMIT := 30
