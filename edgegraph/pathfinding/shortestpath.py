#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Algorithms for finding the shortest path between two points.

This module provides functions to solve the shortest path problem and its
variants:

* Single pair shortest path; the shortest path between a known start and
  destination vertex

... and at this time, that's all that's implemented!  More to come soon!

.. seealso::

   Descriptive documentation about what solvers are implemented can be found
   here: :ref:`usage/algos/pathfinding`.
"""

from __future__ import annotations

import heapq
from typing import TYPE_CHECKING
from collections.abc import Callable

from edgegraph.traversal import helpers

if TYPE_CHECKING:
    from edgegraph.structure import Vertex, Universe


METHODS = [
    "dijkstra",
]


def _init_single_source(
    start: Vertex,
) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
    """
    INITIALIZE-SINGLE-SOURCE() subroutine.

    Purely a convienence function (and to keep linters from yelling about
    duplicate code).

    :param start: Starting vertex.
    :return: Three-tuple of dictionaries, for ``dist[v]``, ``prev[v]``, and
       ``weight[v]``.
    """
    return {start: 0}, {start: None}


def _relax(
    dist: dict[Vertex, float],
    prev: dict[Vertex, Vertex | None],
    u: Vertex,
    v: Vertex,
    weightfunc: Callable,
) -> None:
    """
    RELAX() subroutine.

    This performs edge relaxation; that is, determining if we can improve the
    shortest path to ``v`` by traversing through ``u``.  If so, perform the
    necessary updates in the ``prev`` and ``dist`` data.

    :param dist: Dictionary of distance information for each vertex so far
       known.
    :param prev: Dictionary of predecessor information for each vertex so far
       known.
    :param u: Source vertex
    :param v: Destination vertex
    :param weightfunc: Edge weighting determination function
    :return: No return; updates ``dist`` and ``prev`` in place
    """
    w = weightfunc(u, v)
    if dist[v] > dist[u] + w:
        dist[v] = dist[u] + w
        prev[v] = u


def _sssp_base_dijkstra(
    uni: Universe,
    start: Vertex,
    weightfunc: Callable,
    stop_at: Vertex | None = None,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    ff_via: Callable | None = None,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
    """
    Perform Dijkstra's algorithm to identify single-source shortest paths
    cross the given graph.

    As this is a private, internal function, the entire algorithm and options
    are not detailed here.  See single_pair_shortest_path() for more
    information.
    """
    dist, prev = _init_single_source(start)

    # Set of vertices we've already visited.
    S = set()

    # The heap elements here have *three* elements, not just priority and item.
    # The first element of each tuple is indeed the priority, and the third
    # element indeed the item -- but the second is an "entry number", or "key",
    # that monotonically increases for each heap push.  This is to work around
    # Python's heap implementation using a built-in sort on a list of tuples,
    # which fails if two tuples are equivalent.  The always-unique entry value
    # ensures no two heap entries are totally identical, but still maintains
    # sort stability -- that is, of items with equal priority, their insertion
    # order is maintained.
    Q: list[Vertex] = []
    heapq.heappush(Q, (0, 0, start))
    entry = 1

    infinity = float("inf")

    # Fairly standard implementation of Dijkstra's algorithm.  Notable
    # differences from the typical textbook implementations include:
    #
    # 1. We discover neighbors on the fly rather than being given a large map
    #    at the start
    # 2. There exists an optional early-break condition if we know the user
    #    wants to only look for a specific vertex (stop_at).
    while Q:
        u = heapq.heappop(Q)[2]

        if u in S:
            continue
        S.add(u)

        if stop_at and stop_at is u:
            return dist, prev

        nbs = helpers.neighbors(
            u,
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            filterfunc=ff_via,
        )
        for v in nbs:

            # filter out vertices not a member of the given universe, if any.
            # by putting the `uni is not None` check first, we can
            # short-circuit the container check if it is not needed
            if (uni is not None) and (v not in uni.vertices):
                continue

            # skip already visited nodes
            if v in S:
                continue

            # discover edges on-the-fly
            if v not in dist:
                dist[v] = infinity

            _relax(dist, prev, u, v, weightfunc)

            heapq.heappush(Q, (dist[v], entry, v))
            entry += 1

    return dist, prev


def _route_dijkstra(
    prev: dict[Vertex, Vertex | None],
    dest: Vertex,
) -> list[Vertex] | None:
    """
    Given a solved internal base Dijkstra map, identify the actual route
    between source and dest.
    """
    S: list[Vertex] = []
    u: Vertex | None = dest

    if u not in prev:
        return None

    while u is not None:
        S.insert(0, u)
        u = prev[u]

    return S


def single_pair_shortest_path(
    uni: Universe,
    start: Vertex,
    dest: Vertex,
    *,
    weightfunc: Callable | None = None,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    method: str = "dijkstra",
) -> tuple[list[Vertex] | None, float | None]:
    """
    Find the shortest path between two vertices in the given universe.

    This function is a frontend for various implementations / algorithms for
    computing the single-pair shortest path (SPSP) problem; that is, finding
    the shortest path between a single pair of nodes.  It returns the path
    between the given nodes (also sometimes called the route), as well as the
    total weight (also sometimes called cost).


    :param uni: Universe to search within.  Set to ``None`` for no universe
       limiting.
    :param start: Vertex to start searching from.
    :param dest: Vertex to search for.
    :param weightfunc: Callback function to determine the weight (also
       sometimes called cost) of transiting between two vertices.  If not
       specified, the default behavior is to weight all edges equally (weight
       of 1).

       .. py:function:: weightfunc(v1, v2)
          :noindex:

          Custom weights on edges are possible via the ``weightfunc`` argument.
          It must be a callable object accepting exactly two position
          arguments, ``u`` and ``v``, which represent a "from" and "to" vertex.
          It must return a number representing the weight of pathing from ``u``
          to ``v``.

          .. seealso::

             Hint: :py:func:`~edgegraph.traversal.helpers.find_links` can
             quickly find you the edges(s) between these two!

          .. warning::

             Some ``method`` options require that all edges are weighted
             positively, or that no negative-weight cycles exist.

          :param v1: The "from" vertex
          :param v2: The "to" vertex
          :return: Cost of transiting from ``v1`` to ``v2``

    :param method: The backend algorithm to use.  Options are:

       * ``"dijkstra"``: Use Dijkstra's algorithm with a priority queue; worst
         case is :math:`O(V^2)`.  No negative weights are allowed.
         (**default**)


       .. seealso::

          More information on these options is available in the
          :ref:`usage/algos/pathfinding` section.

    :param direction_sensitive: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors`.  This may be one of:

       * :py:const:`~edgegraph.traversal.helpers.DIR_SENS_FORWARD` (default),
         to follow edges only forward (when directed),
       * :py:const:`~edgegraph.traversal.helpers.DIR_SENS_ANY`, to follow edges
         regardless of their direction,
       * :py:const:`~edgegraph.traversal.helpers.DIR_SENS_BACKWARD`, to only
         follow edges backwards (when directed).

    :param unknown_handling: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors`.  This may be one of:

       * :py:const:`~edgegraph.traversal.helpers.LNK_UNKNOWN_ERROR` (default),
         to throw an exception,
       * :py:const:`~edgegraph.traversal.helpers.LNK_UNKNOWN_NEIGHBOR`, to
         treat such edges as neighbors (and take the edge),
       * :py:const:`~edgegraph.traversal.helpers.LNK_UNKNOWN_NONNEIGHBOR`, to
         treat such edges as non-neighbors (do not take the edge).

    :param ff_via: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors` function's
       ``filterfunc`` argument.

       .. py:function:: ff_via(e, v2)
          :noindex:

          Determines if an edge (``e``) from a given vertex to another (``v2``)
          should be followed.  If not, that entire section of the graph will
          not be searched (assuming no other entries to that area).

          :param e: The edge connecting ``v1`` to ``v2``.
          :param v2: The vertex under consideration.
          :return: Whether or not ``v2`` should be considered a neighbor of
             ``v``, when reached via ``e``.

    :return: A two-tuple of:

       #. A :py:class:`list` of :py:class:`~edgegraph.structure.vertex.Vertex`
          objects representing the actual path taken to reach from ``start`` to
          ``dest``.  The start and end vertices are included in this list.

          If there is no path between the given vertices, ``None`` is given
          here instead.  If the start and destination vertices are the same,
          the value here will be ``[v1, v1]``.

       #. The total weight of the path between start and end vertices (the sum
          of the given ``weightfunc``'s return for all hops in the discovered
          path).

          If there is no path between the given vertices, ``None`` is given
          here instead.  If the start and destination vertices are the same,
          the value here will be zero regardless of edge weighting (as there is
          no distance between an object and itself).
    """
    if weightfunc is None:
        weightfunc = lambda u, v: 1

    if start is None:
        raise ValueError("Cannot begin path searching with start=None!")

    if start is dest:
        # if the start *is* the destination, then we don't have to do anything
        # at all!
        return [start, start], 0

    # Omission of "if ff_via is None" and always-true lambda here is not a
    # mistake!  helpers.neighbors() has a special case for its filterfunc being
    # None, which improves performance over an always-true function (it can
    # eliminate a stack frame transition).

    if method == "dijkstra":
        dist, prev = _sssp_base_dijkstra(
            uni,
            start,
            weightfunc,
            stop_at=dest,
            unknown_handling=unknown_handling,
            direction_sensitive=direction_sensitive,
            ff_via=ff_via,
        )
        path = _route_dijkstra(prev, dest)

        # decide whether to return a distance or not.  use a renamed variable
        # to avoid confusing mypy too much.
        if path is not None:
            retdist = dist[dest]
        else:
            retdist = None

        return (path, retdist)

    raise NotImplementedError(f"method='{method}' is unrecognized")
