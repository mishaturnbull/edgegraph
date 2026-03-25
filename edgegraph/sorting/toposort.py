# -*- coding: utf-8 -*-

"""
Algorithms for topological ordering of graphs.

This module provides a topological sorting / ordering capability, allowing
ordering of graphs based on their dependent vertices.  Most commonly, this is
useful for dependency calculation.

.. seealso::

   Descriptive documentation about what solvers are implemented can be found
   here: :ref:`usage/algos/sorting/toposort`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from edgegraph import exceptions
from edgegraph.traversal import helpers

if TYPE_CHECKING:
    from typing import Callable

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
    """
    Kahn's topo-sort algorithm backend.

    This is an internal-use-only function for running Kahn's algorithm as a
    backend to the toposort API.

    :param uni: The universe to sort.  No starting vertex is specified.
    :param direction_sensitive: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`.
    :param unknown_handling: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`.
    :param ff_via: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`'s ``filterfunc``.
    :return: A list of vertices in a topological ordering.
    :raises ValueError: if argument(s) are invalid.
    :raises GraphContainsCyclesError: if the graph contains a cycle.
    """

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
    vert: Vertex,
    topo_ordered: list[Vertex],
    unvisited: set[Vertex],
    marks: set[Vertex],
    direction_sensitive: int,
    unknown_handling: int,
    ff_via: Callable,
):
    """
    Depth-first search recursive element.

    Internal-use-only helper function for DFS-based toposorts.

    :param vert: Vertex currently under examination.
    :param topo_ordered: Current state of the ordering under construction.
    :param unvisited: Set of vertices not yet visited.
    :param marks: Set of vertices marked as processed.
    :param direction_sensitive: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`.
    :param unknown_handling: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`.
    :param ff_via: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`'s ``filterfunc``.
    :return: Nothing; operates in-place.
    """
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
    """
    Modified DFS topo-sort algorithm backend.

    This is an internal-use-only backend for topological sorting based on DFS.

    :param uni: The universe to sort.  No starting vertex is specified.
    :param direction_sensitive: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`.
    :param unknown_handling: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`.
    :param ff_via: Direct pass-through to
       :py:func:`edgegraph.traversal.helpers.neighbors`'s ``filterfunc``.
    :return: A list of vertices in a topological ordering.
    :raises ValueError: if argument(s) are invalid.
    :raises GraphContainsCyclesError: if the graph contains a cycle.
    """

    unvisited: set[Vertex] = set(uni.vertices)
    marks: set[Vertex] = set()
    topo_ordered: list[Vertex] = []

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
    """
    Provide a topological ordering (sort) of a given universe's vertices.

    This function is a frontend for various implementations / algorithms for
    computing a topological ordering of a graph; that is, a linear ordering of
    a graph such that for every directed edge :math:`(u, v)`, :math:`u` comes
    before :math;`v` in the ordered list.

    Note that in many cases, multiple such ordering exist for a given graph.
    This function does not (currently) declare sorting stability; that is, it
    is only guaranteed to return a valid ordering, not necessarily the same
    ordering every time when called with the same arguments.

    Topological sorts are not defined for graphs which contain cycles.  If a
    graph provided here contains a cycle,
    :py:exc:`~edgegraph.exceptions.GraphContainsCyclesError` will be raised.

    :param uni: The universe whose vertices are to be ordered.
    :param direction_sensitive: Selector for direction-sensitivity.  This is
       passed directly through to internal calls of
       :py:func:`~edgegraph.traversal.helpers.neighbors`.  Either forward or
       backward options are valid for all backends; certain backends MAY allow
       the ANY option, but there are typically severe restrictions in graph
       layout for this to work.
    :param unknown_handling: Selector for behavior when encountering an unknown
       link class.  This is passed directly through to internal calls of
       :py:func:`~edgegraph.traversal.helpers.neighbors`.
    :param ff_via: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors` function's
       ``filterfunc`` argument.  If not specified, the default option only
       requires that ``v2`` is a member of the ``uni`` argument.  If it is
       specified, the user-provided function is AND-gated with that same check
       (i.e., you cannot use this to escape the bounds of ``uni``).

       .. py:function:: ff_via(e, v2)
          :noindex:

          Determins if an edge (``e``) from a given vertex to another (``v2``)
          should be followed.  If not, that entire section of the graph will
          not be considered for ordering (assuming no other entries to that
          area).

          :param e: The edge connecting ``v1`` to ``v2``.
          :param v2: The vertex under consideration.
          :return: Whether or not ``v2`` should be considered a neighbor of
             ``v``, when reached via ``e``.

    :param method: The backend algorithm to use.  Options are:

       * ``"kahn"``: use Kahn's algorithm.  Worst case is approximately
         :math:`O(V+E)`, and does not use a recursive implementation.
       * ``"dfs"``: use a modified DFS algorithm.  Worst case is approximately
         :math:`O(V)`, but this uses a recursive implementation.

    :return: A list of :py:class:`~edgegraph.structure.vertex.Vertex` objects,
       in a topological order.
    :raises edgegraph.exceptions.GraphContainsCyclesError: if the graph given
       in ``uni`` contains cycles (cycles which are not followed, due to edge
       directionality, unknown-link options, or filter-function will not raise
       this exception).
    :raises ValueError: on an invalid argument.  This may be delegated to
       individual method backends which implement different limitations.
    """

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
