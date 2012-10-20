# -*- coding: utf-8 -*-
import pytest

from pytest_quickcheck.generator import IS_PY3
if IS_PY3:
    unicode = str

@pytest.mark.randomize(("i1", int), ncalls=1)
def test_generate_int_type(i1):
    assert isinstance(i1, int)

@pytest.mark.randomize(("i1", int), ("i2", int), ncalls=1)
def test_generate_ints_type(i1, i2):
    assert isinstance(i1, int)
    assert isinstance(i2, int)

@pytest.mark.randomize(("s1", str), ncalls=1)
def test_generate_str_type(s1):
    assert isinstance(s1, str)

@pytest.mark.randomize(("u1", unicode), ncalls=1)
def test_generate_unicode_type(u1):
    assert isinstance(u1, unicode)

@pytest.mark.randomize(("f1", float), ncalls=1)
def test_generate_float_type(f1):
    assert isinstance(f1, float)

@pytest.mark.randomize(("b1", bool), ncalls=1)
def test_generate_bool_type(b1):
    assert isinstance(b1, bool)

@pytest.mark.randomize(("l1", [int, str]), ncalls=1)
def test_generate_list_type(l1):
    assert isinstance(l1, list)
    assert isinstance(l1[0], int)
    assert isinstance(l1[1], str)

@pytest.mark.randomize(("s1", set([int, str])), ncalls=1)
def test_generate_set_type(s1):
    assert isinstance(s1, set)
    result = list(map(lambda x: isinstance(x, int) or isinstance(x, str), s1))
    assert result[0] and result[1]

@pytest.mark.randomize(("t1", (int, str)), ncalls=1)
def test_generate_tuple_type(t1):
    assert isinstance(t1, tuple)
    assert isinstance(t1[0], int)
    assert isinstance(t1[1], str)

@pytest.mark.randomize(("d1", {'x': int, 'y': str}), ncalls=1)
def test_generate_dict_type(d1):
    assert isinstance(d1, dict)
    assert isinstance(d1["x"], int)
    assert isinstance(d1["y"], str)

@pytest.mark.randomize(("n1", None), ncalls=1)
def test_generate_none(n1):
    assert n1 is None
