//
//  dynamic_string.h
//
//  Created by Kevin Colley on 5/2/18.
//

#ifndef DYNAMIC_STRING_H
#define DYNAMIC_STRING_H

#include <stddef.h>
#include <stdbool.h>
#include "dynamic_array.h"

/*! Dynamically resizing string */
typedef dynamic_array(char) dynamic_string;

/*! Compute the string length of a dynamic string (excludes null terminator) */
static inline size_t string_length(const dynamic_string* pstr) {
	size_t length = pstr->count;
	if(length >= 1 && pstr->elems[length - 1] == '\0') {
		--length;
	}
	return length;
}

/*! Determine whether the dynamic string is empty */
static inline bool string_empty(const dynamic_string* pstr) {
	return pstr->count == 0 || (pstr->count == 1 && pstr->elems[0] == '\0');
}

/*! Append a character to a dynamic string */
static inline void string_appendChar(dynamic_string* pstr, char c) {
	/* If the string is currently null-terminated, replace null-terminator with new char */
	if(pstr->count >= 1 && pstr->elems[pstr->count - 1] == '\0') {
		pstr->elems[pstr->count - 1] = c;
	}
	else {
		array_append(pstr, c);
	}
}

/*! Inserts the character at the specified index */
static inline void string_insertChar(dynamic_string* pstr, size_t i, char c) {
	array_insert(pstr, i, &c);
}

/*! Removes the character at the specified index */
static inline void string_removeIndex(dynamic_string* pstr, size_t i) {
	array_removeIndex(pstr, i);
}

/*! Removes the indexed range from the string */
static inline void string_removeRange(dynamic_string* pstr, size_t start, size_t end) {
	array_removeRange(pstr, start, end);
}

/*! Get a reference to the string's contents as a null-terminated C string */
static inline char* string_cstr(dynamic_string* pstr) {
	/* This will only add a null terminator if the string doesn't already end with one */
	string_appendChar(pstr, '\0');
	return pstr->elems;
}

/*! Copies the string's contents as a newly allocated C string */
static inline char* string_dup(const dynamic_string* pstr) {
	return strndup(pstr->elems, pstr->count);
}

/*! Append a C string to a dynamic string */
static inline void string_append(dynamic_string* pstr, const char* cstr) {
	if(!cstr) {
		return;
	}
	
	/* Chop off null terminator if it exists and extend the character array */
	pstr->count = string_length(pstr);
	array_extend(pstr, cstr, strlen(cstr));
}

/*! Append a C string to a dymaic string, copying a maximum of length bytes */
static inline void string_appendLength(dynamic_string* pstr, const char* cstr, size_t length) {
	if(!cstr || length == 0) {
		return;
	}
	
	/* Chop off null terminator if it exists and extend the character array */
	pstr->count = string_length(pstr);
	array_extend(pstr, cstr, strnlen(cstr, length));
}

/*! Clear the contents of a dynamic string */
static inline void string_clear(dynamic_string* pstr) {
	array_clear(pstr);
}


#endif /* DYNAMIC_STRING_H */
