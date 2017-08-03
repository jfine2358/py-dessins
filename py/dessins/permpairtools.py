'''Tools for pairs of permutations

A permpair is the underlying data of a dessin. A dessin is a permpair,
up to relabelling, and with additional methods.
'''

from .othertools import SetDiff
from .permtools import iter_seen_cycle

# https://stackoverflow.com/questions/1701199/is-there-an-analogue-to-java-illegalstateexception-in-python
# https://stackoverflow.com/questions/10726919/what-error-to-raise-when-class-state-is-invalid
class StateError(ValueError):
    pass


def iter_component_cycles(permpair):

    '''Iterate over cycles in permpair, grouped by irreducible component.

    >>> from .permtools import perm_from_str
    >>> def doit(s0, s1):
    ...     permpair = (perm_from_str(s0), perm_from_str(s1))
    ...     return tuple(iter_component_cycles(permpair))

    Both perms the identity permutation.
    >>> doit('', '')
    ()
    >>> doit('0', '0')
    (('S', 0), ('a', (0,)), ('b', (0,)), ('E', 0))
    >>> doit('01', '01')
    (('S', 0), ('a', (0,)), ('b', (0,)), ('E', 0), ('S', 1), ('a', (1,)), ('b', (1,)), ('E', 1))

    Checked - this output is correct.
    >>> doit('120', '201')
    (('S', 0), ('a', (0, 1, 2)), ('b', (0, 2, 1)), ('E', 0))
    >>> doit('120', '012')
    (('S', 0), ('a', (0, 1, 2)), ('b', (0,)), ('b', (1,)), ('b', (2,)), ('E', 0))
    >>> doit('012', '201')
    (('S', 0), ('a', (0,)), ('b', (0, 2, 1)), ('a', (1,)), ('a', (2,)), ('E', 0))
    '''

    state = IterCyclesState(permpair)
    for edge in state.iter_components():
        yield 'S', edge
        yield from state.iter_cycles()
        yield 'E', edge


class IterCyclesState:
    '''State device for iter_cycles(permpair).

    >>> ICS = IterCyclesState
    >>> permpair = (range(0), range(0))
    >>> state = ICS(permpair)
    >>> tuple(state.iter_components())
    ()

    >>> permpair = (range(1), range(1))
    >>> state = ICS(permpair)
    >>> next(state.iter_components())
    0
    >>> tuple(next(state.iter_cycles()))
    ('a', (0,))

    # Expect a state exception.
    >>> # next(state.iter_components())

    '''

    def __init__(self, permpair):

        alpha, beta = permpair
        self.cycletype = tuple  # Or perhaps type(alpha).
        self.permpair = permpair
        self.seen = bytearray(len(alpha))
        # TODO: This is odd choice of name. Perhaps mode is better
        self.state = 'COMPONENT' # Allowed to get next component.

        # We use missing to drive the loop. The seed is initial state.
        self.missing = SetDiff()
        self.seed = []

        # This is a hangover from earlier code.
        self.alpha_beta = dict(a = alpha, b = beta)


    def iter_components(self):
        '''Yield component_state.'''

        while True:
            if self.state != 'COMPONENT':
                raise StateError
            edge = self.seen.find(False)
            if edge == -1:
                return
            else:
                # New component, so store the new edge for later use.
                self.seed = [edge]
                self.state = 'CYCLE' # Allowed to get next cycle.
                yield edge


    def iter_cycles(self):

        if self.state != 'CYCLE':
            raise StateError

        while True:

            if self.seed:
                yield self.get_key_cycle('a', self.seed[0])
                self.seed = []
            elif self.missing[0]:
                a = min(self.missing[0])
                yield self.get_key_cycle('a', a)
            elif self.missing[1]:
                b = min(self.missing[1])
                yield self.get_key_cycle('b', b)
            else:
                break

        if self.missing[0] or self.missing[1]:
            raise ValueError

        self.state = 'COMPONENT'


    def get_key_cycle(self, key, edge):

        # TODO: Getting cycle not part of state management.
        perm = self.alpha_beta[key]
        cycle = self.cycletype(iter_seen_cycle(self.seen, perm, edge))

        i = dict(a=0, b=1)[key]
        self.missing.update(1 - i, set(cycle))

        return key, cycle
