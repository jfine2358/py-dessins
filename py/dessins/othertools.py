'''Other tools'''

import string

BASE62_CHARS = string.digits + string.ascii_letters
BASE62_LOOKUP = dict(zip(BASE62_CHARS, range(len(BASE62_CHARS))))
def bytes_from_str62(s):
    '''Return base 62 conversion of string to bytes.

    >>> seq = bytes_from_str62('09azAZ')
    >>> tuple(seq)
    (0, 9, 10, 35, 36, 61)

    >>> type(seq) == bytes
    True

    >>> bytes_from_str62('abc$')
    Traceback (most recent call last):
    ValueError: 'abc$'
    '''
    try:
        return bytes(BASE62_LOOKUP[i] for i in s)
    except KeyError:
        raise ValueError(repr(s))


def str62_from_bytes(seq):
    '''Return base 62 conversion of bytes to string.

    >>> seq = bytes_from_str62('09azAZ')
    >>> str62_from_bytes(seq)
    '09azAZ'

    >>> str62_from_bytes(bytes([62]))
    Traceback (most recent call last):
    ValueError: b'>'

    GOTCHA: TODO: Fix this negative indexing problem.
    >>> str62_from_bytes([-1])
    'Z'
    '''
    try:
        return ''.join(BASE62_CHARS[i] for i in seq)
    except IndexError:
        raise ValueError(repr(seq))
