#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for linking vertices to vertices.
"""

from edgegraph.structure import vertex, link

# W0212 (protected-access) is about accessing protected members (those starting
# with _) of a client class.  This is performed quite a lot in this test suite,
# as it is necessary to complete test objectives.
# pylint: disable=W0212

def test_assoc_from_link():
    """
    Ensure that adding a vertex to a link also updates link records in the
    vertex object.
    """
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
    """
    Ensure that adding a link to a vertex also updates vertex records in the
    link object.
    """
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
    """
    Ensure the base link class can handle large numbers of vertices.
    """
    l = link.Link(_force_creation=True)
    verts = []
    for _ in range(100):
        verts.append(vertex.Vertex())
        l.add_vertex(verts[-1])

    assert l._vertices == verts, \
            "Link did not accept large number of vertices!"

    for v in verts:
        assert l in v._links, \
                "Link did not bind to large number of vertices!"

def test_vert_no_dup_links():
    """
    Ensure that vertices do not accept the same instance of a link twice.
    """
    l = link.Link(_force_creation=True)
    v1 = vertex.Vertex()

    v1.add_to_link(l)
    v1.add_to_link(l)

    assert v1.links == (l,), \
            "Vertex accepted a duplicate (``is``) link!"

def test_link_dup_verts():
    """
    Ensure that links do accept the same instance of a vertex twice.
    """
    l = link.Link(_force_creation=True)
    v1 = vertex.Vertex()

    for _ in range(100):
        l.add_vertex(v1)

    assert len(l.vertices) == 100, \
            "Link did not accept duplicate (``is``) vertices!"
    for vert in l.vertices:
        assert vert is v1, \
                "Link did not bind to duplicate (``is``) vertices!"

    assert v1.links == (l,), \
            "Vertex accepted a duplicate (``is``) link!"

def test_link_removal_by_vertex():
    """
    Ensure that vertices can remove themselves from links.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    l = link.Link(vertices=[v1, v2], _force_creation=True)

    v1.remove_from_link(l)

    assert v1.links == tuple(), \
            "Vertex remove_from_link did not unassociate link!"
    assert l.vertices == (v2,), \
            "Vertex remove_from_link did not unassociate vertex from link!"

    # test that removing something not present has no action
    v1.remove_from_link(l)

    assert v1.links == tuple(), \
            "Removing link-not-present from vertex readded it??"
    assert l.vertices == (v2,), \
            "Removing link-not-present from vertex reassoc'd it to link??"

def test_link_removal_by_link():
    """
    Ensure links can remove vertices from themselves.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    l = link.Link(vertices=[v1, v2], _force_creation=True)

    l.unlink_from(v1)

    assert v1.links == tuple(), \
            "Link unlink_from did not unassociate link from vertex!"
    assert l.vertices == (v2,), \
            "Link unlink_from did not unassociate link!"

    # test that removing something not present has no action
    l.unlink_from(v1)

    assert v1.links == tuple(), \
            "Removing vertex-not-present from link reassoc'd it to vert??"
    assert l.vertices == (v2,), \
            "Removing vertex-not-present from link readded it??"

