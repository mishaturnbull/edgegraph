"""
Unit tests for structure.collections.sortedset module.
"""

import itertools
import pickle
import random
from threading import RLock

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
    assert isinstance(set_, set), "sorted set inited incorrectly?"
    assert len(set_) == num, "set was not inited to the right length"
    assert set_._list, "list was empty"
    assert len(set_._list) == num, "list was not inited to the right length"
    assert set_._list == a, "list did not init to the expected sequence"
    assert list(set_) == a, "sorted set did not cast to the expected sequence"


def test_sortedset_init_generator():
    """
    Ensure we can initalize a sorted set from a generator and order
    is maintained.
    """
    num = 10
    a = list(range(num))
    gen = (i for i in a)

    set_ = SortedSet(gen)
    assert isinstance(set_, set), "sorted set inited incorrectly?"
    assert len(set_) == num, "set was not inited to the right length"
    assert set_._list, "list was empty"
    assert len(set_._list) == num, "list was not inited to the right length"
    assert set_._list == a, "list did not init to the expected sequence"
    assert list(set_) == a, "sorted set did not cast to the expected sequence"


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
    assert isinstance(set_, set), "sorted set inited incorrectly?"
    assert len(set_) == half, "set was not inited to the right length"
    assert set_._list, "list was empty"
    assert len(set_._list) == half, "list was not inited to the right length"
    assert set_._list == a, "list did not init to the expected sequence"
    assert list(set_) == a, "sorted set did not cast to the expected sequence"


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
    assert len(a) == 0, "set was not empty"
    assert len(a._list) == 0, "list was not empty"

    a.add(val)

    assert len(a) == 1, "incorrect number of values in set"
    assert len(a._list) == 1, "incorrect number of values in list"
    assert a[0] == 1, "incorrect value at index"


def test_sortedset_duplicated_add():
    """
    Test adding a value already contained in a sorted set
    """
    val = 1

    a = SortedSet((1,))
    assert len(a) == 1, "incorrect number of values in set"
    assert len(a._list) == 1, "incorrect number of values in list"
    assert a[0] == val, "incorrect value at index"

    a.add(val)

    assert len(a) == 1, "incorrect number of values in set"
    assert len(a._list) == 1, "incorrect number of values in set"
    assert a[0] == val, "incorrect value at index"


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

    assert a._list == vals, "underlying list was in incorrect sequence"
    assert list(a) == vals, "sorted set did not cast to the expected sequence"


def test_sortedset_clear():
    """
    Test clearing all data in the sorted set
    """
    num = 50
    a = SortedSet(range(num))
    assert len(a) == num, "sorted set inited to with incorrect length"
    assert len(a._list) == num, "list of sorted set inited to incorrect length"

    a.clear()
    assert len(a) == 0, "length of sorted set was not zero"
    assert len(a._list) == 0, "length of underlying list was not zero"


def test_sortedset_discard():
    """
    Test discarding values from a sorted set
    """
    num = 50
    a = SortedSet(range(num))
    assert len(a) == num, "sorted set inited to with incorrect length"
    assert len(a._list) == num, "list of sorted set inited to incorrect length"

    # Test removing a value in the sorted set
    a.discard(0)
    assert len(a) == num - 1, "sorted set did not decrease in length"
    assert len(a._list) == num - 1, "list did not decrease in length"

    # Test discarding a value that doesn't exist in the sorted set
    a.discard(0)
    assert len(a) == num - 1, "sorted set should not have decreased in length"
    assert len(a._list) == num - 1, "list should not have decreased in length"


def test_sortedset_remove():
    """
    Test removing values from a sorted set
    """
    num = 50
    a = SortedSet(range(num))
    assert len(a) == num, "sorted set inited to with incorrect length"
    assert len(a._list) == num, "list did not decrease in length"

    a.remove(0)
    assert len(a) == num - 1, "sorted set did not decrease in length"
    assert len(a._list) == num - 1, "list did not decrease in length"

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

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x not in B, A)), (
        "failed to get expected sorted list from operation"
    )
    assert c is not a, "failed to create a new set"


def test_sortedset_difference_multiple_iterable():
    """
    Test the set difference implementation with a multiple iterables.
    """
    a_test = set(A)
    c_test = a_test.difference(B, D)

    a = SortedSet(A)
    c = a.difference(B, D)

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x not in B, A)), (
        "failed to get expected sorted list from operation"
    )
    assert c is not a, "failed to create a new set"


def test_sortedset_difference_generator():
    """
    Test the set difference implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.difference(B)

    a = SortedSet(A)
    c = a.difference(b_generator())

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x not in B, A)), (
        "failed to get expected sorted list from operation"
    )
    assert c is not a, "failed to create a new set"


def test_sortedset_difference_update_single_iterable():
    """
    Test the set difference update implementation with a single iterable.
    """
    a_test = set(A)
    a_test.difference_update(B)

    a = SortedSet(A)
    a.difference_update(B)

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x not in B, A)), (
        "failed to get expected sorted list from operation"
    )


def test_sortedset_difference_update_multiple_iterable():
    """
    Test the set difference update implementation with multiple iterables.
    """
    a_test = set(A)
    a_test.difference_update(B, D)

    a = SortedSet(A)
    a.difference_update(B, D)

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x not in B, A))


def test_sortedset_difference_update_generator():
    """
    Test the set difference update implementation with a generator.
    """
    a_test = set(A)
    a_test.difference_update(B)

    a = SortedSet(A)
    a.difference_update(b_generator())

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x not in B, A)), (
        "failed to get expected sorted list from operation"
    )


def test_sortedset_intersection_single_iterable():
    """
    Test the set intersection implementation with a single iterable.
    """
    a_test = set(A)
    c_test = a_test.intersection(B)

    a = SortedSet(A)
    c = a.intersection(B)

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x in B, A)), (
        "failed to get expected sorted list from operation"
    )
    assert c is not a, "failed to create a new set"


def test_sortedset_intersection_multiple_iterable():
    """
    Test the set intersection implementation with multiple iterables.
    """
    a_test = set(A)
    c_test = a_test.intersection(B, D)

    a = SortedSet(A)
    c = a.intersection(B, D)

    assert c == c_test, "failed to get expected set from operation"
    assert not c._list
    assert c is not a, "failed to create a new set"


def test_sortedset_intersection_generator():
    """
    Test the set intersection implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.intersection(B)

    a = SortedSet(A)
    c = a.intersection(b_generator())

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x in B, A)), (
        "failed to get expected sorted list from operation"
    )
    assert c is not a, "failed to create a new set"


def test_sortedset_intersection_update_single_iterable():
    """
    Test the set intersection update implementation with a single iterable.
    """
    a_test = set(A)
    a_test.intersection_update(B)

    a = SortedSet(A)
    a.intersection_update(B)

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x in B, A)), (
        "failed to get expected sorted list from operation"
    )


def test_sortedset_intersection_update_multiple_iterable():
    """
    Test the set intersection update implementation with multiple iterables.
    """
    a_test = set(A)
    a_test.intersection_update(B, D)

    a = SortedSet(A)
    a.intersection_update(B, D)

    assert a == a_test, "failed to get expected set from operation"
    assert not a._list, "failed to create a new set"


def test_sortedset_intersection_update_generator():
    """
    Test the set intersection update implementation with a generator.
    """
    a_test = set(A)
    a_test.intersection_update(B)

    a = SortedSet(A)
    a.intersection_update(b_generator())

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x in B, A)), (
        "failed to get expected sorted list from operation"
    )


def test_sortedset_symmetric_difference():
    """
    Test the set symmetric difference implementation with a standard iterable.
    """
    a_test = set(A)
    c_test = a_test.symmetric_difference(B)

    a = SortedSet(A)
    c = a.symmetric_difference(B)

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B)
    ), "failed to get expected sorted list from operation"
    assert c is not a, "failed to create a new set"


def test_sortedset_symmetric_difference_generator():
    """
    Test the set symmetric difference implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.symmetric_difference(B)

    a = SortedSet(A)
    c = a.symmetric_difference(b_generator())

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B),
    ), "failed to get expected sorted list from operation"
    assert c is not a, "failed to create a new set"


def test_sortedset_symmetric_difference_update():
    """
    Test the set symmetric difference update implementation with a standard iterable.
    """
    a_test = set(A)
    a_test.symmetric_difference_update(B)

    a = SortedSet(A)
    a.symmetric_difference_update(B)

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B),
    ), "failed to get expected sorted list from operation"


def test_sortedset_symmetric_difference_update_generator():
    """
    Test the set symmetric difference implementation with a generator.
    """
    a_test = set(A)
    a_test.symmetric_difference_update(B)

    a = SortedSet(A)
    a.symmetric_difference_update(b_generator())

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == list(filter(lambda x: x not in B, A)) + list(
        filter(lambda x: x not in A, B),
    ), "failed to get expected sorted list from operation"


def test_sortedset_union_single_iterable():
    """
    Test the set intersection implementation with a single iterable.
    """
    a_test = set(A)
    c_test = a_test.union(B)

    a = SortedSet(A)
    c = a.union(B)

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == C, "failed to get expected sorted list from operation"
    assert c is not a, "failed to create a new set"


def test_sortedset_union_multiple_iterable():
    """
    Test the set intersection implementation with multiple iterables.
    """
    a_test = set(A)
    c_test = a_test.union(B, D)

    a = SortedSet(A)
    c = a.union(B, D)

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == E, "failed to get expected sorted list from operation"
    assert c is not a, "failed to create a new set"


def test_sortedset_union_generator():
    """
    Test the set intersection implementation with a generator.
    """
    a_test = set(A)
    c_test = a_test.union(B)

    a = SortedSet(A)
    c = a.union(b_generator())

    assert c == c_test, "failed to get expected set from operation"
    assert c._list == C, "failed to get expected sorted list from operation"
    assert c is not a, "failed to create a new set"


def test_sortedset_update_single_iterable():
    """
    Test the set intersection update implementation with a single iterable.
    """
    a_test = set(A)
    a_test.update(B)

    a = SortedSet(A)
    a.update(B)

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == C, "failed to get expected sorted list from operation"


def test_sortedset_update_multiple_iterable():
    """
    Test the set intersection update implementation with multiple iterables.
    """
    a_test = set(A)
    a_test.update(B, D)

    a = SortedSet(A)
    a.update(B, D)

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == E, "failed to get expected sorted list from operation"


def test_sortedset_update_generator():
    """
    Test the set intersection update implementation with a generator.
    """
    a_test = set(A)
    a_test.update(B)

    a = SortedSet(A)
    a.update(b_generator())

    assert a == a_test, "failed to get expected set from operation"
    assert a._list == C, "failed to get expected sorted list from operation"


def test_sortedset_pop():
    """
    Test popping a value from a sorted set
    """
    num = 50
    a = SortedSet(range(num))

    assert len(a) == num, "set did not init to correct size"
    assert len(a._list) == num, "list did not init to the correct size"

    # Setup popping value at end of set
    val = a[-1]
    assert a[-1] is val, "unexpected value at last index"
    assert a.pop() is val, "popped unexpected value"

    # Verify pop
    assert a[-1] is not val, "value at last index was unchanged"
    assert len(a) == num - 1, "size of set did not change"
    assert len(a._list) == num - 1, "size of list did not change"
    assert val not in a, "value remained in set after popping"
    assert val not in a._list, "value remained in list after popping"

    # Setup popping value in middle of set
    val = a[10]
    assert a[10] is val, "unexpected value at index 10"
    assert a.pop(10) is val, "popped unexpected value"

    # Verify pop
    assert a[10] is not val, "value at index 10 was unchanged"
    assert len(a) == num - 2, "size of set did not change"
    assert len(a._list) == num - 2, "size of list did not change"
    assert val not in a, "value remained in set after popping"
    assert val not in a._list, "value remained in list after popping"

    # Attempt to pop value outside of index
    with pytest.raises(IndexError):
        a.pop(49)


def test_sortedset_get_view():
    """
    Test getting the sorted set's view
    """
    a = SortedSet()
    b = a.get_view(RLock())
    assert b._set is a, "view is of wrong object"


def test_sortedset_get_list():
    """
    Test getting the sorted set's view
    """
    vals = list(range(50))
    a = SortedSet(vals)
    b = a.get_list()

    assert b is not vals, "b is the same object as vals"
    assert b == vals, "list of objects in sorted set does not match"

    assert b is not a._list, "b is the same object as the set's list"
    assert b == a._list, "b does not match a's list"


def test_sortedset_iter():
    """
    Test iterating over the sorted set
    """
    vals = list(range(50))
    a = SortedSet(vals)

    for i, j in enumerate(a):
        assert j == vals[i], "non-matching value in iterable"

    inv_vals = list(reversed(vals))
    for i, j in enumerate(reversed(a)):
        assert j == inv_vals[i], "non-matching value in reversed iterable"


def test_sortedset_sort():
    """
    Test sorting the sorting set
    """

    class _Temp:
        count = itertools.count()

        def __init__(self):
            self.val = next(self.count)

    vals = [_Temp() for _ in range(50)]
    a = SortedSet(reversed(vals))

    assert a[0].val == 49, "unexpected value at first index in set"
    assert a[-1].val == 0, "unexpected value at last index in set"

    a.sort(key=lambda x: x.val)

    assert a[0].val == 0, "unexpected value at first index in set after sort"
    assert a[-1].val == 49, "unexpected value at last index in set after sort"


def test_sortedset_operator_difference():
    """
    Test using the operator for difference
    """
    a_test = SortedSet(A)
    c_test = a_test.difference(SortedSet(B))

    a = SortedSet(A)
    c = a - SortedSet(B)

    assert c == c_test, "set with operator did not match set without operator"
    assert c._list == c_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_difference_update():
    """
    Test using the operator for difference update
    """
    a_test = SortedSet(A)
    a_test.difference_update(SortedSet(B))

    a = SortedSet(A)
    a -= SortedSet(B)

    assert a == a_test, "set with operator did not match set without operator"
    assert a._list == a_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_intersection():
    """
    Test using the operator for intersection
    """
    a_test = SortedSet(A)
    c_test = a_test.intersection(SortedSet(B))

    a = SortedSet(A)
    c = a & SortedSet(B)

    assert c == c_test, "set with operator did not match set without operator"
    assert c._list == c_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_intersection_update():
    """
    Test using the operator for intersection update
    """
    a_test = SortedSet(A)
    a_test.intersection_update(SortedSet(B))

    a = SortedSet(A)
    a &= SortedSet(B)

    assert a == a_test, "set with operator did not match set without operator"
    assert a._list == a_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_symmetric_difference():
    """
    Test using the operator for symmetric difference
    """
    a_test = SortedSet(A)
    c_test = a_test.symmetric_difference(SortedSet(B))

    a = SortedSet(A)
    c = a ^ SortedSet(B)

    assert c == c_test, "set with operator did not match set without operator"
    assert c._list == c_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_symmetric_difference_update():
    """
    Test using the operator for symmetric difference update
    """
    a_test = SortedSet(A)
    a_test.symmetric_difference_update(SortedSet(B))

    a = SortedSet(A)
    a ^= SortedSet(B)

    assert a == a_test, "set with operator did not match set without operator"
    assert a._list == a_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_union():
    """
    Test using the operator for union
    """
    a_test = SortedSet(A)
    c_test = a_test.union(SortedSet(B))

    a = SortedSet(A)
    c = a | SortedSet(B)

    assert c == c_test, "set with operator did not match set without operator"
    assert c._list == c_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_operator_update():
    """
    Test using the operator for updates
    """
    a_test = SortedSet(A)
    a_test.update(B)

    a = SortedSet(A)
    a |= SortedSet(B)

    assert a == a_test, "set with operator did not match set without operator"
    assert a._list == a_test._list, (
        "list with operator did not match list without operator"
    )


def test_sortedset_pickle():
    """
    Test pickling a sorted set
    """
    a = SortedSet(range(50))
    pickled = pickle.dumps(a)
    b = pickle.loads(pickled)  # noqa: S301

    assert a is not b, "a and b were the same object"
    assert a == b, "a and b were not equivalent"


def test_sortedset_comparsion():
    """
    Test the sorted set basic comparsions
    """
    a = SortedSet()
    b = SortedSet()

    assert a == b, "empty sets were not equal"

    a.add(1)
    assert a != b, "empty sets were equal"

    b.add(1)
    assert a == b, "sets should be equal with adding values in same order"

    a.add(2)
    a.add(3)

    b.add(3)
    b.add(2)

    assert a != b, (
        "a and b should not be equal with values added in different orders"
    )
    assert a == {1, 2, 3}, "a's set was not equal to the expected set"
    assert b == {1, 2, 3}, "b's set was not equal to the expected set"
    assert a != [1, 2, 3], (
        "a should be not equal to a list with equivalent ordering"
    )
    assert b != [1, 3, 2], (
        "b should be not equal to a list with equivalent ordering"
    )


def test_sortedset_hash():
    """
    Test using the sorted sets hash method
    """
    a = SortedSet()
    b = SortedSet()
    assert a == b, "a was not equivalent to b"
    assert hash(a) != hash(b), (
        "equivalent mutable objects should have different hashes"
    )


def test_sortedsetview_dunder():
    """
    Test using the sorted set view's base dunder methods
    """
    num = 50
    vals = list(range(num))
    a = SortedSet(vals)
    view1 = a.get_view(RLock())

    assert len(view1) == num, "length of view was not equal to the set's length"
    assert 0 in view1, "value in set not in view"
    assert 100 not in view1, "value not in set is in view"
    assert view1 == a, "view's values not equivalent to set"

    assert list(view1) == vals, "casted view not equivalent to expected values"
    assert view1[-1] == vals[-1], (
        "last index of view not equal to expected value"
    )
    assert view1[0] == vals[0], (
        "first index of view not equal to expected value"
    )


def test_sortedsetview_comparsion():
    """
    Test using the sorted set view's comparsion operators
    """
    num = 50
    vals = list(range(num))

    a = SortedSet(vals)
    b = SortedSet(vals)
    lock = RLock()
    view1 = a.get_view(lock)
    view2 = a.get_view(lock)
    view3 = b.get_view(RLock())

    assert view1 is not view2, "views are not different objects"
    assert view1 == view2, "views are not equivalent"
    assert not view1 != view2, "views are not equivalent"  # noqa: SIM202

    assert view1 == set(vals), (
        "view was not equivlent to set of expected values"
    )
    assert view1 == list(vals), (
        "view was not equivlent to list of expected values"
    )
    assert view1 == tuple(vals), (
        "view was not equivlent to tuple of expected values"
    )
    assert not view1 == 0, "view is not equivlent to non supported comparsion"  # noqa: SIM201

    assert view1 is not view3, "views are not different objects"
    assert view1 == view3, "views are not equivalent"

    vals.pop()
    c = SortedSet(vals)
    view4 = c.get_view(RLock())

    assert view1 is not view4, "views are not different objects"
    assert view1 != view4, "views are equivalent"
    assert view1 != set(vals), "view was equivlent to set of expected values"
    assert view1 != list(vals), "view was equivlent to list of expected values"
    assert view1 != tuple(vals), (
        "view was equivlent to tuple of expected values"
    )
    assert view1 != 0, "view is equivlent to non supported comparsion"


def test_sortedsetview_hash():
    """
    Test using the sorted sets hash method
    """
    set_ = SortedSet()
    lock = RLock()
    a = set_.get_view(lock)
    b = set_.get_view(lock)
    assert a == b, "a was not equivalent to b"
    assert hash(a) != hash(b), (
        "equivalent mutable objects should have different hashes"
    )
