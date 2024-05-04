#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.twoendedlink.TwoEndedLink class.
"""

from edgegraph.structure import Vertex, DirectedEdge, UnDirectedEdge
from edgegraph.builder import adjlist

def test_adjlist_edgetype():
    """
    Ensure the adjacency list builder respects edge types.
    """
    vs = [Vertex(), Vertex(), Vertex()]
    adj = {
            vs[0]: [vs[1]],
            vs[1]: [vs[2]],
        }

    adjlist.load_adj_dict(adj, DirectedEdge)

    l0to1 = vs[0].links[0]
    l1to2 = vs[2].links[0]

    assert isinstance(l0to1, DirectedEdge), \
            "load_adj_dict used wrong edge type!"
    assert isinstance(l1to2, DirectedEdge), \
            "load_adj_dict used wrong edge type!"

def test_adjlist_build_clrs09_22_1():
    """
    This graph is taken from [CLRS09]_, figure 22.1.

    .. uml::

       object v0
       object v1
       object v2
       object v3
       object v4

       v0 -- v1
       v0 -- v4
       v1 -- v2
       v1 -- v3
       v1 -- v4
       v2 -- v3
       v3 -- v4
    """
    v = []
    for _ in range(5):
        v.append(Vertex())

    adj = {
        v[0]: [v[1], v[4]],
        v[1]: [v[2], v[3], v[4]],
        v[2]: [v[3]],
        v[3]: [v[4]],
        v[4]: [],
        }

    uni = adjlist.load_adj_dict(adj, UnDirectedEdge)

    # this test needs to be independent of the traversal / inspection logic, so
    # we'll have to check each link individually

    assert len(uni.vertices) == 5, "load_adj_list made wrong # of verts!"

    # v0 links
    assert len(v[0].links) == 2, "v0 has wrong # of links!"
    assert v[0].links[0].other(v[0]) is v[1], \
            "v0 -- v1 link is not right!"
    assert v[0].links[1].other(v[0]) is v[4], \
            "v0 -- v4 link is not right!"

    # v1 links
    assert len(v[1].links) == 4, "v1 has wrong # of links!"
    assert v[1].links[0].other(v[1]) is v[0], \
            "v1 -- v0 (back) link is not right!"
    assert v[1].links[1].other(v[1]) is v[2], \
            "v1 -- v2 link is not right!"
    assert v[1].links[2].other(v[1]) is v[3], \
            "v1 -- v3 link is not right!"
    assert v[1].links[3].other(v[1]) is v[4], \
            "v1 -- v4 link is not right!"

    # v2 links
    assert len(v[2].links) == 2, "v2 has wrong # of links!"
    assert v[2].links[0].other(v[2]) is v[1], \
            "v2 -- v1 (back) link is not right!"
    assert v[2].links[1].other(v[2]) is v[3], \
            "v2 -- v3 link is not right!"

    # v3 links
    assert len(v[3].links) == 3, "v3 has wrong # of links!"
    assert v[3].links[0].other(v[3]) is v[1], \
            "v3 -- v1 (back) link is not right!"
    assert v[3].links[1].other(v[3]) is v[2], \
            "v3 -- v2 (back) link is not right!"
    assert v[3].links[2].other(v[3]) is v[4], \
            "v3 -- v4 link is not right!"

    # v4 links
    assert len(v[4].links) == 3, "v4 has wrong # of links!"
    assert v[4].links[0].other(v[4]) is v[0], \
            "v4 -- v0 (back) link is not right!"
    assert v[4].links[1].other(v[4]) is v[1], \
            "v4 -- v1 (back) link is not right!"
    assert v[4].links[2].other(v[4]) is v[3], \
            "v4 -- v3 (back) link is not right!"

