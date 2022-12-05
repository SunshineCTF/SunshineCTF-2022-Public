TARGET := MagicTheGatheRIIng

BITS := 64
NX := 1
CANARY := 1
RELRO := 1
# DEBUG := 1
STRIP := 1

DOCKER_IMAGE := magic-the-gatheriing
DOCKER_PORTS := 22002
DOCKER_TIMELIMIT := 600
DOCKER_RUN_ARGS := --read-only

PUBLISH_LIBC := $(TARGET)-libc.so
PUBLISH := $(TARGET) $(TARGET)-libc.so
