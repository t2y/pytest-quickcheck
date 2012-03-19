# -*- coding: utf-8 -*-
import pytest

def pytest_addoption(parser):
    parser.addoption("--randomize", action="store_true",
                     help="random data test")

def pytest_configure(config):
    from pytest_quickcheck.generator import DATA_TYPE_OPTION as opt
    config.addinivalue_line("markers",
        "randomize((argname, type), **options): mark the test function with "
        "random data generating any data type.\n"
        "  There are options for each data type: (see doc for details)\n"
        "  {0}\n  {1}\n  {2}".format(
            *("{0}: {1}".format(i, opt[i]) for i in opt)))

def pytest_runtest_setup(item):
    if not isinstance(item, item.Function):
        return
    if item.config.option.randomize and not hasattr(item.obj, 'randomize'):
        pytest.skip("test with randomize only")

def pytest_generate_tests(metafunc):
    from pytest_quickcheck.generator import generate, parse
    if hasattr(metafunc.function, "randomize"):
        randomize = metafunc.function.randomize
        for argname, data_def in randomize.args:
            data_type, retrieve = parse(data_def)
            ncalls = randomize.kwargs.get("ncalls", 3)
            values = [retrieve(generate(data_type, **randomize.kwargs))
                        for _ in range(ncalls)]
            metafunc.parametrize(argname, values)
