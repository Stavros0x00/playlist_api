# Test the utils.py functions
from api.utils import chunks


def test_chunks():
    test_list = list(range(999999))
    for index, chunk in enumerate(chunks(test_list, 100000)):
        if index == 0:
            assert isinstance(chunk, list)
            assert len(chunk) == 100000

        elif index == 9:
            assert isinstance(chunk, list)
            assert len(chunk) == 99999
