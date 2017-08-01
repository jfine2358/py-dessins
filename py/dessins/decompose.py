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


def iter_seen_cycle(seen, perm, start):
    '''Yield start, perm[start], ... until we return to start.

    If perm not a permutation, may get exception or infinite loop.
    '''

    edge = start
    for i in range(len(perm)):
        seen[edge] = True
        yield edge
        edge = perm[edge]
        if edge == start:
            break

    raise ValueError('Not a permutation - infinite loop.')


class DecomposeState:
    '''State variables for iter_decompose(dessin).

    Maintains the loop invariants of iter_decompose(dessin). The flow
    of control is in iter_decompose.
    '''
    def __init__(self, dessin):

        self.alpha, self.beta = dessin
        self.seen = bytearray(len(self.alpha))


# TODO: Be consistent in use of dessin = pair of permutations.
def iter_decompose(alpha, beta):
    '''Decomposition of pair of permutations into irreducibles.

    '''
    dessin = alpha, beta
    assert len(alpha) == len(beta)
    seen = bytearray(len(alpha))
    state = DecomposeState(dessin)

    def get_cycle(c, v):

        perm, support = dict(
            a = (alpha, a_support),
            b = (beta, b_support),
        )[c]

        cycle = tuple(iter_cycle(perm, v))
        for tmp in cycle:
            seen[tmp] = True
        support.update(cycle)

        return c, cycle

    # Each iteration yields the i-th irreducible.
    for i in range(len(alpha)):

        # Either seed the next irreducible, or exit.
        a = seen.find(False)
        if a == -1:
            return

        yield 'S', i            # Start of i-th irreducible.

        # Yield the components of the i-th irreducible.
        a_support = set()
        b_support = set()

        # Get things going. Yield current irreducible's first cycle.
        yield get_cycle('a', a)

        b_missing = a_support - b_support
        if b_missing:
            b = min(b_missing)
            yield get_cycle('b', b)

        yield 'E', i            # End of i-th irreducible.
