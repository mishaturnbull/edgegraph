# -*- coding: utf-8 -*-

"""
Unit tests specific to Kahns algorithm backend for topological sorting.
"""

import pytest

from edgegraph.sorting import toposort
from edgegraph.traversal import helpers


def test_kahns_invalid_args(graph_clrs09_22_8):
    uni, _ = graph_clrs09_22_8

    with pytest.raises(ValueError):
        toposort.topological_ordering(
            uni, direction_sensitive=helpers.DIR_SENS_ANY, method="kahn"
        )
