'''Tools for permutations

'''

import collections

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
