#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.vertex.Vertex class.
"""

from edgegraph.structure import base, vertex, universe, link

# W0212 is protected-access, or, access to a protected member (starting with a
# _) of a client class.  In this case, the test objectives require we inspect
# internal state of the objects, so we need to read these attributes.
# pylint: disable=W0212

def test_vertex_subclass():
    """
    Ensure Vertex trees up to correct subclass and attributes are operating
    correctly.
    """
    assert issubclass(vertex.Vertex, base.BaseObject)

    unis = [universe.Universe(), universe.Universe()]

    v = vertex.Vertex(
            uid=-100,
            attributes={"fifteen": 15},
            universes=unis,
            )

    assert v.uid == -100
    assert v.fifteen == 15
    assert unis[0] in v.universes
    assert unis[1] in v.universes
    assert len(v.universes) == 2
    assert dir(v) == ['fifteen']

def test_vertex_creation():
    """
    Ensure we can create Vertices with default options.
    """
    v = vertex.Vertex()

    assert len(v.links) == 0, "vertex init'd with links!!"
    assert len(dir(v)) == 0, "vertex init'd with attributes!!"

def test_vertex_create_with_links():
    """
    Ensure we can create vertices with base Link objects in a list.
    """
    links = []
    for _ in range(3):
        links.append(link.Link(_force_creation=True))

    v1 = vertex.Vertex(links=links)
    assert v1._links == links, "vertex did not accept list of links!"
    assert v1.links == tuple(links), "vertex did not return tuple of links!"

def test_vertex_create_with_links_set():
    """
    Ensure we can create vertices with base Link objects in a set.
    """
    links = set()
    for _ in range(3):
        links.add(link.Link(_force_creation=True))

    v2 = vertex.Vertex(links=links)
    # sets are unordered, can't just compare to a list
    for obj in v2.links:
        assert obj in links, "found unexpected linkin vertex links!"
    assert len(v2.links) == len(links), "vertex links is not expected length!"
    assert isinstance(v2.links, tuple), "vertex links is not correct type!"

def test_vertex_create_with_tuple():
    """
    Ensure we can create vertices with base Link objects in a tuple.
    """
    links = []
    for _ in range(3):
        links.append(link.Link(_force_creation=True))
    links = tuple(links)

    v3 = vertex.Vertex(links=links)
    assert v3.links == links, "vertex .links did not equal expected!"
    assert isinstance(v3.links, tuple), "vertex links is not correct type!"

def test_vertex_create_with_generator():
    """
    Ensure we can create vertices with base Link objects in a genexpr.
    """
    links = []
    for _ in range(3):
        links.append(link.Link(_force_creation=True))

    def gen():
        for l in links:
            yield l
    v4 = vertex.Vertex(links=gen())
    assert v4.links == tuple(links), "vertex .links did not equal expected!"
    assert isinstance(v4.links, tuple), "vertex links is not correct type!"

def test_vert_add_to_uni():
    """
    Ensure we can add a Vertex to multiple universes.
    """
    v = vertex.Vertex()

    unis = []
    for _ in range(50):
        unis.append(universe.Universe())
        v.add_to_universe(unis[-1])

    assert len(v.universes) == 50, "vertex .universes has wrong # elements!"
    for uni in unis:
        assert v in uni.vertices, "vertex add_to_universe did not back-ref!"

