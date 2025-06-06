# -*- coding: utf-8 -*-

"""
Provides fixtures and PyTest hooks for all testing usage.

See:
https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

from __future__ import annotations

import logging

import pytest

from edgegraph.structure import Vertex

# guido, forgive me
from .fixtures import *  # noqa: F403

LOG = logging.getLogger(__name__)


# https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-parametrize
# use strings for the params ("cache" and "nocache") instead of raw booleans
# to improve readability in the test output ("what's this random [True]??")
@pytest.fixture(params=["cache", "nocache"], autouse=True)
def enforce_cache_testing(request):
    """
    Run *all* tests both with and without vertex neighbor caching,
    automatically.

    This fixture is automatically applied to every test function, and
    parameterizes it to run both with and without ``Vertex.NEIGHBOR_CACHING``
    enabled.
    """
    enable = request.param == "cache"
    Vertex.NEIGHBOR_CACHING = enable

    # reset cache stats and sentinel
    Vertex._QA_NB_INVALID = object()
    Vertex._CACHE_STATS = {}

    yield

    LOG.debug(f"For test case {request.node}:")
    LOG.debug(Vertex.total_cache_stats())
