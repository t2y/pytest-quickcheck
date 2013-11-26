# -*- coding: utf-8 -*-
import pytest
from pytest_quickcheck.generator import Generator, \
    list_of, nonempty_list_of, dict_of

DEFAULT_NCALLS = 3

def pytest_namespace():
    return dict((x, globals()[x]) for x in [
        "list_of", "nonempty_list_of", "dict_of", "Generator"])

def pytest_addoption(parser):
    parser.addoption("--randomize", action="store_true",
                     help="random data test")

def pytest_configure(config):
    from pytest_quickcheck.generator import DATA_TYPE_OPTION as opt
    config.addinivalue_line(
        "markers",
        "randomize(argname=type, **options): mark the test function with "
        "random data generating any data type.\n"
        "  There are options for each data type: (see doc for details)\n  " +
        "\n  ".join("{0}: {1}".format(i, opt[i]) for i in opt))

def pytest_runtest_setup(item):
    if not isinstance(item, item.Function):
        return
    if item.config.option.randomize and not hasattr(item.obj, 'randomize'):
        pytest.skip("test with randomize only")

def pytest_generate_tests(metafunc):
    from pytest_quickcheck.generator import (DATA_TYPE_OPTIONS, IS_PY3,
                                             generate, parse)
    if hasattr(metafunc.function, "randomize"):
        randomize = metafunc.function.randomize

        if IS_PY3 and hasattr(metafunc.function, "__annotations__"):
            anns = metafunc.function.__annotations__.items()
            randomize.args += tuple(i for i in anns)

        ncalls = randomize.kwargs.pop("ncalls", DEFAULT_NCALLS)
        data_option = {}
        for opt in DATA_TYPE_OPTIONS:
            if opt in randomize.kwargs:
                data_option[opt] = randomize.kwargs.pop(opt)
        randomize.args += tuple(i for i in randomize.kwargs.items())

        for argname, data_def in randomize.args:
            data_type, retrieve = parse(data_def)
            values = [retrieve(generate(data_type, **data_option))
                      for _ in range(ncalls)]
            metafunc.parametrize(argname, values)
