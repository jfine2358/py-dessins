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

        self.cycletype = tuple  # Or perhaps type(alpha).
        self.permpair = permpair
        self.seen = bytearray(len(permpair[0]))
        self.mode = 'COMPONENT' # Allowed to get next component.

        # We use missing to drive the loop. The seed is initial state.
        self.missing = SetDiff()
        self.seed = []


    def iter_components(self):
        '''Yield component_state.'''

        while True:
            if self.mode != 'COMPONENT':
                raise StateError
            edge = self.seen.find(False)
            if edge == -1:
                return
            else:
                # New component, so store the new edge for later use.
                self.seed = [edge]
                self.mode = 'CYCLE' # Allowed to get next cycle.
                yield edge


    def iter_cycles(self):

        if self.mode != 'CYCLE':
            raise StateError

        while True:

            if self.seed:
                edge = self.seed[0]
                alpha_beta = 0
                self.seed = []
                yield self.get_key_cycle(alpha_beta, edge)

            elif self.missing[0]:
                a = min(self.missing[0])
                yield self.get_key_cycle(0, a)
            elif self.missing[1]:
                b = min(self.missing[1])
                yield self.get_key_cycle(1, b)
            else:
                break

        if self.missing[0] or self.missing[1]:
            raise ValueError

        self.mode = 'COMPONENT'


    def get_key_cycle(self, i, edge):

        # Get the cycle.
        perm = self.permpair[i]
        cycle = self.cycletype(iter_seen_cycle(self.seen, perm, edge))

        # Update the records.
        self.missing.update(1 - i, set(cycle))

        # Return so-called (key, cycle) pair.
        return 'ab'[i], cycle
