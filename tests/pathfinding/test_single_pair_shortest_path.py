#!python3
# -*- coding: utf-8 -*-

"""
Unit tests for the single_pair_shortest_path() function.
"""

from edgegraph.pathfinding import shortestpath


def test_sssp_dijkstra_smoketest(graph_clrs09_22_6):
    uni, verts = graph_clrs09_22_6

    # start at vert R (1) and pathfind over to W (6)
    start = verts[1]
    dest = verts[6]

    sol = shortestpath.single_pair_shortest_path(uni, start, dest, weightfunc=None, method='dijkstra')

    path, dist = sol

    assert path == [verts[1], verts[8], verts[0], verts[6]]
    assert dist == 3

