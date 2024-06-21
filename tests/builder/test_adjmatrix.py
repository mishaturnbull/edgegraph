#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.twoendedlink.TwoEndedLink class.
"""

import pytest
from edgegraph.structure import Vertex, UnDirectedEdge
from edgegraph.builder import adjmatrix


def test_adjmatrix_edgetype():
    """
    Ensure adjmatrix respects user's edge type.
    """
    v = [Vertex(), Vertex(), Vertex()]
    mat = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]

    uni = adjmatrix.load_adj_matrix(mat, v, UnDirectedEdge)

    assert len(uni.vertices) == 3, "load_adj_matrix loaded wrong # of verts!"

    l0to1 = v[0].links[0]
    l1to1 = v[1].links[1]

    assert isinstance(l0to1, UnDirectedEdge), "v0 -- v1 link is wrong class!"
    assert l0to1.vertices == (v[0], v[1]), "v0 -- v1 link is wrong!"
    assert isinstance(l1to1, UnDirectedEdge), "v0 -- v1 link is wrong class!"
    assert l1to1.vertices == (v[1], v[1]), "v1 -- v1 (self) link is wrong!"


def test_adjmatrix_nonsquare():
    """
    Ensure adjmatrix throws an error when the given matrix is not square.
    """
    v = [Vertex(), Vertex(), Vertex()]
    mat = [
        [0, 1, 0],
        [0, 1],
        [0, 1, 0],
    ]

    with pytest.raises(ValueError):
        adjmatrix.load_adj_matrix(mat, v)


def test_adjmatrix_sidelen():
    """
    Ensure adjmatrix throws an error if the vertex array does not match the
    matrix size.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    mat = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]

    with pytest.raises(ValueError):
        adjmatrix.load_adj_matrix(mat, v)


def test_adjmatrix_clrs09_22_2():
    """
    This graph is taken from [CLRS09]_, figure 22.2.

    .. uml::

       object v0
       object v1
       object v2
       object v3
       object v4
       object v5

       v0 --> v2
       v0 --> v3
       v1 --> v4
       v2 --> v4
       v2 --> v5
       v3 --> v1
       v4 --> v4
       v5 --> v5
    """
    v = []
    for _ in range(6):
        v.append(Vertex())

    mat = [
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1],
    ]

    uni = adjmatrix.load_adj_matrix(mat, v)

    assert len(uni.vertices) == 6, "load_adj_mat loaded wrong # of verts!"

    # v0 links
    assert len(v[0].links) == 2, "v0 has wrong # of links!"
    assert v[0].links[0].other(v[0]) is v[1], "v0 -- v1 link is not right!"
    assert v[0].links[1].other(v[0]) is v[3], "v0 -- v3 link is not right!"

    # v1 links
    assert len(v[1].links) == 3, "v1 has wrong # of links"
    assert v[1].links[0].other(v[1]) is v[0], "v1 -- v0 (back) link is not right!"
    assert v[1].links[1].other(v[1]) is v[4], "v1 -- v4 link is not right!"
    assert v[1].links[2].other(v[1]) is v[3], "v1 -- v3 (back) link is not right!"

    # v2 links
    assert len(v[2].links) == 2, "v2 has wrong # of links"
    assert v[2].links[0].other(v[2]) is v[4], "v2 -- v4 link is not right!"
    assert v[2].links[1].other(v[2]) is v[5], "v2 -- v5 link is not right!"

    # v3 links
    assert len(v[3].links) == 3, "v3 has wrong # of links"
    assert v[3].links[0].other(v[3]) is v[0], "v3 -- v0 (back) link is not right!"
    assert v[3].links[1].other(v[3]) is v[1], "v3 -- v1 link is not right!"
    assert v[3].links[2].other(v[3]) is v[4], "v3 -- v4 (back) link is not right!"

    # v4 links
    assert len(v[4].links) == 3, "v4 has wrong # of links!"
    assert v[4].links[0].other(v[4]) is v[1], "v4 -- v1 (back) link is not right!"
    assert v[4].links[1].other(v[4]) is v[2], "v4 -- v2 (back) link is not right!"
    assert v[4].links[2].other(v[4]) is v[3], "v4 -- v3 link is not right!"

    # v5 links
    assert len(v[5].links) == 2, "v5 has wrong # of links!"
    assert v[5].links[0].other(v[5]) is v[2], "v5 -- v2 (back) link is not right!"
    assert v[5].links[1].other(v[5]) is v[5], "v5 -- v5 (self) link is not right!"
