#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.twoendedlink.TwoEndedLink class.
"""

import logging
import time
import pytest
from edgegraph.structure import (
    Vertex,
    TwoEndedLink,
    DirectedEdge,
    UnDirectedEdge,
)
from edgegraph.traversal import helpers
from edgegraph.builder import adjlist, explicit

# C1803 is use-implicit-booleaness-not-comparison
# however, the caes it wants to correct in here are like ``assert nb == []``,
# which, in the context of the text, expresses intent much more clearly than
# ``assert not nb``.  so, shut up!
# C0115 is missing-class-docstring
# happens where we want to subclass Vertex or TwoEndedLink or something.  for
# test applications, full class docstrings aren't necessary
# W0613 is unused-argument
# test parameters for filterfunc()'s.  for testing purposes, some parameters
# are ignored.
# pylint: disable=C1803, C0115, W0613

LOG = logging.getLogger(__name__)


def test_neighbors_undirected():
    """
    Ensure the neighbors function works with undirected edges.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
        v[0]: [v[1], v[2], v[3]],
    }
    nb = helpers.neighbors(v[0])
    assert nb == [], "neighbors before linking!"

    adjlist.load_adj_dict(adj, UnDirectedEdge)

    nb = helpers.neighbors(v[0])
    assert nb == [v[1], v[2], v[3]], "neighbors returned wrong!"


def test_neighbors_directed():
    """
    Ensure neighbors function is sensitive to direction of edges.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
        v[0]: [v[1]],
        v[1]: [v[2]],
    }
    adjlist.load_adj_dict(adj, DirectedEdge)

    v0nb = helpers.neighbors(v[0], direction_sensitive=helpers.DIR_SENS_FORWARD)
    v1nb = helpers.neighbors(v[1], direction_sensitive=helpers.DIR_SENS_FORWARD)

    assert v0nb == [v[1]], "v0 neighbors incorrect!"
    assert v1nb == [v[2]], "v1 neighbors incorrect!"


def test_neighbors_directed_nonsensitive():
    """
    Ensure neighbors function direction sensitivity can be turned off.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
        v[0]: [v[1]],
        v[1]: [v[2]],
    }
    adjlist.load_adj_dict(adj, DirectedEdge)

    v0nb = helpers.neighbors(v[0], direction_sensitive=helpers.DIR_SENS_ANY)
    v1nb = helpers.neighbors(v[1], direction_sensitive=helpers.DIR_SENS_ANY)

    assert v0nb == [v[1]], "v0 neighbors incorrect!"
    assert v1nb == [v[0], v[2]], "v1 neighbors incorrect!"


def test_neighbors_directed_backwards():
    """
    Ensure neighbors function direction sensitivity works backwards.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
        v[0]: [v[1]],
        v[1]: [v[2]],
    }
    adjlist.load_adj_dict(adj, DirectedEdge)

    v0nb = helpers.neighbors(
        v[0], direction_sensitive=helpers.DIR_SENS_BACKWARD
    )
    v1nb = helpers.neighbors(
        v[1], direction_sensitive=helpers.DIR_SENS_BACKWARD
    )
    v2nb = helpers.neighbors(
        v[2], direction_sensitive=helpers.DIR_SENS_BACKWARD
    )

    assert v0nb == [], "v0 neighbors incorrect!"
    assert v1nb == [v[0]], "v1 neighbors incorrect!"
    assert v2nb == [v[1]], "v2 neighbors incorrect!"


def test_neighbors_unknown_link_type():
    """
    Ensure neighbors function handles unknown edge types as the caller desires.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
        v[0]: [v[1]],
        v[1]: [v[2]],
    }
    adjlist.load_adj_dict(adj, TwoEndedLink)

    with pytest.raises(NotImplementedError):
        helpers.neighbors(
            v[0],
            direction_sensitive=helpers.DIR_SENS_FORWARD,
            unknown_handling=helpers.LNK_UNKNOWN_ERROR,
        )

    v0nb1 = helpers.neighbors(
        v[0],
        direction_sensitive=helpers.DIR_SENS_FORWARD,
        unknown_handling=helpers.LNK_UNKNOWN_NEIGHBOR,
    )
    v0nb2 = helpers.neighbors(
        v[0],
        direction_sensitive=helpers.DIR_SENS_FORWARD,
        unknown_handling=helpers.LNK_UNKNOWN_NONNEIGHBOR,
    )

    assert v0nb1 == [v[1]], "LNK_UNKNOWN_NEIGHBOR behavior wrong!"
    assert v0nb2 == [], "LNK_UNKNOWN_NONNEIGHBOR behavior wrong!"


def test_neighbors_unknown_link_type_backwards():
    """
    Ensure neighbors function handles unknown edge types when in backwards
    mode.
    """
    v = [Vertex(), Vertex(), Vertex(), Vertex()]
    adj = {
        v[0]: [v[1]],
        v[1]: [v[2]],
    }
    adjlist.load_adj_dict(adj, TwoEndedLink)

    with pytest.raises(NotImplementedError):
        helpers.neighbors(
            v[0],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            unknown_handling=helpers.LNK_UNKNOWN_ERROR,
        )

    v0nb1 = helpers.neighbors(
        v[0],
        direction_sensitive=helpers.DIR_SENS_BACKWARD,
        unknown_handling=helpers.LNK_UNKNOWN_NEIGHBOR,
    )
    v0nb2 = helpers.neighbors(
        v[0],
        direction_sensitive=helpers.DIR_SENS_BACKWARD,
        unknown_handling=helpers.LNK_UNKNOWN_NONNEIGHBOR,
    )

    assert v0nb1 == [v[1]], "LNK_UNKNOWN_NEIGHBOR behavior wrong!"
    assert v0nb2 == [], "LNK_UNKNOWN_NONNEIGHBOR behavior wrong!"


def test_neighbors_filter_func_subclass_directededge():
    """
    Ensure the neighbors function filterfunc works in a vertex application.
    """

    class VT1(Vertex):
        pass

    class VT2(VT1):
        pass

    #       0         1        2      3      4     5
    v = [Vertex(), Vertex(), VT1(), VT1(), VT2(), VT2()]
    adj = {
        v[0]: [v[1], v[2], v[4]],
        v[2]: [v[0], v[3], v[4]],
        v[4]: [v[0], v[2], v[5]],
    }
    adjlist.load_adj_dict(adj, DirectedEdge)

    def filterfunc(e, v2):
        return isinstance(v2, VT1)

    nb1 = set(helpers.neighbors(v[0], filterfunc=filterfunc))
    assert nb1 == {v[2], v[4]}, "Neighbors filterfunc gave wrong answer"

    nb2 = set(helpers.neighbors(v[2], filterfunc=filterfunc))
    assert nb2 == {v[3], v[4]}, "Neighbors filterfunc gave wrong answer"

    nb3 = set(helpers.neighbors(v[4], filterfunc=filterfunc))
    assert nb3 == {v[2], v[5]}, "Neighbors filterfunc gave wrong answer"


def test_neighbors_filter_func_subclass_nondirected():
    """
    Ensure the neighbors function filterfunc works in a vertex and direction
    non-sensitive application.
    """

    class VT1(Vertex):
        pass

    class VT2(VT1):
        pass

    #       0         1        2      3      4     5
    v = [Vertex(), Vertex(), VT1(), VT1(), VT2(), VT2()]
    adj = {
        v[0]: [v[1], v[2], v[4]],
        v[1]: [v[0], v[2], v[4]],
        v[2]: [v[0], v[3], v[4]],
        v[3]: [v[0], v[2], v[4]],
        v[4]: [v[0], v[2], v[5]],
        v[5]: [v[0], v[2], v[4]],
    }
    adjlist.load_adj_dict(adj, DirectedEdge)

    def filterfunc(e, v2):
        return isinstance(v2, VT1)

    nb1 = set(
        helpers.neighbors(
            v[0],
            direction_sensitive=helpers.DIR_SENS_ANY,
            filterfunc=filterfunc,
        )
    )
    assert nb1 == {
        v[2],
        v[3],
        v[4],
        v[5],
    }, "Neighbors filterfunc gave wrong answer"

    nb2 = set(
        helpers.neighbors(
            v[2],
            direction_sensitive=helpers.DIR_SENS_ANY,
            filterfunc=filterfunc,
        )
    )
    assert nb2 == {v[3], v[4], v[5]}, "Neighbors filterfunc gave wrong answer"

    nb3 = set(
        helpers.neighbors(
            v[4],
            direction_sensitive=helpers.DIR_SENS_ANY,
            filterfunc=filterfunc,
        )
    )
    assert nb3 == {v[2], v[3], v[5]}, "Neighbors filterfunc gave wrong answer"


def test_neighbors_filter_func_subclass_undirected():
    """
    Ensure the neighbors function filterfunc works in a vertex and
    undirectededge application.
    """

    class VT1(Vertex):
        pass

    class VT2(VT1):
        pass

    #       0         1        2      3      4     5
    v = [Vertex(), Vertex(), VT1(), VT1(), VT2(), VT2()]
    adj = {
        v[0]: [v[1], v[2], v[4]],
        v[1]: [v[0], v[2], v[4]],
        v[2]: [v[0], v[3], v[4]],
        v[3]: [v[0], v[2], v[4]],
        v[4]: [v[0], v[2], v[5]],
        v[5]: [v[0], v[2], v[4]],
    }
    adjlist.load_adj_dict(adj, UnDirectedEdge)

    def filterfunc(e, v2):
        return isinstance(v2, VT1)

    nb1 = set(
        helpers.neighbors(v[0], direction_sensitive=True, filterfunc=filterfunc)
    )
    assert nb1 == {
        v[2],
        v[3],
        v[4],
        v[5],
    }, "Neighbors filterfunc gave wrong answer"

    nb2 = set(
        helpers.neighbors(v[2], direction_sensitive=True, filterfunc=filterfunc)
    )
    assert nb2 == {v[3], v[4], v[5]}, "Neighbors filterfunc gave wrong answer"

    nb3 = set(
        helpers.neighbors(v[4], direction_sensitive=True, filterfunc=filterfunc)
    )
    assert nb3 == {v[2], v[3], v[5]}, "Neighbors filterfunc gave wrong answer"


def test_neighbors_filter_func_subclass_directed_backwards():
    class VT1(Vertex):
        pass

    class VT2(VT1):
        pass

    #       0         1        2      3      4     5
    v = [Vertex(), Vertex(), VT1(), VT1(), VT2(), VT2()]
    adj = {
        v[0]: [v[1], v[2], v[4]],
        v[1]: [v[0], v[2], v[4]],
        v[2]: [v[0], v[3], v[4]],
        v[3]: [v[0], v[2], v[4]],
        v[4]: [v[0], v[2], v[5]],
        v[5]: [v[0], v[2], v[4]],
    }
    adjlist.load_adj_dict(adj, DirectedEdge)

    def filterfunc(e, v2):
        return isinstance(v2, VT1)

    nb1 = set(
        helpers.neighbors(
            v[0],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=filterfunc,
        )
    )
    nb2 = set(
        helpers.neighbors(
            v[2],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=filterfunc,
        )
    )
    nb3 = set(
        helpers.neighbors(
            v[4],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=filterfunc,
        )
    )

    assert nb1 == {v[2], v[3], v[4], v[5]}
    assert nb2 == {v[3], v[4], v[5]}
    assert nb3 == {v[2], v[3], v[5]}


def test_neighbors_filter_func_subclass_undirected_backwards():
    class VT1(Vertex):
        pass

    class VT2(VT1):
        pass

    #       0         1        2      3      4     5
    v = [Vertex(), Vertex(), VT1(), VT1(), VT2(), VT2()]
    adj = {
        v[0]: [v[1], v[2], v[4]],
        v[1]: [v[0], v[2], v[4]],
        v[2]: [v[0], v[3], v[4]],
        v[3]: [v[0], v[2], v[4]],
        v[4]: [v[0], v[2], v[5]],
        v[5]: [v[0], v[2], v[4]],
    }
    adjlist.load_adj_dict(adj, UnDirectedEdge)

    def filterfunc(e, v2):
        return isinstance(v2, VT1)

    nb1 = set(
        helpers.neighbors(
            v[0],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=filterfunc,
        )
    )
    nb2 = set(
        helpers.neighbors(
            v[2],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=filterfunc,
        )
    )
    nb3 = set(
        helpers.neighbors(
            v[4],
            direction_sensitive=helpers.DIR_SENS_BACKWARD,
            filterfunc=filterfunc,
        )
    )

    assert nb1 == {v[2], v[3], v[4], v[5]}
    assert nb2 == {v[3], v[4], v[5]}
    assert nb3 == {v[2], v[3], v[5]}


def test_neighbors_bad_directionality(graph_clrs09_22_6):
    """
    Ensure an exception is raised when an invalid value is passed to the
    direction_sensitive argument.
    """

    _, verts = graph_clrs09_22_6
    with pytest.raises(ValueError):
        helpers.neighbors(verts[0], direction_sensitive=-1)


def test_findlinks_smoketest():
    """
    Sanity check of find_links().
    """

    v1, v2 = Vertex(), Vertex()
    e1 = explicit.link_directed(v1, v2)
    e2 = explicit.link_directed(v1, v2)
    e3 = explicit.link_directed(v2, v1)

    t1 = helpers.find_links(v1, v2)
    assert t1 == {e1, e2}, "find_links found the wrong links w/ default args!"
    t2 = helpers.find_links(v2, v1)
    assert t2 == {
        e3,
    }, "find_links found the wrong links w/ default args!"


def test_findlinks_no_links():
    """
    Check that findlinks returns empty when no links should be returned.
    """

    v1, v2 = Vertex(), Vertex()

    t1 = helpers.find_links(v1, v2)
    assert t1 == set(), "find_links returned when there are no links!"

    t2 = helpers.find_links(v1, v2, direction_sensitive=False)
    assert t2 == set(), "find_links returned when there are no links!"

    explicit.link_directed(v2, v1)
    t3 = helpers.find_links(v1, v2)
    assert t3 == set(), "find_links returned when no outbound links!"

    t4 = helpers.find_links(
        v1, v2, direction_sensitive=False, filterfunc=lambda e: False
    )
    assert t4 == set(), "find_links returned with filterfunc-always-false!"


def test_findlinks_tlyf(graph_clrs09_22_6):
    """
    Test findlinks in a graph application (test like you fly).
    """
    _, verts = graph_clrs09_22_6

    s_out = helpers.find_links(verts[2], verts[5])
    assert len(s_out) == 1, "find_links found more than it should've!"
    e1 = list(s_out)[0]
    assert e1.v1 is verts[2], "find_links found the wrong link!"
    assert e1.v2 is verts[5], "find_links found the wrong link!"

    # add another link to the same pathway
    e2 = explicit.link_directed(verts[2], verts[5])
    s_out2 = helpers.find_links(verts[2], verts[5])
    assert len(s_out2) == 2, "find_links did not find right # of links!"
    e2a = (s_out2 - s_out).pop()
    assert e2a is e2, "I am a bad programmer!"
    # no more testing needed -- we already know e2.v1 and e2.v2


def test_findlinks_non_dir_sensitive(graph_clrs09_22_6):
    """
    Test findlinks without direction sensitivity.
    """
    _, verts = graph_clrs09_22_6

    xout = helpers.find_links(verts[7], verts[9], direction_sensitive=True)
    assert len(xout) == 1, "find_links accepted a back-link!"
    e1 = list(xout)[0]
    assert e1.v1 is verts[7], "find_links found the wrong link!"
    assert e1.v2 is verts[9], "find_links found the wrong link!"

    xall = helpers.find_links(verts[7], verts[9], direction_sensitive=False)
    assert len(xall) == 2, "find_links did not accept back-links!"
    e2 = (xall - xout).pop()
    assert e2.v1 is verts[9], "find_links found the wrong link!"
    assert e2.v2 is verts[7], "find_links found the wrong link!"


def test_findlinks_unknown_edge_type():
    """
    Test that findlinks handles unknown edge types according to input.
    """

    class MyLink(TwoEndedLink):
        pass

    v1, v2 = Vertex(), Vertex()
    e = explicit.link_from_to(v1, MyLink, v2)

    links = helpers.find_links(
        v1, v2, unknown_handling=helpers.LNK_UNKNOWN_NONNEIGHBOR
    )
    assert len(links) == 0, "find_links did not treat unknown link as nonnb!"

    links = helpers.find_links(
        v1, v2, unknown_handling=helpers.LNK_UNKNOWN_NEIGHBOR
    )
    assert len(links) == 1, "find_links did not treat unknown link as neighbor!"
    assert links.pop() is e, "find_links found the wrong link!"

    with pytest.raises(NotImplementedError):
        helpers.find_links(v1, v2, unknown_handling=helpers.LNK_UNKNOWN_ERROR)


def test_findlinks_filterfunc():
    """
    Test the filter function attribute of find_links.
    """
    v1, v2 = Vertex(), Vertex()

    e1 = DirectedEdge(v1, v2, attributes={"i": 1})
    e2 = UnDirectedEdge(v1, v2, attributes={"i": 10})

    l1 = helpers.find_links(v2, v1, filterfunc=lambda e: e.i > 5)
    assert l1 == {
        e2,
    }, "find_links did not find the right link!"
    l2 = helpers.find_links(v2, v1, filterfunc=lambda e: e.i < 5)
    assert l2 == set(), "find_links filterfunc didn't filter!"

    l3 = helpers.find_links(v1, v2, filterfunc=lambda e: e.i != 5)
    assert l3 == {e1, e2}, "find_links did not find right links!"
    l4 = helpers.find_links(v2, v1, filterfunc=lambda e: e.i > 5)
    assert l4 == {
        e2,
    }, "find_links did not find the right link!"


@pytest.mark.slow
@pytest.mark.parametrize("n_links", [1, 10, 100, 500])
def test_findlinks_stress(n_links):
    """
    Timing of the find_links function.
    """

    v1, v2 = Vertex(), Vertex()
    edges = []
    for _ in range(n_links):
        edges.append(explicit.link_directed(v1, v2))

    iters = 2500

    t_start = time.monotonic_ns()
    for _ in range(iters):
        helpers.find_links(v1, v2)
    t_end = time.monotonic_ns()

    # analysis
    t_diff = t_end - t_start
    t_per = t_diff / iters

    # convert to seconds
    t_diff /= 1_000_000_000
    t_per /= 1_000_000_000
    LOG.info(f"Total {t_diff} s, avg cycle {t_per} s")
