# -*- coding: utf-8 -*-
import pytest

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
