#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for linking vertices to vertices, specifically created in the
__init__ methods of both classes.
"""

from edgegraph.structure import vertex, link

# W0212 (protected-access) is about accessing protected members (those starting
# with _) of a client class.  This is performed quite a lot in this test suite,
# as it is necessary to complete test objectives.
# pylint: disable=W0212


def test_create_link_with_verts():
    """
    Ensure creating a link with vertex arguments works correctly.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    l = link.Link(vertices=[v1, v2], _force_creation=True)

    assert l.vertices == (v1, v2), "Link did not accept vertices from __init__!"

    assert v1.links == (l,), "Link did not bind to vertex during __init__!"
    assert v2.links == (l,), "Link did not bind to vertex during __init__!"


def test_create_vert_with_links():
    """
    Ensure creating a vertex with link arguments works correctly.
    """
    l1 = link.Link(_force_creation=True)
    l2 = link.Link(_force_creation=True)

    v = vertex.Vertex(links=[l1, l2])

    assert v._links == [l1, l2], "Vertex did not accept links from __init__!"

    assert l1.vertices == (v,), "Vertex did not bind to link during __init__!"
    assert l2.vertices == (v,), "Vertex did not bind to link during __init__!"


def test_create_link_with_vert_then_add():
    """
    Ensure that we can still add vertices to a link after instantiation, and it
    doesn't break anything else.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    v3 = vertex.Vertex()

    l = link.Link(vertices=[v1, v2], _force_creation=True)

    l.add_vertex(v3)

    assert l.vertices == (
        v1,
        v2,
        v3,
    ), "Link did not accept vertices from both __init__ and adding!"
    assert v1.links == (
        l,
    ), "Link (presumably) unbound from vertex after __init__!"
    assert v2.links == (
        l,
    ), "Link (presumably) unbound from vertex after __init__!"
    assert v3.links == (l,), "Link did not bind to vertex after __init__!"


def test_create_vert_with_link_then_add():
    """
    Ensure that we can still add links to a vertex after instantiation, and it
    doesn't break anything else.
    """
    l1 = link.Link(_force_creation=True)
    l2 = link.Link(_force_creation=True)
    l3 = link.Link(_force_creation=True)

    v = vertex.Vertex(links=[l1, l2])

    v.add_to_link(l3)

    assert v.links == (
        l1,
        l2,
        l3,
    ), "Vertex did not accept links from both __init__ and adding!"
    assert l1.vertices == (
        v,
    ), "Vertex (presumably) unbound from link after __init__!"
    assert l2.vertices == (
        v,
    ), "Vertex (presumably) unbound from link after __init__!"
    assert l3.vertices == (v,), "Vertex did not bind to link after __init__!"
