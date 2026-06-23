# -*- coding: utf-8 -*-

"""
Unit tests for core functionality of the SPLP module.
"""

import pytest

from edgegraph.builder import explicit
from edgegraph.pathfinding import longestpath
from edgegraph.structure import Vertex
from edgegraph.traversal import helpers


@pytest.mark.parametrize("method", longestpath.METHODS)
def test_splp_smoketest(graph_clrs09_22_6, method):
    uni, verts = graph_clrs09_22_6

    start = verts[1]
    dest = verts[6]

    sol = longestpath.single_pair_longest_path(
            uni, start, dest, weightfunc=None, method=method
            )
    path, dist = sol

    assert path == [verts[1], verts[4], verts[8], verts[0], verts[2], verts[5], verts[6]]
    assert dist == 6

@pytest.mark.parametrize("method", longestpath.METHODS)
def test_splp_backwards(graph_clrs09_22_6, method):
    uni, verts = graph_clrs09_22_6

    start = verts[6]
    dest = verts[1]

    sol = longestpath.single_pair_longest_path(
            uni, start, dest, method=method, direction_sensitive=helpers.DIR_SENS_BACKWARD,
            )
    path, dist = sol

    assert path == [verts[6], verts[5], verts[2], verts[0], verts[8], verts[4], verts[1]]
    assert dist == 6

