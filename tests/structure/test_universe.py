#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for Universe object.
"""

import pytest
from edgegraph.structure import base, vertex, universe

def test_universe_subclass():
    assert issubclass(universe.Universe, vertex.Vertex), \
            "Universe has wrong superclass!"

    u = universe.Universe(
            uid=-100,
            attributes={"thirteen": 13},
            )

    assert u.uid == -100, \
            "Universe UID was not taken from __init__"
    assert u.thirteen == 13, \
            "Universe attributes were not taken from __init__"

def test_universe_vertex_add():
    u = universe.Universe()
    vs = []
    for i in range(5):
        vs.append(vertex.Vertex(attributes={i: i}))
    
    u.add_vertex(vs[0])
    u.add_vertex(vs[1])
    u.add_vertex(vs[0])

    assert isinstance(u.vertices, frozenset), \
            f"universe.vertices gave wrong type {type(u.vertices)}"

    assert len(u.vertices) == 2, \
            "universe.vertices did not deduplicate vertices"
    assert vs[0] in u.vertices, \
            "universe.add_vertex did not take vs[0]"
    assert vs[1] in u.vertices, \
            "universe.add_vertex did not take vs[1]"

    assert u in vs[0].universes, \
            "universes.add_vertex did not set u in vertex.universes"
    assert u in vs[1].universes, \
            "universes.add_vertex did not set u in vertex.universes"

def test_universe_vertex_init():
    vs = []
    for i in range(100):
        vs.append(vertex.Vertex())

    u = universe.Universe(vertices=vs)

    assert isinstance(u.vertices, frozenset), \
            "universe.vertices gave wrong type"
    assert len(u.vertices) == 100, \
            "wrong number of objects in universe.vertices (from __init__)"
    for v in vs:
        assert u in v.universes, \
                "universe(vertices=...) did not back-ref to vertices.universes"

def test_universe_laws_updating():
    l1 = universe.UniverseLaws(cycles=True)
    l2 = universe.UniverseLaws(cycles=False)

    assert l1.applies_to is None, \
            "UniverseLaws __init__'d with a non-None applies_to"
    assert l2.applies_to is None, \
            "UniverseLaws __init__'d with a non-None applies_to"

    u = universe.Universe(laws=l1)
    assert u.laws is l1, \
            "universe did not accept laws from __init__"
    assert l1.applies_to is u, \
            "universe laws in __init__ did not set applies_to"
    assert u.laws.cycles is True, \
            "universe laws did not apply laws"

    u.laws = l2

    assert u.laws is l2, \
            "switching universe laws did not update universe reference"
    assert l1.applies_to is None, \
            "switching universe laws did not un-apply old set"
    assert l2.applies_to is u, \
            "switching universe laws did not apply new set"
    assert u.laws.cycles is False, \
            "switching universe laws did not change the laws"


