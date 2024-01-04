#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for linking vertices to vertices.
"""

import pytest
from edgegraph.structure import vertex, link

def test_assoc_from_link():
    l = link.Link(_force_creation=True)
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    l.add_vertex(v1)
    l.add_vertex(v2)

    # test private state is correct
    assert l._vertices == [v1, v2], \
            "Link._vertices incorrect after adding 2 vertices!"
    assert l in v1._links, \
            "Link did not bind to specified vertex!"
    assert l in v2._links, \
            "Link did not bind to specified vertex!"

    # test public state is correct
    assert l.vertices == (v1, v2), \
            "Link.vertices incorrect after adding 2 vertices!"
    assert l in v1.links, \
            "Link did not bind to specified vertex!"
    assert l in v2.links, \
            "Link did not bind to specified vertex!"

def test_assoc_from_vert():
    l = link.Link(_force_creation=True)
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    v1.add_to_link(l)
    v2.add_to_link(l)

    # test private state is correct
    assert l._vertices == [v1, v2], \
            "Link._vertices incorrect after being added to two vertices!"
    assert l in v1._links, \
            "Vertex did not bind to specified link!"
    assert l in v2._links, \
            "Vertex did not bind to specified link!"

    # test public state is correct
    assert l.vertices == (v1, v2), \
            "Link.vertices incorrect after being added to two vertices!"
    assert l in v1.links, \
            "Vertex did not bind to specified link!"
    assert l in v2.links, \
            "Vertex did not bind to specified link!"

def test_link_base_class_multivert():
    l = link.Link(_force_creation=True)
    verts = []
    for i in range(100):
        verts.append(vertex.Vertex())
        l.add_vertex(verts[-1])

    assert l._vertices == verts, \
            "Link did not accept large number of vertices!"

    for v in verts:
        assert l in v._links, \
                "Link did not bind to large number of vertices!"

def test_vert_no_dup_links():
    l = link.Link(_force_creation=True)
    v1 = vertex.Vertex()

    v1.add_to_link(l)
    v1.add_to_link(l)

    assert v1.links == (l,), \
            "Vertex accepted a duplicate (``is``) link!"

def test_link_dup_verts():
    l = link.Link(_force_creation=True)
    v1 = vertex.Vertex()

    for i in range(100):
        l.add_vertex(v1)

    assert len(l.vertices) == 100, \
            "Link did not accept duplicate (``is``) vertices!"
    for vert in l.vertices:
        assert vert is v1, \
                "Link did not bind to duplicate (``is``) vertices!"

    assert v1.links == (l,), \
            "Vertex accepted a duplicate (``is``) link!"
    
