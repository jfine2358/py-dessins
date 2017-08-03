'''For storing code oddments

We don't even require this code to work.
'''

import string

def hidden():

    def test_imports():

        from dessins.permtools import perm_from_str36
        from dessins.permtools import str36_from_perm


    def test_perm_to_and_from_str36():

        from dessins.permtools import perm_from_str36
        from dessins.permtools import str36_from_perm

        # TODO: Add some tests.


    # TODO: This needs a review.
    # TODO: Refactor out general purpose code?
    DIGITS_AND_LOWERCASE = string.digits + string.ascii_lowercase
    def perm_from_str36(s):
        '''Create permutation (of length at most 36) from string s.

        >>> perm = perm_from_str36('1230')
        >>> tuple(perm)
        (1, 2, 3, 0)
        >>> type(perm) == bytes
        True

        See also str36_from_perm(perm).
        '''
        if s.lower() != s:
            raise ValueError

        perm = bytes(int(c, 36) for c in s)
        if not is_perm(perm):
            raise ValueError("Failed to convert '%' to a permutation" % s)
        return perm


    def str36_from_perm(perm):
        '''Return string encoding of perm (of length at most 36).

        >>> str36_from_perm([1, 2, 3, 0])
        '1230'
        >>> str36_from_perm(range(36))
        '0123456789abcdefghijklmnopqrstuvwxyz'

        See also perm_from_str36(s).
        '''

        if not is_perm(perm):
            raise ValueError("Argument is not a permutation")
        if len(perm) > 36:
            raise ValueError("Argument is too long")

        return ''.join(DIGITS_AND_LOWERCASE[i] for i in perm)


def more_hidden():

    from functools import reduce
    import operator
    def num_product(iterable):
        return reduce(operator.mul, iterable, 1)
