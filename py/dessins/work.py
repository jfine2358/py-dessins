'''Work file for dessins'''

class BytesDessin(tuple):

    def __new__(cls, alpha, beta):

        if len(alpha) != len(beta):
            raise ValueError

        return tuple.__new__(cls, (alpha, beta))


    def __len__(self):

        return len(self[0])
