#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for traversal.breadthfirst module.
"""

import pytest
from edgegraph.structure import Vertex, Universe
from edgegraph.traversal import breadthfirst
from edgegraph.builder import explicit

# everything except 1 and 4 should be findable from the starting vertex
bfs_searchdat = [[i, True] for i in range(10)]
bfs_searchdat[1][1] = False
bfs_searchdat[4][1] = False


@pytest.mark.parametrize("target,find", bfs_searchdat)
def test_bfs_search_for(graph_clrs09_22_6, target, find):
    """
    Ensure we can find vertices with a breadth-first search.
    """
    uni, answers = graph_clrs09_22_6
    search = breadthfirst.bfs(uni, answers[0], "i", target)

    if find:
        assert search.i == target, f"BFS found wrong answer -- i = {search.i}"
    else:
        assert search is None, "BFS found wrong answer -- {search} ??"


# test the odd / edge cases


def test_bfs_empty():
    """
    Ensure BFS doesn't return anything when the universe is empty.
    """
    uni = Universe()
    start = None
    search = breadthfirst.bfs(uni, start, "i", 8)
    assert search is None, "BFS did not return None on empty universe!"


def test_bfs_nonuniverse_vert(graph_clrs09_22_6):
    """
    Ensure ValueError raised on a starting vertex outside the universe.
    """
    uni, _ = graph_clrs09_22_6
    extra = Vertex(attributes={"i": -1})

    with pytest.raises(ValueError):
        breadthfirst.bfs(uni, extra, "i", 7)


def test_bfs_search_for_nonexistent(graph_clrs09_22_6):
    """
    Ensure we don't find a vertex that doesn't exist.
    """
    uni, verts = graph_clrs09_22_6
    search = breadthfirst.bfs(uni, verts[0], "i", -1)
    assert search is None, f"BFS found an answer when shouldn't: i={search.i}"


def test_bfs_search_out_of_uni(graph_clrs09_22_6):
    """
    Ensure we don't find anything outside of the universe.
    """
    uni, uverts = graph_clrs09_22_6
    extra = Vertex(attributes={"i": -1})
    explicit.link_undirected(uverts[6], extra)
    search = breadthfirst.bfs(uni, uverts[0], "i", -1)
    assert search is None, f"BFS found an answer when shouldn't: i={search.i}"


def test_bfs_search_wrong_attr(graph_clrs09_22_6):
    """
    Ensure we don't find the wrong attribute.
    """
    uni, verts = graph_clrs09_22_6
    del verts[6].i
    verts[6].j = 10
    search = breadthfirst.bfs(uni, verts[0], "i", 10)
    right = breadthfirst.bfs(uni, verts[0], "j", 10)
    assert search is None, f"BFS found an answer when shouldn't: i={search.i}"
    assert right is verts[6], "BFS did not find right answer!"


def test_bfs_none_universe(graph_clrs09_22_6):
    """
    Ensure BFS works with universe = None.
    """
    _, verts = graph_clrs09_22_6
    search = breadthfirst.bfs(None, verts[0], "i", 7)
    assert search is verts[7], "BFS did not find answer when uni=None!"


def test_bfs_finds_first_vertex(graph_clrs09_22_6):
    """
    Ensure BFS finds the starting vertex, if that's what it's given.
    """
    uni, verts = graph_clrs09_22_6
    for vert in verts:
        search = breadthfirst.bfs(uni, vert, "i", vert.i)
        assert search is vert, f"BFS did not identify the starting vertex!"


###############################################################################
# traversal!

# test the overall answer
bft_data = [
    [0, [0, 2, 3, 6, 5, 7, 8, 9]],
    [1, [1, 4, 8, 0, 2, 3, 6, 5, 7, 9]],
    [2, [2, 5, 6]],
    [3, [3, 7, 8, 9, 0, 2, 6, 5]],
    [4, [4, 8, 0, 2, 3, 6, 5, 7, 9]],
    [5, [5, 6, 2]],
    [6, [6, 2, 5]],
    [7, [7, 9]],
    [8, [8, 0, 2, 3, 6, 5, 7, 9]],
    [9, [9, 7]],
]


@pytest.mark.parametrize("start,expected", bft_data)
def test_bft_from(graph_clrs09_22_6, start, expected):
    """
    Make sure traversals work right, starting from any given node.
    """
    uni, verts = graph_clrs09_22_6
    trav = breadthfirst.bft(uni, verts[start])
    vals = [v.i for v in trav]

    assert vals == expected, "BFT gave wrong answer!"


# odd / edge cases


def test_bft_empty():
    """
    Ensure no traversal on an empty universe.
    """
    trav = breadthfirst.bft(Universe(), None)
    assert trav is None, "BFT did not return None on empty universe!"


def test_bft_nonuniverse_vert(graph_clrs09_22_6):
    """
    Ensure starting on a Vertex outside the universe raises an error.
    """
    uni, _ = graph_clrs09_22_6
    extra = Vertex(attributes={"i": -1})

    with pytest.raises(ValueError):
        breadthfirst.bft(uni, extra)


def test_bft_trav_out_of_uni(graph_clrs09_22_6):
    """
    Ensure we don't traverse outside the universe.
    """
    uni, verts = graph_clrs09_22_6
    extra = Vertex(attributes={"i": -1})
    explicit.link_undirected(verts[6], extra)
    trav = breadthfirst.bft(uni, verts[0])
    vals = [v.i for v in trav]
    assert -1 not in vals, "BFT found an out-of-universe vert!"


def test_bft_none_universe(graph_clrs09_22_6):
    """
    Ensure BFT works when universe = None.
    """
    _, verts = graph_clrs09_22_6
    trav = breadthfirst.bft(None, verts[0])
    trav = [v.i for v in trav]
    assert trav == [
        0,
        2,
        3,
        6,
        5,
        7,
        8,
        9,
    ], "BFT did not traverse when uni = None!"


###############################################################################
# stress testing


@pytest.mark.slow
def test_bft_stress(graph_clrs09_22_6):
    """
    Stress-test breadth first traversal.
    """
    uni, verts = graph_clrs09_22_6
    for _ in range(10000):
        trav = breadthfirst.bft(uni, verts[0])
        assert [v.i for v in trav] == bft_data[0][
            1
        ], "BFT traversal wrong in stress-test!"
