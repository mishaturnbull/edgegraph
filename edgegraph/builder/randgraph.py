#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Procedures for creating random graphs.
"""

from __future__ import annotations

import random
from edgegraph.structure import Vertex, DirectedEdge, Universe
from edgegraph.builder import adjlist


def randgraph(
    count: int = 15,
    edge: type = DirectedEdge,
    connectivity: float | None = None,
    ensurelink: bool | None = True,
) -> Universe:
    """
    Create a random graph.

    This function creates a graph with the specified number of verticies, and
    returns it as a :py:class:`~edgegraph.structure.universe.Universe`.  Their
    links are decided randomly.

    :param count: How many verticies to create.  Default 15.
    :param edge: Type of edge to use.  Default
       :py:class:`~edgegraph.structure.directededge.DirectedEdge`.
    :param connectivity: Rough control over how many edges are created for each
       vertex.  If specified, must be a float ``0 < connectivity <= 1``.  If
       not specified, calculated automatically to author's preference.
    :param ensurelink: Ensure that every vertex gets at least one edge.
    :return: a :py:class:`~edgegraph.structure.universe.Universe` object
       containing the graph.
    """
    verts = [Vertex(attributes={"i": i}) for i in range(count)]

    if connectivity is None:
        # this seems to give a good ratio of vertex-edge, as long as count is
        # more than 3
        connectivity = 5 / count

    adj = {}
    for i in range(count):

        k = int(random.randint(1, max(1, i)) * connectivity)
        if ensurelink:
            k = max(k, 1)

        adj[verts[i]] = random.sample(verts, k)

    return adjlist.load_adj_dict(adj, linktype=edge)
