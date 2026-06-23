# -*- coding: utf-8 -*-

"""
Algorithms for finding the longest path between two points.
"""

from edgegraph.pathfinding import shortestpath
from edgegraph.traversal import helpers

METHODS = [
    "dijkstra",
]


def _default_weightfunc(u, v):
    return -1


def single_pair_longest_path(
    uni,
    start,
    dest,
    weightfunc=None,
    direction_sensitive=helpers.DIR_SENS_FORWARD,
    unknown_handling=helpers.LNK_UNKNOWN_ERROR,
    ff_via=None,
    method="dijkstra",
):

    if weightfunc is None:
        weightfunc = _default_weightfunc
    else:
        weightfunc = lambda u, v: -weightfunc(u, v)

    if start is None:
        raise ValueError("Cannot begin path searching with start=None!")

    path, dist = shortestpath.single_pair_shortest_path(
        uni,
        start,
        dest,
        weightfunc=weightfunc,
        direction_sensitive=direction_sensitive,
        unknown_handling=unknown_handling,
        ff_via=ff_via,
        method=method,
    )

    return (path, -dist)
