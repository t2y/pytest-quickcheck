# -*- coding: utf-8 -*-
import pytest
from pytest_quickcheck.data import listof, listof1

@pytest.mark.randomize(("s1", "str"), fixed_length=32, ncalls=1)
def test_create_file_with_randomize(tmpdir, s1):
    p = tmpdir.mkdir("sub").join("tmp.txt")
    p.write(s1)
    assert len(s1) == 32
    assert p.read() == s1
    assert len(tmpdir.listdir()) == 1

@pytest.mark.parametrize("prime", [3, 5, 7])
@pytest.mark.randomize(("i1", "int"), ("f1", "float"), max_num=100, ncalls=2)
def test_gen_parametrize_with_randomize_int_float(prime, i1, f1):
    assert prime in [3, 5, 7]
    assert isinstance(i1, int)
    assert i1 < 100
    assert isinstance(f1, float)

@pytest.mark.parametrize("prime", [3, 5, 7])
@pytest.mark.randomize(
    ("d1", "{'x': int, 'y': [str, (int, int)], 'z': {'x': str}}"),
    max_num=100, max_length=5, ncalls=1
)
def test_gen_parametrize_with_randomize_dict(prime, d1):
    assert prime in [3, 5, 7]
    assert isinstance(d1, dict)
    assert isinstance(d1["x"], int)
    assert isinstance(d1["y"], list)
    assert isinstance(d1["y"][0], str)
    assert isinstance(d1["y"][1], tuple)
    assert isinstance(d1["y"][1][0], int)
    assert isinstance(d1["y"][1][1], int)
    assert isinstance(d1["z"], dict)
    assert isinstance(d1["z"]["x"], str)

@pytest.mark.parametrize("prime", [3, 5, 7])
@pytest.mark.randomize(s1=str, choices=["hello", "bye"])
def test_gen_parametrize_with_randomize_str_substitution(prime, s1):
    assert prime in [3, 5, 7]
    assert isinstance(s1, str)
    assert s1 in ("hello", "bye")

@pytest.mark.randomize(l=listof(int))
def test_listof(l):
    assert isinstance(l, list)
    assert all(isinstance(i, int) for i in l), l

@pytest.mark.randomize(l=listof1(int))
def test_listof1(l):
    assert isinstance(l, list), l
    assert len(l) >= 1

@pytest.mark.randomize(l=listof(str, min_num=10, max_num=12))
def test_listof_min_max(l):
    assert isinstance(l, list)
    assert 10 <= len(l) <= 12
    assert all(isinstance(s, str) for s in l), l

@pytest.mark.randomize(l=listof1(str, choices=["hodor"]))
def test_listof_options(l):
    assert list(set(l)) == ["hodor"]
