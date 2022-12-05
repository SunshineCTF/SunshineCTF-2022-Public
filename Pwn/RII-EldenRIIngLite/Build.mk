TARGET := EldenRIIngLite

CFLAGS := -Wl,-rpath=$$ORIGIN,--dynamic-linker=./ld-linux-x86-64.so.2,-z,origin

BITS := 64
NX := 1
CANARY := 1
RELRO := 1
STRIP := 1

CC := gcc

DOCKER_IMAGE := elden-riing-lite
DOCKER_PORTS := 22003
DOCKER_TIMELIMIT := 600
DOCKER_RUN_ARGS := --read-only

PUBLISH_LIBC := ./libc.so.6
PUBLISH_LD := ./ld-linux-x86-64.so.2
PUBLISH_BUILD := $(TARGET)
PUBLISH := $(PUBLISH_LIBC) $(PUBLISH_LD)
