BINARY := EldenRIIngLite

DOCKER_IMAGE := elden
DOCKER_CHALLENGE_NAME := $(BINARY)
DOCKER_CHALLENGE_PATH := $(DIR)/$(BINARY)
DOCKER_PORTS := 22003
DOCKER_TIMELIMIT := 600
DOCKER_BUILD_ARGS := --build-arg "DIR=$(DIR)"
DOCKER_BUILD_DEPS := $(DIR)/pwnableserver $(DIR)/libpwnableharness64.so $(DIR)/ld-2.31.so

PUBLISH_LIBC := $(BINARY)-libc.so
PUBLISH := $(BINARY) ld-2.31.so