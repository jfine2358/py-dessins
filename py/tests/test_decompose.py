'''Test work file for dessins'''

from dessins.decompose import iter_decompose


def TID(alpha, beta):
    '''Tuple Iter Decompose.'''
    return tuple(iter_decompose(alpha, beta))


def test_TID_empty():

    assert TID((), ()) == ()
