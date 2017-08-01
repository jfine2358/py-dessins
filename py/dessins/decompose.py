'''Decompose a dessin into irreducibles


'''


def iter_decompose(alpha, beta):

    '''Decomposition of pair of permutations into irreducibles.

    '''

    assert len(alpha) == len(beta)
    seen = bytearray(len(alpha))

    # Each iteration yields the i-th irreducible.
    for i in range(len(alpha)):

        # Either seed the next irreducible, or exit.
        n = seen.find(False)
        if n == -1:
            return

        yield 'S', i            # Signal start of next irreducible.

        # Yield the components of the i-th irreducible.
        # To be completed.

        yield 'E', i            # Signal end of current irreducible.
