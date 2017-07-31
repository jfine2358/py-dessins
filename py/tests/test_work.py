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
