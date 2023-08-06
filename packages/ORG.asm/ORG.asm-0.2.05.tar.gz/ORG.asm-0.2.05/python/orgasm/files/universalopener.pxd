#cython: language_level=3

from .uncompress cimport CompressedFile

cpdef CompressedFile uopen(str name, mode=?)