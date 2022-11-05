Requirements
------------

* Python 2.7 or 3.7 and later

Features
--------

* Provide **pytest.mark.randomize** function for generating random test data

Installation
============

::

    $ pip install pytest-quickcheck

Quick Start
===========

Just pass the signature of function to *randomize* marker.
The signature is represented a tuple consist of argument name and its type.

::

    @pytest.mark.randomize(i1=int, i2=int, ncalls=1)
    def test_generate_ints(i1, i2):
        pass

More complex data structure::

    @pytest.mark.randomize(
        d1={'x': int, 'y': [str, (int, int)], 'z': {'x': str}}
    )
    def test_generate_dict(d1):
        pass

The *randomize* marker is able to use with *parametrize* marker.

::

    @pytest.mark.parametrize("prime", [2, 3, 5])
    @pytest.mark.randomize(i1=int, f1=float, ncalls=1)
    def test_gen_parametrize_with_randomize_int_float(prime, i1, f1):
        pass

Using command line option ``--randomize`` restricts only the *randomize* test.

::

    $ py.test -v --randomize test_option.py 
    ==========================================================================================
    test session starts
    ==========================================================================================
    test_option.py:5: test_normal SKIPPED
    test_option.py:8: test_generate_ints[74-22] PASSED

Usage
=====

There some options for each data type::

    $ py.test --markers
    @pytest.mark.randomize(argname=type, **options): mark the test function with
    random data generating any data type.
      There are options for each data type: (see doc for details)
      int: ['min_num', 'max_num']
      float: ['min_num', 'max_num', 'positive']
      str: ['encoding', 'fixed_length', 'min_length', 'max_length', 'str_attrs']
      list_of, nonempty_list_of, dict_of: ['items', 'min_items', 'max_items']

* common option

  | **ncalls**: set the number of calls. Defaults to 3. (e.g. ncalls=5)
  | **choices**: choose from given sequence. (e.g. choices=[3, 5, 7])

* int

  | **min_num**: lower limit for generating integer number. (e.g. min_num=0)
  | **max_num**: upper limit for generating integer number. (e.g. max_num=10)

* float

  | **min_num**: lower limit for generating real number. (e.g. min_num=0.0)
  | **max_num**: upper limit for generating real number. (e.g. max_num=1.0)
  | **positive**: generate only positive real number if set to `True`.
    Defaults to `False`. (e.g. positive=True)

* str

  | **encoding**: generate unicode string encoded given character code.
    (e.g. encoding="utf-8")  # for Python 2.x only
  | **fixed_length**: generate fixed length string. (e.g. fixed_length=8)
  | **max_length**: generate the string less than or equal to max length
    (e.g. max_length=32)
  | **str_attrs**: generate the string in given letters.
    set a tuple consist of attribute names in the `string module`_.
    (e.g. str_attrs=("digits", "punctuation")

* list_of, nonempty_list_of, dict_of

  | **items**: number of items.
  | **min_items**: lower limit on number of items.
  | **max_items**: upper limit on number of items.

Probably, `tests/test_plugin_basic.py` is useful for
learning how to use these options.

.. _string module: http://docs.python.org/library/string.html

Generating Collections
======================

To generate a variable length list of items::

    from pytest import list_of

    @pytest.mark.randomize(l=list_of(int))
    def test_list_of(l):
        pass

You can control its size with the ``items``, ``min_items`` and
``max_items`` options, or use the ``nonempty_list_of`` shortcut.

::
 
    @pytest.mark.randomize(l=list_of(int, num_items=10))
    def test_list_of_length(l):
        assert len(l) == 10

    @pytest.mark.randomize(l=list_of(int, min_items=10, max_items=100))
    def test_list_of_minimum_length(l):
        assert len(l) >= 10

    from pytest import nonempty_list_of

    @pytest.mark.randomize(l=nonempty_list_of(int)
    def test_list_of_minimum_length(l):
        assert len(l) >= 1

Options for data types work as usual::

    @pytest.mark.randomize(l=list_of(str, num_items=10), choices=["a", "b", "c"])
    def test_list_of(l):
        assert l[0] in ["a", "b", "c"]

(Note what goes into the ``list_of()`` call and what goes outside.)

You can also generate a dict::

    from pytest import dict_of
    @pytest.mark.randomize(d=dict_of(str, int))
    def test_list_of(l):
        pass


Python 3
========

For Python 3, the signature of function is given as function annotation.

::

    @pytest.mark.randomize(min_num=0, max_num=2, ncalls=5)
    def test_generate_int_anns(i1: int):
        pass

Mixed representation is also OK, but it might not be useful. 

::

    @pytest.mark.randomize(i1=int, fixed_length=8)
    def test_generate_arg_anns_mixed(i1, s1: str):
        pass

See also: `PEP 3107 -- Function Annotations`_

.. _PEP 3107 -- Function Annotations: http://www.python.org/dev/peps/pep-3107/

Backward Compatibility
======================

Under 0.6 version, types were specified by strings containing the name
of the type. It's still supported if you like.

::

    @pytest.mark.randomize(("i1", "int"), ("i2", "int"), ncalls=1)
