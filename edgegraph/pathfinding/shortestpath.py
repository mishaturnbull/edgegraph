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
    return {start: 0}, {start: None}

def _relax(dist, prev, u, v, weightfunc):
    w = weightfunc(u, v)
    if dist[v] > dist[u] + w:
        dist[v] = dist[u] + w
        prev[v] = u

def _sssp_base_dijkstra(uni, start, weightfunc):
    dist, prev = _init_single_source(start)
    S = set()
    Q = []
    heapq.heappush(Q, (0, 0, start))
    entry = 1

    infinity = float('inf')

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

            alt = dist[u] + weightfunc(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

            heapq.heappush(Q, (dist[v], entry, v))
            entry += 1

            _relax(dist, prev, u, v, weightfunc)

    return dist, prev

def _route_dijkstra(dist, prev, source, dest):
    S = []
    u = dest
    if prev[u] is not None or u is source:
        while u is not None:
            S.insert(0, u)
            u = prev[u]

    return S

def single_pair_shortest_path(uni, start, dest, weightfunc=None, method='dijkstra'):
    if weightfunc is None:
        weightfunc = lambda u, v: 1

    if method == 'dijkstra':
        dist, prev = _sssp_base_dijkstra(uni, start, weightfunc)
        path = _route_dijkstra(dist, prev, start, dest)
        dist = dist[dest]
        return (path, dist)

    raise NotImplementedError(f"method='{method}' is unrecognized")

