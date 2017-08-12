'''Breadth first search for permutations pairs'''


from .permtools import Relabel


def iter_bfs(permpair, root):
    '''
    >>> p1 = tuple(map(int, '0123456789'))
    >>> p2 = tuple(map(int, '1439678502'))
    >>> p3 = tuple(map(int, '3145926087'))

    # TODO: Fix off-by-one bug in Relabel.
    >>> items = tuple(iter_bfs((p2, p3), 4))
    >>> str(items).replace(' ', '')
    '(1,2,3,1,4,5,6,3,7,0,8,6,9,7,2,8,5,4,0,9)'
    '''

    size = len(permpair[0])
    relabel = Relabel(size)
    edge_zero = relabel.forward(root)

    for new_label in range(size):

        old_label = relabel.backward(new_label)

        # Column view of permpair would help here.
        old_alpha = permpair[0][old_label]
        old_beta = permpair[1][old_label]

        new_alpha = relabel.forward(old_alpha)
        new_beta = relabel.forward(old_beta)

        yield new_alpha
        yield new_beta
