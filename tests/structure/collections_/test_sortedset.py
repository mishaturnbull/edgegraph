"""
Unit tests for structure.collections.sortedset module.
"""

import itertools
import pickle
import random

import pytest

from edgegraph.structure.collections_.sortedset import SortedSet

A = list(range(10))
B = list(range(5, 15))
C = A + list(filter(lambda x: x not in A, B))
D = list(range(15, 25))
E = C + D


def b_generator():
    """
    Basic generator to assist with testing
    """
    yield from B


def test_sortedset_init():
    """
    Ensure we can initalize a sorted set
    """
    set_ = SortedSet()
    assert isinstance(set_, set), "sorted set inited incorrectly?"
    assert len(set_) == 0, "set was not empty"
    assert not set_._list, "underlying list was not initalized correctly"


def test_sortedset_init_sequence():
    """
    Ensure we can initalize a sorted set with a sequence of data
    and order is maintained.
    """
    num = 10
    a = list(range(num))

    set_ = SortedSet(a)
    assert isinstance(set_, set)
    assert len(set_) == num
    assert set_._list
    assert set_._list == a
    assert list(set_) == a


def test_sortedset_init_generator():
    """
    Ensure we can initalize a sorted set from a generator and order
    is maintained.
    """
    num = 10
    a = list(range(num))
    gen = (i for i in a)

    set_ = SortedSet(gen)
    assert isinstance(set_, set)
    assert len(set_) == num
    assert set_._list
    assert set_._list == a
    assert list(set_) == a


def test_sortedset_init_repeated():
    """
    Ensure that sorted set doesn't store repeated values
    when initalizing from an iterable
    """
    num = 10
    half = num // 2
    a = list(range(half))
    b = a * 2

    for i in a:
        assert b.count(i) == 2

    set_ = SortedSet(b)
    assert isinstance(set_, set)
    assert len(set_) == half
    assert set_._list
    assert set_._list == a
    assert list(set_) == a


def test_sortedset_init_bad_type():
    """
    Ensure we can't initalize from a non-iterable object.
    """
    a = 1
    with pytest.raises(TypeError):
        SortedSet(a)


def test_sortedset_basic_add():
    """
    Test adding value to an empty sorted set
    """
    val = 1

    a = SortedSet()
    assert len(a) == 0
    assert len(a._list) == 0

    a.add(val)

    assert len(a) == 1
    assert len(a._list) == 1
    assert a[0] == 1


def test_sortedset_duplicated_add():
    """
    Test adding a value already contained in a sorted set
    """
    val = 1

    a = SortedSet((1,))
    assert len(a) == 1
    assert len(a._list) == 1

    a.add(val)

    assert len(a) == 1
    assert len(a._list) == 1
    assert a[0] == 1


def test_sortedset_add_order():
    """
    Tests to make sure values added to set stay in insertion order
    """
    a = SortedSet()

    vals = []
    while True:
        val = random.randint(1, 100)
        if val in a:
            continue

        a.add(val)
        vals.append(val)

        if len(vals) >= 30:
            break

    assert a._list == vals


def test_sortedset_clear():
    """
    Test clearing all data in the sorted set
    """
    num = 50
    a = SortedSet(range(num))
    assert len(a) == num
    assert len(a._list) == num

    a.clear()
    assert len(a) == 0
    assert len(a._list) == 0


def test_sortedset_discard():
    """
    Test discarding values from a sorted set
    """
    num = 50
    a = SortedSet(range(num))
    assert len(a) == num
    assert len(a._list) == num

    a.discard(0)
    assert len(a) == num - 1
    assert len(a._list) == num - 1

    a.discard(0)
    assert len(a) == num - 1
    assert len(a._list) == num - 1


def test_sortedset_remove():
    """
    Test removing values from a sorted set
    """
    num = 50
    a = SortedSet(range(num))
    assert len(a) == num
    assert len(a._list) == num

    a.remove(0)
    assert len(a) == num - 1
    assert len(a._list) == num - 1

    with pytest.raises(KeyError):
        a.remove(0)


def test_sortedset_difference_single_iterable():
    """
    Test the set difference implementation with a single iterable.
    """
    a_test = set(A)
    c_test = a_test.difference(B)

    a = SortedSet(A)
    c = a.difference(B)

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A))
    assert c is not a


def test_sortedset_difference_multiple_iterable():
    """
    Test the set difference implementation with a multiple iterables.
    """
    a_test = set(A)
    c_test = a_test.difference(B, D)

    a = SortedSet(A)
    c = a.difference(B, D)

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A))
    assert c is not a


def test_sortedset_difference_generator():
    """
    Test the set difference implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.difference(B)

    a = SortedSet(A)
    c = a.difference(b_generator())

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A))
    assert c is not a


def test_sortedset_difference_update_single_iterable():
    """
    Test the set difference update implementation with a single iterable.
    """
    a_test = set(A)
    a_test.difference_update(B)

    a = SortedSet(A)
    a.difference_update(B)

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A))


def test_sortedset_difference_update_multiple_iterable():
    """
    Test the set difference update implementation with multiple iterables.
    """
    a_test = set(A)
    a_test.difference_update(B, D)

    a = SortedSet(A)
    a.difference_update(B, D)

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A))


def test_sortedset_difference_update_generator():
    """
    Test the set difference update implementation with a generator.
    """
    a_test = set(A)
    a_test.difference_update(B)

    a = SortedSet(A)
    a.difference_update(b_generator())

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A))


def test_sortedset_intersection_single_iterable():
    """
    Test the set intersection implementation with a single iterable.
    """
    a_test = set(A)
    c_test = a_test.intersection(B)

    a = SortedSet(A)
    c = a.intersection(B)

    assert c == c_test
    assert c._list == list(filter(lambda x: x in B, A))
    assert c is not a


def test_sortedset_intersection_multiple_iterable():
    """
    Test the set intersection implementation with multiple iterables.
    """
    a_test = set(A)
    c_test = a_test.intersection(B, D)

    a = SortedSet(A)
    c = a.intersection(B, D)

    assert c == c_test
    assert not c._list
    assert c is not a


def test_sortedset_intersection_generator():
    """
    Test the set intersection implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.intersection(B)

    a = SortedSet(A)
    c = a.intersection(b_generator())

    assert c == c_test
    assert c._list == list(filter(lambda x: x in B, A))
    assert c is not a


def test_sortedset_intersection_update_single_iterable():
    """
    Test the set intersection update implementation with a single iterable.
    """
    a_test = set(A)
    a_test.intersection_update(B)

    a = SortedSet(A)
    a.intersection_update(B)

    assert a == a_test
    assert a._list == list(filter(lambda x: x in B, A))


def test_sortedset_intersection_update_multiple_iterable():
    """
    Test the set intersection update implementation with multiple iterables.
    """
    a_test = set(A)
    a_test.intersection_update(B, D)

    a = SortedSet(A)
    a.intersection_update(B, D)

    assert a == a_test
    assert not a._list


def test_sortedset_intersection_update_generator():
    """
    Test the set intersection update implementation with a generator.
    """
    a_test = set(A)
    a_test.intersection_update(B)

    a = SortedSet(A)
    a.intersection_update(b_generator())

    assert a == a_test
    assert a._list == list(filter(lambda x: x in B, A))


def test_sortedset_symmetric_difference():
    """
    Test the set symmetric difference implementation with a standard iterable.
    """
    a_test = set(A)
    c_test = a_test.symmetric_difference(B)

    a = SortedSet(A)
    c = a.symmetric_difference(B)

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    )
    assert c is not a


def test_sortedset_symmetric_difference_generator():
    """
    Test the set symmetric difference implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.symmetric_difference(B)

    a = SortedSet(A)
    c = a.symmetric_difference(b_generator())

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    )
    assert c is not a


def test_sortedset_symmetric_difference_update():
    """
    Test the set symmetric difference update implementation with a standard iterable.
    """
    a_test = set(A)
    a_test.symmetric_difference_update(B)

    a = SortedSet(A)
    a.symmetric_difference_update(B)

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    )


def test_sortedset_symmetric_difference_update_generator():
    """
    Test the set symmetric difference implementation with a generator.
    """
    a_test = set(A)
    a_test.symmetric_difference_update(B)

    a = SortedSet(A)
    a.symmetric_difference_update(b_generator())

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    )


def test_sortedset_union_single_iterable():
    """
    Test the set intersection implementation with a single iterable.
    """
    a_test = set(A)
    c_test = a_test.union(B)

    a = SortedSet(A)
    c = a.union(B)

    assert c == c_test
    assert c._list == C
    assert c is not a


def test_sortedset_union_multiple_iterable():
    """
    Test the set intersection implementation with multiple iterables.
    """
    a_test = set(A)
    c_test = a_test.union(B, D)

    a = SortedSet(A)
    c = a.union(B, D)

    assert c == c_test
    assert c._list == E
    assert c is not a


def test_sortedset_union_generator():
    """
    Test the set intersection implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.union(B)

    a = SortedSet(A)
    c = a.union(b_generator())

    assert c == c_test
    assert c._list == C
    assert c is not a


def test_sortedset_update_single_iterable():
    """
    Test the set intersection update implementation with a single iterable.
    """
    a_test = set(A)
    a_test.update(B)

    a = SortedSet(A)
    a.update(B)

    assert a == a_test
    assert a._list == C


def test_sortedset_update_multiple_iterable():
    """
    Test the set intersection update implementation with multiple iterables.
    """
    a_test = set(A)
    a_test.update(B, D)

    a = SortedSet(A)
    a.update(B, D)

    assert a == a_test
    assert a._list == E


def test_sortedset_update_generator():
    """
    Test the set intersection update implementation with a generator.
    """
    a_test = set(A)
    a_test.update(B)

    a = SortedSet(A)
    a.update(b_generator())

    assert a == a_test
    assert a._list == C


def test_sortedset_pop():
    """
    Test popping a value from a sorted set
    """
    num = 50
    a = SortedSet(range(num))

    assert len(a) == num
    assert len(a._list) == num

    # Setup popping value at end of set
    val = a[-1]
    assert a[-1] is val
    assert a.pop() == val

    # Verify pop
    assert a[-1] is not val
    assert len(a) == num - 1
    assert len(a._list) == num - 1
    assert val not in a
    assert val not in a._list

    # Setup popping value in middle of set
    val = a[10]
    assert a[10] is val
    assert a.pop(10) == val

    # Verify pop
    assert a[10] is not val
    assert len(a) == num - 2
    assert len(a._list) == num - 2
    assert val not in a
    assert val not in a._list

    # Attempt to pop value outside of index
    with pytest.raises(IndexError):
        a.pop(49)


def test_sortedset_get_view():
    """
    Test getting the sorted set's view
    """
    a = SortedSet()
    b = a.get_view()
    assert b._set is a


def test_sortedset_get_list():
    """
    Test getting the sorted set's view
    """
    vals = list(range(50))
    a = SortedSet(vals)
    b = a.get_list()

    assert b == vals
    assert b is not vals

    assert b == a._list
    assert b is not a._list


def test_sortedset_iter():
    """
    Test iterating over the sorted set
    """
    vals = list(range(50))
    a = SortedSet(vals)

    for i, j in enumerate(a):
        assert j == vals[i]

    inv_vals = list(reversed(vals))
    for i, j in enumerate(reversed(a)):
        assert j == inv_vals[i]


def test_sortedset_sort():
    """
    Test sorting the sorting set
    """

    class _Temp:
        count = itertools.count()

        def __init__(self):
            self.int = next(self.count)

    vals = [_Temp() for _ in range(50)]
    a = SortedSet(reversed(vals))

    assert a[0].int == 49
    assert a[-1].int == 0

    a.sort(key=lambda x: x.int)

    assert a[0].int == 0
    assert a[-1].int == 49


def test_sortedset_operator_difference():
    """
    Test using the operator for difference
    """
    a_test = SortedSet(A)
    c_test = a_test.difference(SortedSet(B))

    a = SortedSet(A)
    c = a - SortedSet(B)

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A))


def test_sortedset_operator_difference_update():
    """
    Test using the operator for difference update
    """
    a_test = SortedSet(A)
    a_test.difference_update(SortedSet(B))

    a = SortedSet(A)
    a -= SortedSet(B)

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A))


def test_sortedset_operator_intersection():
    """
    Test using the operator for intersection
    """
    a_test = SortedSet(A)
    c_test = a_test.intersection(SortedSet(B))

    a = SortedSet(A)
    c = a & SortedSet(B)

    assert c == c_test
    assert c._list == list(filter(lambda x: x in B, A))


def test_sortedset_operator_intersection_update():
    """
    Test using the operator for intersection update
    """
    a_test = SortedSet(A)
    a_test.intersection_update(SortedSet(B))

    a = SortedSet(A)
    a &= SortedSet(B)

    assert a == a_test
    assert a._list == list(filter(lambda x: x in B, A))


def test_sortedset_operator_symmetric_difference():
    """
    Test using the operator for symmetric difference
    """
    a_test = SortedSet(A)
    c_test = a_test.symmetric_difference(SortedSet(B))

    a = SortedSet(A)
    c = a ^ SortedSet(B)

    assert c == c_test
    assert c._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    )


def test_sortedset_operator_symmetric_difference_update():
    """
    Test using the operator for symmetric difference update
    """
    a_test = set(A)
    a_test.symmetric_difference_update(SortedSet(B))

    a = SortedSet(A)
    a ^= SortedSet(B)

    assert a == a_test
    assert a._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    )


def test_sortedset_operator_union():
    """
    Test using the operator for union
    """
    a_test = SortedSet(A)
    c_test = a_test.union(SortedSet(B))

    a = SortedSet(A)
    c = a | SortedSet(B)

    assert c == c_test
    assert c._list == C


def test_sortedset_operator_update():
    """
    Test using the operator for updates
    """
    a_test = set(A)
    a_test.update(B)

    a = SortedSet(A)
    a |= SortedSet(B)

    assert a == a_test
    assert a._list == C


def test_sortedset_pickle():
    """
    Test pickling a sorted set
    """
    a = SortedSet(range(50))
    pickled = pickle.dumps(a)
    b = pickle.loads(pickled)

    assert a is not b
    assert a == b


def test_sortedset_comparsion():
    """
    Test the sorted set basic comparsions
    """
    a = SortedSet()
    b = SortedSet()

    assert a == b

    a.add(1)
    assert a != b

    b.add(1)
    assert a == b

    a.add(2)
    a.add(3)

    b.add(3)
    b.add(2)

    assert a != b
    assert a == {1, 2, 3}
    assert b == {1, 2, 3}
    assert a != [1, 2, 3]
    assert b != [1, 3, 2]


def test_sortedset_hash():
    """
    Test using the sorted sets hash method
    """
    a = SortedSet()
    b = SortedSet()
    assert a is not b
    set_ = {a, b}
    assert len(set_) == 2


def test_sortedsetview_dunder():
    """
    Test using the sorted set view's base dunder methods
    """
    num = 50
    vals = list(range(num))
    a = SortedSet(vals)
    view1 = a.get_view()

    assert len(view1) == num
    assert 0 in view1
    assert 100 not in view1

    assert list(view1) == vals
    assert view1[-1] == vals[-1]
    assert view1[0] == vals[0]
    assert view1[0] != vals[-1]


def test_sortedsetview_comparsion():
    """
    Test using the sorted set view's comparsion operators
    """
    num = 50
    vals = list(range(num))

    a = SortedSet(vals)
    view1 = a.get_view()
    view2 = a.get_view()

    assert view1 is not view2
    assert view1 == view2

    assert view1 == set(vals)
    assert view1 == list(vals)
    assert view1 == tuple(vals)
    assert not view1 == 0

    vals.pop()
    c = SortedSet(vals)
    view3 = c.get_view()

    assert view1 is not view3
    assert view1 != view3
    assert view1 != set(vals)
    assert view1 != list(vals)
    assert view1 != tuple(vals)
    assert view1 != 0


def test_sortedsetview_hash():
    """
    Test using the sorted sets hash method
    """
    set_ = SortedSet()
    a = set_.get_view()
    b = set_.get_view()
    assert a is not b
    set_ = {a, b}
    assert len(set_) == 2
