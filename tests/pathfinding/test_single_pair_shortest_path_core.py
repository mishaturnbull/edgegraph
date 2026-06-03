# -*- coding: utf-8 -*-

"""
Unit tests for the core functionality (dispatch, API) of the SPSP module.
"""

import itertools

import pytest

from edgegraph.builder import explicit
from edgegraph.pathfinding import shortestpath
from edgegraph.structure import Vertex
from edgegraph.traversal import helpers


@pytest.mark.parametrize("method", shortestpath.METHODS)
def test_spsp_smoketest(graph_clrs09_22_6, method):
    """
    Smoke-test single-pair-shortest-path for each method.

    This does basically nothing except verify that all the advertised methods
    are available and do not (immediately) crash.  Further verification of
    their correctness will be performed in a separate test.
    """

    uni, verts = graph_clrs09_22_6

    # start at vert R (1) and pathfind over to W (6)
    start = verts[1]
    dest = verts[6]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=None, method=method
    )

    path, dist = sol

    assert path == [verts[1], verts[8], verts[0], verts[6]]
    assert dist == 3


def test_spsp_unknown_method(graph_clrs09_22_6):
    """
    Ensure the SPSP function does not allow unknown methods.
    """
    uni, verts = graph_clrs09_22_6
    start = verts[1]
    dest = verts[0]

    with pytest.raises(NotImplementedError):
        shortestpath.single_pair_shortest_path(
            # these arguments are all fine -- ensure the only possibility of
            # failure is from the solver name
            uni,
            start,
            dest,
            weightfunc=None,
            # despite "Dijkstra" being here, this is not valid...
            method="I would like you to use Dijkstra's method, please.",
        )


@pytest.mark.parametrize("method", shortestpath.METHODS)
def test_spsp_vert_not_found(graph_clrs09_22_6, method):
    """
    Ensure the desired ``(None, None)`` is returned if there is no available
    solution for the given pair (i.e., ``v`` is unreachable from ``u``).

    This case is for a vertex that has no edges reaching to it.
    """
    uni, verts = graph_clrs09_22_6
    start = verts[1]
    dest = Vertex()

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=None, method=method
    )

    path, dist = sol

    assert path is None, "SPSP found a path for an impossible solution!"
    assert dist is None, "SPSP found a dist for an impossible solution!"


@pytest.mark.parametrize("method", shortestpath.METHODS)
def test_spsp_no_valid_path(graph_clrs09_22_6, method):
    """
    Ensure the desired ``(None, None)`` is returned if there is no available
    solution -- but they are connected (i.e., edges point the wrong way, etc).

    This case is for a vertex that is connected, but the edge directionality
    prevents traversing to it.
    """
    uni, verts = graph_clrs09_22_6
    start = verts[8]
    dest = verts[1]

    sol = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=None, method=method
    )

    path, dist = sol

    assert path is None, "SPSP found a path for an impossible solution!"
    assert dist is None, "SPSP found a dist for an impossible solution!"


def test_spsp_arg_validation(graph_clrs09_22_6):
    """
    Confirm the SPSP argument validation and early-return cases.
    """
    uni, verts = graph_clrs09_22_6

    # test start == dest case
    sol = shortestpath.single_pair_shortest_path(
        uni, verts[1], verts[1], weightfunc=None, method="dijkstra"
    )

    path, dist = sol

    assert path == [
        verts[1],
        verts[1],
    ], "SPSP returned incorrect path for start == dest"
    assert dist == 0, "Should never have distance between a vertex and itself"

    # test start is None case
    with pytest.raises(ValueError, match="path searching with start=None"):
        sol = shortestpath.single_pair_shortest_path(
            uni, None, verts[1], weightfunc=None, method="dijkstra"
        )


@pytest.mark.parametrize("method", shortestpath.METHODS)
def test_spsp_uni_none(graph_clrs09_22_6, method):
    """
    Ensure the shortest path solvers correctly respect the universe=None and
    universe!=None cases.
    """
    uni, verts = graph_clrs09_22_6
    start = verts[1]
    dest = verts[9]

    # create another vertex which connects the start and dest in a much shorter
    # fashion, but is not a member of the universe
    extra = Vertex(attributes={"i": 10})
    explicit.link_directed(start, extra)
    explicit.link_directed(extra, dest)

    # with uni=uni, we should NOT hop over the extra vertex, as it is not a
    # member of the universe
    path, dist = shortestpath.single_pair_shortest_path(
        uni, start, dest, weightfunc=None, method=method
    )

    assert path == [
        start,
        verts[8],
        verts[0],
        verts[3],
        verts[7],
        dest,
    ], "SPSP uni=uni did not find correct path"
    assert dist == 5, "SPSP uni=uni got the wrong distance"

    # with uni=None, we should take the shortcut
    path, dist = shortestpath.single_pair_shortest_path(
        None, start, dest, weightfunc=None, method=method
    )

    assert path == [
        start,
        extra,
        dest,
    ], "SPSP uni=None did not find correct path"
    assert dist == 2, "SPSP uni=None got the wrong distance"


###############################################################################
# Test for pathfinding correctness
###############################################################################

spsp_data = [
    # format of the data is start, dest, [path], dist
    [0, 6, [0, 6], 1],
    [1, 8, [1, 8], 1],
    [1, 6, [1, 8, 0, 6], 3],
    [0, 0, [0, 0], 0],
    [9, 9, [9, 9], 0],
    [5, 2, [5, 6, 2], 2],
    [1, 7, [1, 8, 0, 3, 7], 4],
    [1, 9, [1, 8, 0, 3, 7, 9], 5],
]


@pytest.mark.parametrize(
    ("method", "data"), itertools.product(shortestpath.METHODS, spsp_data)
)
def test_spsp_correct_defaults(graph_clrs09_22_6, method, data):
    """
    Test the single-pair shortest path solvers for correctness.
    """
    uni, verts = graph_clrs09_22_6

    path, dist = shortestpath.single_pair_shortest_path(
        uni,
        verts[data[0]],
        verts[data[1]],
        method=method,
    )

    # verify path answer
    for pathidx, vertidx in enumerate(data[2]):
        entry_in_path = path[pathidx]
        vertex = verts[vertidx]

        assert entry_in_path is vertex, f"solver got bad step; path = {path}"

    # verify distance answer
    assert dist is data[3], f"{method} solver got dist wrong"


def _getweight(u, v):
    """
    Testing purposes only - access edge weights from the weighted-graph
    fixtures.
    """
    edges = helpers.find_links(u, v)
    weight = float("inf")
    for e in edges:
        weight = min(weight, e.weight)
    return weight


spsp_data_weighted = [
    # graph fixture name, start, dest, [path], dist
    ["graph_cheapest_is_shortest", 0, 5, [0, 5], 4],
    ["graph_cheapest_is_shortest", 1, 5, [1, 2, 3, 4, 5], 4],
    ["graph_cheapest_is_shortest", 2, 5, [2, 3, 4, 5], 3],
    ["graph_cheapest_is_shortest", 0, 4, [0, 1, 2, 3, 4], 4],
    ["graph_cheapest_is_longest", 0, 5, [0, 1, 2, 3, 4, 5], 15],
    ["graph_cheapest_is_longest", 1, 5, [1, 2, 3, 4, 5], 2 + 3 + 4 + 5],
    ["graph_cheapest_is_longest", 2, 5, [2, 3, 4, 5], 3 + 4 + 5],
    ["graph_cheapest_is_longest", 0, 4, [0, 1, 2, 3, 4], 1 + 2 + 3 + 4],
]


@pytest.mark.parametrize(
    ("method", "data"),
    itertools.product(shortestpath.METHODS, spsp_data_weighted),
)
def test_spsp_correct_weighted(request, method, data):
    """
    Test the single-pair shortest path solvers for correctness in a
    non-standard weight environment.
    """
    uni, verts = request.getfixturevalue(data[0])
    path, dist = shortestpath.single_pair_shortest_path(
        uni,
        verts[data[1]],
        verts[data[2]],
        weightfunc=_getweight,
        method=method,
    )

    # verify path answer
    for pathidx, vertidx in enumerate(data[3]):
        entry_in_path = path[pathidx]
        vertex = verts[vertidx]

        assert entry_in_path is vertex, f"solver got bad step; path = {path}"

    # verify distance answer
    assert dist is data[4], f"{method} solver got dist wrong"
