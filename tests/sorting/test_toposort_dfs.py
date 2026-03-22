# -*- coding: utf-8 -*-

"""
Unit tets for topological sorts based on a depth-first search.
"""

from edgegraph.sorting import toposort

def test_bfs_topo_smoketest(graph_clrs09_22_8):
    uni, verts = graph_clrs09_22_8

    topo = toposort.topological_ordering(uni, method="dfs")

    breakpoint()

