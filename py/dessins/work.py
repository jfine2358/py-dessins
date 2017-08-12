from array import array
from .permtools import Relabel


# Lando + Zvonkin, p90, Fig 2.9
A = '10 23 04 51 62 35 46'
# Lando + Zvonkin, p91, Fig 2.10
B = '10 21 03 42 35 64 56'

def doit(s):
    '''
    >>> doit(A)
    (1, 0, 2, 3, 0, 4, 5, 1, 6, 2, 3, 5, 4, 6)
    >>> doit(B)
    (1, 0, 2, 1, 0, 3, 4, 2, 3, 5, 6, 4, 5, 6)
    '''
    return tuple(map(int, s.replace(' ', '')))


A1 = doit(A)
B1 = doit(B)


def bytes_from_ints(typecode, ints):

    return array(typecode, ints).tobytes()

A2 = bytes_from_ints('L', A1)
B2 = bytes_from_ints('L', B1)


def aaa_from_bytes(bindata):
    '''
    >>> alpha, beta, length= aaa_from_bytes(A2)
    >>> tuple(map(alpha, range(length)))
    (1, 2, 0, 5, 6, 3, 4)
    >>> tuple(map(beta, range(length)))
    (0, 3, 4, 1, 2, 5, 6)
    '''

    ulongs = memoryview(bindata).cast('L')
    length = len(ulongs[::2])
    alpha = ulongs[::2].__getitem__
    beta = ulongs[1::2].__getitem__
    return alpha, beta, length


A3 = aaa_from_bytes(A2)
B3 = aaa_from_bytes(B2)


class PermPair:
    '''
    >>> tuple(map(A4.alpha, range(len(A4))))
    (1, 2, 0, 5, 6, 3, 4)
    >>> tuple(map(A4.beta, range(len(A4))))
    (0, 3, 4, 1, 2, 5, 6)

    >>> A4_A4 = A4 * A4
    >>> tuple(map(A4_A4.alpha, range(14)))
    (8, 9, 7, 12, 13, 10, 11, 15, 16, 14, 19, 20, 17, 18)

    >>> A4_B4 = A4 * B4
    >>> tuple(map(A4_B4.alpha, range(14)))
    (8, 9, 7, 11, 10, 13, 12, 15, 16, 14, 18, 17, 20, 19)

    >>> AAA = A4 * A4 * A4 * A4 * A4 * A4 * A4
    >>> BBB = B4 * B4 * B4 * B4 * B4 * B4 * B4

    >>> magic = sum(i * 7 ** i for i in range(7))
    >>> len(tuple(AAA.iter_relabel(magic)))
    5040
    >>> len(tuple(AAA.iter_relabel(magic)))
    5040

    >>> len(A_top), len(B_top)
    (2520, 2520)

    >>> len(A_top * B_top)
    6350400

    >>> len(tuple((A_top * B_top).iter_relabel(0)))
    12700800

    '''

    __slots__ = 'alpha', 'beta', 'length'

    def __init__(self, alpha, beta, length):

        self.alpha = alpha
        self.beta = beta
        self.length = length


    def __len__(self):
        return self.length


    def __mul__(self, other):

        if not isinstance(other, PermPair):
            raise ValueError

        length = self.length * other.length

        def alpha(edge):

            i, j = divmod(edge, other.length)
            return other.length * self.alpha(i) + other.alpha(j)

        def beta(edge):

            i, j = divmod(edge, other.length)
            return other.length * self.beta(i) + other.beta(j)

        return PermPair(alpha, beta, length)


    def iter_relabel(self, root):

        length = len(self)
        relabel = Relabel(length)
        edge_zero = relabel.forward(root) # Seed the relabelling.

        for new_label in range(length):

            # Stop when we run out of new labels.
            if new_label >= relabel.size:
                break

            old_label = relabel.backward(new_label)
            old_alpha = self.alpha(old_label)
            old_beta = self.beta(old_label)

            yield relabel.forward(old_alpha)
            yield relabel.forward(old_beta)


A4 = PermPair(*A3)
B4 = PermPair(*B3)


def doit2():

    AAA = A4 * A4 * A4 * A4 * A4 * A4 * A4
    BBB = B4 * B4 * B4 * B4 * B4 * B4 * B4
    magic = sum(i * 7 ** i for i in range(7))

    A_top = PermPair(*aaa_from_bytes(bytes_from_ints('L', AAA.iter_relabel(magic))))
    B_top = PermPair(*aaa_from_bytes(bytes_from_ints('L', BBB.iter_relabel(magic))))

    return A_top, B_top


A_top, B_top = doit2()
