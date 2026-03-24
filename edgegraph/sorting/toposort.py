# -*- coding: utf-8 -*-

"""
Algorithms for topological ordering of graphs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from edgegraph import exceptions
from edgegraph.traversal import helpers

if TYPE_CHECKING:
    from edgegraph.structure import Universe, Vertex

METHODS = [
    "kahn",
    "dfs",
]


def _topo_base_kahns(uni: Universe) -> list[Vertex]:

    incoming_links_count = {}
    queue = []
    topological_ordering = []
    visited = 0

    for vert in uni.vertices:
        incoming_links_count[vert] = 0

        for _ in helpers.neighbors(
            vert,
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=lambda link, vert2: vert2 in uni.vertices,
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
            filterfunc=lambda link, vert2: vert2 in uni.vertices,
        ):
            incoming_links_count[neighbor] -= 1
            if incoming_links_count[neighbor] == 0:
                queue.append(neighbor)

    if visited != len(uni.vertices):
        msg = (
            "Kahns algorithm does not support topologically sorting graphs "
            "which contain cycles (this one does)!"
        )
        raise exceptions.GraphContainsCyclesError(msg)

    return topological_ordering


def _topo_base_dfs(uni: Universe) -> list[Vertex]:

    unvisited = set(uni.vertices)
    marks = set()
    topological_ordering = []

    def visit(vert):
        if vert not in unvisited:
            return

        if vert in marks:
            msg = (
                "DFS-based topo sort does not support topologically "
                "sorting graphs which contain cycles (this one does)!"
            )
            raise exceptions.GraphContainsCyclesError(msg)

        marks.add(vert)

        for neighbor in helpers.neighbors(
            vert,
            direction_sensitive=helpers.DIR_SENS_FORWARD,
            filterfunc=lambda link, vert2: vert2 in uni.vertices,
        ):
            visit(neighbor)

        unvisited.remove(vert)
        topological_ordering.insert(0, vert)

    while unvisited:
        # similar to unvisited.pop(), but does not remove from the list
        # see https://stackoverflow.com/a/48874729
        for vert in unvisited:
            break
        visit(vert)

    return topological_ordering


def topological_ordering(uni: Universe, method="kahn"):

    if method == "kahn":
        return _topo_base_kahns(uni)
    if method == "dfs":
        return _topo_base_dfs(uni)

    # If we reach this point, we didn't select a valid backend in method
    msg = f"{method} is not a known topological sort backend!"
    raise ValueError(msg)
