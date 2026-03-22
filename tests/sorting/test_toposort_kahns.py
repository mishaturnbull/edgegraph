# -*- coding: utf-8 -*-

"""
Unit tests for topological sorts based on Kahns algorithm.
"""

from edgegraph.sorting import toposort

def test_kahn_smoketest(graph_clrs09_22_8):
    uni, verts = graph_clrs09_22_8

    topo = toposort.topological_ordering(uni, method="kahn")

    breakpoint()

