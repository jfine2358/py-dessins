'''Tools for dessins

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
