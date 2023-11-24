#!/usr/bin/python3
# -*- boding: utf-8 -*-

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

def test_base_obj_uid():
    bo = base.BaseObject()

    assert bo.uid is bo._uid

    with pytest.raises(NotImplementedError):
        bo.uid = 15

    assert bo.uid != 15
    assert bo._uid != 15
    assert 'uid' not in bo._attributes
    assert '_uid' not in bo._attributes

def test_base_obj_universe():
    bo = base.BaseObject()

    assert bo.universe is bo._universe

    uni = object()
    bo.universe = uni

    assert bo.universe is uni
    assert bo._universe is uni
    assert 'universe' not in bo._attributes
    assert '_universe' not in bo._attributes

