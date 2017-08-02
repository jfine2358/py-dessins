'''Tools for permutations

'''

import collections
import string

def is_perm(seq):
    '''Return True if seq is permutation of {0, ..., n}.

    >>> is_perm([0,1]) and is_perm([1, 0]) and is_perm([1, 2, 0])
    True
    >>> not is_perm([1]) and not is_perm([2, 0, 0])
    True
    '''
    if not isinstance(seq, collections.Sequence):
        return False

    value = list(seq)
    value.sort()
    return value == list(range(len(value)))


# TODO: This needs a review.
# TODO: Refactor out general purpose code?
DIGITS_AND_LOWERCASE = string.digits + string.ascii_lowercase
def perm_from_str36(s):
    '''Create permutation (of length at most 36) from string s.

    >>> perm = perm_from_str36('1230')
    >>> tuple(perm)
    (1, 2, 3, 0)
    >>> type(perm) == bytes
    True

    See also str36_from_perm(perm).
    '''
    if s.lower() != s:
        raise ValueError

    perm = bytes(int(c, 36) for c in s)
    if not is_perm(perm):
        raise ValueError("Failed to convert '%' to a permutation" % s)
    return perm


def str36_from_perm(perm):
    '''Return string encoding of perm (of length at most 36).

    >>> str36_from_perm([1, 2, 3, 0])
    '1230'
    >>> str36_from_perm(range(36))
    '0123456789abcdefghijklmnopqrstuvwxyz'

    See also perm_from_str36(s).
    '''

    if not is_perm(perm):
        raise ValueError("Argument is not a permutation")
    if len(perm) > 36:
        raise ValueError("Argument is too long")

    return ''.join(DIGITS_AND_LOWERCASE[i] for i in perm)


def iter_cycle(perm, start):
    '''Yield start, perm[start], ... until we return to start.

    If infinite loop, raise ValueError.

    >>> tuple(iter_cycle([1, 2, 0], 0))
    (0, 1, 2)
    >>> tuple(iter_cycle([1, 2, 0], 1))
    (1, 2, 0)
    >>> tuple(iter_cycle([1, 2, 0], 2))
    (2, 0, 1)

    >>> tuple(iter_cycle((1, 1), 0))
    Traceback (most recent call last):
    ValueError: Not a permutation - infinite loop broken.
    '''

    curr = start
    for i in range(len(perm)):
        yield curr
        curr = perm[curr]
        if curr == start:
            return

    raise ValueError('Not a permutation - infinite loop broken.')


def iter_seen_cycle(seen, perm, start):
    '''As iter_cycle, but set seen[curr] = True, and then yield curr.

    Used in iter_cycles(perm), to simplify recording of loop state.
    '''

    curr = start
    for i in range(len(perm)):
        seen[curr] = True       # Only change from iter_cycle.
        yield curr
        curr = perm[curr]
        if curr == start:
            return

    raise ValueError('Not a permutation - infinite loop broken.')
