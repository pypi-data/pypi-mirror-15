#cython: language_level=3

'''
Created on 25 mars 2016

@author: coissac
'''

from urllib.request import urlopen


cpdef CompressedFile uopen(str name, mode='r'):
    cdef CompressedFile c
    
    try:
        f = urlopen(name)
    except ValueError:
        f = open(name,mode) 
        
    c = CompressedFile(f)
    
    return c
    