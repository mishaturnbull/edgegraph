# -*- coding: utf-8 -*-

"""
Unit tests that ensure no negative effects of caching are observed.
"""

import pytest

from edgegraph.builder import explicit
from edgegraph.structure import vertex
from edgegraph.traversal import breadthfirst, depthfirst

travs = [
    depthfirst.dft_recursive,
    depthfirst.dft_iterative,
    breadthfirst.bft,
]


@pytest.mark.parametrize("trav", travs)
def test_updated_graph_trav_results(graph_clrs09_22_6, trav):
    """
    Ensure different results of traversing a graph before and after an update.
    """
    uni, verts = graph_clrs09_22_6

    vertex.Vertex.NEIGHBOR_CACHING = True

    # check traversal fn before edits are made
    before = trav(uni, verts[0])

    # unlink start vertex from every outbound edge
    explicit.unlink(verts[0], verts[2])
    explicit.unlink(verts[0], verts[3])
    explicit.unlink(verts[0], verts[6])

    # check after the update
    after = trav(uni, verts[0])

    # if before and after are the same, we have a problem
    assert before != after, "Editing graph did not affect traversal!!"

    vertex.Vertex.NEIGHBOR_CACHING = False
