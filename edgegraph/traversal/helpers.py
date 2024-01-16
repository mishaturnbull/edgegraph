#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Helper functions for graph traversals.
"""

from __future__ import annotations

from edgegraph.structure import Vertex, DirectedEdge, UnDirectedEdge

LNK_UNKNOWN_NONNEIGHBOR = 0
LNK_UNKNOWN_NEIGHBOR = 1
LNK_UNKNOWN_ERROR = 2

def neighbors(vert: Vertex,
        direction_sensitive: bool=True,
        unknown_handling: int=LNK_UNKNOWN_ERROR,
        ) -> list[Vertex]:

    neighbors = []
    for link in vert.links:

        if direction_sensitive:
            # undirected edges don't matter
            if issubclass(type(link), UnDirectedEdge):
                neighbors.append(link.other(vert))

            # for directed edges, only add the neighbor if vert is the origin
            elif issubclass(type(link), DirectedEdge) and (link.v1 is vert):
                neighbors.append(link.other(vert))

            # we're looking at v2 -- the destination
            # TODO: is it more time efficient to move the v1/v2 comparison into
            # an if nested under the directededge check?
            elif issubclass(type(link), DirectedEdge) and (link.v2 is vert):
                pass

            else:
                if unknown_handling == LNK_UNKNOWN_NONNEIGHBOR:
                    continue
                elif unknown_handling == LNK_UNKNOWN_NEIGHBOR:
                    neighbors.append(link.other(vert))
                else:
                    raise NotImplementedError(f"Unknown link class {type(link)}")

        else:
            neighbors.append(link.other(vert))

    return neighbors

