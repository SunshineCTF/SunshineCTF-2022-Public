//
//  genrandstr.c
//
//  Created by Kevin Colley on 11/3/13.
//

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>
#include <ctype.h>
#include "stopwatch.h"
#include "dynamic_string.h"
#include "randstr.h"

// Anything higher than this is typically infeasible to generate
// as a random string in a reasonable time, and might not be possible
// at all due to the limitation of UINT_MAX.
#define CHUNK_MAX 4

// When generating a chunk of a random string, allow up to this many
// seconds to elapse before reducing the chunk length. Set to 0 to
// disable the timeout.
#define GEN_CHUNK_TIMEOUT 0


static unsigned grsf_verbosity = 1;


static void printEscaped(const char* data, size_t length, FILE* fp) {
	size_t i;
	for(i = 0; i < length; i++) {
		char c = data[i];
		if(0x20 <= c && c <= 0x7e) {
			fputc(c, fp);
		}
		else {
			fprintf(fp, "\\x%02x", c);
		}
	}
}


bool genRandStr(const char* text, unsigned* out_seed, int* out_base, unsigned timeout) {
	size_t n = strlen(text);
	static dynamic_string pool;
	unsigned seed;
	Stopwatch sw;
	static unsigned seed_start;
	
	if(timeout != 0) {
		Stopwatch_start(&sw);
	}
	
	for(seed = seed_start; seed != seed_start - 1; seed++) {
		// Only check the time every 256 iterations for perf
		if(timeout != 0 && (seed & 0xff) == 0) {
			if(Stopwatch_elapsed(&sw) > (double)timeout) {
				// Out of time
				return false;
			}
		}
		
		srand(seed);
		
		// Clear the string without deallocating its buffer
		pool.count = 0;
		
		bool bad = false;
		
		size_t i;
		for(i = 0; i < n; i++) {
			int c = rand() % 27;
			if(c == 0) {
				bad = true;
				break;
			}
			string_appendChar(&pool, c);
		}
		
		if(!bad && rand() % 27 == 0) {
			int base = text[0] - pool.elems[0];
			
			for(i = 0; i < n; i++) {
				if(text[i] - pool.elems[i] != base) {
					bad = true;
					break;
				}
			}
			
			if(!bad) {
				*out_seed = seed;
				*out_base = base;
				seed_start = seed + 1;
				return true;
			}
		}
	}
	
	return false;
}

static inline const char* unsigned_toString(unsigned x) {
	static char str[20];
	snprintf(str, sizeof(str), "%u", x);
	return str;
}

char* generateFormat(const char* text, size_t length, size_t* out_length) {
	static dynamic_array(char) format_buffer;
	char gen[CHUNK_MAX + 1];
	
	// Clear the string without deallocating its buffer
	format_buffer.count = 0;
	
	const char* end = text + length;
	while(text < end) {
		// Handle blocks of punctuation (chars not in [a-z]) by
		// emitting as <length>x<hexchars>
		unsigned numPunct;
		for(numPunct = 0; text < end; numPunct++) {
			if(islower(*text)) {
				break;
			}
			text++;
		}
		
		if(numPunct != 0) {
			if(grsf_verbosity >= 3) {
				fprintf(stderr, "Encoding chunk: \"%.*s\"\n", (int)numPunct, text - numPunct);
			}
			
			size_t pos = format_buffer.count;
			const char* punctStr = unsigned_toString(numPunct);
			array_extend(&format_buffer, punctStr, strlen(punctStr));
			array_append(&format_buffer, 'x');
			unsigned i;
			for(i = 0; i < numPunct; i++) {
				char hexbyte[3];
				snprintf(hexbyte, sizeof(hexbyte), "%02x", (text - numPunct)[i] ^ RANDSTR_PUNCT_XOR);
				array_extend(&format_buffer, hexbyte, 2);
			}
			
			if(grsf_verbosity >= 3) {
				fprintf(stderr, "Added chunk \"");
				printEscaped(&format_buffer.elems[pos], format_buffer.count - pos, stderr);
				fprintf(stderr, "\"\n");
			}
		}
		
		// Handle blocks of lowercase characters by emitting as
		// <base><seed>.
		unsigned numLower;
		for(numLower = 0; text < end && numLower < CHUNK_MAX; numLower++) {
			if(!islower(*text)) {
				break;
			}
			text++;
		}
		
		strncpy(gen, text - numLower, numLower);
		while(numLower != 0) {
			gen[numLower] = '\0';
			unsigned seed;
			int base;
			if(grsf_verbosity >= 3) {
				fprintf(stderr, "Encoding chunk: \"%s\"\n", gen);
			}
			if(!genRandStr(gen, &seed, &base, GEN_CHUNK_TIMEOUT)) {
				// Failed to generate at current length, so reduce and try again
				numLower--;
				text--;
				continue;
			}
			
			size_t pos = format_buffer.count;
			array_append(&format_buffer, (char)base);
			
			const char* seedStr = unsigned_toString(seed);
			array_extend(&format_buffer, seedStr, strlen(seedStr));
			array_append(&format_buffer, '.');
			if(grsf_verbosity >= 3) {
				fprintf(stderr, "Added chunk \"%.*s\"\n", (int)(format_buffer.count - pos), &format_buffer.elems[pos]);
			}
			break;
		}
	}
	
	*out_length = format_buffer.count;
	return &format_buffer.elems[0];
}


int grsfEncode(const char* str, size_t length) {
	size_t fmt_length = 0;
	char* fmt = generateFormat(str, length, &fmt_length);
	
	size_t i;
	for(i = 0; i < fmt_length; i++) {
		putchar(fmt[i]);
	}
	
	return 0;
}

int grsfEncodeEscaped(const char* str, size_t length) {
	size_t fmt_length = 0;
	char* fmt = generateFormat(str, length, &fmt_length);
	
	printEscaped(fmt, fmt_length, stdout);
	
	return 0;
}

static void writeChunk(void* cookie, const char* chunk, size_t length) {
	(void)cookie;
	size_t i;
	for(i = 0; i < length; i++) {
		putchar(chunk[i]);
	}
}

int grsfDecode(const char* str, size_t length) {
	if(grsf_verbosity >= 3) {
		fprintf(stderr, "Decoding: \"");
		printEscaped(str, length, stderr);
		fprintf(stderr, "\"\n");
	}
	
	const char* end = decodeRandomString(str, writeChunk, NULL);
	
	if(end != str + length) {
		if(grsf_verbosity >= 1) {
			fprintf(stderr, "Decode failure at: \"");
			printEscaped(end, length - (end - str), stderr);
			fprintf(stderr, "\"\n");
		}
		return EXIT_FAILURE;
	}
	
	return 0;
}

int main(int argc, char* argv[]) {
	if(argc < 2) {
		goto usage;
	}
	
	char* verbosity_str = getenv("GRSF_VERBOSE");
	if(verbosity_str) {
		grsf_verbosity = strtoul(verbosity_str, NULL, 0);
	}
	
	int (*func)(const char*, size_t) = NULL;
	if(strcmp(argv[1], "encode") == 0) {
		func = &grsfEncode;
	}
	else if(strcmp(argv[1], "encode_escaped") == 0) {
		func = &grsfEncodeEscaped;
	}
	else if(strcmp(argv[1], "decode") == 0) {
		func = &grsfDecode;
	}
	else {
		goto usage;
	}
	
	dynamic_array(char) input = {0};
	int c;
	while((c = getchar()) != EOF) {
		array_append(&input, (char)c);
	}
	
	return func(&input.elems[0], input.count);
	
usage:
	if(grsf_verbosity >= 1) {
		fprintf(stderr, "Usage: %s encode/encode_escaped/decode\n", argv[0]);
	}
	return EXIT_FAILURE;
}
