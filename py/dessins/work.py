from array import array


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


def aaa_from_bytes(bindata):
    '''
    >>> alpha, beta = aaa_from_bytes(A2)
    >>> tuple(map(alpha, range(7)))
    (1, 2, 0, 5, 6, 3, 4)
    >>> tuple(map(beta, range(7)))
    (0, 3, 4, 1, 2, 5, 6)
    '''

    ulongs = memoryview(bindata).cast('L')
    alpha = ulongs[::2].__getitem__
    beta = ulongs[1::2].__getitem__
    return alpha, beta
