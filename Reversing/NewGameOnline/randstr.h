//
//  randstr.h
//
//  Created by Kevin Colley on 10/3/21.
//

#ifndef RANDSTR_H
#define RANDSTR_H

#include <stddef.h>

#define RANDSTR_PUNCT_XOR 0xf

typedef void StringChunkCB(void* cookie, const char* bytes, size_t length);


const char* randomString(unsigned seed, int base);
const char* decodeRandomString(const char* randFmt, StringChunkCB* cb, void* cookie);

#endif /* RANDSTR_H */
