'''Tools for permutations

'''

import collections
import itertools

from .othertools import bytes_from_str62 as perm_from_str
from .othertools import str62_from_bytes as str_from_perm


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


def iter_cycles(perm):
    '''Decompose perm into disjoint cycles, lowest index first.

    >>> perm = perm_from_str('3214560')
    >>> cycles = tuple(iter_cycles(perm))

    >>> list(map(list, cycles)) # Convert cycles to list of lists.
    [[0, 3, 4, 5, 6], [1, 2]]

    Every cycle has the same type, namely type(perm). Here, bytes.
    >>> set(map(type, cycles)) == {type(perm)} == {bytes}
    True
    '''

    seen = bytearray(len(perm)) # Records indexes yielded in a cycle.
    cycletype = type(perm)      # Yielded cycle has same type as perm.

    start = -1
    while True:

        # Short cut: If (index <= start) then index is already seen.
        # GOTCHA: Negative indexing: bytes(6).find(False, -1) == 5
        start = seen.find(False, start + 1)
        if start == -1:
            return              # Not found, no more cycles, all done.

        yield cycletype(iter_seen_cycle(seen, perm, start))


def iter_cartprod(*perms):
    '''Iterate over Cartesian product of permutations.

    This product is the component-wise permutation of the Cartesian
    product of the index sets. We enumerate the tuples in the index
    set Cartesian product.

    For example:
    >>> str_from_perm(bytes(iter_cartprod(
    ...   perm_from_str('210'),
    ...   perm_from_str('0123'),
    ... )))
    '89ab45670123'
    '''

    # Each index in the Cartesian product will be a sum of scaled
    # terms. Think of a milometer.

    # Each factor is the product of the lengths of the subsequent
    # permutations. This ugly code does just that.
    prev = 1
    factors = []
    for perm in reversed(perms):
        factors.append(prev)
        prev *= len(perm)
    factors.reverse()

    # Now apply the scales to the permutations.
    scaled_perms = tuple(
        tuple(n * i for i in perm)
        for n, perm in zip(factors, perms)
    )

    # The rest is easy.
    for terms in itertools.product(*scaled_perms):
        yield sum(terms)
