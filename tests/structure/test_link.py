#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.link.Link class.
"""

import pytest
from edgegraph.structure import base, vertex, link

# W0611 is unused-import.  The entire objective of these tests is to ensure we
# can import the objects; their usage is tested elsewhere.
# W0212 is protected-access, or, access to a protected member (starting with a
# _) of a client class.  In this case, the test objectives require we inspect
# internal state of the objects, so we need to read these attributes.
# pylint: disable=W0611, W0212

def test_link_subclass():
    """
    Ensure Link object trees to correct superclass.
    """
    assert issubclass(link.Link, base.BaseObject), "Link has wrong superclass!"

    l = link.Link(
            uid=-100,
            attributes={"fifteen": 15},
            _force_creation=True,
            )

    assert l.uid == -100
    assert l.fifteen == 15

def test_link_error_on_create():
    """
    Ensure we cannot directly create a link instance.
    """
    with pytest.raises(TypeError):
        link.Link()

def test_link_subclass_does_not_err():
    """
    Ensure subclasses of links can be created directly.
    """
    class LinkSubClass(link.Link):
        '''Subclass of link for testing purposes.'''

    # we only need to make sure there's no errors here, not check for anything
    # specific
    LinkSubClass()
    LinkSubClass(_force_creation=True)
    LinkSubClass(_force_creation=False)

def test_link_creation():
    """
    Ensure that links can be forced into existence and do not spawn in any
    attributes.
    """
    l = link.Link(_force_creation=True)

    assert len(l.vertices) == 0, "Link init'd with vertices!"
    assert len(dir(l)) == 0, "Link init'd with attributes!"

def test_link_creation_vertices():
    """
    Ensure links can contain vertices passed to it in a list.
    """
    verts = [vertex.Vertex(), vertex.Vertex()]

    l = link.Link(vertices=verts, _force_creation=True)

    assert l._vertices == verts, "Link init'd with wrong vertices!"
    assert l.vertices == tuple(verts), "Link init'd with wrong vertices!"

def test_link_creation_vertices_set():
    """
    Ensure links can contain vertices passed to it in a set.
    """
    verts = {vertex.Vertex(), vertex.Vertex()}

    l = link.Link(vertices=verts, _force_creation=True)

    for vert in verts:
        assert vert in l.vertices, "Link init'd with missing vertex!"
    assert len(l.vertices) == len(verts), \
            "Link init'd with wrong num of vertices!"
    assert isinstance(l._vertices, list), "Link init did not conv vertices!"
    assert isinstance(l.vertices, tuple), "Link .vertices returned wrong type!"

