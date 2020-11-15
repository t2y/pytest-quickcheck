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


def _get_ncalls(randomize, data_option):
    randomize_kwargs_ncalls = randomize.kwargs.pop("ncalls", None)
    if randomize_kwargs_ncalls is not None:
        return randomize_kwargs_ncalls

    data_option_ncalls = data_option.pop("ncalls", None)
    if data_option_ncalls is not None:
        return data_option_ncalls

    return DEFAULT_NCALLS


def _set_parameterize(metafunc, randomize, data_option):
    from pytest_quickcheck.generator import generate, parse

    ncalls = _get_ncalls(randomize, data_option)
    for argname, data_def in randomize.args:
        data_type, retrieve = parse(data_def)
        values = [retrieve(generate(data_type, **data_option))
                  for _ in range(ncalls)]
        metafunc.parametrize(argname, values)


def exclude_randomize_args_in_annotations(randomize, anns):
    randomize_args = {i[0] for i in randomize.args}
    for ann in anns:
        variable_name = ann[0]
        if variable_name in randomize_args:
            continue
        if variable_name == "return":
            continue
        yield ann


def get_randomize_args(randomize, anns):
    if randomize is None:
        return tuple(i for i in anns if i[0] != "return")
    return tuple(exclude_randomize_args_in_annotations(randomize, anns))


def pytest_generate_tests(metafunc):
    from pytest_quickcheck.generator import DATA_TYPE_OPTIONS, IS_PY3

    if not _has_pytestmark(metafunc):
        return

    randomize = None
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
                metafunc.function.pytestmark[i] = randomize

            _set_parameterize(metafunc, randomize, data_option)

    if IS_PY3 and hasattr(metafunc.function, "__annotations__"):
        anns = metafunc.function.__annotations__.items()
        args = get_randomize_args(randomize, anns)
        if args:
            randomize = Mark("randomize", args, {})
            _set_parameterize(metafunc, randomize, ann_data_option)
