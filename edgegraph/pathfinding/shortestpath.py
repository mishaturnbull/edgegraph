#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Algorithms for finding the shortest path between two points.

.. todo::

   documentation
"""

from __future__ import annotations

import heapq

from edgegraph.traversal import helpers, breadthfirst


def _init_single_source(start):
    """
    INITIALIZE-SINGLE-SOURCE() subroutine.

    Purely a convienence function (and to keep linters from yelling about
    duplicate code).

    :param start: Starting vertex.
    :return: Three-tuple of dictionaries, for ``dist[v]``, ``prev[v]``, and
       ``weight[v]``.
    """
    return {start: 0}, {start: None}


def _relax(dist, prev, u, v, weightfunc):
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
    uni,
    start,
    weightfunc,
    stop_at=None,
    direction_sensitive=None,
    ff_via=None,
    unknown_handling=None,
):
    """
    Perform Dijkstra's algorithm to identify single-source shortest paths
    cross the given graph.

    .. todo::

       * documentation
       * all neighbors passthru (ff_via, ff_result?  does that make sense here?)
       * code comments
    """
    dist, prev = _init_single_source(start)
    S = set()
    Q = []
    heapq.heappush(Q, (0, 0, start))
    entry = 1

    infinity = float("inf")

    while len(Q):
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

            if v in S:
                continue

            # discover edges on-the-fly
            if v not in dist:
                dist[v] = infinity

            alt = dist[u] + weightfunc(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

            heapq.heappush(Q, (dist[v], entry, v))
            entry += 1

            _relax(dist, prev, u, v, weightfunc)

    return dist, prev


def _route_dijkstra(dist, prev, source, dest):
    """
    Given a solved internal base Dijkstra map, identify the actual route
    between source and dest.
    """
    S = []
    u = dest
    if prev[u] is not None or u is source:
        while u is not None:
            S.insert(0, u)
            u = prev[u]

    return S


def single_pair_shortest_path(
    uni,
    start,
    dest,
    *,
    weightfunc=None,
    direction_sensitive=helpers.DIR_SENS_FORWARD,
    unknown_handling=helpers.LNK_UNKNOWN_ERROR,
    ff_via=None,
    method="dijkstra",
):
    """
    Find the shortest path between two vertices in the given universe.

    This function is a frontend for various implementations / algorithms for
    computing the single-pair shortest path (SPSP) problem; that is, finding
    the shortest path between a single pair of nodes.  It returns the path
    between the given nodes (also sometimes called the route), as well as the
    total weight (also sometimes called cost).

    Custom weights on edges are possible via the ``weightfunc`` argument.  It
    must be a callable object accepting exactly two position arguments, ``u``
    and ``v``, which represent a "from" and "to" vertex.  It must return a
    number representing the weight of pathing from ``u`` to ``v``.  (Hint:
    :py:func:`~edgegraph.traversal.helpers.find_links` can quickly find you the
    edges(s) between these two!)

    .. warning::

       Some ``method`` options require that all edges are weighted positively,
       or that no negative-weight cycles exist.

    :param uni: Universe to search within.  Set to ``None`` for no universe
       limiting.
    :param start: Vertex to start searching from.
    :param dest: Vertex to search for.
    :param weightfunc: Callback function to determine the weight (also
       sometimes called cost) of transiting between two vertices.  If not
       specified, the default behavior is to weight all edges equally (weight
       of 1).
    :param method: The backend algorithm to use.  Options are:

       * ``"dijkstra"``: Use Dijkstra's algorithm with a priority queue; worst
         case is :math:`O(V^2)`. (**default**)

    :return: A two-tuple of:

       #. A :py:class:`list` of :py:class:`~edgegraph.structure.vertex.Vertex`
          objects representing the actual path taken to reach from ``start`` to
          ``dest``.  The start and end vertices are included in this list.
       #. The total weight of the path between start and end vertices (the sum
          of the given ``weightfunc``'s return for all hops in the discovered
          path).
    """
    if weightfunc is None:
        weightfunc = lambda u, v: 1

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
        path = _route_dijkstra(dist, prev, start, dest)
        dist = dist[dest]
        return (path, dist)

    raise NotImplementedError(f"method='{method}' is unrecognized")
