#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.directededge.DirectedEdge class.
"""

import pytest
from edgegraph.structure import base, vertex, universe, link, directededge

def test_diedge_subclass():
    assert issubclass(directededge.DirectedEdge, link.Link), \
            "DirectedEdge has wrong superclass!"

    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = directededge.DirectedEdge(v1, v2, uid=-100, attributes={'fifteen': 15})

    assert e.vertices == (v1, v2), "DirectedEdge did not pass vertices to super!"
    assert e.uid == -100, "DirectedEdge did not pass UID to super!"
    assert e.fifteen == 15, "DirectedEdge did not pass attributes to super!"

def test_diedge_init_vertices():
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = directededge.DirectedEdge(v1, v2)

    assert e.v1 is v1, "DirectedEdge did not store v1!"
    assert e.v2 is v2, "DirectedEdge did not store v2!"

    f = directededge.DirectedEdge()

    assert f.v1 is None, "DirectedEdge did not accept v1=None!"
    assert f.v2 is None, "DirectedEdge did not accept v2=None!"

def test_diedge_init_vertices_wrong():
    # hand it the vertex type itself -- type(Vertex) should be `type`
    with pytest.raises(TypeError):
        directededge.DirectedEdge(v1=vertex.Vertex)

    with pytest.raises(TypeError):
        directededge.DirectedEdge(v2=vertex.Vertex)

