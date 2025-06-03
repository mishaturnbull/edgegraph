#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for DirectedEdge assocations with their vertices.
"""

from edgegraph.structure import vertex, directededge


def test_diredge_assoc_on_init():
    """
    Test DirectedEdge can associate with vertices in init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = directededge.DirectedEdge(v1, v2)

    assert e.vertices == (
        v1,
        v2,
    ), "DirectedEdge did not associate links from __init__!"

    assert v1.links == (e,), "DirectedEdge did not bind to vertex in __init__!"
    assert v2.links == (e,), "DirectedEdge did not bind to vertex in __init__!"


def test_diredge_assoc_postinit():
    """
    Test DirectedEdge can associate with vertices after init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = directededge.DirectedEdge()

    assert e.vertices == (
        None,
        None,
    ), "DirectedEdge associated with vertices in __init__??"

    e.v1 = v1

    assert e.vertices == (
        v1,
        None,
    ), "DirectedEdge did not associate v1 postinit!"
    assert v1.links == (e,), "DIrectedEdge did not bind vertex link!"
    assert v2.links == tuple(), "What the actual hell happened here"

    e.v2 = v2

    assert e.vertices == (v1, v2), "DirectedEdge did not associate v2 postinit!"
    assert v1.links == (e,), "DirectedEdge v2-set altered v1 links!"
    assert v2.links == (e,), "DIrectedEdge v2-set did not bind v2 links!"


def test_diredge_assoc_update_v1():
    """
    Test that DirectedEdge can change v1 after assigned in init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    v3 = vertex.Vertex()
    e = directededge.DirectedEdge(v1, v2)

    assert e.vertices == (
        v1,
        v2,
    ), "DirEdge did not start with right vertices from __init__!"

    e.v1 = v3

    assert e.vertices == (v3, v2), "DirEdge did not set v1 correctly!"
    assert v1.links == tuple(), (
        "DirEdge v1-set did not remove links from old v1!"
    )
    assert v2.links == (e,), "DirEdge v1-set altered v2 links!"
    assert v3.links == (e,), "DirEdge v1-set did not bind to new v1!"


def test_diredge_assoc_update_v2():
    """
    Test that DirectedEdge can change v2 after assigned in init.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    v3 = vertex.Vertex()
    e = directededge.DirectedEdge(v1, v2)

    assert e.vertices == (
        v1,
        v2,
    ), "DirEdge did not start with right vertices from __init__!"

    e.v2 = v3

    assert e.vertices == (v1, v3), "DirEdge did not set v2 correctly!"
    assert v1.links == (e,), "DirEdge v2-set altered v1 links!"
    assert v2.links == tuple(), (
        "DirEdge v2-set did not remove links from old v2!"
    )
    assert v3.links == (e,), "DirEdge v2-set did not bind to new v2!"
