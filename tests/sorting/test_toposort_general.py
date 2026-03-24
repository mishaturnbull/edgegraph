# -*- coding: utf-8 -*-

"""
Unit tests for topological sorts which work on all toposorting algorithms.

Quirks unique to specific algorithms (Kahns, DFS-based, etc) are tested in
their own modules.
"""

import pytest

from edgegraph import exceptions
from edgegraph.sorting import toposort
from edgegraph.traversal import helpers


@pytest.mark.parametrize("algo", toposort.METHODS)
def test_toposort_ordering(algo, graph_clrs09_22_8):
    """
    Borderline smoke-test level check of topological sort correctness.

    Call the function, then verify that running through it in order doesn't
    give any dependency issues.

    This graph fixture (22.8) does not contain any cycles.
    """
    uni, verts = graph_clrs09_22_8

    topo = toposort.topological_ordering(uni, method=algo)

    # make sure no nodes have unfinished inbound edges
    seen = set()
    for vert in topo:
        incoming = helpers.neighbors(
            vert, direction_sensitive=helpers.DIR_SENS_BACKWARD
        )
        for ivert in incoming:
            assert ivert in seen, "Toposort was incorrect!"

        seen.add(vert)

    assert seen == set(verts), "Did not examine all vertices in the sort!"


@pytest.mark.parametrize("algo", toposort.METHODS)
def test_toposort_die_on_cycle(algo, graph_clrs09_22_6):
    """
    Check that a contains-cycles error is raised when a graph contains a cycle.

    This graph fixture (22.6) *does* contain cycles.
    """
    uni, _ = graph_clrs09_22_6

    with pytest.raises(exceptions.GraphContainsCyclesError):
        toposort.topological_ordering(uni, method=algo)
