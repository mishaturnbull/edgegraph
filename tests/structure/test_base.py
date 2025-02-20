#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.base module.
"""

import pytest
from edgegraph.structure import base, universe

# W0212 is protected-access, or, access to a protected member (starting with a
# _) of a client class.  In this case, the test objectives require we inspect
# internal state of the objects, so we need to read these attributes.
# pylint: disable=W0212


def test_base_obj_creation():
    """
    Ensure we can create base objects with no attributes.
    """
    bo = base.BaseObject()
    assert isinstance(bo, base.BaseObject), "baseobject init'd wrong??"


def test_base_obj_attributes():
    """
    Ensure we can assign attributes to an instance of BaseObject using the dot
    access.
    """
    bo = base.BaseObject()

    bo.x = 7
    bo.y = 15
    bo.z = "Twelve"

    assert bo.x == 7, "bo.x did not getattr!"
    assert bo.y == 15, "bo.y did not getattr!"
    assert bo.z == "Twelve", "bo.z did not getattr!"

    assert {
        "x": 7,
        "y": 15,
        "z": "Twelve",
    }.items() <= vars(
        bo
    ).items(), "BaseObject attributes were not stored correctly!"


def test_base_obj_items():
    """
    Ensure we can assign attributes to an instance of BaseObject using the item
    access method.
    """
    bo = base.BaseObject()

    bo["x"] = 7
    bo["y"] = 15
    bo["z"] = "Twelve"

    assert bo["x"] == 7, "bo['x'] did get getitem!"
    assert bo["y"] == 15, "bo['y'] did not getitem!"
    assert bo["z"] == "Twelve", "bo['z'] did not getitem!"

    assert {
        "x": 7,
        "y": 15,
        "z": "Twelve",
    }.items() <= vars(
        bo
    ).items(), "BaseObject attributes were not stored correctly!"


def test_base_obj_item_attr_interop():
    """
    Ensure attributes can be set and retrieved from both dot and getitem
    approaches.
    """
    bo = base.BaseObject()

    bo.a = 9
    bo.b = -123
    bo.c = "Fourteen"
    bo["x"] = 7
    bo["y"] = 15
    bo["z"] = "Twelve"

    assert bo["a"] == 9, "bo['a'] did not getitem!"
    assert bo["b"] == -123, "bo['b'] did not getitem!"
    assert bo["c"] == "Fourteen", "bo['c'] did not getitem!"
    assert bo.x == 7, "bo.x did not getattr!"
    assert bo.y == 15, "bo.y did not getattr!"
    assert bo.z == "Twelve", "bo.z did not getattr!"


def test_base_obj_getitem_protected():
    """
    Ensure access to the masked attributes is forwarded to getattr.
    """
    bo = base.BaseObject()
    bo["a"] = 15

    assert bo["a"] == 15, "bo['a'] did not getitem!"
    assert {"a": 15}.items() <= vars(
        bo
    ).items(), "bo getitem did not forward to getattr!"


def test_base_obj_init_attributes():
    """
    Ensure attributes passed to the instantiation are retained.
    """
    bo = base.BaseObject(attributes={"fifteen": 15, "twelve": 12})

    assert bo.fifteen == 15, "bo attributes not read from __init__"
    assert bo.twelve == 12, "bo attributes not read from __init__"

    assert {
        "fifteen": 15,
        "twelve": 12,
    }.items() <= vars(bo).items(), "bo attriutes not read from __init__"


def test_base_obj_init_attributes_wrong():
    """
    Ensure the correct error is raised when handing invalid objects to the
    attributes during instantiation.
    """
    with pytest.raises(TypeError):
        base.BaseObject(attributes="A string should not be valid!")

    with pytest.raises(TypeError):
        base.BaseObject(attributes=["Nor", "should", "a", "list"])

    with pytest.raises(TypeError):
        base.BaseObject(attributes=123456789)


def test_base_obj_del_attr():
    """
    Ensure we can delete attributes of base objects.
    """
    b = base.BaseObject()
    b.x = 12
    b.y = 15
    del b.x

    assert {"y": 15}.items() <= vars(
        b
    ).items(), "bo delattr removed other (assigned post-init)"
    assert not (
        {"x": 12}.items() <= vars(b).items()
    ), "bo delattr didn't (assigned post-init)"

    b1 = base.BaseObject(attributes={"z": 25, "a": 1})
    del b1.z

    assert {"a": 1}.items() <= vars(
        b1
    ).items(), "bo delattr removed other (assigned in init)"
    assert not (
        {"z": 25}.items() <= vars(b1).items()
    ), "bo delattr didn't (assigned in init)"


def test_base_obj_del_item():
    """
    Ensure we can delete items from base objects.
    """
    b = base.BaseObject()
    b.x = 12
    b.y = 15
    del b["x"]

    assert {"y": 15}.items() <= vars(
        b
    ).items(), "bo delitem removed other (assigned post-init)"
    assert not (
        {"x": 12}.items() <= vars(b).items()
    ), "bo delitem didn't remove (assigned post-init)"

    b1 = base.BaseObject(attributes={"z": 25, "a": 1})
    del b1["z"]

    assert {"a": 1}.items() <= vars(
        b1
    ).items(), "bo delitem removed other (assigned in init)"
    assert not (
        {"z": 25}.items() <= vars(b1).items()
    ), "bo delitem didn't remove (assigned in init)"


def test_base_obj_universes():
    """
    Ensure the universes attribute is not exposed.
    """
    bo = base.BaseObject()
    uni = universe.Universe()
    bo.add_to_universe(uni)

    assert uni in bo.universes, "add_to_universe didn't!"
    assert uni in bo._universes, "add_to_universe didn't!"

    bo.remove_from_universe(uni)

    assert uni not in bo.universes, "remove_from_universe didn't!"
    assert uni not in bo._universes, "remove_from_universe didn't!"

    # should fail, as the universe has already been removed.  when trying to
    # remove an object from a list that does not contain it, you get a
    # ValueError
    with pytest.raises(ValueError):
        bo.remove_from_universe(uni)


def test_base_obj_init_universes_list():
    """
    Ensure we can instantiate a BaseObject with universes given as a list.
    """
    unis = []
    for _ in range(3):
        unis.append(universe.Universe())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(
        unis
    ), "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, list), ".universes gave wrong type"


def test_base_obj_init_universes_set():
    """
    Ensure we can instantiate a BaseObject with universes given as a set.
    """
    unis = set()
    for _ in range(3):
        unis.add(universe.Universe())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(
        unis
    ), "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, list), ".universes gave wrong type"


def test_base_obj_init_universes_tuple():
    """
    Ensure we can instantiate a BaseObject with universes given as a tuple.
    """
    unis = (universe.Universe(), universe.Universe(), universe.Universe())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(
        unis
    ), "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, list), ".universes gave wrong type"


def test_base_obj_init_universes_generator():
    """
    Ensure we can instantiate a BaseObject with universes given as a genexpr.
    """
    unis = []
    for _ in range(3):
        unis.append(universe.Universe())

    def gen():
        yield from unis

    bo = base.BaseObject(universes=gen())

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(
        unis
    ), "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, list), ".universes gave wrong type"


def test_base_obj_init_universes_deduplicate():
    """
    Ensure universes passed to the instantiator are deduplicated.
    """
    uni = universe.Universe()
    unis = [uni] * 50

    bo = base.BaseObject(universes=unis)

    assert len(bo.universes) == 1, "duplicate universes got through __init__"
