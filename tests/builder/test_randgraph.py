#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for the random graph generator.
"""

import pytest
from edgegraph.structure import Universe, DirectedEdge, UnDirectedEdge
from edgegraph.builder import randgraph

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

