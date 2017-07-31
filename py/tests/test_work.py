'''Test work file for dessins'''
import pytest

from dessins.work import BytesDessin

def test_create():

    d = BytesDessin(bytes(range(4)), bytes(range(4)))

    assert len(d) == 4

    with pytest.raises(ValueError):
        BytesDessin(bytes(range(3)), bytes(range(4)))


def test_iter_cycles():

    from dessins.work import iter_cycles

    assert list(iter_cycles([])) == []
    assert list(iter_cycles([0, 1, 2])) == [(0,), (1,), (2,)]
    assert list(iter_cycles([1, 0, 2])) == [(0, 1), (2,)]


def test_product():

    from dessins.work import iter_product

    from functools import reduce
    import operator
    def num_product(iterable):
        return reduce(operator.mul, iterable, 1)

    for lengths in (
            (),
            (1,),
            (1, 1),
            (3, 2, 1),
            (3, 4, 5),

    ):
        expect = tuple(range(num_product(lengths)))
        actual = tuple(iter_product(*map(range, lengths)))
        assert actual == expect

    assert tuple(iter_product(range(3, -1, -1), range(2, -1, -1))) == \
                 (11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
