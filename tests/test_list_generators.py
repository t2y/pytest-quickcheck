import pytest
from pytest import list_of, nonempty_list_of, dict_of, Generator

@pytest.mark.randomize(l=list_of(int))
def test_list_of(l):
    assert isinstance(l, list)
    assert all(isinstance(i, int) for i in l), l

@pytest.mark.randomize(l=nonempty_list_of(int), ncalls=50)
def test_nonempty_list_of(l):
    assert isinstance(l, list), l
    assert len(l) >= 1

@pytest.mark.randomize(l=list_of(str, min_items=10, max_items=12),
                       fixed_length=5)
def test_list_of_options(l):
    assert isinstance(l, list)
    assert 10 <= len(l) <= 12
    assert all(isinstance(s, str) and len(s) == 5 for s in l), l

@pytest.mark.randomize(l=list_of(str, items=15))
def test_list_of_num_items(l):
    assert len(l) == 15

@pytest.mark.randomize(l=list_of(str, items=15, min_items=1000))
def test_list_of_items_precedes_over_min_items(l):
    assert len(l) == 15

@pytest.mark.randomize(l=list_of(int), min_num=-10, max_num=-1)
def test_int_options_dont_affect_list_of(l):
    # if min_items, max_items would affect list_of it would raise an error
    # because min_items must be nonnegative

    assert isinstance(l, list)
    assert all(x < 0 for x in l), l

def test_list_of_negative_size():
    with pytest.raises(AssertionError):
        list_of(str, min_items=-1, max_items=-1).generate()

def test_list_of_illogical_size():
    with pytest.raises(AssertionError):
        list_of(str, min_items=2, max_items=1).generate()

def test_list_of_unsupported_options():
    with pytest.raises(NotImplementedError):
        list_of(str, choices="something").generate()

@pytest.mark.randomize(l=nonempty_list_of(str), choices=["hodor"])
def test_list_of_global_options(l):
    assert list(set(l)) == ["hodor"]

@pytest.mark.randomize(d=dict_of(int, str, items=5))
def test_dict_of(d):
    assert len(d) == 5
    assert all(isinstance(k, int) and isinstance(v, str) for k, v in d.items())

@pytest.mark.randomize(d=dict_of(int, str, items=100),
                       min_num=1, max_num=100, ncalls=20)
def test_dict_of_unique_keys(d):
    assert len(d) == 100

class pair(Generator):
    def __init__(self, data, **options):
        self.data = data
        self.options = options

    def generate(self, **kwargs):
        options = dict(self.options)
        options.update(kwargs)
        return (self.generate_data(self.data, **options),
                self.generate_data(self.data, **options))

@pytest.mark.randomize(x=pair(str, fixed_length=8))
def test_custom_generator(x):
    a, b = x
    assert len(a) == len(b) == 8
