'''Tests for dessins.permtools

'''

import itertools
import pytest

def test_import():

    import dessins.permtools
    from dessins.permtools import is_perm
    from dessins.permtools import iter_cycle
    from dessins.permtools import iter_seen_cycle
    from dessins.permtools import iter_cycles

def test_is_perm():

    from dessins.permtools import is_perm

    # Every itertools permutation passes ...
    for i in range(5):
        for item in itertools.permutations(range(i)):
            # ... whatever the sequence type.
            for t in list, tuple, bytes:
                assert is_perm(t(item)), (t, item)

    # Non-permutations of {0, ..., n} fail.
    assert not is_perm([1])
    assert not is_perm([1, 1])
    assert not is_perm(['a', 'b', 'c'])

    # Every suitable sequence of ints passes.
    for item in (
            list(range(4)),
            bytes(range(4)),
    ):
        assert is_perm(item), item

    # Empty iterables fail, if not a sequence.
    assert not is_perm(dict())
    assert not is_perm(set())

    # Empty strings pass!
    assert is_perm(str())


def test_iter_cycle():

    from dessins.permtools import iter_cycle
    # And put some more tests here.


def test_iter_seen_cycle():

    # TODO: This example could be made clearer.
    from dessins.permtools import iter_seen_cycle

    perm = tuple(map(int, '1029647385'))
    seen = bytearray(len(perm))

    cycle1 = []
    # Populate cycle1, updating seen as we go.
    for i in iter_seen_cycle(seen, perm, 3):
        assert seen[i] == True
        cycle1.append(i)

    # Check that the seen indexes are exactly those in cycle.
    assert cycle1 == [3, 9, 5, 4, 6, 7]
    for i in range(len(perm)):
        assert seen[i] == (i in cycle1)

    # Now for another cycle, with a new starting point.
    assert 1 not in cycle1
    cycle2 = []
    for i in iter_seen_cycle(seen, perm, 1):
        assert seen[i] == True
        cycle2.append(i)

    assert cycle2 == [1, 0]

    # Check that every seen index is in a seen cycle, and vice versa.
    for i in range(len(perm)):
        assert seen[i] == (i in cycle1 + cycle2)


def test_iter_cycles():

    from dessins.permtools import iter_cycles
    # TODO: Add some tests.
