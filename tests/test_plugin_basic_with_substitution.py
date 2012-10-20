# -*- coding: utf-8 -*-
import string

import pytest

from pytest_quickcheck.generator import IS_PY3
if IS_PY3:
    unicode = str

@pytest.mark.randomize(i1=int, ncalls=1)
def test_generate_int_subs(i1):
    assert isinstance(i1, int)

@pytest.mark.randomize(i1=int, min_num=0, max_num=2, ncalls=5)
def test_generate_int_with_option_subs(i1):
    assert isinstance(i1, int)
    assert 0 <= i1 <= 2

@pytest.mark.randomize(i1=int, i2=int, ncalls=1)
def test_generate_ints_subs(i1, i2):
    assert isinstance(i1, int)
    assert isinstance(i2, int)

@pytest.mark.randomize(i1=int, choices=[0, 1])
def test_generate_int_with_choices_subs(i1):
    assert isinstance(i1, int)
    assert i1 in [0, 1]

@pytest.mark.randomize(s1=str, ncalls=1)
def test_generate_str_subs(s1):
    assert isinstance(s1, str)

@pytest.mark.randomize(s1=str, fixed_length=2)
def test_generate_str_with_fixed_length_subs(s1):
    assert isinstance(s1, str)
    assert len(s1) == 2

@pytest.mark.randomize(s1=str, max_length=3, ncalls=5)
def test_generate_str_with_max_length_subs(s1):
    assert isinstance(s1, str)
    assert len(s1) <= 3

@pytest.mark.randomize(s1=str, str_attrs=("octdigits",))
def test_generate_str_with_octdigits_subs(s1):
    assert isinstance(s1, str)
    assert s1 == "".join(i for i in s1 if string.octdigits)

@pytest.mark.randomize(s1=str, str_attrs=("digits", "punctuation"))
def test_generate_str_with_attrs_subs(s1):
    assert isinstance(s1, str)
    assert s1 == "".join(i for i in s1 if string.digits or string.punctuation)

@pytest.mark.randomize(s1=str, encoding="utf-8", ncalls=1)
def test_generate_str_with_decoded_subs(s1):
    assert isinstance(s1, unicode)
    assert isinstance(s1.encode("utf-8").decode("utf-8"), unicode)

@pytest.mark.randomize(u1=unicode, ncalls=1)
def test_generate_unicode_subs(u1):
    assert isinstance(u1, unicode)

@pytest.mark.randomize(s1=str, s2=str, ncalls=1)
def test_generate_strs_subs(s1, s2):
    assert isinstance(s1, str)
    assert isinstance(s2, str)

@pytest.mark.randomize(s1=str, s2=str, choices=["hello", "bye"])
def test_generate_strs_subs(s1, s2):
    assert isinstance(s1, str)
    assert isinstance(s2, str)
    assert s1 in ("hello", "bye")
    assert s2 in ("hello", "bye")

@pytest.mark.randomize(f1=float, ncalls=1)
def test_generate_float_subs(f1):
    assert isinstance(f1, float)

@pytest.mark.randomize(f1=float, min_num=-1.0, max_num=1.0, ncalls=5)
def test_generate_float_with_min_max_subs(f1):
    assert isinstance(f1, float)
    assert -1.0 <= f1 <= 1.0

@pytest.mark.randomize(f1=float, positive=True, ncalls=5)
def test_generate_positive_float_subs(f1):
    assert isinstance(f1, float)
    assert 0.0 <= f1

@pytest.mark.randomize(f1=float, choices=[0.0, 0.1])
def test_generate_float_with_choices_subs(f1):
    assert isinstance(f1, float)
    assert f1 in [0.0, 0.1]

@pytest.mark.randomize(f1=float, f2=float, ncalls=1)
def test_generate_floats_subs(f1, f2):
    assert isinstance(f1, float)
    assert isinstance(f2, float)

@pytest.mark.randomize(b1=bool, ncalls=1)
def test_generate_bool_subs(b1):
    assert isinstance(b1, bool)

@pytest.mark.randomize(b1=bool, b2=bool, ncalls=1)
def test_generate_bools_subs(b1, b2):
    assert isinstance(b1, bool)
    assert isinstance(b2, bool)

@pytest.mark.randomize(l1=[int, str], ncalls=1)
def test_generate_list_subs(l1):
    assert isinstance(l1, list)
    assert isinstance(l1[0], int)
    assert isinstance(l1[1], str)

@pytest.mark.randomize(s1=set([int, str]), ncalls=1)
def test_generate_set_subs(s1):
    assert isinstance(s1, set)
    result = list(map(lambda x: isinstance(x, int) or isinstance(x, str), s1))
    assert result[0] and result[1]

@pytest.mark.randomize(t1=(int, str), ncalls=1)
def test_generate_tuple_subs(t1):
    assert isinstance(t1, tuple)
    assert isinstance(t1[0], int)
    assert isinstance(t1[1], str)

@pytest.mark.randomize(d1={'x': int, 'y': str}, ncalls=1)
def test_generate_dict_subs(d1):
    assert isinstance(d1, dict)
    assert isinstance(d1["x"], int)
    assert isinstance(d1["y"], str)

@pytest.mark.randomize(n1=None, ncalls=1)
def test_generate_none_subs(n1):
    assert n1 is None
