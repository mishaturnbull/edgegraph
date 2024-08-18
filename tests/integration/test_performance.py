#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Dedicated performance tests designed to identify slow points.
"""

import itertools
import logging
import time
import pytest
from edgegraph.builder import randgraph
from edgegraph.traversal import breadthfirst, depthfirst

pytestmark = pytest.mark.perf

LOG = logging.getLogger(__name__)

@pytest.mark.perf
@pytest.mark.parametrize("howmany,nverts", itertools.product([3, 10, 30, 50], [10, 100, 500]))
def test_bulk_randgraph(howmany, nverts):
    """
    Generate lots of large random graphs.
    """
    times = [None] * howmany

    t_start = time.monotonic_ns()

    for i in range(howmany):
        t_substart = time.monotonic_ns()

        randgraph.randgraph(count=nverts, connectivity=1)

        t_subend = time.monotonic_ns()
        times[i] = t_subend - t_substart

    t_end = time.monotonic_ns()

    overall = t_end - t_start
    avg = sum(times) / len(times)
    vtime = avg / nverts
    avg /= 1_000_000_000
    missing = overall - sum(times)
    dur = overall / 1_000_000_000

    LOG.info(f"Randgraph performance: total {dur} s, avg {avg} s, vert time "
             f"{vtime} ns ({howmany} x {nverts} verts); {missing} ns miss")

@pytest.mark.perf
@pytest.mark.parametrize("howmany", [1, 10, 100])
def test_bulk_bft(complete_graph_1k_undirected, howmany):
    """
    Test breadth-first traversing a large graph (1k nodes).
    """
    uni, verts = complete_graph_1k_undirected
    times = [None] * howmany

    LOG.info("Begin test routine")

    t_start = time.monotonic_ns()

    for i in range(howmany):
        t_substart = time.monotonic_ns()

        breadthfirst.bft(uni, verts[0])

        t_subend = time.monotonic_ns()
        times[i] = t_subend - t_substart

    t_end = time.monotonic_ns()

    overall = t_end - t_start
    avg = sum(times) / len(times)
    avg /= 1_000_000_000
    missing = overall - sum(times)
    dur = overall / 1_000_000_000

    LOG.info(f"BFT performance: total {dur} s, avg {avg} s, {missing} ns miss")

