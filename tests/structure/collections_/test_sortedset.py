"""
Unit tests for structure.collections.sortedset module.
"""

import pytest

from edgegraph.structure.collections_.sortedset import SortedSet


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
    Ensure we can't initalize from a non-iterable object
    """
    a = 1
    with pytest.raises(TypeError):
        SortedSet(a)
