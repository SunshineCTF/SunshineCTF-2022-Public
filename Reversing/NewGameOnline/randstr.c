//
//  randstr.c
//
//  Created by Kevin Colley on 10/3/21.
//

#include "randstr.h"
#include <ctype.h>
#include <stdlib.h>
#include <string.h>


const char* randomString(unsigned seed, int base) {
	srand(seed);
	int r, c;
	int end = 0;
	
	static char chunk[10];
	
	while(1) {
		r = rand();
		c = r % 27;
		
		if(c == 0) {
			break;
		}
		
		chunk[end++] = c + base;
		
		if(end + 1 == sizeof(chunk)) {
			break;
		}
	}
	
	chunk[end] = '\0';
	return chunk;
}

const char* decodeRandomString(const char* randFmt, StringChunkCB* cb, void* cookie) {
	while(*randFmt != '\0') {
		char* end = NULL;
		char c = *randFmt++;
		if(isdigit(c)) {
			// <length>x<hexchars>
			unsigned long length = strtoul(randFmt - 1, &end, 10);
			if(*end != 'x' || length * 2 > strlen(randFmt)) {
				// Illegal length
				return randFmt - 1;
			}
			
			randFmt = (const char*)end + 1;
			size_t i;
			for(i = 0; i < length; i++) {
				char hexchars[3];
				hexchars[0] = randFmt[2*i];
				hexchars[1] = randFmt[2*i + 1];
				hexchars[2] = '\0';
				char* hexend = NULL;
				char c = (char)strtoul(hexchars, &hexend, 16);
				if(*hexend != '\0') {
					// Not a proper hexpair
					return randFmt;
				}
				c ^= RANDSTR_PUNCT_XOR;
				cb(cookie, &c, 1);
			}
			randFmt += length * 2;
		}
		else {
			// <base><seed>.
			unsigned seed = (unsigned)strtoul(randFmt, &end, 10);
			if(*end != '.') {
				// Not a number followed by period
				return randFmt - 1;
			}
			
			const char* s = randomString(seed, (int)c);
			cb(cookie, s, strlen(s));
			
			randFmt = (const char*)end + 1;
		}
	}
	return randFmt;
}
