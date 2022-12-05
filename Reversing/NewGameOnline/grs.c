//
//  grs.c
//
//  Created by Kevin Colley on 10/3/21.
//

#include "grs.h"
#include <stdint.h>
#include "randstr.h"
#include "dynamic_string.h"

void grsf_cb(void* cookie, const char* chunk, size_t length) {
	dynamic_array(char)* bytestring = cookie;
	array_extend(bytestring, chunk, length);
}

const char* grsf_decode(const char* randFmt, const char** out_end, size_t* out_length) {
	static dynamic_array(char) grsf_buf;
	grsf_buf.count = 0;
	
	const char* end = decodeRandomString(randFmt, grsf_cb, &grsf_buf);
	
	if(out_end) {
		*out_end = end;
	}
	
	if(out_length) {
		*out_length = grsf_buf.count;
	}
	
	// Append NUL-terminator
	array_append(&grsf_buf, '\0');
	return &grsf_buf.elems[0];
}

const char* grsf(const char* randFmt) {
	return grsf_decode(randFmt, NULL, NULL);
}
