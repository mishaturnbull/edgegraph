# -*- coding: utf-8 -*-

"""
Graphs with weights set on all edges.
"""

from __future__ import annotations

import pytest

from edgegraph.builder import explicit
from edgegraph.structure import DirectedEdge, Universe, Vertex


class WeightedDirectedEdge(DirectedEdge):
    """
    A subclass of :py:class:`~edgegraph.structure.directededge.DirectedEdge`
    which supports a custom  ``weight`` attribute.
    """

    def __init__(
        self, v1=None, v2=None, weight=None, *, uid=None, attributes=None
    ):
        """
        Create a weighted directed edge.  All parameters the same as
        :class:`~edgegraph.structure.directededge.DirectedEdge`, except the
        addition of a numerical ``weight``.
        """
        super().__init__(v1, v2, uid=uid, attributes=attributes)

        self.weight = weight


@pytest.fixture
def graph_cheapest_is_shortest():
    """
    This graph is a fairly common case in the wild where the cheapest path is
    also the shortest, but it is not homogenously weighted.

    .. uml::

       left to right direction

       object 0
       object 1
       object 2
       object 3
       object 4
       object 5

       0 --> 1 : 1
       1 --> 2 : 1
       2 --> 3 : 1
       3 --> 4 : 1
       4 --> 5 : 1
       0 --> 5 : 4

    :return: a two-tuple containing a
       :py:class:`~edgegraph.structure.universe.Universe` of the graph, and a
       :py:class:`list` of all :py:class:`~edgegraph.structure.vertex.Vertex`
       objects.  The order of this list is shown by the numbers in the above
       diagram; the number of a vertex is its index in the list.

       Edges on the graph have a ``weight`` attribute.
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
    This graph is set up with a fewer-hops path between two nodes that is
    *more* expensive than another path with more hops.  It is meant to ensure
    pathfinding weight evaluation is working properly.

    .. uml::

       left to right direction

       object 0
       object 1
       object 2
       object 3
       object 4
       object 5

       0 --> 1 : 1
       1 --> 2 : 2
       2 --> 3 : 3
       3 --> 4 : 4
       4 --> 5 : 5
       0 --> 5 : 20

    :return: a two-tuple containing a
       :py:class:`~edgegraph.structure.universe.Universe` of the graph, and a
       :py:class:`list` of all :py:class:`~edgegraph.structure.vertex.Vertex`
       objects.  The order of this list is shown by the numbers in the above
       diagram; the number of a vertex is its index in the list.

       Edges on the graph have a ``weight`` attribute.
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


@pytest.fixture
def graph_neg_weight_no_loops():
    """
    This graph is set up with a single edge with negaitve weight.

    No negative cycles (or cycles of any kind) are present.

    .. uml::

       left to right direction

       object 0
       object 1
       object 2
       object 3

       0 --> 1: 1
       1 --> 2: -5
       2 --> 3: 1
       0 --> 3: 1
    """
    verts = [Vertex(attributes={"i": i}) for i in range(4)]

    # weight the edges
    explicit.link_from_to(verts[0], WeightedDirectedEdge, verts[1]).weight = 1
    explicit.link_from_to(verts[1], WeightedDirectedEdge, verts[2]).weight = -5
    explicit.link_from_to(verts[2], WeightedDirectedEdge, verts[3]).weight = 1
    explicit.link_from_to(verts[0], WeightedDirectedEdge, verts[3]).weight = 2

    return Universe(vertices=verts), verts
