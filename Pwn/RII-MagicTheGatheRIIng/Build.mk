TARGET := MagicTheGatheRIIng

UBUNTU_VERSION := 20.04

BITS := 64
NX := 1
CANARY := 1
RELRO := 1
STRIP := 1

DOCKER_IMAGE := sun22-magic-the-gatheriing
DOCKER_PORTS := 22002
DOCKER_TIMELIMIT := 600

# Publish the exact libc used by the challenge (from the 20.04 base image)
PUBLISH_LIBC := $(TARGET)-libc.so
PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: run the solver and verify it prints the flag.
# The exploit is probabilistic, so the solver self-retries; give it extra
# headroom beyond the default 120s.
CHECK_TIMEOUT := 300
$(call ctf_check_slow,$(DIR),$(DOCKER_PORTS),python3 solution.py)
