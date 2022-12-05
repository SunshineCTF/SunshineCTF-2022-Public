FEN_DIR := $(DIR)
FEN_BUILD := $(BUILD_DIR)
TARGET := fen.unstripped
PRODUCTS := $(FEN_BUILD)/fen.unstripped $(FEN_DIR)/fen $(FEN_DIR)/fen.debug

BITS := 64

NX := 1
ASLR := 1
RELRO := 1
CANARY := 1
DEBUG := 1

# Stripping is done manually below so the solve script can use symbols
# STRIP := 1

# TODO: Disable this before challenge is ready
# CFLAGS := -DFEN_DEBUG=1


$(FEN_DIR)/fen: $(FEN_BUILD)/fen.unstripped
	$(_V)echo "Stripping symbols for $(FEN_DIR)"
	$(_v)objcopy --strip-all $< $@

$(FEN_DIR)/fen.debug: $(FEN_BUILD)/fen.unstripped
	$(_V)echo "Extracting debug info for $(FEN_DIR)"
	$(_v)objcopy --only-keep-debug $< $@


DOCKER_IMAGE := fen
DOCKER_PORTS := 22001
DOCKER_TIMELIMIT := 30
# DOCKER_PASSWORD := grand master of haxx

PUBLISH := fen
