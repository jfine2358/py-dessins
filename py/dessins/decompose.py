'''Decompose a dessin into irreducibles


'''


def iter_decompose(alpha, beta):

    '''Decomposition of pair of permutations into irreducibles.

    '''

    assert len(alpha) == len(beta)
    seen = bytearray(len(alpha))

    for i in range(len(alpha)):

        n = seen.find(False)
        if n == -1:
            return

        yield ddt
