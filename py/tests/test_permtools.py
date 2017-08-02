'''Tests for dessins.permtools

'''

import itertools
import pytest

def test_import():

    import dessins.permtools
    from dessins.permtools import is_perm
    from dessins.permtools import iter_cycle


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
