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


def _topo_base_kahns(
    uni: Universe,
    *,
    direction_sensitive: int = helpers.DIR_SENS_BACKWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
) -> list[Vertex]:

    incoming_links_count = {}
    queue = []
    topological_ordering = []
    visited = 0

    if direction_sensitive == helpers.DIR_SENS_FORWARD:
        incoming_edge_direction = helpers.DIR_SENS_BACKWARD
    elif direction_sensitive == helpers.DIR_SENS_BACKWARD:
        incoming_edge_direction = helpers.DIR_SENS_FORWARD
    else:
        msg = (
            "Kahns algorithm topological support only supports "
            "DIR_SENS_FORWARD and DIR_SENS_BACKWARD for "
            "direction_sensitive option!"
        )
        raise ValueError(msg)

    for vert in uni.vertices:
        incoming_links_count[vert] = 0

        for _ in helpers.neighbors(
            vert,
            direction_sensitive=incoming_edge_direction,
            unknown_handling=unknown_handling,
            filterfunc=ff_via,
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
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            filterfunc=ff_via,
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


def _topo_dfs_visit(
    vert,
    topo_ordered,
    unvisited,
    marks,
    direction_sensitive,
    unknown_handling,
    ff_via,
):
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
        direction_sensitive=direction_sensitive,
        unknown_handling=unknown_handling,
        filterfunc=ff_via,
    ):
        _topo_dfs_visit(
            neighbor,
            topo_ordered,
            unvisited,
            marks,
            direction_sensitive,
            unknown_handling,
            ff_via,
        )

    unvisited.remove(vert)
    topo_ordered.insert(0, vert)


def _topo_base_dfs(
    uni: Universe,
    *,
    direction_sensitive: int = helpers.DIR_SENS_BACKWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
) -> list[Vertex]:

    unvisited = set(uni.vertices)
    marks = set()
    topo_ordered = []

    while unvisited:
        # similar to unvisited.pop(), but does not remove from the list
        # see https://stackoverflow.com/a/48874729
        for vert in unvisited:
            break
        _topo_dfs_visit(
            vert,
            topo_ordered,
            unvisited,
            marks,
            direction_sensitive,
            unknown_handling,
            ff_via,
        )

    return topo_ordered


def topological_ordering(
    uni: Universe,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    method="kahn",
) -> list[Vertex]:

    # and-gate custom filterfuncs to enforce universe containment
    if ff_via is not None:

        def _ff_via(link, vert):
            return (vert in uni.vertices) and ff_via(link, vert)
    else:

        def _ff_via(_, vert):
            return vert in uni.vertices

    if method == "kahn":
        return _topo_base_kahns(
            uni,
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            ff_via=_ff_via,
        )
    if method == "dfs":
        return _topo_base_dfs(
            uni,
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            ff_via=_ff_via,
        )

    # If we reach this point, we didn't select a valid backend in method
    msg = f"{method} is not a known topological sort backend!"
    raise ValueError(msg)
