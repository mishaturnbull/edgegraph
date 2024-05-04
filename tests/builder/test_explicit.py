#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.twoendedlink.TwoEndedLink class.
"""

from edgegraph.structure import (Vertex, TwoEndedLink, DirectedEdge,
        UnDirectedEdge)
from edgegraph.builder import explicit

def test_link_basecls():
    """
    Ensure the base class TwoEndedLink is behaving correctly.
    """
    v1 = Vertex()
    v2 = Vertex()

    # make sure the preconditions are as expected
    assert v1.links == tuple(), "v1 had links after __init__??"
    assert v2.links == tuple(), "v2 had links after __init__??"

    # call test func!
    lnk = explicit.link_from_to(v1, TwoEndedLink, v2)

    # check the link is right
    assert isinstance(lnk, TwoEndedLink), "link_from_to made wrong link type!"
    assert lnk.v1 is v1, "link_from_to assigned wrong v1!"
    assert lnk.v2 is v2, "link_from_to assigned wrong v2!"
    assert lnk.vertices == (v1, v2), "lnk has wrong .vertices?"

    # check v1 is right
    assert len(v1.links) == 1, "link_from_to assigned more than 1 link to v1!"
    assert v1.links[0] is lnk, "link_from_to binding to v1 is wrong!"

    # check v2 is right
    assert len(v2.links) == 1, "link_from_to assigned more than 1 link to v2!"
    assert v2.links[0] is lnk, "link_from_to binding to v2 is wrong!"

def test_link_directed():
    """
    Ensure the link_directed() shortcut function creates the right link type.
    """
    v1 = Vertex()
    v2 = Vertex()

    # make sure the preconditions are as expected
    assert v1.links == tuple(), "v1 had links after __init__??"
    assert v2.links == tuple(), "v2 had links after __init__??"

    lnk = explicit.link_directed(v1, v2)

    assert isinstance(lnk, DirectedEdge)

def test_link_undirected():
    """
    Ensure the unlink_directed() shortcut function creates the right link type.
    """
    v1 = Vertex()
    v2 = Vertex()

    # make sure the preconditions are as expected
    assert v1.links == tuple(), "v1 had links after __init__??"
    assert v2.links == tuple(), "v2 had links after __init__??"

    lnk = explicit.link_undirected(v1, v2)

    assert isinstance(lnk, UnDirectedEdge)

def test_link_basecls_chain():
    """
    verts[0] -- verts[1] -- verts[2] -- verts[3]
    """

    verts = [Vertex(), Vertex(), Vertex(), Vertex()]

    l1 = explicit.link_from_to(verts[0], TwoEndedLink, verts[1])

    assert verts[0].links == (l1,), "verts[0] has wrong links"
    assert verts[1].links == (l1,), "verts[1] has wrong links"
    assert verts[2].links == tuple(), "verts[2] has wrong links"
    assert verts[3].links == tuple(), "verts[3] has wrong links"
    assert l1.vertices == (verts[0], verts[1]), "l1 has wrong vertices"

    l2 = explicit.link_from_to(verts[1], TwoEndedLink, verts[2])

    assert verts[0].links == (l1,), "verts[0] has wrong links"
    assert verts[1].links == (l1, l2), "verts[1] has wrong links"
    assert verts[2].links == (l2,), "verts[2] has wrong links"
    assert verts[3].links == tuple(), "verts[3] has wrong links"
    assert l1.vertices == (verts[0], verts[1]), "l1 has wrong vertices"
    assert l2.vertices == (verts[1], verts[2]), "l2 has wrong vertices"

    l3 = explicit.link_from_to(verts[2], TwoEndedLink, verts[3])

    assert verts[0].links == (l1,), "verts[0] has wrong links"
    assert verts[1].links == (l1, l2), "verts[1] has wrong links"
    assert verts[2].links == (l2, l3), "verts[2] has wrong links"
    assert verts[3].links == (l3,), "verts[3] has wrong links"
    assert l1.vertices == (verts[0], verts[1]), "l1 has wrong vertices"
    assert l2.vertices == (verts[1], verts[2]), "l2 has wrong vertices"
    assert l3.vertices == (verts[2], verts[3]), "l3 has wrong vertices"

