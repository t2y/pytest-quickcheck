"""An attempt at
http://www.chiark.greenend.org.uk/~sgtatham/algorithms/equivalence.html:

In the general case, I do not believe there is a better solution than
Mr. Tatham's.

In the specific case where you may assume that the "universe" is huge
relative to the set of all disconnected values, there may be something
we can do...

From the page, (c) Simon Tatham:

Introduction

An equivalence relation on a set is a partition of the set into
classes. Two elements are considered equivalent if they are in the
same class, and not if they are not.

In some situations, you might find yourself dealing with a set of
elements and gradually discover ways in which they behave differently;
so you might want to keep track of which ones are different and which
ones are not.

(In other situations, you might find yourself dealing with a set of
distinct elements and gradually discover that some are equivalent to
others; but there's a known algorithm for this. It's made easier by
the fact that if all elements start off distinct, you're unlikely ever
to be dealing with too many of them to enumerate individually.)
Desired Properties

So I'm looking for data structures with these operations:

    Canonify. Given an element of the set, return a canonical element
    of the equivalence class containing that element. Any two
    equivalent elements should return the same element when
    canonified. Any two non-equivalent elements should return
    different elements.

    Enumerate. Run through all the equivalence classes one by one,
    probably by means of their canonical elements.

    Disconnect. Given a subset of the set, arrange that every
    equivalence class is either totally inside the subset or totally
    outside it, by means of splitting any class that crosses the
    boundary into two.

Best Known Approximations

For a small and dense set, where it's feasible to use the set elements
as array indices, there's a reasonable implementation of all this:
have an array A with one element for each set element. Then, for each
set element e, let A[e] contain the canonical element of the class
containing e. The canonical element of any class is defined to be the
smallest-value element of that class.

Then the "canonify" operation is a simple array lookup, and the
"enumerate" operation consists of going through the array looking for
any e satisfying A[e] = e. Disconnection is O(N), and connection is
also O(N); but by assumption N is small, so that isn't too big a
problem.

For a sparse set - perhaps the set of all strings, or the set of basic
blocks in a compilation process - I have no answer.

Applications

One clear application for equivalence classes with a disconnect
operation is the algorithm that constructs a deterministic finite
state machine from a nondeterministic one (used in regular expression
processing). Most of the character set can be treated as equivalent:
any character not mentioned explicitly in the regular expression
behaves just the same as any other, and any two characters that are
always used as part of the same character class are equivalent. For
example, in the regular expression
(0[xX][0-9A-Fa-f]+|[1-9][0-9]*|0[0-7]*), there is no need to treat all
ASCII characters differently. The equivalence classes are [0], [Xx],
[A-Fa-f], [1-7], [8-9], and everything else. So we only need to
compute six transitions for each state, instead of 256. (back to
algorithms index).

"""

class Equivalence(object):
    """Keeps track of splitting a universe set into equivalence sets.
    Performs well when universe is huge or infinite and all other
    equivalence sets are relatively small.

    Assumes that values are ordered, although having infinite ordered
    values is enough (what we really need is the ability to generate a
    "bigger" value for any value).

    The important idea behind the algorithm is that of maintaining a
    separate "rest" equivalence partition, outside of the data
    structures for keeping track of everything,

    """
    def __init__(self, valid_item=0):
        """
        valid_item can be any valid item in the universal set.
        """
        self._subsets = []
        self._item_to_subset = {}
        self._rest_canonical = valid_item

    def canonify(self, item):
        # O(1) amortized
        s = self._item_to_subset.get(item, None)
        if s is None:
            return self._rest_canonical
        return self._arbitrary(s)

    def enumerate(self):
        # O(n) amortized, where n is number of equivalence partitions
        for s in self._subsets:
            yield self._arbitrary(s)
        yield self._rest_canonical

    def disconnect(self, items):
        # O(n) amortized where n is number of items
        subset = set(items)
        if len(subset) == 0:
            return
        if self._item_to_subset.get(self._arbitrary(subset), None) == subset:
            # we already know this equivalence
            return
        virgin = []
        touching = {}
        for item in subset:
            s = self._item_to_subset.get(item, None)
            if s is None:
                virgin.append(item)
            else:
                touching.setdefault(id(s), []).append(item)
        # This looks like O(n) amortized: if there are k parts, on
        # average each has n/k items, so it is O(k * n/k) == O(n).
        # This calculation works for the edge cases where k is 1,
        # sqrt(n), and n, so I trust it.
        for part in touching.values():
            whole = self._item_to_subset[part[0]]
            if len(whole) != len(part):
                # len(part) != 0, so some are in and some are out. Must split
                whole.difference_update(part)  # a.difference_update(b) is O(b)
                self._create(part)
        if len(virgin) > 0:
            self._create(virgin)
            self._update_rest(virgin)

    def _update_rest(self, subset):
        """subset should contain at least all "virgin" items (items
        that used to be in "rest" and are now in a specified
        equivalence). Chooses a new canonical for the "rest" set.

        """
        self._rest_canonical = max(self._rest_canonical, max(subset) + 1)

    def _create(self, items):
        subset = set(items)
        for item in items:
            self._item_to_subset[item] = subset
        self._subsets.append(subset)

    @staticmethod
    def _arbitrary(s):
        """Returns an arbitrary item from set s. Consistently returns
        the same item as long as s remains the same.

        """
        return next(iter(s))


import pytest
from pytest import list_of, nonempty_list_of

@pytest.mark.randomize(equivalence=nonempty_list_of(int),
                       unrelateds=nonempty_list_of(list_of(int)),
                       min_num=-10, max_num=100)
def test_canonify(equivalence, unrelateds, n_calls=1000):
    e = Equivalence()
    e.disconnect(equivalence)
    canon = e.canonify(equivalence[0])

    equivalence = set(equivalence)
    assert canon in equivalence
    for unrelated in unrelateds:
        unrelated = list(set(unrelated).difference(equivalence))
        e.disconnect(unrelated)
        for item in equivalence:
            assert e.canonify(item) == canon

@pytest.mark.randomize(equivalences=list_of(list_of(int)))
def test_enumerate(equivalences, n_calls=100):
    e = Equivalence()
    for equivalence in equivalences:
        e.disconnect(equivalence)
        canons = list(e.enumerate())
        # change e without changing any equivalence
        new = e._rest_canonical
        e.disconnect([new])
        canons2 = list(e.enumerate())
        assert len(canons2) == len(canons) + 1
        # the only different item is the new rest canon
        assert len(set(canons2).difference(set(canons))) == 1

if __name__ == '__main__':
    from traceback import print_exc

    e = Equivalence()
    while True:
        try:
            print("c number                - canonify")
            print("e                       - enumerate")
            print("d number1 number2 ...   - disconnect")
            print("q                       - quit")
            command = raw_input(":").split()  # pragma: no flakes
            if command[0] == "q":
                break
            elif command[0] == "c":
                assert len(command) == 2
                print(e.canonify(int(command[1])))
            elif command[0] == "e":
                print(list(e.enumerate()))
            elif command[0] == "d":
                e.disconnect(map(int, command[1:]))
            else:
                print("usage error")
        except Exception:
            print_exc()
