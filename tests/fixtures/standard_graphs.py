# -*- coding: utf-8 -*-

"""
Various "standard" graphs that you might find on your local whiteboard.
"""

from __future__ import annotations

import pytest

from edgegraph.builder import explicit
from edgegraph.structure import Universe, Vertex


@pytest.fixture
def complete_graph_1k_directed():
    """
    Return a complete graph with directed edges of 1,000 nodes.

    In this graph, every vertex is linked to every other (including itself)
    with a directed edge.
    """

    uni = Universe()
    verts = [Vertex(attributes={"i": i}, universes=[uni]) for i in range(1000)]
    for v in verts:
        for u in verts:
            explicit.link_directed(v, u)

    return uni, verts


@pytest.fixture
def complete_graph_1k_undirected():
    """
    Return a complete graph with undirected edges of 1,000 nodes.
    """

    uni = Universe()
    verts = [Vertex(attributes={"i": i}, universes=[uni]) for i in range(1000)]
    for i, v in enumerate(verts[::-1]):
        for u in verts[i + 1 :]:
            explicit.link_undirected(v, u)

    return uni, verts


@pytest.fixture
def straightline_graph_1k_directed():
    """
    Returns a graph that forms a straight line, of size 1,000 nodes.

    This looks like A --> B --> C --> D ....
    """

    uni = Universe()
    verts = [Vertex(attributes={"i": i}, universes=[uni]) for i in range(1000)]

    for i, v in enumerate(verts[:-1]):
        explicit.link_directed(v, verts[i + 1])

    return uni, verts
