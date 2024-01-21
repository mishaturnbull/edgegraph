#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for traversal.breadthfirst module.
"""

import pytest
from edgegraph.structure import (Vertex, TwoEndedLink, DirectedEdge,
        UnDirectedEdge, Universe)
from edgegraph.traversal import breadthfirst
from edgegraph.builder import adjlist, explicit

@pytest.fixture
def graph():
    """
    The graph generated in this function is taken from [CLRS09]_, figure 22.6.
    """
    verts = []
    for i in range(10):
        verts.append(Vertex(attributes={'i': i}))
    #0,1, 2, 3, 4, 5, 6, 7, 8, 9
    q, r, s, t, u, v, w, x, y, z = verts
    adj = {
            q: [s, t, w],
            r: [u, y],
            s: [v],
            t: [x, y],
            u: [y],
            v: [w],
            x: [z],
            y: [q],
            z: [x],
        }
    uni = adjlist.load_adj_dict(adj, DirectedEdge)
    assert len(uni.vertices) == 10, "BFS graph setup wrong # verts??"
    return uni, verts

# everything except 1 and 4 should be findable from the starting vertex
bfs_searchdat = [[i, True] for i in range(10)]
bfs_searchdat[1][1] = False
bfs_searchdat[4][1] = False

@pytest.mark.parametrize("target,find", bfs_searchdat)
def test_bfs_search_for(graph, target, find):
    uni, answers = graph
    search = breadthfirst.bfs(uni, answers[0], 'i', target)
   
    if find:
        assert search.i == target, f"BFS found wrong answer -- i = {search.i}"
    else:
        assert search is None, "BFS found wrong answer -- {search} ??"

# test the odd / edge cases

def test_bfs_empty():
    uni = Universe()
    start = None
    search = breadthfirst.bfs(uni, start, 'i', 8)
    assert search is None, "BFS did not return None on empty universe!"

def test_bfs_nonuniverse_vert(graph):
    uni, verts = graph
    extra = Vertex(attributes={'i': -1})

    with pytest.raises(ValueError):
        search = breadthfirst.bfs(uni, extra, 'i', 7)

def test_bfs_search_for_nonexistent(graph):
    uni, verts = graph
    search = breadthfirst.bfs(uni, verts[0], 'i', -1)
    assert search is None, f"BFS found an answer when shouldn't: i={search.i}"

def test_bfs_search_out_of_uni(graph):
    uni, uverts = graph
    extra = Vertex(attributes={'i': -1})
    explicit.link_undirected(uverts[6], extra)
    search = breadthfirst.bfs(uni, uverts[0], 'i', -1)
    assert search is None, f"BFS found an answer when shouldn't: i={search.i}"

def test_bfs_search_wrong_attr(graph):
    uni, verts = graph
    del verts[6].i
    verts[6].j = 10
    search = breadthfirst.bfs(uni, verts[0], 'i', 10)
    right = breadthfirst.bfs(uni, verts[0], 'j', 10)
    assert search is None, f"BFS found an answer when shouldn't: i={search.i}"
    assert right is verts[6], "BFS did not find right answer!"

