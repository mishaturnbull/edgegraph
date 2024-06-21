#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for UnDirectedEdge assocations with their vertices.
"""

from edgegraph.structure import vertex, undirectededge


def test_undiredge_assoc_on_init():
    """
    Test UnDirectedEdge accepts vertices through init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = undirectededge.UnDirectedEdge(v1, v2)

    assert e.vertices == (
        v1,
        v2,
    ), "UnDirectedEdge did not associate links from __init__!"

    assert v1.links == (e,), "UnDirectedEdge did not bind to vertex in __init__!"
    assert v2.links == (e,), "UnDirectedEdge did not bind to vertex in __init__!"


def test_undiredge_assoc_postinit():
    """
    Test UnDirectedEdge can still associate with links post-init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = undirectededge.UnDirectedEdge()

    assert e.vertices == (
        None,
        None,
    ), "UnDirectedEdge associated with vertices in __init__??"

    e.v1 = v1

    assert e.vertices == (v1, None), "UnDirectedEdge did not associate v1 postinit!"
    assert v1.links == (e,), "UnDIrectedEdge did not bind vertex link!"
    assert v2.links == tuple(), "What the actual hell happened here"

    e.v2 = v2

    assert e.vertices == (v1, v2), "UnDirectedEdge did not associate v2 postinit!"
    assert v1.links == (e,), "UnDirectedEdge v2-set altered v1 links!"
    assert v2.links == (e,), "UnDIrectedEdge v2-set did not bind v2 links!"


def test_undiredge_assoc_update_v1():
    """
    Test UnDirectedEdge can change v1 after association in init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    v3 = vertex.Vertex()
    e = undirectededge.UnDirectedEdge(v1, v2)

    assert e.vertices == (
        v1,
        v2,
    ), "UnDirEdge did not start with right vertices from __init__!"

    e.v1 = v3

    assert e.vertices == (v3, v2), "UnDirEdge did not set v1 correctly!"
    assert v1.links == tuple(), "UnDirEdge v1-set did not remove links from old v1!"
    assert v2.links == (e,), "UnDirEdge v1-set altered v2 links!"
    assert v3.links == (e,), "UnDirEdge v1-set did not bind to new v1!"


def test_undiredge_assoc_update_v2():
    """
    Test UnDirectedEdge can change v2 after association in init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    v3 = vertex.Vertex()
    e = undirectededge.UnDirectedEdge(v1, v2)

    assert e.vertices == (
        v1,
        v2,
    ), "UnDirEdge did not start with right vertices from __init__!"

    e.v2 = v3

    assert e.vertices == (v1, v3), "UnDirEdge did not set v2 correctly!"
    assert v1.links == (e,), "UnDirEdge v2-set altered v1 links!"
    assert v2.links == tuple(), "UnDirEdge v2-set did not remove links from old v2!"
    assert v3.links == (e,), "UnDirEdge v2-set did not bind to new v2!"
