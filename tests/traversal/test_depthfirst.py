#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for traversal.depthfirst module.
"""

import itertools
import pytest
from edgegraph.structure import (Vertex, TwoEndedLink, DirectedEdge,
        UnDirectedEdge, Universe)
from edgegraph.traversal import depthfirst
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
            w: [s],
            x: [z],
            y: [q],
            z: [x],
        }
    uni = adjlist.load_adj_dict(adj, DirectedEdge)
    assert len(uni.vertices) == 10, "DFS graph setup wrong # verts??"
    return uni, verts

###############################################################################
# traversals!

dftr_data = [
        [0, [0, 2, 5, 6, 3, 7, 9, 8]],
        [1, [1, 4, 8, 0, 2, 5, 6, 3, 7, 9]],
        [2, [2, 5, 6]],
        [3, [3, 7, 9, 8, 0, 2, 5, 6]],
        [4, [4, 8, 0, 2, 5, 6, 3, 7, 9]],
        [5, [5, 6, 2]],
        [6, [6, 2, 5]],
        [7, [7, 9]],
        [8, [8, 0, 2, 5, 6, 3, 7, 9]],
        [9, [9, 7]],
        ]

@pytest.mark.parametrize("start,expected", dftr_data)
def test_dftr_from(graph, start, expected):
    uni, verts = graph
    trav = depthfirst.dft_recursive(uni, verts[start])
    vals = [v.i for v in trav]

    assert vals == expected, f"dftr bad! {vals}"

dfti_data = [
        [0, [0, 6, 2, 5, 3, 8, 7, 9]],
        [1, [1, 8, 0, 6, 2, 5, 3, 7, 9, 4]],
        [2, [2, 5, 6]],
        [3, [3, 8, 0, 6, 2, 5, 7, 9]],
        [4, [4, 8, 0, 6, 2, 5, 3, 7, 9]],
        [5, [5, 6, 2]],
        [6, [6, 2, 5]],
        [7, [7, 9]],
        [8, [8, 0, 6, 2, 5, 3, 7, 9]],
        [9, [9, 7]],
        ]

@pytest.mark.parametrize("start,expected", dfti_data)
def test_dfti_from(graph, start, expected):
    uni, verts = graph
    trav = depthfirst.dft_iterative(uni, verts[start])
    vals = [v.i for v in trav]

    assert vals == expected, f"{vals}"

# test odd / edge cases
travs = [
        depthfirst.dft_recursive,
        depthfirst.dft_iterative,
    ]

@pytest.mark.parametrize("func", travs)
def test_dft_empty(func):
    uni = Universe()
    start = None
    res = func(uni, start)
    assert res is None, f"{func} did not return None on empty universe!"

@pytest.mark.parametrize("func", travs)
def test_dft_nonuniverse(graph, func):
    uni, verts = graph
    extra = Vertex(attributes={'i': -1})

    with pytest.raises(ValueError):
        search = func(uni, extra)

@pytest.mark.parametrize("func", travs)
def test_dft_trav_out_of_uni(graph, func):
    uni, verts = graph
    extra = Vertex(attributes={'i': -1})
    explicit.link_undirected(verts[6], extra)
    trav = func(uni, verts[0])
    vals = [v.i for v in trav]
    assert -1 not in vals, f"{func} found an out-of-universe vert!"

# make sure they do the same thing every time, given the same inputs.  this was
# an issue during development due to the use of unordered sets
#
# need to be careful here that we only care that things are the same *between
# runs*, and not match any given order, as there are multiple correct answers
# for a DFT of any given graph
@pytest.mark.parametrize("func", travs)
def test_dft_deterministic(graph, func):
    uni, verts = graph
    prev = None
    ans = None
    for i in range(1000):
        if prev is None:
            continue

        ans = func(graph, verts[0])
        assert ans == prev, "dft_recursive is not deterministic!"
        prev = ans

###############################################################################
# searches!

searches = [
        depthfirst.dfs_recursive,
        depthfirst.dfs_iterative,
        ]
dfs_data = [[i, True] for i in range(10)]
dfs_data[1][1] = False
dfs_data[4][1] = False

@pytest.mark.parametrize("func,sdat", itertools.product(searches, dfs_data))
def test_dfs_search_for(graph, func, sdat):
    uni, verts = graph
    target, find = sdat
    search = func(uni, verts[0], 'i', target)

    if find:
        assert search.i == target, "wrong!"
    else:
        assert search is None, "also wrong!"

@pytest.mark.parametrize("func", searches)
def test_dfs_empty(func):
    uni = Universe()
    start = None
    res = func(uni, start, 'i', 15)
    assert res is None, f"{func} did not return None on empty universe!"

@pytest.mark.parametrize("func", searches)
def test_dfs_nonuniverse(graph, func):
    uni, verts = graph
    extra = Vertex(attributes={'i': -1})

    with pytest.raises(ValueError):
        search = func(uni, extra, 'i', -1)

@pytest.mark.parametrize("func", searches)
def test_dfs_search_out_of_uni(graph, func):
    uni, verts = graph
    extra = Vertex(attributes={'i': -1})
    explicit.link_undirected(verts[6], extra)
    search = func(uni, verts[0], 'i', -1)
    assert search is None, f"{func} found vertex out of universe!"

@pytest.mark.parametrize("func", searches)
def test_bfs_search_wrong_attr(graph, func):
    uni, verts = graph
    del verts[6].i
    verts[6].j = 10
    search = func(uni, verts[0], 'i', 10)
    right = func(uni, verts[0], 'j', 10)
    assert search is None, f"{func} found an answer when shouldn't: i={search.i}"
    assert right is verts[6], f"{func} did not find right answer!"

