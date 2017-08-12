'''
Let's look at relabelling.
>>> for t in sorted([(tuple(A.iter_relabel(i)), i) for i in range(7)]): print(t)
((1, 0, 0, 2, 3, 1, 4, 3, 2, 5, 6, 4, 5, 6), 6)
((1, 0, 0, 2, 3, 1, 4, 5, 2, 4, 6, 3, 5, 6), 5)
((1, 0, 2, 3, 0, 4, 5, 1, 6, 2, 3, 5, 4, 6), 0)
((1, 2, 0, 1, 3, 0, 4, 3, 2, 5, 6, 4, 5, 6), 4)
((1, 2, 0, 1, 3, 0, 4, 5, 2, 4, 6, 3, 5, 6), 3)
((1, 2, 3, 1, 4, 0, 0, 5, 2, 4, 6, 3, 5, 6), 2)
((1, 2, 3, 4, 5, 0, 0, 3, 6, 1, 2, 5, 4, 6), 1)

>>> for t in sorted([(tuple(B.iter_relabel(i)), i) for i in range(7)]): print(t)
((1, 0, 0, 2, 3, 1, 2, 4, 5, 3, 6, 5, 4, 6), 6)
((1, 0, 2, 1, 0, 3, 4, 2, 3, 5, 6, 4, 5, 6), 0)
((1, 0, 2, 3, 0, 2, 4, 1, 3, 5, 6, 4, 5, 6), 1)
((1, 2, 0, 1, 3, 0, 2, 4, 5, 3, 6, 5, 4, 6), 5)
((1, 2, 0, 3, 4, 0, 5, 1, 2, 4, 6, 5, 3, 6), 4)
((1, 2, 0, 3, 4, 0, 5, 1, 6, 4, 3, 5, 2, 6), 3)
((1, 2, 3, 1, 4, 0, 0, 3, 2, 5, 6, 4, 5, 6), 2)

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

'''

from .work import A4 as A
from .work import B4 as B

AA = A * A
AB = A * B
BB = B * B
