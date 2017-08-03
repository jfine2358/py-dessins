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
        yield from state.iter_side_cycles()
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
    >>> tuple(next(state.iter_side_cycles()))
    ('a', (0,))

    # Expect a state exception.
    >>> # next(state.iter_components())

    '''

    def __init__(self, permpair):

        self.cycletype = tuple  # Or perhaps type(alpha).
        self.permpair = permpair
        self.seen = bytearray(len(permpair[0]))
        self.mode = 'COMPONENT' # Allowed to get next component.

        # We use balance to drive the loop. The seed is initial state.
        self.balance = SetDiff()
        self.seed = []


    def iter_components(self):
        '''Yield component_state.'''

        while True:
            if self.mode != 'COMPONENT':
                raise StateError

            edge = self.seen.find(False)
            if edge != -1:
                # New component, so store the new edge for later use.
                self.seed = [edge]
                self.mode = 'CYCLE' # Allowed to get next cycle.
                yield edge
            else:
                break


    def iter_side_cycles(self):

        if self.mode != 'CYCLE':
            raise StateError

        while True:

            # Either get (side, edge) or exit while loop.
            if self.seed:
                side, edge = 0, self.seed[0]
                self.seed = []
            else:
                for side in range(2):
                    if self.balance[side]:
                        edge = min(self.balance[side])
                        break   # Found an edge for current side.
                else:
                    # Fell through for loop, so exit while loop.
                    break

            # Get the cycle and update the balance.
            perm = self.permpair[side]
            cycle = self.cycletype(iter_seen_cycle(self.seen, perm, edge))
            self.balance.update(1 - side, set(cycle))

            # All done, yield the result (with a side indicator).
            yield 'ab'[side], cycle

        if self.balance[0] or self.balance[1]:
            raise ValueError

        self.mode = 'COMPONENT'


def group_component_cycles_filter(comp_cycles):
    '''Yield pair of cycles for each component in comp_cycles.

    >>> gccf = group_component_cycles_filter
    >>> tuple(gccf((('S', 0), ('a', 'A1'), ('b', 'B1'), ('E', 0))))
    ((['A1'], ['B1']),)
    '''

    comp_cycles = iter(comp_cycles) # Must be an iterator.
    while True:

        key, value = next(comp_cycles)
        if key != 'S':
            raise ValueError

        cycles_pair = ([], [])

        for key, cycle in comp_cycles:

            if key == 'E':
                yield cycles_pair
                break
            else:
                side = dict(a=0, b=1)[key]
                cycles_pair[side].append(cycle)

        else:
            # Fell through the loop.
            raise ValueError
