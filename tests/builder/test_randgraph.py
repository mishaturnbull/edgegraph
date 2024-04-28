#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for the random graph generator.
"""

import logging
import time
import pytest
from edgegraph.structure import DirectedEdge, UnDirectedEdge
from edgegraph.builder import randgraph

LOG = logging.getLogger(__name__)

@pytest.mark.parametrize('i', range(1, 25))
def test_randgraph_count(i):
    """
    Ensure the randgraph builder creates the correct number of vertices.
    """
    uni = randgraph.randgraph(count=i, connectivity=1)
    assert len(uni.vertices) == i

@pytest.mark.parametrize('edgetype', [DirectedEdge, UnDirectedEdge])
def test_randgraph_edgetype(edgetype):
    """
    Ensure all created edges are of the given edge type.
    """
    uni = randgraph.randgraph(count=100, edge=edgetype)
    for vert in uni.vertices:
        for link in vert.links:
            assert isinstance(link, edgetype)

def test_randgraph_ensurelink_false():
    """
    Ensure that zero connectivity is viable with ensurelink=False.
    """
    uni = randgraph.randgraph(count=50, connectivity=0, ensurelink=False)
    for vert in uni.vertices:
        assert len(vert.links) == 0

def test_randgraph_ensurelink_true():
    """
    Ensure that zero connectivity is impossible with ensurelink=True.
    """
    uni = randgraph.randgraph(count=50, connectivity=0, ensurelink=True)
    for vert in uni.vertices:
        assert len(vert.links) > 0

@pytest.mark.slow
def test_randgraph_stresstest():
    """
    Generate a few hundred random graphs, with increasing numbers of nodes.
    """
    count = 150
    times = [None] * count

    t_start = time.monotonic_ns()

    for j in range(count):
        t_substart = time.monotonic_ns()

        randgraph.randgraph(count=j, connectivity=1)

        t_subend = time.monotonic_ns()
        times[j] = t_subend - t_substart

    t_end = time.monotonic_ns()

    diffs = [times[i] - times[i-1] for i in range(1, count)]
    avg_diff = sum(diffs) / len(diffs)
    avg_diff /= 1_000_000_000

    dur = (t_end - t_start) / 1_000_000_000
    LOG.info(f"Randgraph stresstest: total {dur} s, node impact {avg_diff} s")

