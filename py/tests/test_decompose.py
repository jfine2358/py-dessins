'''Test work file for dessins'''

from dessins.decompose import iter_decompose


def TID(alpha, beta):
    '''Tuple Iter Decompose.'''
    return tuple(iter_decompose(alpha, beta))


def test_TID_zero():
    '''Test for the  unique dessin of length zero.'''
    assert TID((), ()) == ()


def test_TID_one():
    '''Test for the  unique dessin of length one.'''
    assert TID((0,), (0,)) == (
        ('S', 0),
        # And we expect more here.
        ('E', 0),
    )
