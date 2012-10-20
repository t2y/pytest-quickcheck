# -*- coding: utf-8 -*-
import pytest

@pytest.mark.randomize(ncalls=1)
def test_generate_int_anns(i1: int):
    assert isinstance(i1, int)

@pytest.mark.randomize(min_num=0, max_num=2, ncalls=5)
def test_generate_int_with_option_anns(i1: int):
    assert isinstance(i1, int)
    assert 0 <= i1 <= 2

@pytest.mark.randomize(ncalls=1)
def test_generate_ints_anns(i1: int, i2: int):
    assert isinstance(i1, int)
    assert isinstance(i2, int)

@pytest.mark.randomize(choices=[0, 1])
def test_generate_int_with_choices_anns(i1: int):
    assert isinstance(i1, int)
    assert i1 in [0, 1]

@pytest.mark.randomize(ncalls=1)
def test_generate_list_anns(l1: [int, str]):
    assert isinstance(l1, list)
    assert isinstance(l1[0], int)
    assert isinstance(l1[1], str)

@pytest.mark.randomize(ncalls=1)
def test_generate_set_anns(s1: set([int, str])):
    assert isinstance(s1, set)
    result = list(map(lambda x: isinstance(x, int) or isinstance(x, str), s1))
    assert result[0] and result[1]

@pytest.mark.randomize(ncalls=1)
def test_generate_tuple_anns(t1: (int, str)):
    assert isinstance(t1, tuple)
    assert isinstance(t1[0], int)
    assert isinstance(t1[1], str)

@pytest.mark.randomize(ncalls=1)
def test_generate_dict_anns(d1: {'x': int, 'y': str}):
    assert isinstance(d1, dict)
    assert isinstance(d1["x"], int)
    assert isinstance(d1["y"], str)

@pytest.mark.randomize(ncalls=1)
def test_generate_none_anns(n1: None):
    assert n1 is None

@pytest.mark.randomize(("i1", "int"), fixed_length=8)
def test_generate_arg_anns_mixed(i1, s1: str):
    assert isinstance(i1, int)
    assert isinstance(s1, str)
    assert len(s1) == 8

@pytest.mark.parametrize("prime", [3, 5])
@pytest.mark.randomize(("f1", "float"), min_num=-1.0, max_num=1.0)
def test_generate_arg_anns_param_mixed(prime, f1, b1: bool):
    assert prime in [3, 5]
    assert isinstance(f1, float)
    assert -1.0 <= f1 <= 1.0
    assert isinstance(b1, bool)

@pytest.mark.parametrize("prime", [3, 5])
@pytest.mark.randomize(("f1", "float"), min_num=-1.0, max_num=1.0)
@pytest.mark.randomize(t1=(str, str), max_length=3)
def test_generate_arg_anns_param_mixed(prime, f1, b1: bool, t1):
    assert prime in [3, 5]
    assert isinstance(f1, float)
    assert -1.0 <= f1 <= 1.0
    assert isinstance(b1, bool)
    assert len(t1[0]) <= 3
    assert len(t1[1]) <= 3
    assert isinstance(t1[0], str)
    assert isinstance(t1[1], str)
    assert isinstance(t1, tuple)
