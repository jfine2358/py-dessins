'''Tests for dessins.tools

'''

import itertools
import pytest

def test_import():

    import dessins.tools


def test_is_perm():
    from dessins.tools import is_perm

    # Every itertools permutation passes.
    for i in range(5):
        for item in itertools.permutations(range(i)):
            # Whatever the sequence type.
            for t in list, tuple, bytes:
                assert is_perm(t(item)), (t, item)

    # But non-permutations of {0, ..., n} fail.
    assert not is_perm([1])
    assert not is_perm([1, 1])

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
