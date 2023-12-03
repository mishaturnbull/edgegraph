#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.vertex.Vertex class.
"""

import pytest
from edgegraph.structure import base, vertex

def test_vertex_subclass():
    assert issubclass(vertex.Vertex, base.BaseObject)

    v = vertex.Vertex(
            uid=-100,
            attributes={"fifteen": 15},
            universes={object(), object()},
            )

    assert v.uid == -100
    assert v.fifteen == 15
    assert len(v.universes) == 2

def test_vertex_creation():
    v = vertex.Vertex()

    assert len(v.links) == 0, "vertex init'd with links!!"
    assert len(dir(v)) == 0, "vertex init'd with attributes!!"

def test_vertex_create_with_links():
    links = [object(), object(), object()]

    v1 = vertex.Vertex(links=links)
    assert v1.links is links

def test_vertex_create_with_links_set():
    links = set([object(), object(), object()])

    v2 = vertex.Vertex(links=links)
    # sets are unordered, can't just compare to a list
    for obj in v2.links:
        assert obj in links
    assert len(v2.links) == len(links)
    assert isinstance(v2.links, list)

def test_vertex_create_with_tuple():
    links = (object(), object(), object())

    v3 = vertex.Vertex(links=links)
    assert v3.links == list(links)
    assert isinstance(v3.links, list)

def test_vertex_create_with_generator():
    links = [object(), object(), object()]

    def gen():
        for l in links:
            yield l
    v4 = vertex.Vertex(links=gen())
    assert v4.links == links
    assert isinstance(v4.links, list)

