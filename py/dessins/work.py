'''Work file for dessins'''

class BytesDessin(tuple):

    def __new__(cls, alpha, beta):

        return tuple.__new__(cls, (alpha, beta))
