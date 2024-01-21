#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.base module.
"""

import pytest
from edgegraph.structure import base, universe

def test_base_obj_creation():
    bo = base.BaseObject()

    assert len(dir(bo)) == 0, "baseobject init'd with attributes!"

def test_base_obj_attributes():
    bo = base.BaseObject()

    bo.x = 7
    bo.y = 15
    bo.z = "Twelve"

    assert bo.x == 7,        "bo.x did not getattr!"
    assert bo.y == 15,       "bo.y did not getattr!"
    assert bo.z == "Twelve", "bo.z did not getattr!"

    assert bo._attributes == {
            'x': 7,
            'y': 15,
            'z': "Twelve"
            }, \
                    "BaseObject attributes were not stored correctly!"

def test_base_obj_items():
    bo = base.BaseObject()

    bo['x'] = 7
    bo['y'] = 15
    bo['z'] = 'Twelve'

    assert bo['x'] == 7,        "bo['x'] did get getitem!"
    assert bo['y'] == 15,       "bo['y'] did not getitem!"
    assert bo['z'] == 'Twelve', "bo['z'] did not getitem!"

    assert bo._attributes == {
            'x': 7,
            'y': 15,
            'z': "Twelve"
            }, \
                    "BaseObject attributes were not stored correctly!"

def test_base_obj_item_attr_interop():
    bo = base.BaseObject()

    bo.a = 9
    bo.b = -123
    bo.c = "Fourteen"
    bo['x'] = 7
    bo['y'] = 15
    bo['z'] = 'Twelve'

    assert bo['a'] == 9,          "bo['a'] did not getitem!"
    assert bo['b'] == -123,       "bo['b'] did not getitem!"
    assert bo['c'] == "Fourteen", "bo['c'] did not getitem!"
    assert bo.x == 7,             "bo.x did not getattr!"
    assert bo.y == 15,            "bo.y did not getattr!"
    assert bo.z == "Twelve",      "bo.z did not getattr!"

def test_base_obj_getitem_protected():
    bo = base.BaseObject()
    bo['a'] = 15

    assert bo['a'] == 15, "bo['a'] did not getitem!"
    assert bo['_attributes'] == {'a': 15}, \
            "bo getitem did not forward to getattr!"

def test_base_obj_setitem_protected():
    bo = base.BaseObject()
    bo['a'] = 15

    assert bo['a'] == 15, "bo['a'] did not getitem!"

    bo['_attributes'] = {'b': 25}

    assert bo._attributes == {'b': 25}, \
            "bo setitem did not forward to setattr!"

def test_base_obj_init_attributes():
    bo = base.BaseObject(
            attributes={"fifteen": 15, "twelve": 12}
            )

    assert bo.fifteen == 15, "bo attributes not read from __init__"
    assert bo.twelve == 12, "bo attributes not read from __init__"

    assert bo._attributes == {
            "fifteen": 15,
            "twelve": 12,
            }, \
                    "bo attriutes not read from __init__"

def test_base_obj_init_attributes_wrong():
    with pytest.raises(TypeError):
        base.BaseObject(
                attributes="A string should not be valid!"
                )

    with pytest.raises(TypeError):
        base.BaseObject(
                attributes=["Nor", "should", "a", "list"]
                )

    with pytest.raises(TypeError):
        base.BaseObject(
                attributes=123456789
                )

def test_base_obj_del_attr():
    b = base.BaseObject()
    b.x = 12
    b.y = 15
    del b.x

    assert b._attributes == {'y': 15}, \
            "bo delattr didn't (assigned post-init)"

    b1 = base.BaseObject(attributes={'z': 25, 'a': 1})
    del b1.z

    assert b1._attributes == {'a': 1}, \
            "bo delattr didn't (assigned in init)"

def test_base_obj_del_item():
    b = base.BaseObject()
    b.x = 12
    b.y = 15
    del b['x']

    assert b._attributes == {'y': 15}, \
            "bo delitem didn't (assigned post-init)"

    b1 = base.BaseObject(attributes={'z': 25, 'a': 1})
    del b1['z']

    assert b1._attributes == {'a': 1}, \
            "bo delitem didn't (assigned in init)"

def test_base_obj_del_item_protected():
    b = base.BaseObject()
    b.x = 12

    with pytest.raises(ValueError):
        del b['_uid']

def test_base_obj_uid():
    bo = base.BaseObject()

    assert 'uid' not in bo._attributes,  "BaseObject UID exposed"
    assert '_uid' not in bo._attributes, "BaseObject _uid exposed"
    assert bo.uid is bo._uid, "BaseObject uid property not returning _uid"

    # UID should be read-only
    with pytest.raises(AttributeError):
        bo.uid = 15

    assert bo.uid != 15, "BaseObject UID was changed!"
    assert bo._uid != 15, "BaseObject _uid was changed!"

def test_base_obj_universes():
    bo = base.BaseObject()

    assert 'universes' not in bo._attributes, "BaseObject universes exposed"
    assert '_universes' not in bo._attributes, "BaseObject _universes exposed"
    assert bo.universes == bo._universes, \
            "BaseObject universes not returning _universes"

    uni = universe.Universe()
    bo.add_to_universe(uni)

    assert uni in bo.universes, "add_to_universe didn't!"
    assert uni in bo._universes, "add_to_universe didn't!"

    bo.remove_from_universe(uni)

    assert uni not in bo.universes, "remove_from_universe didn't!"
    assert uni not in bo._universes, "remove_from_universe didn't!"

    # should fail, as the universe has already been removed.  when trying to
    # remove an object from a set that does not contain it, you get a KeyError
    with pytest.raises(KeyError):
        bo.remove_from_universe(uni)

def test_base_obj_init_universes_list():
    unis = []
    for i in range(3):
        unis.append(universe.Universe())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(unis), \
            "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, frozenset), \
            ".universes gave wrong type"

def test_base_obj_init_universes_set():
    unis = set()
    for i in range(3):
        unis.add(universe.Universe())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(unis), \
            "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, frozenset), \
            ".universes gave wrong type"

def test_base_obj_init_universes_tuple():
    unis = (universe.Universe(), universe.Universe(), universe.Universe())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(unis), \
            "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, frozenset), \
            ".universes gave wrong type"

def test_base_obj_init_universes_generator():
    unis = []
    for i in range(3):
        unis.append(universe.Universe())

    def gen():
        for u in unis:
            yield u
    bo = base.BaseObject(universes=gen())

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis, "found something unexpected in .universes"
    assert len(bo.universes) == len(unis), \
            "universes passed to __init__ is not same len as .universes!"
    assert isinstance(bo.universes, frozenset), \
            ".universes gave wrong type"

def test_base_obj_init_universes_deduplicate():
    uni = universe.Universe()
    unis = [uni] * 50

    bo = base.BaseObject(universes=unis)

    assert len(bo.universes) == 1, "duplicate universes got through __init__"

