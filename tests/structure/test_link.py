#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.link.Link class.
"""

import pytest
from edgegraph.structure import base, vertex, universe, link

def test_link_subclass():
    assert issubclass(link.Link, base.BaseObject), "Link has wrong superclass!"

    l = link.Link(
            uid=-100,
            attributes={"fifteen": 15},
            _force_creation=True,
            )

    assert l.uid == -100
    assert l.fifteen == 15

def test_link_error_on_create():
    with pytest.raises(TypeError):
        link.Link()

def test_link_subclass_does_not_err():
    class LinkSubClass(link.Link):
        pass

    # we only need to make sure there's no errors here, not check for anything
    # specific
    LinkSubClass()
    LinkSubClass(_force_creation=True)
    LinkSubClass(_force_creation=False)

def test_link_creation():
    l = link.Link(_force_creation=True)

    assert len(l.vertices) == 0, "Link init'd with vertices!"
    assert len(dir(l)) == 0, "Link init'd with attributes!"

def test_link_creation_vertices():
    verts = [vertex.Vertex(), vertex.Vertex()]

    l = link.Link(vertices=verts, _force_creation=True)

    assert l._vertices == verts, "Link init'd with wrong vertices!"
    assert l.vertices == tuple(verts), "Link init'd with wrong vertices!"

def test_link_creation_vertices_set():
    verts = {vertex.Vertex(), vertex.Vertex()}

    l = link.Link(vertices=verts, _force_creation=True)

    for vert in verts:
        assert vert in l.vertices, "Link init'd with missing vertex!"
    assert len(l.vertices) == len(verts), \
            "Link init'd with wrong num of vertices!"
    assert isinstance(l._vertices, list), "Link init did not conv vertices!"
    assert isinstance(l.vertices, tuple), "Link .vertices returned wrong type!"

