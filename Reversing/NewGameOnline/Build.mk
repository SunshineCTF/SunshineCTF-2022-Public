RANDSTR_DIR := $(DIR)
RANDSTR_BUILD := $(BUILD_DIR)

RANDSTR_CHALL := NewGameOnline
RANDSTR_TOOL := grsf

TARGETS := $(RANDSTR_CHALL) $(RANDSTR_TOOL)

$(RANDSTR_CHALL)_SRCS := main.grsf.c randstr.c grs.c
$(RANDSTR_TOOL)_SRCS := genrandstr.c randstr.c stopwatch.c

CFLAGS := -Wall -Wextra -Werror -Wno-format-security -Wno-multichar -I$(RANDSTR_BUILD)

BITS := 64
ASLR := 1
NX := 1
CANARY := 1
RELRO := 1

$(RANDSTR_CHALL)_STRIP := 1
# $(RANDSTR_CHALL)_DEBUG := 1
$(RANDSTR_CHALL)_LDLIBS := -ldl

$(RANDSTR_TOOL)_OFLAGS := -O2

PUBLISH_BUILD := $(RANDSTR_CHALL)

GRSF_FILES := $(wildcard $(RANDSTR_DIR)/*.grsf.c)
$(GRSF_FILES): %.grsf.c: | $(RANDSTR_DIR)/grsf.py $(RANDSTR_BUILD)/$(RANDSTR_TOOL)
	$(_V)echo 'Generating random format strings for $@, this may take a while...'
	$(_v)python3 $(RANDSTR_DIR)/grsf.py $(RANDSTR_BUILD)/$(RANDSTR_TOOL) $@

# Force run the grsf.py script over all *.grsf.c files regardless of modification times
.PHONY: $(GRSF_FILES)

# Don't ever delete the *.grsf.c files, as they are the source and are modified in-place
.PRECIOUS: $(GRSF_FILES)

.PHONY: grsf-remove
grsf-remove: | $(RANDSTR_DIR)/grsf.py $(RANDSTR_BUILD)/$(RANDSTR_TOOL)
	$(_V)echo 'Stripping random format strings from: $(GRSF_FILES)'
	$(_v)GRSF_REMOVE=1 python3 $(RANDSTR_DIR)/grsf.py $(RANDSTR_BUILD)/$(RANDSTR_TOOL) $(GRSF_FILES)
