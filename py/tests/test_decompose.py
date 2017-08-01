'''Test work file for dessins'''

from dessins.decompose import iter_cycle
from dessins.decompose import iter_seen_cycle
from dessins.decompose import iter_decompose
from dessins.decompose import DecomposeState

# TODO: Static data for test suite.

def TIC(perm, v):
    '''Tuple Iter Cycle.'''
    return tuple(iter_cycle(perm, v))


def TID(alpha, beta):
    '''Tuple Iter Decompose.'''
    return tuple(iter_decompose(alpha, beta))


class TestDecomposeState:

    def test(self):

        state = DecomposeState(((0,), (0,)))
        assert state.seen == bytearray(b'\x00')


def test_TIC_one():

    assert TIC((0,), 0) == (0,)


def test_TID_zero():
    '''Test for the  unique dessin of length zero.'''
    assert TID((), ()) == ()


def test_TID_one():
    '''Test for the  unique dessin of length one.'''
    assert TID((0,), (0,)) == (
        ('S', 0),
        ('a', (0,)),
        ('b', (0,)),
        ('E', 0),
    )

def test_TID_cycle_one():
    '''Test for the  unique dessin of length two.'''
    assert TID((1, 0), (1, 0)) == (
        ('S', 0),
        ('a', (0, 1)),
        ('b', (0, 1)),
        ('E', 0),
    )
