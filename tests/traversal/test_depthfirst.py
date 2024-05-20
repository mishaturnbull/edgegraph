#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for traversal.depthfirst module.
"""

import itertools
import pytest
from edgegraph.structure import Vertex, Universe
from edgegraph.traversal import depthfirst
from edgegraph.builder import explicit

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
def test_dftr_from(graph_clrs09_22_6, start, expected):
    """
    Test traversing from a given starting point, using the recursive
    implementation.
    """
    uni, verts = graph_clrs09_22_6
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
def test_dfti_from(graph_clrs09_22_6, start, expected):
    """
    Test traversing from a given starting point, using the iterative
    implementation.
    """
    uni, verts = graph_clrs09_22_6
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
    """
    Test ValueError is thrown when universe is empty.
    """
    uni = Universe()
    start = None
    with pytest.raises(ValueError):
        func(uni, start)

@pytest.mark.parametrize("func", travs)
def test_dft_nonuniverse(graph_clrs09_22_6, func):
    """
    Test ValueError is thrown when starting vertex is not in the universe.
    """
    uni, _ = graph_clrs09_22_6
    extra = Vertex(attributes={'i': -1})

    with pytest.raises(ValueError):
        func(uni, extra)

@pytest.mark.parametrize("func", travs)
def test_dft_trav_out_of_uni(graph_clrs09_22_6, func):
    """
    Ensure we don't find vertices connected to the graph, but out of the
    universe.
    """
    uni, verts = graph_clrs09_22_6
    extra = Vertex(attributes={'i': -1})
    explicit.link_undirected(verts[6], extra)
    trav = func(uni, verts[0])
    vals = [v.i for v in trav]
    assert -1 not in vals, f"{func} found an out-of-universe vert!"

@pytest.mark.parametrize("func", travs)
def test_dft_deterministic(graph_clrs09_22_6, func):
    """
    Make sure they do the same thing every time, given the same inputs.  this
    was an issue during development due to the use of unordered sets

    Need to be careful here that we only care that things are the same *between
    runs*, and not match any given order, as there are multiple correct answers
    for a DFT of any given graph.
    """
    uni, verts = graph_clrs09_22_6
    prev = None
    ans = func(uni, verts[0])
    for _ in range(1000):
        prev = ans
        ans = func(uni, verts[0])
        assert ans == prev, "dft_recursive is not deterministic!"

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
def test_dfs_search_for(graph_clrs09_22_6, func, sdat):
    """
    Test that we find vertices we should, and don't we shouldn't.

    What?
    """
    uni, verts = graph_clrs09_22_6
    target, find = sdat
    search = func(uni, verts[0], 'i', target)

    if find:
        assert search.i == target, "wrong!"
    else:
        assert search is None, "also wrong!"

# test the odd / edge cases

@pytest.mark.parametrize("func", searches)
def test_dfs_empty(func):
    """
    Ensure ValueError is raised on empty universes.
    """
    uni = Universe()
    start = None
    with pytest.raises(ValueError):
        func(uni, start, 'i', 15)

@pytest.mark.parametrize("func", searches)
def test_dfs_nonuniverse(graph_clrs09_22_6, func):
    """
    Ensure starting at a vertex outside of the universe causes an error.
    """
    uni, _ = graph_clrs09_22_6
    extra = Vertex(attributes={'i': -1})

    with pytest.raises(ValueError):
        func(uni, extra, 'i', -1)

@pytest.mark.parametrize("func", searches)
def test_dfs_search_out_of_uni(graph_clrs09_22_6, func):
    """
    Ensure we don't find a vertex outside of the universe.
    """
    uni, verts = graph_clrs09_22_6
    extra = Vertex(attributes={'i': -1})
    explicit.link_undirected(verts[6], extra)
    search = func(uni, verts[0], 'i', -1)
    assert search is None, f"{func} found vertex out of universe!"

@pytest.mark.parametrize("func", searches)
def test_dfs_search_wrong_attr(graph_clrs09_22_6, func):
    """
    Ensure the attribute selection is working right.
    """
    uni, verts = graph_clrs09_22_6
    del verts[6].i
    verts[6].j = 10
    search = func(uni, verts[0], 'i', 10)
    right = func(uni, verts[0], 'j', 10)
    assert search is None, f"{func} found an answer when shouldn't: i={search.i}"
    assert right is verts[6], f"{func} did not find right answer!"

@pytest.mark.parametrize("func", searches)
def test_dfs_finds_first_vertex(graph_clrs09_22_6, func):
    """
    Ensure we find the starting vertex, if it matches criteria.
    """
    uni, verts = graph_clrs09_22_6
    for vert in verts:
        search = func(uni, vert, 'i', vert.i)
        assert search is vert, f"{func} did not identify the starting vertex!"

###############################################################################
# stress testing

stress_combo = [
        (depthfirst.dft_recursive, dftr_data[0][1]),
        (depthfirst.dft_iterative, dfti_data[0][1]),
        ]

@pytest.mark.slow
@pytest.mark.parametrize("combo", stress_combo)
def test_dft_stress(graph_clrs09_22_6, combo):
    """
    Depth-first traversal stress testing.
    """
    uni, verts = graph_clrs09_22_6
    func, answer = combo
    for _ in range(10000):
        trav = func(uni, verts[0])
        assert [v.i for v in trav] == answer, \
                "Depth-first traversal gave wrong answer in stress test!"

