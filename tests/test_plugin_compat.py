# -*- coding: utf-8 -*-
import pytest

from _pytest.mark import MarkInfo

try:
    from _pytest.mark import Mark

    mark0 = MarkInfo(Mark('mark0', (), {}))
    mark1 = MarkInfo(Mark('mark1', (), {}))
    mark1_expected = MarkInfo(Mark('mark1', (1, 2), {'x': 1}))
    mark2 = MarkInfo(Mark('mark2', (1, 2), {'x': 1}))
    mark2_expected = MarkInfo(Mark('mark2', (1, 2, 3, 4), {'x': 1, 'y': 2}))
    mark3 = MarkInfo(Mark('mark3', (('x', 'y'),), {'overwrite': 1}))
    mark3_expected = MarkInfo(
        Mark('mark3', (('x', 'y'), ('a', 'b')), {'overwrite': 5})
    )
except ImportError:
    mark0 = MarkInfo('mark0', (), {})
    mark1 = MarkInfo('mark1', (), {})
    mark1_expected = MarkInfo('mark1', (1, 2), {'x': 1})
    mark2 = MarkInfo('mark2', (1, 2), {'x': 1})
    mark2_expected = MarkInfo('mark2', (1, 2, 3, 4), {'x': 1, 'y': 2})
    mark3 = MarkInfo('mark3', (('x', 'y'),), {'overwrite': 1})
    mark3_expected = MarkInfo(
        'mark3', (('x', 'y'), ('a', 'b')), {'overwrite': 5}
    )

from pytest_quickcheck import plugin


@pytest.mark.parametrize(("markinfo", "args", "kwargs", "expected"), [
    (mark0, (), {}, mark0),
    (mark1, (1, 2), {'x': 1}, mark1_expected),
    (mark2, (3, 4), {'y': 2}, mark2_expected),
    (mark3, (('a', 'b'),), {'overwrite': 5}, mark3_expected),
])
def test_compat_modify_args(markinfo, args, kwargs, expected):
    plugin._compat_modify_args(markinfo, *args, **kwargs)
    assert expected.name == markinfo.name
    assert expected.args == markinfo.args
    assert expected.kwargs == markinfo.kwargs
