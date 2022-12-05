//
//  macros.h
//
//  Created by Kevin Colley on 11/1/20.
//

#ifndef MACROS_H
#define MACROS_H

#include <assert.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdio.h>

#ifndef UNIQUIFY
#define UNIQUIFY(macro, args...) UNIQUIFY_(macro, __COUNTER__, ##args)
#define UNIQUIFY_(macro, id, args...) UNIQUIFY__(macro, id, ##args)
#define UNIQUIFY__(macro, id, args...) macro(id, ##args)
#endif

#define STRINGIFY(arg) STRINGIFY_(arg)
#define STRINGIFY_(arg) #arg

/* On release builds, ASSERT(cond) tells the compiler that cond must be true */
#if NDEBUG
#define ASSERT(expr) do { \
	if(!(expr)) { \
		__builtin_unreachable(); \
	} \
} while(0)
#else /* NDEBUG */
#define ASSERT(expr) assert(expr)
#endif /* NDEBUG */

#define CMP(op, a, b) ({ \
	__typeof__((a)+(b)) _a = (a); \
	__typeof__(_a) _b = (b); \
	(_a op _b) ? _a : _b; \
})
#define MIN(a, b) CMP(<, a, b)
#define MAX(a, b) CMP(>, a, b)

#define ARRAY_COUNT(arr) (sizeof(arr) / sizeof(arr[0]))

/*! Frees the pointer pointed to by the parameter and then sets it to NULL */
#define destroy(pptr) do { \
	__typeof__(*(pptr)) volatile* _pptr = (pptr); \
	if(!_pptr) { \
		break; \
	} \
	free(*_pptr); \
	*_pptr = NULL; \
} while(0)

#define fail() fail_(__LINE__)
static inline void fail_(int line) {
	printf("Uh oh, something went wrong. Contact the admin for help and provide this failure code: %d\n", line);
	exit(EXIT_FAILURE);
}

#endif /* MACROS_H */
