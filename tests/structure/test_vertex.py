#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.vertex.Vertex class.
"""

import pytest
from edgegraph.structure import base, vertex, universe, link

def test_vertex_subclass():
    assert issubclass(vertex.Vertex, base.BaseObject)

    unis = [universe.Universe(), universe.Universe()]

    v = vertex.Vertex(
            uid=-100,
            attributes={"fifteen": 15},
            universes=unis,
            )

    assert v.uid == -100
    assert v.fifteen == 15
    assert len(v.universes) == 2
    assert unis[0] in v.universes
    assert unis[1] in v.universes
    assert len(v.universes) == 2

def test_vertex_creation():
    v = vertex.Vertex()

    assert len(v.links) == 0, "vertex init'd with links!!"
    assert len(dir(v)) == 0, "vertex init'd with attributes!!"

def test_vertex_create_with_links():
    links = [link.Link(), link.Link(), link.Link()]

    v1 = vertex.Vertex(links=links)
    assert v1._links is links, "vertex did not accept list of links!"
    assert v1.links == tuple(links), "vertex did not return tuple of links!"

def test_vertex_create_with_links_set():
    links = set([link.Link(), link.Link(), link.Link()])

    v2 = vertex.Vertex(links=links)
    # sets are unordered, can't just compare to a list
    for obj in v2.links:
        assert obj in links, "found unexpected linkin vertex links!"
    assert len(v2.links) == len(links), "vertex links is not expected length!"
    assert isinstance(v2.links, tuple), "vertex links is not correct type!"

def test_vertex_create_with_tuple():
    links = (link.Link(), link.Link(), link.Link())

    v3 = vertex.Vertex(links=links)
    assert v3.links == links, "vertex .links did not equal expected!"
    assert isinstance(v3.links, tuple), "vertex links is not correct type!"

def test_vertex_create_with_generator():
    links = [link.Link(), link.Link(), link.Link()]

    def gen():
        for l in links:
            yield l
    v4 = vertex.Vertex(links=gen())
    assert v4.links == tuple(links), "vertex .links did not equal expected!"
    assert isinstance(v4.links, tuple), "vertex links is not correct type!"

def test_vert_add_to_uni():
    v = vertex.Vertex()

    unis = []
    for i in range(50):
        unis.append(universe.Universe())
        v.add_to_universe(unis[-1])

    assert len(v.universes) == 50, "vertex .universes has wrong # elements!"
    for uni in unis:
        assert v in uni.vertices, "vertex add_to_universe did not back-ref!"

