#!python3
# -*- coding: utf-8 -*-

"""
Unit tests for the single_pair_shortest_path() function.
"""

from edgegraph.traversal import helpers
from edgegraph.pathfinding import shortestpath


def test_sssp_dijkstra_smoketest(graph_clrs09_22_6):
    uni, verts = graph_clrs09_22_6

    # start at vert R (1) and pathfind over to W (6)
    start = verts[1]
    dest = verts[6]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=None, method="dijkstra"
    )

    path, dist = sol

    assert path == [verts[1], verts[8], verts[0], verts[6]]
    assert dist == 3


def _getweight(u, v):
    edges = helpers.find_links(u, v)
    weight = float("inf")
    for e in edges:
        weight = min(weight, e.weight)
    return weight


def test_sssp_dijkstra_weighted_nochange(graph_cheapest_is_shortest):
    uni, verts = graph_cheapest_is_shortest

    start = verts[0]
    dest = verts[5]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=_getweight, method="dijkstra"
    )
    path, dist = sol

    assert path == [verts[0], verts[5]]
    assert dist == 4


def test_sssp_dijkstra_weighted_diff(graph_cheapest_is_longest):
    uni, verts = graph_cheapest_is_longest

    start = verts[0]
    dest = verts[5]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=_getweight, method="dijkstra"
    )
    path, dist = sol

    assert dist == 15
    assert path == verts
