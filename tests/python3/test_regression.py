import pytest


@pytest.mark.randomize(total=int, min_num=0, max_num=100, ncalls=10)
def test_regression1(total: int) -> None:
    assert isinstance(total, int)
