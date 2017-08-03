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


class SetDiff(tuple):
    '''Record and update difference between two sets

    Think of this as a double-pan balance scale for sets.

    The basic operation is adding elements to one side or the
    other. If the same element is added first to one side and then the
    other, it removes (cancels) the element on the first side.

    >>> diff = SetDiff()
    >>> diff
    (set(), set())

    We can add an element to one side of the other.
    >>> diff.add(0, 'a'); diff
    ({'a'}, set())
    >>> diff.add(1, 'b'); diff
    ({'a'}, {'b'})

    It's an error to add an element to a side that already has it.
    >>> diff.add(0, 'a')
    Traceback (most recent call last):
    ValueError

    If element already in diff, add to other side to remove from diff.
    >>> diff.add(1, 'a'); diff
    (set(), {'b'})

    >>> diff.add(0, 'b'); diff
    (set(), set())
    '''

    def __new__(cls):

        return tuple.__new__(cls, (set(), set()))


    def add(self, i, elt):
        '''Add elt to side i (or remove from other side).'''

        self.update(i, {elt})


    def update(self, i, elts):
        '''Add elts to side i (or remove from other side).'''

        if i == 0:
            tgt, other = self
        elif i == 1:
            other, tgt = self
        else:
            raise ValueError

        if not elts.isdisjoint(tgt):
            raise ValueError

        tgt.update(elts.difference(other))
        other.difference_update(elts)
