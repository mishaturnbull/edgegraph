#!python3
# -*- coding: utf-8 -*-

"""
Graphs with heterogenous weights set on all edges.
"""

from __future__ import annotations

import pytest
from edgegraph.structure import Vertex, DirectedEdge, Universe
from edgegraph.builder import explicit

class WeightedDirectedEdge (DirectedEdge):

    def __init__(self, v1=None, v2=None, weight=None, *, uid=None, attributes=None):
        super().__init__(v1, v2, uid=uid, attributes=attributes)

        self.weight = weight

@pytest.fixture
def graph_cheapest_is_shortest():
    """
    .. todo::

       doc
    """

    verts = [Vertex(attributes={"i": i}) for i in range(6)]

    # a bunch of 1-weight edges
    explicit.link_from_to(verts[0], WeightedDirectedEdge, verts[1]).weight = 1
    explicit.link_from_to(verts[1], WeightedDirectedEdge, verts[2]).weight = 1
    explicit.link_from_to(verts[2], WeightedDirectedEdge, verts[3]).weight = 1
    explicit.link_from_to(verts[3], WeightedDirectedEdge, verts[4]).weight = 1
    explicit.link_from_to(verts[4], WeightedDirectedEdge, verts[5]).weight = 1

    # "bypass lane" -- weight of 1 from start to end
    explicit.link_from_to(verts[0], WeightedDirectedEdge, verts[5]).weight = 4

    return Universe(vertices=verts), verts

@pytest.fixture
def graph_cheapest_is_longest():
    """
    .. todo::

       doc
    """

    verts = [Vertex(attributes={"i": i}) for i in range(6)]

    # a bunch of 1-weight edges
    explicit.link_from_to(verts[0], WeightedDirectedEdge, verts[1]).weight = 1
    explicit.link_from_to(verts[1], WeightedDirectedEdge, verts[2]).weight = 2
    explicit.link_from_to(verts[2], WeightedDirectedEdge, verts[3]).weight = 3
    explicit.link_from_to(verts[3], WeightedDirectedEdge, verts[4]).weight = 4
    explicit.link_from_to(verts[4], WeightedDirectedEdge, verts[5]).weight = 5

    # "bypass lane" -- weight of 1 from start to end
    explicit.link_from_to(verts[0], WeightedDirectedEdge, verts[5]).weight = 20

    return Universe(vertices=verts), verts
