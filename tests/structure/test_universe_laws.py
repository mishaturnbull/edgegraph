#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for UniverseLaws object.
"""

import pytest
from edgegraph.structure import base, universe

# W0212 is protected-access, or, access to a protected member (starting with a
# _) of a client class.  In this case, the test objectives require we inspect
# internal state of the objects, so we need to read these attributes.
# pylint: disable=W0212


def test_uni_laws_inheritance():
    """
    Ensure UniverseLaws trees up to correct subclass.
    """
    assert issubclass(
        universe.UniverseLaws, base.BaseObject
    ), "UniverseLaws has wrong superclass!"


def test_uni_laws_init_defaults():
    """
    Ensure UniverseLaws have sane defaults out of the box.
    """
    l1 = universe.UniverseLaws()
    assert l1._attributes == {
        "_edge_whitelist": None,
        "_mixed_links": False,
        "_cycles": True,
        "_multipath": True,
        "_multiverse": False,
        "_applies_to": None,
    }, "UniverseLaws has wrong default options!"


def test_uni_laws_init_nondefault():
    """
    Ensure UniverseLaws instantiated with non-default options retains them.
    """
    l2 = universe.UniverseLaws(
        edge_whitelist={int: {str: float}},
        mixed_links=True,
        cycles=False,
        multipath=False,
        multiverse=False,
        applies_to=None,
    )
    assert l2._attributes == {
        "_edge_whitelist": {int: {str: float}},
        "_mixed_links": True,
        "_cycles": False,
        "_multipath": False,
        "_multiverse": False,
        "_applies_to": None,
    }, "UniverseLaws did not respect __init__ options!"


def test_uni_laws_attrs():
    """
    Ensure UniverseLaws attribute getters are working.
    """
    l = universe.UniverseLaws(edge_whitelist={int: {str: float}})

    assert (
        l.edge_whitelist == l._attributes["_edge_whitelist"]
    ), "UniverseLaws cannot get edge_whitelist"
    assert (
        l.mixed_links is l._attributes["_mixed_links"]
    ), "UniverseLaws cannot get mixed_links"
    assert l.cycles is l._attributes["_cycles"], "UniverseLaws cannot get cycles"
    assert (
        l.multipath is l._attributes["_multipath"]
    ), "UniverseLaws cannot get multipath"
    assert (
        l.multiverse is l._attributes["_multiverse"]
    ), "UniverseLaws cannot get multiverse"
    assert (
        l.applies_to is l._attributes["_applies_to"]
    ), "UniverseLaws cannot get applies_to"


def test_uni_laws_wrong_edge_rules():
    """
    Ensure invalid edge rules are detected and raise an error.
    """
    bad = [
        {"cat": "dog"},
        [1, 2, 3, 4, 5],
        {"cat": [1, 2, 3, 4, 5]},
    ]

    for wrong in bad:
        with pytest.raises(ValueError):
            universe.UniverseLaws(edge_whitelist=wrong)


def test_uni_laws_attr_readonly():
    """
    Ensure all attributes are readonly, and raise appropriate errors when write
    is attempted.
    """
    l = universe.UniverseLaws(edge_whitelist={int: {str: float}})

    with pytest.raises(AttributeError):
        l.edge_whitelist = l.edge_whitelist

    with pytest.raises(TypeError):
        l.edge_whitelist["dog"] = "cat"

    with pytest.raises(TypeError):
        l.edge_whitelist[int][str] = "cat"

    with pytest.raises(AttributeError):
        l.mixed_links = not l.mixed_links

    with pytest.raises(AttributeError):
        l.cycles = not l.cycles

    with pytest.raises(AttributeError):
        l.multipath = not l.multipath

    with pytest.raises(AttributeError):
        l.multiverse = not l.multiverse

    with pytest.raises(AttributeError):
        l.applies_to = object()
