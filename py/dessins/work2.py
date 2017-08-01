



def iter_cycles(dessin):
    '''Iterate over cycles in dessin, grouped by irreducible component.

    >>> dessin = (range(0), range(0))
    >>> tuple(iter_cycles(dessin))
    ()
    '''

    state = IterCyclesState(dessin)
    for component in state.iter_components():
        yield 'S'
        yield from component.iter_cycles()
        yield 'E'


class IterCyclesState:
    '''State device for iter_cycles(dessin).

    >>> dessin = (range(0), range(0))
    >>> ICS = IterCyclesState
    >>> state = ICS(dessin)
    '''

    def __init__(self, dessin):

        alpha, beta = dessin
        self.dessin = dessin
        self.seen = bytearray(len(alpha))
        self.a_missing = set()
        self.b_missing = set()


    def iter_components(self):
        '''Yield component_state.'''

        while True:
            if self.a_missing or self.b_missing:
                raise StateError
            edge = self.seen.find(False)
            if edge == -1:
                return
            else:
                self.a_missing.add(edge)
                yield self.IterComponentState(edge)
