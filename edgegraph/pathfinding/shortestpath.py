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
    return {start: 0}, {start: None}, {start: 0}


def _relax(dist, prev, weight, u, v, weightfunc):
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
        weight[v] = weight[u] + w


def _sssp_base_dijkstra(uni, start, weightfunc):
    """
    Perform Dijkstra's algorithm to identify single-source shortest paths
    cross the given graph.

    .. todo::

       * documentation
       * add an early-break option if we know to look for a specific node
       * all neighbors passthru (ff_via, ff_result?  does that make sense here?)
       * code comments
    """
    dist, prev, weight = _init_single_source(start)
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

        nbs = helpers.neighbors(u)
        for v in nbs:

            if v in S:
                continue

            # discover edges on-the-fly
            if v not in dist:
                dist[v] = infinity
                weight[v] = infinity

            heapq.heappush(Q, (dist[v], entry, v))
            entry += 1

            _relax(dist, prev, weight, u, v, weightfunc)

    return dist, prev, weight


def _route_dijkstra(dist, prev, source, dest):
    S = []
    u = dest
    if prev[u] is not None or u is source:
        while u is not None:
            S.insert(0, u)
            u = prev[u]

    return S


def single_pair_shortest_path(
    uni, start, dest, weightfunc=None, method="dijkstra"
):
    if weightfunc is None:
        weightfunc = lambda u, v: 1

    if method == "dijkstra":
        dist, prev, weight = _sssp_base_dijkstra(uni, start, weightfunc)
        breakpoint()
        path = _route_dijkstra(dist, prev, start, dest)
        dist = dist[dest]
        weight = weight[dest]
        return (path, dist, weight)

    raise NotImplementedError(f"method='{method}' is unrecognized")
