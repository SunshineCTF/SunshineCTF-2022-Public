//
//  dynamic_array.h
//
//  Created by Kevin Colley on 5/2/18.
//

#ifndef DYNAMIC_ARRAY_H
#define DYNAMIC_ARRAY_H

#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "macros.h"

/*! Helper macro for defining a dynamic array that holds elements of a given type */
#define dynamic_array(type...) \
struct { \
	size_t count; \
	size_t cap; \
	type* elems; \
}

/*! Helper macro to get the type of an element in a dynamic array */
#define element_type(arr) __typeof__(*(arr).elems)

/*! Helper macro to get the size of an element in a dynamic array */
#define element_size(arr) sizeof(*(arr).elems)

/*! Helper macro for iterating over a dynamic array */
#define foreach(parr, pcur) UNIQUIFY(foreach_, parr, pcur)
#define foreach_(id, parr, pcur) enumerate_(id, parr, _iter_idx_##id, pcur)

/*! Helper macro for iterating over a dynamic array with access to the index variable */
#define enumerate(parr, idx, pcur) UNIQUIFY(enumerate_, parr, idx, pcur)
#define enumerate_(id, parr, idx, pcur) \
for(int _iter_once_idx_##id = 1; _iter_once_idx_##id; _iter_once_idx_##id = 0) \
for(__typeof__(parr) _parr_##id = (parr); _iter_once_idx_##id; _iter_once_idx_##id = 0) \
for(size_t idx = 0; idx < _parr_##id->count; idx++) \
	for(int _iter_once_cur_##id = 1; _iter_once_cur_##id; _iter_once_cur_##id = 0) \
	for(__typeof__(_parr_##id->elems) pcur = &_parr_##id->elems[idx]; \
		((void)pcur, _iter_once_cur_##id); _iter_once_cur_##id = 0)

/*! Helper macro for expanding a dynamic array. This will zero-initialize the extra
 allocated space and will abort if the requested allocation size cannot be allocated.
 */
#define array_expand(parr) do { \
	__typeof__(parr) _array_expand_parr = (parr); \
	_expand_array(&_array_expand_parr->elems, &_array_expand_parr->cap); \
} while(0)
#define _expand_array(parr, pcap) \
_expand_size_array((void**)(parr), sizeof(**(parr)), pcap, sizeof(*(pcap)))
static inline void _expand_size_array(void** parr, size_t elem_size, void* pcap, size_t cap_sz) {
	size_t old_count;
	switch(cap_sz) {
		case 1: old_count = *(uint8_t*)pcap; break;
		case 2: old_count = *(uint16_t*)pcap; break;
		case 4: old_count = *(uint32_t*)pcap; break;
		case 8: old_count = *(uint64_t*)pcap; break;
		default: ASSERT(!"Unexpected cap_sz");
	}
	
	size_t new_count = MAX(old_count + 1, old_count * 7 / 4);
	
	/* Expand allocation */
	void* ret = realloc(*parr, elem_size * new_count);
	if(!ret) {
		abort();
	}
	
	/* Zero-fill the expanded space */
	memset((char*)ret + elem_size * old_count, 0, elem_size * (new_count - old_count));
	
	switch(cap_sz) {
		case 1: *(uint8_t*)pcap = (uint8_t)new_count; break;
		case 2: *(uint16_t*)pcap = (uint16_t)new_count; break;
		case 4: *(uint32_t*)pcap = (uint32_t)new_count; break;
		case 8: *(uint64_t*)pcap = (uint64_t)new_count; break;
	}
	*parr = ret;
}

/*! Helper macro to expand a dynamic array when it's full */
#define _expand_if_full(parr) do { \
	__typeof__(parr) _expand_if_full_parr = (parr); \
	if(_expand_if_full_parr->count == _expand_if_full_parr->cap) { \
		array_expand(_expand_if_full_parr); \
	} \
} while(0)

/*! Helper macro to append an element to the end of a dynamic array */
#define array_append(parr, elem...) do { \
	__typeof__(parr) _array_append_parr = (parr); \
	_expand_if_full(_array_append_parr); \
	_array_append_parr->elems[_array_append_parr->count++] = (elem); \
} while(0)

/*! Helper macro to append an array to the end of a dynamic array */
#define array_extend(parr, src, srccount) do { \
	__typeof__(parr) _array_extend_parr = (parr); \
	const __typeof__(*_array_extend_parr->elems)* _array_extend_src = (src); \
	size_t _array_extend_srccount = (srccount); \
	ASSERT(sizeof(*_array_extend_src) == sizeof(*_array_extend_parr->elems)); \
	if(!_array_extend_src || _array_extend_srccount == 0) { \
		break; \
	} \
	size_t _array_extend_dstsize = _array_extend_parr->count * sizeof(*_array_extend_parr->elems); \
	size_t _array_extend_srcsize = _array_extend_srccount * sizeof(*_array_extend_src); \
	size_t _array_extend_newsize = _array_extend_dstsize + _array_extend_srcsize; \
	while(_array_extend_parr->cap < _array_extend_newsize) { \
		array_expand(_array_extend_parr); \
	} \
	memcpy(_array_extend_parr->elems + _array_extend_parr->count, src, _array_extend_srcsize); \
	_array_extend_parr->count += _array_extend_srccount; \
} while(0)

/*! Helper macro for inserting an element into a dynamic array */
#define array_insert(parr, index, pelem) do { \
	__typeof__(parr) _array_insert_parr = (parr); \
	_expand_if_full(_array_insert_parr); \
	_insert_element_array(_array_insert_parr->elems, index, pelem, _array_insert_parr->count++); \
} while(0)
#define _insert_element_array(arr, index, pelem, count) \
_insert_index_array(arr, sizeof(*(arr)), index, pelem, count)
static inline void _insert_index_array(
	void* arr,
	size_t elem_size,
	size_t index,
	const void* pelem,
	size_t count
) {
	/* Move from the target position */
	void* target = (char*)arr + index * elem_size;
	void* dst = (char*)target + elem_size;
	size_t move_size = (count - index) * elem_size;
	memmove(dst, target, move_size);
	memcpy(target, pelem, elem_size);
}

/*! Helper macro to remove an indexed range of a dynamic array */
#define array_removeRange(parr, start, end) do { \
	__typeof__(parr) _array_removeRange_parr = (parr); \
	size_t _array_removeRange_start = (start); \
	size_t _array_removeRange_end = (end); \
	ASSERT(_array_removeRange_end >= start); \
	if(_array_removeRange_start == _array_removeRange_end) { \
		break; \
	} \
	if(_array_removeRange_end > _array_removeRange_parr->count) { \
		_array_removeRange_end = _array_removeRange_parr->count; \
	} \
	size_t _array_removeRange_moveBytes = ( \
		(_array_removeRange_parr->count - _array_removeRange_end) * sizeof(*_array_removeRange_parr->elems) \
	); \
	memmove(&_array_removeRange_parr->elems[start], &_array_removeRange_parr->elems[end], _array_removeRange_moveBytes); \
	_array_removeRange_parr->count -= _array_removeRange_end - _array_removeRange_start; \
} while(0)

/*! Helper macro for removing an element from a dynamic array by its pointer */
#define array_removeElement(parr, pelem) do { \
	__typeof__(parr) _array_removeElement_parr = (parr); \
	array_removeIndex(_array_removeElement_parr, (pelem) - _array_removeElement_parr->elems); \
} while(0)

/*! Helper macro for removing an element from a dynamic array */
#define array_removeIndex(parr, index) do { \
	__typeof__(parr) _array_removeIndex_parr = (parr); \
	size_t _array_removeIndex_index = (index); \
	if(_array_removeIndex_index >= _array_removeIndex_parr->count) { \
		break; \
	} \
	_array_remove_index(_array_removeIndex_parr->elems, _array_removeIndex_index, _array_removeIndex_parr->count--); \
} while(0)
#define _array_remove_index(arr, index, count) \
_remove_index_array(arr, sizeof(*(arr)), index, count)
static inline void _remove_index_array(void* arr, size_t elem_size, size_t index, size_t count) {
	void* dst = (char*)arr + index * elem_size;
	void* src = (char*)dst + elem_size;
	size_t move_size = (count - (index + 1)) * elem_size;
	memmove(dst, src, move_size);
}

/*! Helper macro to shrink excess space in a dynamic array */
#define array_shrink(parr) do { \
	__typeof__(parr) _array_shrink_parr = (parr); \
	_array_shrink_parr->elems = (__typeof__(_array_shrink_parr->elems))realloc( \
		_array_shrink_parr->elems, \
		_array_shrink_parr->count * sizeof(*_array_shrink_parr->elems) \
	); \
	if(!_array_shrink_parr->elems) { \
		abort(); \
	} \
	_array_shrink_parr->cap = _array_shrink_parr->count; \
} while(0)

/*! Helper macro to clear the contents of an array */
#define array_clear(parr) do { \
	__typeof__(parr) _array_clear_parr = (parr); \
	destroy(&_array_clear_parr->elems); \
	_array_clear_parr->count = _array_clear_parr->cap = 0; \
} while(0)

/*! Helper macro to destroy all elements in an array and then the array itself */
#define array_destroy(parr) do { \
	__typeof__(parr) _array_destroy_parr = (parr); \
	foreach(_array_destroy_parr, _array_destroy_pcur) { \
		destroy(_array_destroy_pcur); \
	} \
	array_clear(_array_destroy_parr); \
} while(0)


#endif /* DYNAMIC_ARRAY_H */
