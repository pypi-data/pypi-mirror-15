# -*- coding: utf-8 -*-
#cython: language_level=3
cimport cython
from libc.stdlib cimport malloc, free

# compile time constant for the array size
DEF ARRAY_SIZE = 200

@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
cpdef int high_quality(bytes quality_values, int min_quality, int window_size=15):
    """Check if a base has been called with low quality.

    Arguments:
        quality_values (int iterable): List of quality values as integer values
            Raw ASCII values are expected here, but phred values work too, if the
            min_quality is chosen accordingly.
        min_quality (int): Threshold that the mean quality of the window
            must surpass to be a valid window. If a window's mean qv is below the
            threshold the window and thereby the read is dropped.
        window_size (int): Size of the windows that are used. (Default 15)
            Stacks uses read_length * 0.15

    Note:
        This version uses a stack allocated array (_quality_values) of a size that
        has to be fixed at compile time. This limits quality value lengths to the
        constant ARRAY_SIZE (currently 200), which is a completely arbitrary value.

    Returns:
        True, if all windows in the read have a mean quality of at least 
        min_quality. False, if one window is below this threshold.
        If that is the case the function terminates.

    Raises:
        ValueError: If the quality values are too long to fit the allocated array.
            The size of the array is controlled (at compile time) using the constant
            ARRAY_SIZE.
    """
    cdef:
        long l=len(quality_values)
        unsigned char _quality_values[ARRAY_SIZE]
        unsigned char value
        int index
        int s = 0
        int last = 0
        int quality_threshold = min_quality * window_size # minimal required quality per window
        int length = l

    # catch sequences which would overflow the stack allocated array
    if l > ARRAY_SIZE:
        raise ValueError("Quality sequence longer than {}. See docstring of high_quality in stacker/read_filter/high_quality/high_quality.pyx for details.".format(ARRAY_SIZE))

    # Copy bytes values to array
    for index, value in enumerate(quality_values):
        _quality_values[index] = value

    # compute sum of first window
    for i in range(window_size):
        s += _quality_values[i]

    if s < quality_threshold:
        return False

    # subtract value leaving the window, add value newly entering the window
    for index in range(window_size, length):
        s += _quality_values[index] - _quality_values[last]
        last += 1
        if s < quality_threshold:
            return False

    # Only reached, if no reason to return false has been found
    # (i.e. no window below threshold)
    return True


# Notes:

# replacing all int by long doesn't improve runtime
# A version using a memory view on from a bytearray built from the bytes was not very effective (~3x slower than basic version)
# The basic version iterated over the bytes object directly
# The fastest version so far (3x faster than basic version) uses malloc to allocate a c array.
# The malloc version can be further improved (20% speedup) by using a stack allocated array of fixed length
# The allocated version can be improved by factor 2 by removing the python call to sum()
# This fix could also be applied to the malloc version.
# the malloc_version should be kept for more flexibility with longer reads


# Archive:

# basic version
# @cython.boundscheck(False)
# @cython.nonecheck(False)
# @cython.wraparound(False)
# cpdef int high_quality_basic(bytes quality_values, int min_quality, int window_size=15):
#     """Check if a base has been called with low quality.

#     Arguments:
#         quality_values (int iterable): List of quality values as integer values
#             Raw ASCII values are expected here, but phred values work too, if the
#             min_quality is chosen accordingly.
#         min_quality (int): Threshold that the mean quality of the window
#             must surpass to be a valid window. If a window's mean qv is below the
#             threshold the window and thereby the read is dropped.
#         window_size (int): Size of the windows that are used. (Default 15)
#             Stacks uses read_length * 0.15 

#     Returns:
#         True, if all windows in the read have a mean quality of at least 
#         min_quality. False, if one window is below this threshold.
#         If that is the case the function terminates.
#     """
#     cdef:
#         int s
#         int last = 0
#         int index
#         int quality_threshold = min_quality * window_size
#         int length = len(quality_values)
    
#     s = sum(quality_values[:window_size])
#     if s < quality_threshold:
#         return False

#     for index in range(window_size, length):
#         s += <int>quality_values[index] - <int>quality_values[last]
#         last += 1
#         if s  < quality_threshold:
#             return False
#     return True



# malloc version
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
cpdef int high_quality_varlength(bytes quality_values, int min_quality, int window_size=15):
    """Check if a base has been called with low quality.

    Arguments:
        quality_values (int iterable): List of quality values as integer values
            Raw ASCII values are expected here, but phred values work too, if the
            min_quality is chosen accordingly.
        min_quality (int): Threshold that the mean quality of the window
            must surpass to be a valid window. If a window's mean qv is below the
            threshold the window and thereby the read is dropped.
        window_size (int): Size of the windows that are used. (Default 15)
            Stacks uses read_length * 0.15 

    Note:
        This version is much slower than the (plain) high_quality function.
        That is due to the stack allocated array it uses, which is limited to
        a completely arbitrary length defined at compile time.
        This version can be user for variable length (especially longer) reads,
        but is slower.

    Returns:
        True, if all windows in the read have a mean quality of at least 
        min_quality. False, if one window is below this threshold.
        If that is the case the function terminates.
    """
    cdef:
        long l=len(quality_values)
        unsigned char *_quality_values = <unsigned char*>malloc(l*sizeof(unsigned char))
        unsigned char value
        int index
        int s = 0
        int last = 0
        int quality_threshold = min_quality * window_size
        int length = l
    
    for index, value in enumerate(quality_values):
        _quality_values[index] = value

    for i in range(window_size):
        s += _quality_values[i]

    if s < quality_threshold:
        free(_quality_values)
        return False

    for index in range(window_size, length):
        s += _quality_values[index] - _quality_values[last]
        last += 1
        if s  < quality_threshold:
            free(_quality_values)
            return False

    free(_quality_values)
    return True


# stack allocated array version
# @cython.boundscheck(False)
# @cython.nonecheck(False)
# @cython.wraparound(False)
# cpdef int high_quality_stack(bytes quality_values, int min_quality, int window_size=15):
#     """Check if a base has been called with low quality.

#     Arguments:
#         quality_values (int iterable): List of quality values as integer values
#             Raw ASCII values are expected here, but phred values work too, if the
#             min_quality is chosen accordingly.
#         min_quality (int): Threshold that the mean quality of the window
#             must surpass to be a valid window. If a window's mean qv is below the
#             threshold the window and thereby the read is dropped.
#         window_size (int): Size of the windows that are used. (Default 15)
#             Stacks uses read_length * 0.15

#     Note:
#         This version uses a stack allocated array (_quality_values) of a size that
#         has to be fixed at compile time. This limits quality value lengths to 200,
#         which is a completely arbitrary value.

#     Returns:
#         True, if all windows in the read have a mean quality of at least 
#         min_quality. False, if one window is below this threshold.
#         If that is the case the function terminates.
#     """
#     cdef:
#         long l=len(quality_values)
#         unsigned char _quality_values[200]
#         unsigned char value
#         int s, index
#         int last = 0
#         int quality_threshold = min_quality * window_size # minimal required quality per window
#         int length = l

#     # catch sequences which would overflow the stack allocated array
#     if l > 200:
#         raise ValueError("Quality sequence longer than 200. See docstring of high_quakity in stacker/read_filter/high_quality/high_quality.pyx for details.")

#     # Copy bytes values to array
#     for index, value in enumerate(quality_values):
#         _quality_values[index] = value

#     # compute sum of first window
#     s = sum(_quality_values[:window_size])
#     if s < quality_threshold:
#         return False

#     # subtract value leaving the window, add value newly entering the window
#     for index in range(window_size, length):
#         s += _quality_values[index] - _quality_values[last]
#         last += 1
#         if s  < quality_threshold:
#             return False

#     # Only reached, if no reason to return false has been found
#     # (i.e. no window below threshold)
#     return True



