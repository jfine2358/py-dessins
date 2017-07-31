'''Test work file for dessins'''

from dessins.work import BytesDessin

def test_create():
    BytesDessin(bytes(range(4)), bytes(range(4)))
