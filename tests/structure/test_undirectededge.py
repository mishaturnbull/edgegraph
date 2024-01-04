#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.link.Link class.
"""

import pytest
from edgegraph.structure import base, vertex, universe, link, undirectededge

def test_undiedge_subclass():
    assert issubclass(undirectededge.UnDirectedEdge, link.Link), \
            "UnDirectedEdge has wrong superclass!"

    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = undirectededge.UnDirectedEdge(v1, v2, uid=-100, attributes={'fifteen': 15})

    assert e.vertices == (v1, v2), "UnDirectedEdge did not pass vertices to super!"
    assert e.uid == -100, "UnDirectedEdge did not pass UID to super!"
    assert e.fifteen == 15, "UnDirectedEdge did not pass attributes to super!"

def test_undiedge_init_vertices():
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = undirectededge.UnDirectedEdge(v1, v2)

    assert e.v1 is v1, "UnDirectedEdge did not store v1!"
    assert e.v2 is v2, "UnDirectedEdge did not store v2!"

    f = undirectededge.UnDirectedEdge()

    assert f.v1 is None, "UnDirectedEdge did not accept v1=None!"
    assert f.v2 is None, "UnDirectedEdge did not accept v2=None!"

def test_undiedge_init_vertices_wrong():
    with pytest.raises(TypeError):
        undirectededge.UnDirectedEdge(object(), vertex.Vertex())

    with pytest.raises(TypeError):
        undirectededge.UnDirectedEdge(vertex.Vertex(), object())

    with pytest.raises(TypeError):
        undirectededge.UnDirectedEdge(object(), object())

