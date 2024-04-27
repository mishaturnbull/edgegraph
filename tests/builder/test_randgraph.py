#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for the random graph generator.
"""

import logging
import time
import pytest
from edgegraph.structure import Universe, DirectedEdge, UnDirectedEdge
from edgegraph.builder import randgraph

LOG = logging.getLogger(__name__)

counts = range(1, 25)
@pytest.mark.parametrize('i', counts)
def test_randgraph_count(i):
    uni = randgraph.randgraph(count=i, connectivity=1)
    assert len(uni.vertices) == i

edgetypes = [DirectedEdge, UnDirectedEdge]
@pytest.mark.parametrize('edgetype', edgetypes)
def test_randgraph_edgetype(edgetype):
    uni = randgraph.randgraph(count=100, edge=edgetype)
    for vert in uni.vertices:
        for link in vert.links:
            assert isinstance(link, edgetype)

def test_randgraph_ensurelink_false():
    uni = randgraph.randgraph(count=50, connectivity=0, ensurelink=False)
    for vert in uni.vertices:
        assert len(vert.links) == 0

def test_randgraph_ensurelink_true():
    uni = randgraph.randgraph(count=50, connectivity=0, ensurelink=True)
    for vert in uni.vertices:
        assert len(vert.links) > 0

@pytest.mark.slow
def test_randgraph_stresstest():
    count = 150
    times = [None] * count

    t_start = time.monotonic_ns()

    for j in range(count):
        t_substart = time.monotonic_ns()

        uni = randgraph.randgraph(count=j, connectivity=1)

        t_subend = time.monotonic_ns()
        times[j] = t_subend - t_substart

    t_end = time.monotonic_ns()

    diffs = [times[i] - times[i-1] for i in range(1, count)]
    avg_diff = sum(diffs) / len(diffs)
    avg_diff /= 1_000_000_000

    dur = (t_end - t_start) / 1_000_000_000
    LOG.info(f"Randgraph stresstest: total {dur} s, node impact {avg_diff} s")

