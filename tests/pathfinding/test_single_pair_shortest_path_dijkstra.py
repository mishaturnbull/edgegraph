#!python3
# -*- coding: utf-8 -*-

"""
Unit tests for the single_pair_shortest_path() function.
"""

from edgegraph.traversal import helpers
from edgegraph.pathfinding import shortestpath


def _getweight(u, v):
    """
    Testing purposes only - access edge weights from the weighted-graph
    fixtures.
    """
    edges = helpers.find_links(u, v)
    weight = float("inf")
    for e in edges:
        weight = min(weight, e.weight)
    return weight


def test_spsp_dijkstra_weighted_nochange(graph_cheapest_is_shortest):
    """
    Ensure that graphs with a custom weighting function A.) work, and B.) solve
    as expected in the case where :math:`weight(u, v) = 1`.
    """
    uni, verts = graph_cheapest_is_shortest

    start = verts[0]
    dest = verts[5]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=_getweight, method="dijkstra"
    )
    path, dist = sol

    assert path == [verts[0], verts[5]]
    assert dist == 4


def test_spsp_dijkstra_weighted_diff(graph_cheapest_is_longest):
    """
    Ensure that graphs with a custom weight function A.) work, and B.) solve as
    expected in the case where :math:`weight(u, v) \\neq  1`.
    """
    uni, verts = graph_cheapest_is_longest

    start = verts[0]
    dest = verts[5]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=_getweight, method="dijkstra"
    )
    path, dist = sol

    assert dist == 15
    assert path == verts
