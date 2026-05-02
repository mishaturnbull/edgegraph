# -*- coding: utf-8 -*-

"""
Unit tests specific to Kahns algorithm backend for topological sorting.
"""

import pytest

from edgegraph.sorting import toposort
from edgegraph.traversal import helpers


def test_kahns_invalid_args(graph_clrs09_22_8):
    """
    Verify that Kahn's algorithm backend does not allow DIR_SENS_ANY option.

    This is because Kahn's algorithm explicitly makes use of incoming edge
    count, and an undirected edge does not carry direction meaning (unlike the
    DFS backend, which sees it more as "neighbors" than "incoming edges").
    """
    uni, _ = graph_clrs09_22_8

    with pytest.raises(ValueError, match="direction_sensitive"):
        toposort.topological_ordering(
            uni, direction_sensitive=helpers.DIR_SENS_ANY, method="kahn"
        )
