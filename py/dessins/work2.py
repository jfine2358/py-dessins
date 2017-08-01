
# https://stackoverflow.com/questions/1701199/is-there-an-analogue-to-java-illegalstateexception-in-python
# https://stackoverflow.com/questions/10726919/what-error-to-raise-when-class-state-is-invalid
class StateError(ValueError):
    pass


def iter_cycles(dessin):
    '''Iterate over cycles in dessin, grouped by irreducible component.

    >>> dessin = (range(0), range(0))
    >>> tuple(iter_cycles(dessin))
    ()

    >>> tuple(iter_cycles((range(2), range(2))))
    (('S', 0), ('a', (0,)), ('b', (0,)), ('E', 0), ('S', 1), ('a', (1,)), ('b', (1,)), ('E', 1))

    Checked - this output is correct.
    >>> tuple(iter_cycles(((1, 2, 0), (2, 0, 1))))
    (('S', 0), ('a', (0, 1, 2)), ('b', (0, 2, 1)), ('E', 0))

    Checked - this output is correct.
    >>> tuple(iter_cycles(((1, 2, 0), range(3))))
    (('S', 0), ('a', (0, 1, 2)), ('b', (0,)), ('b', (1,)), ('b', (2,)), ('E', 0))

    Checked - this output is correct.
    >>> tuple(iter_cycles((range(3), (2, 0, 1))))
    (('S', 0), ('a', (0,)), ('b', (0, 2, 1)), ('a', (1,)), ('a', (2,)), ('E', 0))
    '''

    state = IterCyclesState(dessin)
    for edge in state.iter_components():
        yield 'S', edge
        yield from state.iter_cycles()
        yield 'E', edge


class IterCyclesState:
    '''State device for iter_cycles(dessin).

    >>> ICS = IterCyclesState
    >>> dessin = (range(0), range(0))
    >>> state = ICS(dessin)
    >>> tuple(state.iter_components())
    ()

    >>> dessin = (range(1), range(1))
    >>> state = ICS(dessin)
    >>> next(state.iter_components())
    0
    >>> tuple(next(state.iter_cycles()))
    ('a', (0,))

    # Expect a state exception.
    >>> # next(state.iter_components())

    '''

    def __init__(self, dessin):

        alpha, beta = dessin
        self.dessin = dessin
        self.seen = bytearray(len(alpha))
        self.state = 'COMPONENT' # Allowed to get next component.

        self.a_missing = set()
        self.a_support = set()
        self.b_missing = set()
        self.b_support = set()

        self.alpha_beta = dict(
            #         perm, support, missing, other_support, other_missing
            a = (alpha, self.a_support, self.a_missing, self.b_support, self.b_missing),
            b = (beta, self.b_support, self.b_missing, self.a_support, self.a_missing),
        )


    def iter_components(self):
        '''Yield component_state.'''

        while True:
            if self.state != 'COMPONENT':
                raise StateError
            edge = self.seen.find(False)
            if edge == -1:
                return
            else:
                self.state = 'CYCLE' # Allowed to get next cycle.
                self.a_missing.add(edge)
                yield edge


    def iter_cycles(self):

        if self.state != 'CYCLE':
            raise StateError

        while True:

            if self.a_missing:
                a = min(self.a_missing)
                yield self.get_key_cycle('a', a)
            elif self.b_missing:
                b = min(self.b_missing)
                yield self.get_key_cycle('b', b)
            else:
                break

        self.state = 'COMPONENT'


    def get_key_cycle(self, key, edge):

        perm, support, missing, other_support, other_missing = self.alpha_beta[key]
        cycle = tuple(iter_seen_cycle(self.seen, perm, edge))

        # This is a new cycle.
        support.update(cycle)
        missing.difference_update(cycle)            # Should be all or nothing.
        # other support is unchanged, but needed.
        other_missing.update(set(cycle) - other_support) # Should be all or nothing.

        return key, cycle


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
            return

    raise ValueError('Not a permutation - infinite loop.')
