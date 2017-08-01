'''Decompose a dessin into irreducibles


'''


def iter_cycle(perm, v):
    '''Yield v, perm[v], ... until we come back to v again.

    If perm not a permutation, may get exception or infinite loop.
    '''

    # TODO: Provide infinite loop safeguard, based on len(perm).
    curr = v
    while True:
        yield curr
        curr = perm[curr]
        if curr == v:
            break


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

        yield 'S', i            # Start of i-th irreducible.

        # Yield the components of the i-th irreducible.

        a_support = set()
        b_support = set()

        # Get things going. Yield current irreducible's first cycle.
        cycle = tuple(iter_cycle(alpha, n))
        yield 'a', cycle
        for tmp in cycle:
            seen[tmp] = True
        a_support.update(cycle)

        b_missing = a_support - b_support
        if b_missing:
            b = min(b_missing)

            # TODO: Refactor this copy and paste code.
            cycle = tuple(iter_cycle(beta, b))
            yield 'b', cycle
            for tmp in cycle:
                seen[tmp] = True
            b_support.update(cycle)

        yield 'E', i            # End of i-th irreducible.
