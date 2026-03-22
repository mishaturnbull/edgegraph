# -*- coding: utf-8 -*-

"""
Algorithms for topological ordering of graphs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from edgegraph.traversal import helpers

if TYPE_CHECKING:
    from edgegraph.structure import Universe, Vertex

METHODS = [
        "kahn",
        ]

class CycleError(Exception):
    pass


def _topo_base_kahns(
        uni: Universe
    ) -> list[Vertex]:

    incoming_links_count = {}
    queue = []
    topological_ordering = []
    visited = 0

    for vert in uni.vertices:
        incoming_links_count[vert] = 0

        for _ in helpers.neighbors(
                vert,
                direction_sensitive=helpers.DIR_SENS_BACKWARD,
                filterfunc=lambda l, u: u in uni.vertices,
                ):
            incoming_links_count[vert] += 1

        if incoming_links_count[vert] == 0:
            queue.append(vert)

    while queue:
        vert = queue.pop(0)
        visited += 1

        topological_ordering.append(vert)

        for neighbor in helpers.neighbors(
                vert,
                direction_sensitive=helpers.DIR_SENS_FORWARD,
                filterfunc=lambda l, u: u in uni.vertices,
                ):
            incoming_links_count[neighbor] -= 1
            if incoming_links_count[neighbor] == 0:
                queue.append(neighbor)

    if visited != len(uni.vertices):
        raise CycleError

    return topological_ordering


def topological_ordering(
        uni: Universe,
        method="kahn"
        ):

    if method == "kahn":
        return _topo_base_kahns(uni)



