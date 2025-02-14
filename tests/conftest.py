#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provides fixtures and PyTest hooks for all testing usage.

See:
https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

from __future__ import annotations

import logging
import pytest

from edgegraph.structure import Universe, Vertex, DirectedEdge
from edgegraph.builder import adjlist, explicit


LOG = logging.getLogger(__name__)


# https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-parametrize
# use strings for the params ("cache" and "nocache") instead of raw booleans
# to improve readability in the test output ("what's this random [True]??")
@pytest.fixture(scope="function", params=["cache", "nocache"], autouse=True)
def enforce_cache_testing(request):
    enable = request.param == "cache"
    Vertex.NEIGHBOR_CACHING = enable

    # reset cache stats and sentinel
    Vertex._QA_NB_INVALID = object()
    Vertex._CACHE_STATS = {}

    yield

    LOG.debug(f"For test case {request.node}:")
    LOG.debug(Vertex.total_cache_stats())


@pytest.fixture
def graph_clrs09_22_6() -> tuple[Universe, list[Vertex]]:
    """
    The graph generated in this function is taken from [CLRS09]_, figure 22.6.

    .. uml::

       object q {
       0
       }
       object r {
       1
       }
       object s {
       2
       }
       object t {
       3
       }
       object u {
       4
       }
       object v {
       5
       }
       object w {
       6
       }
       object x {
       7
       }
       object y {
       8
       }
       object z {
       9
       }

       q --> s
       q --> t
       q --> w
       r --> u
       r --> y
       s --> v
       t --> x
       t --> y
       u --> y
       v --> w
       w --> s
       x --> z
       y --> q
       z --> x

    :return: a two-tuple containing a
       :py:class:`~edgegraph.structure.universe.Universe` of the graph, and a
       :py:class:`list` of all :py:class:`~edgegraph.structure.vertex.Vertex`
       objects.  The order of this list is shown by the numbers in the above
       diagram; the number of a vertex is its index in the list.
    """
    verts = [Vertex(attributes={"i": i}) for i in range(10)]
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
    return uni, verts


@pytest.mark.fixture
def graph_clrs09_22_8() -> tuple[Universe, list[Vertex]]:
    """
    The graph generated by this function is taken from [CLRS09]_, figure 22.8.

    .. uml::

       object m {
       0
       }
       object n {
       1
       }
       object o {
       2
       }
       object p {
       3
       }
       object q {
       4
       }
       object r {
       5
       }
       object s {
       6
       }
       object t {
       7
       }
       object u {
       8
       }
       object v {
       9
       }
       object w {
       10
       }
       object x {
       11
       }
       object y {
       12
       }
       object z {
       13
       }

       m --> q
       m --> r
       m --> x
       n --> q
       n --> u
       n --> o
       o --> r
       o --> v
       o --> s
       p --> o
       p --> s
       p --> z
       q --> t
       r --> u
       r --> y
       s --> r
       u --> t
       v --> x
       v --> w
       w --> z
       y --> v

    :return: a two-tuple containing a
       :py:class:`~edgegraph.structure.universe.Universe` of the graph, and a
       :py:class:`list` of all :py:class:`~edgegraph.structure.vertex.Vertex`
       objects.  The order of this list is shown by the numbers in the above
       diagram; the number of a vertex is its index in the list.
    """
    verts = [Vertex(attributes={"i": i}) for i in range(14)]
    m, n, o, p, q, r, s, t, u, v, w, x, y, z = verts
    adj = {
        m: [q, r, x],
        n: [q, u, o],
        o: [r, v, s],
        p: [o, s, z],
        q: [t],
        r: [u, y],
        s: [r],
        u: [t],
        v: [x, w],
        w: [z],
        y: [v],
    }
    uni = adjlist.load_adj_dict(adj, DirectedEdge)
    return uni, verts


@pytest.fixture
def complete_graph_1k_directed():
    """
    Return a complete graph with directed edges of 1,000 nodes.

    In this graph, every vertex is linked to every other (including itself)
    with a directed edge.
    """

    uni = Universe()
    verts = [Vertex(attributes={"i": i}, universes=[uni]) for i in range(1000)]
    for v in verts:
        for u in verts:
            explicit.link_directed(v, u)

    return uni, verts


@pytest.fixture
def complete_graph_1k_undirected():
    """
    Return a complete graph with undirected edges of 1,000 nodes.
    """

    uni = Universe()
    verts = [Vertex(attributes={"i": i}, universes=[uni]) for i in range(1000)]
    for i, v in enumerate(verts[::-1]):
        for u in verts[i + 1 :]:
            explicit.link_undirected(v, u)

    return uni, verts
