import pytest
from _pytest.mark import Mark

from pytest_quickcheck.generator import Generator
from pytest_quickcheck.generator import list_of, nonempty_list_of, dict_of

DEFAULT_NCALLS = 3

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

    pytest.list_of = globals()["list_of"]
    pytest.nonempty_list_of = globals()["nonempty_list_of"]
    pytest.dict_of = globals()["dict_of"]
    pytest.Generator = globals()["Generator"]


def pytest_runtest_setup(item):
    if not isinstance(item, pytest.Function):
        return
    if item.config.option.randomize and not hasattr(item.obj, 'randomize'):
        pytest.skip("test with randomize only")

def _has_pytestmark(metafunc):
    if not hasattr(metafunc.function, "pytestmark"):
        return False
    pytestmark = metafunc.function.pytestmark
    if len(pytestmark) == 0:
        return False
    return True

def _set_parameterize(metafunc, randomize, data_option):
    from pytest_quickcheck.generator import generate, parse

    ncalls = randomize.kwargs.pop("ncalls", DEFAULT_NCALLS)
    for argname, data_def in randomize.args:
        data_type, retrieve = parse(data_def)
        values = [retrieve(generate(data_type, **data_option))
                  for _ in range(ncalls)]
        metafunc.parametrize(argname, values)

def pytest_generate_tests(metafunc):
    from pytest_quickcheck.generator import DATA_TYPE_OPTIONS, IS_PY3

    if not _has_pytestmark(metafunc):
        return

    ann_data_option = {}

    for i, mark in enumerate(metafunc.function.pytestmark):
        if mark.name == "randomize":
            randomize = mark
            data_option = {}
            for opt in DATA_TYPE_OPTIONS:
                if opt in randomize.kwargs:
                    data_option[opt] = randomize.kwargs.pop(opt)
                    ann_data_option.update(data_option)

            args = tuple(i for i in randomize.kwargs.items())
            if args:
                randomize = Mark(randomize.name, args, {})
                print(randomize)
                metafunc.function.pytestmark[i] = randomize

            _set_parameterize(metafunc, randomize, data_option)

    if IS_PY3 and hasattr(metafunc.function, "__annotations__"):
        anns = metafunc.function.__annotations__.items()
        args = tuple(i for i in anns)
        if args:
            randomize = Mark("randomize", args, {})
            _set_parameterize(metafunc, randomize, ann_data_option)
