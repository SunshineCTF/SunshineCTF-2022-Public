//
//  grs.h
//
//  Created by Kevin Colley on 10/3/21.
//

#ifndef GRS_H
#define GRS_H

#include <stddef.h>

const char* grsf_decode(const char* randFmt, const char** out_end, size_t* out_length);
const char* grsf(const char* randFmt);

#endif /* GRS_H */
