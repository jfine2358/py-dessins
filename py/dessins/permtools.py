'''Tools for permutations

'''

from array import array
import bisect
import collections
import itertools

from .othertools import bytes_from_str62 as perm_from_str
from .othertools import str62_from_bytes as str_from_perm

class Relabel:
    '''Dynamically build up a partial relabelling table.

    Create empty partial relabelling of {0, .., 9}.
    >>> relabel = Relabel(10)

    Add some entries. New labels are created in numeric order.
    >>> labels = (7, 4, 6, 1, 0)
    >>> new_labels = tuple(map(relabel.forward, labels))
    >>> new_labels
    (0, 1, 2, 3, 4)

    We can find the original labels.
    >>> tuple(map(relabel.backward, new_labels))
    (7, 4, 6, 1, 0)

    The relabelling table is dynamic. We can add to it as we go.
    >>> relabel.backward(5)
    Traceback (most recent call last):
    ValueError: Index i = 5 out of bounds (current size = 5)
    >>> relabel.forward(9)
    5
    >>> relabel.backward(5)
    9

    TODO: Move this to test_permtools.
    >>> relabel = Relabel(10)
    >>> relabel.forward(4)
    0
    >>> relabel.forward(4)
    0
    '''

    def __init__(self, maxsize):

        # TODO: Document that len(self) is ambiguous?
        # TODO: Provide read-only views?
        # TODO: allow for maxsize > 255.
        # TODO: Provide item access methods?
        self._size = 0
        self._zero_origin = None
        self._backward = array('L', itertools.repeat(0, maxsize))
        self._forward = array('L', itertools.repeat(0, maxsize))


    @property
    def size(self):
        # Definitely don't want anyone changing this.
        return self._size


    def backward(self, i):

        if 0 <= i < self._size:
            return self._backward[i]
        else:
            msg = 'Index i = %s out of bounds (current size = %s)'
            raise ValueError(msg %  (i, self._size))


    def forward(self, i):

        if i < 0:
            raise ValueError('Negative index %s ambiguous' % i)

        value = self._forward[i]
        if value or (i == self._zero_origin):
            return value

        size = self._forward[i] = self._size
        self._backward[size] = i
        if size == 0:
            # Had written i = self._zero_origin.
            # Add a test that exercises this line of code!
            self._zero_origin = i
        self._size += 1
        return size             # Before the increment.


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


def rebase_cycles(cycles):
    '''Rebase cycles, to use {0, 1, ..., n}, with no gaps.

    Preserves relative order between indices.
    >>> rc = rebase_cycles
    >>> tuple(rc([[9, 3, 7], [4]]))
    ((3, 0, 2), (1,))

    '''

    # Two-pass algorithm, so make sure we can reread cycles.
    # TODO: Instead, raise exception.
    cycles = tuple(cycles)
    cycletype = tuple           # TODO: Allow other values.

    # Create sorted list of values.
    values = []
    for cyc in cycles:
        values.extend(cyc)
    values.sort()

    # For each cycle, apply the lookup.
    return tuple(
        cycletype(bisect.bisect_left(values, i) for i in cyc)
        for cyc in cycles
    )


def perm_from_cycles(cycles):
    '''Produce permutations from cycles, assumed rebased.

    >>> pfc = perm_from_cycles
    >>> pfc([])
    []
    >>> pfc([[3, 0, 1, 2]])
    [1, 2, 3, 0]

    Assumes cycles rebased.
    '''

    length = sum(map(len, cycles))

    value = [None] * length

    for cyc in cycles:

        # TODO: Make it a zip loop? Runs quicker?
        prev = cyc[-1]
        for curr in cyc:
            value[prev] = curr
            prev = curr

    return value
