'''
Let's look at relabelling.
>>> for t in sorted(every_relabel_of(A_orig)): print(t)
((1, 0, 0, 2, 3, 1, 4, 3, 2, 5, 6, 4, 5, 6), 6)
((1, 0, 0, 2, 3, 1, 4, 5, 2, 4, 6, 3, 5, 6), 5)
((1, 0, 2, 3, 0, 4, 5, 1, 6, 2, 3, 5, 4, 6), 0)
((1, 2, 0, 1, 3, 0, 4, 3, 2, 5, 6, 4, 5, 6), 4)
((1, 2, 0, 1, 3, 0, 4, 5, 2, 4, 6, 3, 5, 6), 3)
((1, 2, 3, 1, 4, 0, 0, 5, 2, 4, 6, 3, 5, 6), 2)
((1, 2, 3, 4, 5, 0, 0, 3, 6, 1, 2, 5, 4, 6), 1)

>>> for t in sorted(every_relabel_of(B_orig)): print(t)
((1, 0, 0, 2, 3, 1, 2, 4, 5, 3, 6, 5, 4, 6), 6)
((1, 0, 2, 1, 0, 3, 4, 2, 3, 5, 6, 4, 5, 6), 0)
((1, 0, 2, 3, 0, 2, 4, 1, 3, 5, 6, 4, 5, 6), 1)
((1, 2, 0, 1, 3, 0, 2, 4, 5, 3, 6, 5, 4, 6), 5)
((1, 2, 0, 3, 4, 0, 5, 1, 2, 4, 6, 5, 3, 6), 4)
((1, 2, 0, 3, 4, 0, 5, 1, 6, 4, 3, 5, 2, 6), 3)
((1, 2, 3, 1, 4, 0, 0, 3, 2, 5, 6, 4, 5, 6), 2)


Now after best relabelling.
>>> tuple(A.iter_relabel(0))
(1, 0, 0, 2, 3, 1, 4, 3, 2, 5, 6, 4, 5, 6)

>>> tuple(B.iter_relabel(0))
(1, 0, 0, 2, 3, 1, 2, 4, 5, 3, 6, 5, 4, 6)

How many terms in a product?
>>> len(AA)
49

The product had two terms.
>>> [len(tuple(AA.iter_relabel(i)))//2 for i in range(7)]
[7, 42, 42, 42, 42, 42, 42]

The product has one term.
>>> [len(tuple(AB.iter_relabel(i)))//2 for i in range(7)]
[49, 49, 49, 49, 49, 49, 49]

The product has two terms.
>>> [len(tuple(BB.iter_relabel(i)))//2 for i in range(7)]
[7, 42, 42, 42, 42, 42, 42]

Let's discover the terms, and their best relabellings.
>>> for t, i in sorted(every_relabel_of(AA))[:5]: print(len(t)//2, i, t[:10])
7 0 (1, 0, 0, 2, 3, 1, 4, 3, 2, 5)
7 48 (1, 0, 0, 2, 3, 1, 4, 5, 2, 4)
42 6 (1, 0, 0, 2, 3, 1, 4, 5, 2, 6)
42 42 (1, 0, 0, 2, 3, 1, 4, 5, 2, 6)
7 24 (1, 0, 2, 3, 0, 4, 5, 1, 6, 2)

>>> for t, i in sorted(every_relabel_of(BB))[:5]: print(len(t)//2, i, t[:10])
7 0 (1, 0, 0, 2, 3, 1, 2, 4, 5, 3)
7 40 (1, 0, 2, 1, 0, 3, 4, 2, 3, 5)
7 48 (1, 0, 2, 3, 0, 2, 4, 1, 3, 5)
42 41 (1, 0, 2, 3, 0, 4, 5, 1, 6, 2)
42 47 (1, 0, 2, 3, 0, 4, 5, 1, 6, 2)

>>> for t, i in sorted(every_relabel_of(AB))[:5]: print(len(t)//2, i, t[:10])
49 42 (1, 0, 0, 2, 3, 1, 4, 5, 6, 7)
49 0 (1, 0, 0, 2, 3, 1, 4, 5, 6, 7)
49 27 (1, 0, 2, 3, 0, 4, 5, 1, 6, 2)
49 26 (1, 0, 2, 3, 0, 4, 5, 1, 6, 2)
49 6 (1, 0, 2, 3, 4, 2, 5, 1, 6, 7)

Now use the information we've obtained.
>>> t = tuple(AA_0.iter_relabel(0)); (len(t)//2, t[:20])
(42, (1, 0, 0, 2, 3, 1, 4, 5, 2, 6, 7, 3, 8, 4, 9, 10, 11, 12, 13, 14))

>>> t = tuple(BB_0.iter_relabel(0)); (len(t)//2, t[:20])
(42, (1, 0, 2, 3, 0, 4, 5, 1, 6, 2, 7, 8, 9, 10, 11, 12, 13, 5, 14, 15))

>>> t = tuple(AB_0.iter_relabel(0)); (len(t)//2, t[:20])
(49, (1, 0, 0, 2, 3, 1, 4, 5, 6, 7, 8, 3, 9, 10, 11, 4, 12, 8, 13, 14))
'''

from .work import A4 as A_orig
from .work import B4 as B_orig

from .work import PermPair
from .work import aaa_from_bytes
from .work import bytes_from_ints


def permpair_from_iterable(ints):

    return PermPair(*aaa_from_bytes(bytes_from_ints('L', ints)))

A = permpair_from_iterable(A_orig.iter_relabel(6))
B = permpair_from_iterable(B_orig.iter_relabel(6))

AA = A * A
AB = A * B
BB = B * B

def every_relabel_of(permpair):

    value = []
    for i in range(len(permpair)):
        ints = tuple(permpair.iter_relabel(i))
        value.append((ints, i))

    return value


# As dessins, AA = A + AA_0.
# As dessins, BB = B + BB_0.
# As dessins, AB = AB_0
AA_0 = permpair_from_iterable(AA.iter_relabel(6))
BB_0 = permpair_from_iterable(BB.iter_relabel(41))
AB_0 = permpair_from_iterable(AB.iter_relabel(42))
