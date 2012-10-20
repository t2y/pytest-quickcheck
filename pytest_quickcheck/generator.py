# -*- coding: utf-8 -*-
import random
import sys
import string
from functools import wraps
from itertools import cycle
from math import log, exp
from operator import getitem

IS_PY3 = sys.version_info[0] == 3
if IS_PY3:
    unicode = str  # FIXME: consider later
    from string import ascii_letters
    _MIN_INT = -sys.maxsize - 1
    _MAX_INT = sys.maxsize
else:
    from string import letters as ascii_letters
    _MIN_INT = -sys.maxint - 1
    _MAX_INT = sys.maxint

DATA_TYPE_OPTION = {
    "common": ["ncalls", "choices"],
    "int": ["min_num", "max_num"],
    "float": ["min_num", "max_num", "positive"],
    "str": ["encoding", "fixed_length", "max_length", "str_attrs"],
}

DATA_TYPE_OPTIONS = set()
DATA_TYPE_OPTIONS.update(*DATA_TYPE_OPTION.values())

_MIN_FLOAT = -1e7
_MAX_FLOAT = 1e7
_MIN_FLOAT_MAG = 1e-7
_MAX_FLOAT_MAG = 1e+7

_ASCII = ascii_letters
_ASCII_LEN = len(_ASCII) - 1

_BOOL_CYCLE = cycle([True, False])


def choice_data(func):
    def _choice_data(*args, **kwargs):
        choices = kwargs.get("choices")
        if choices:
            return random.choice(choices)
        else:
            return func(*args, **kwargs)
    return _choice_data

def sanitize_option(data_def):
    def _sanitize_option(func):
        @wraps(func)
        def __sanitize_option(*args, **kwargs):
            sanitized_kwargs = {}
            for key in DATA_TYPE_OPTION[data_def]:
                value = kwargs.get(key)
                if value is not None:
                    sanitized_kwargs[key] = value
            return func(*args, **sanitized_kwargs)
        return __sanitize_option
    return _sanitize_option

@choice_data
@sanitize_option("int")
def get_int(min_num=_MIN_INT, max_num=_MAX_INT):
    return random.randint(min_num, max_num)

@choice_data
@sanitize_option("float")
def get_float(min_num=_MIN_FLOAT, max_num=_MAX_FLOAT,
              min_mag=_MIN_FLOAT_MAG, max_mag=_MAX_FLOAT_MAG, positive=False):
    if positive:
        min_mag, max_mag = log(min_mag), log(max_mag)
        scale_range = max_mag - min_mag
        return exp(random.random() * scale_range + min_mag)
    else:
        length = max_num - min_num
        return random.random() * length + min_num

@choice_data
@sanitize_option("str")
def get_str(encoding=None, fixed_length=None, max_length=32, str_attrs=None):
    base, end = str_attrs if str_attrs else (_ASCII, _ASCII_LEN)
    length = fixed_length if fixed_length else random.randint(0, max_length)
    if end < length:
        length = end
    s = "".join(getitem(base, random.randint(0, end)) for _ in range(length))
    if encoding and not IS_PY3:
        s = unicode(s, encoding)
    return s

def get_unicode(**kwargs):
    if not kwargs.get("encoding"):
        kwargs["encoding"] = "utf-8"
    return get_str(**kwargs)

def get_bool():
    return next(_BOOL_CYCLE)


class OptionOptimizer(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.need_optimize = {
            "str_attrs": self.optimize_str_attrs,
        }

    def __call__(self, *args, **kwargs):
        for key in self.need_optimize:
            value = kwargs.get(key)
            if value:
                try:
                    kwargs[key] = self.cache[value]
                except KeyError:
                    optimized_value = self.need_optimize[key](value)
                    kwargs[key] = self.cache[value] = optimized_value
            return self.func(*args, **kwargs)

    def optimize_str_attrs(self, attrs):
        base = "".join(getattr(string, attr) for attr in attrs)
        return base, len(base) - 1

@OptionOptimizer
def generate(data, **kwargs):
    if data is int:
        yield get_int(**kwargs)
    elif data is float:
        yield get_float(**kwargs)
    elif data is str:
        yield get_str(**kwargs)
    elif data is unicode:
        yield get_unicode(**kwargs)
    elif data is bool:
        yield get_bool()
    elif isinstance(data, (list, set, tuple)):
        for value in data:
            yield retrieve_func(value)(generate(value, **kwargs))
    elif isinstance(data, dict):
        _dict = data.copy()
        for key, value in data.items():
            _dict[key] = retrieve_func(value)(generate(value, **kwargs))
        yield _dict
    elif data is None:
        yield None
    else:
        raise NotImplementedError("Unknown data type")

def retrieve_func(data):
    if isinstance(data, (list, set, tuple)):
        return type(data)
    else:
        return next

def parse(data_def):
    data_type = eval(data_def) if isinstance(data_def, str) else data_def
    return data_type, retrieve_func(data_type)
