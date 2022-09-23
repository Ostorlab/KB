Data passed to NewStringUTF must be in Modified UTF-8 format

UTF-16 strings are not zero-terminated

Object references should never be compared using == or != in native code. When testing for object equality, the IsSameObject() function should be used instead of ==.