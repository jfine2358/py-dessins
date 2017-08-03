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
    from dessins.permtools import iter_cartprod


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


def test_iter_cartprod():

    from dessins.permtools import iter_cartprod
    from dessins.permtools import perm_from_str
    from dessins.permtools import str_from_perm

    def doit(s):
        perms = tuple(map(perm_from_str, s.split()))
        perm = bytes(iter_cartprod(*perms))
        return str_from_perm(perm)

    # Product of identity perms is identity perm.
    assert doit('012 01') == '012345'

    # Product of reversing perms is reversing perm.
    assert doit('210 10') == '543210'

    # Multiplication is by blocks.
    assert doit('210 0123') == '89ab45670123'
    assert doit('10 0123456789') == 'abcdefghij0123456789'
