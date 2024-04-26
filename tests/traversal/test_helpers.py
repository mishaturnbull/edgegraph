#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.twoendedlink.TwoEndedLink class.
"""

import pytest
from edgegraph.structure import (Vertex, TwoEndedLink, DirectedEdge,
        UnDirectedEdge)
from edgegraph.traversal import helpers
from edgegraph.builder import adjlist

# C1803 is use-implicit-booleaness-not-comparison
# however, the caes it wants to correct in here are like ``assert nb == []``,
# which, in the context of the text, expresses intent much more clearly than
# ``assert not nb``.  so, shut up!
# pylint: disable=C1803

def test_neighbors_undirected():
    """
    Ensure the neighbors function works with undirected edges.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
            v[0]: [v[1], v[2], v[3]],
        }
    nb = helpers.neighbors(v[0])
    assert nb == [], "neighbors before linking!"

    adjlist.load_adj_dict(adj, UnDirectedEdge)

    nb = helpers.neighbors(v[0])
    assert nb == [v[1], v[2], v[3]], "neighbors returned wrong!"

def test_neighbors_directed():
    """
    Ensure neighbors function is sensitive to direction of edges.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
            v[0]: [v[1]],
            v[1]: [v[2]],
        }
    adjlist.load_adj_dict(adj, DirectedEdge)

    v0nb = helpers.neighbors(v[0], direction_sensitive=True)
    v1nb = helpers.neighbors(v[1], direction_sensitive=True)

    assert v0nb == [v[1]], "v0 neighbors incorrect!"
    assert v1nb == [v[2]], "v1 neighbors incorrect!"

def test_neighbors_directed_nonsensitive():
    """
    Ensure neighbors function direction sensitivity can be turned off.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
            v[0]: [v[1]],
            v[1]: [v[2]],
        }
    adjlist.load_adj_dict(adj, DirectedEdge)

    v0nb = helpers.neighbors(v[0], direction_sensitive=False)
    v1nb = helpers.neighbors(v[1], direction_sensitive=False)

    assert v0nb == [v[1]], "v0 neighbors incorrect!"
    assert v1nb == [v[0], v[2]], "v1 neighbors incorrect!"

def test_neighbors_unknown_link_type():
    """
    Ensure neighbors function handles unknown edge types as the caller desires.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
            v[0]: [v[1]],
            v[1]: [v[2]],
        }
    adjlist.load_adj_dict(adj, TwoEndedLink)

    with pytest.raises(NotImplementedError):
        helpers.neighbors(v[0], direction_sensitive=True,
                unknown_handling=helpers.LNK_UNKNOWN_ERROR)

    v0nb1 = helpers.neighbors(v[0], direction_sensitive=True,
            unknown_handling=helpers.LNK_UNKNOWN_NEIGHBOR)
    v0nb2 = helpers.neighbors(v[0], direction_sensitive=True,
            unknown_handling=helpers.LNK_UNKNOWN_NONNEIGHBOR)

    assert v0nb1 == [v[1]], "LNK_UNKNOWN_NEIGHBOR behavior wrong!"
    assert v0nb2 == [], "LNK_UNKNOWN_NONNEIGHBOR behavior wrong!"

