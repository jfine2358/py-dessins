'''Work file for dessins'''

import itertools

def iter_cycles(perm):
    '''Decompose permutation perm into sequence of disjoint cycles.

    Assumes perm is rearrangement of (0, ..., len(perm) - 1). Yields
    non-empty tuples, smallest element first.
    '''

    # Iterate over the cycles.
    done = bytearray(len(perm)) # As we go, done[item] = True.
    start = -1                  # Starting point of previous cycle.
    while True:

        # Move to start point of next cycle, or return if all done.
        start = done.find(False, start + 1)
        if start == -1:
            break               # No more cycles.

        # Start a new cycle, marking start as done.
        cycle = [start]
        done[start] = True

        # Add items to the cycle, starting at the start.
        item = start
        while True:

            # Is the cycle already closed?
            item = perm[item]
            if done[item]:
                yield tuple(cycle)
                break           # No more items in current cycle.
            else:
                # Add item to cycle, and record item as done.
                cycle.append(item)
                done[item] = True


def iter_product(*permutations):
    '''Iterate over Cartesian product of permutations.
    '''

    perms = tuple(permutations)

    prev = 1
    factors = []
    for perm in reversed(perms):
        factors.append(prev)
        prev *= len(perm)

    factors.reverse()

    scaled_perms = tuple(
        tuple(n * i for i in perm)
        for n, perm in zip(factors, perms)
    )

    for terms in itertools.product(*scaled_perms):
        yield sum(terms)


class BytesDessin(tuple):

    def __new__(cls, alpha, beta):

        if len(alpha) != len(beta):
            raise ValueError

        return tuple.__new__(cls, (alpha, beta))


    def __len__(self):

        return len(self[0])
