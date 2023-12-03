#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.base module.
"""

import pytest
from edgegraph.structure import base

def test_base_obj_creation():
    bo = base.BaseObject()

    assert len(dir(bo)) == 0, "baseobject init'd with attributes!"

def test_base_obj_attributes():
    bo = base.BaseObject()

    bo.x = 7
    bo.y = 15
    bo.z = "Twelve"

    assert bo.x == 7
    assert bo.y == 15
    assert bo.z == "Twelve"

    assert bo._attributes == {
            'x': 7,
            'y': 15,
            'z': "Twelve"
            }

def test_base_obj_init_attributes():
    bo = base.BaseObject(
            attributes={"fifteen": 15, "twelve": 12}
            )

    assert bo.fifteen == 15
    assert bo.twelve == 12

    assert bo._attributes == {
            "fifteen": 15,
            "twelve": 12,
            }

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

def test_base_obj_uid():
    bo = base.BaseObject()

    assert 'uid' not in bo._attributes
    assert '_uid' not in bo._attributes
    assert bo.uid is bo._uid

    with pytest.raises(NotImplementedError):
        bo.uid = 15

    assert bo.uid != 15
    assert bo._uid != 15

def test_base_obj_universes():
    bo = base.BaseObject()

    assert 'universe' not in bo._attributes
    assert '_universe' not in bo._attributes
    assert bo.universes == bo._universes

    uni = object()
    bo.add_to_universe(uni)

    assert uni in bo.universes
    assert uni in bo._universes

    bo.remove_from_universe(uni)

    assert uni not in bo.universes
    assert uni not in bo._universes

    with pytest.raises(KeyError):
        bo.remove_from_universe(uni)

def test_base_obj_init_universes_list():
    unis = [object(), object(), object()]

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis
    assert len(bo.universes) == len(unis)
    assert isinstance(bo.universes, frozenset)

def test_base_obj_init_universes_set():
    unis = set([object(), object(), object()])

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis
    assert len(bo.universes) == len(unis)
    assert isinstance(bo.universes, frozenset)

def test_base_obj_init_universes_tuple():
    unis = (object(), object(), object())

    bo = base.BaseObject(universes=unis)

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis
    assert len(bo.universes) == len(unis)
    assert isinstance(bo.universes, frozenset)

def test_base_obj_init_universes_generator():
    unis = [object(), object(), object()]

    def gen():
        for u in unis:
            yield u
    bo = base.BaseObject(universes=gen())

    # sets are unordered, can't just compare to a list
    for obj in bo.universes:
        assert obj in unis
    assert len(bo.universes) == len(unis)
    assert isinstance(bo.universes, frozenset)

def test_base_obj_init_universes_deduplicate():
    obj = object()
    unis = [obj] * 50

    bo = base.BaseObject(universes=unis)

    assert len(bo.universes) == 1

