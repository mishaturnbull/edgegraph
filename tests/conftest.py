#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provides fixtures and PyTest hooks for all testing usage.

See:
https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

from __future__ import annotations

import pytest

from edgegraph.structure import Universe, Vertex, DirectedEdge
from edgegraph.builder import adjlist

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
    verts = [Vertex(attributes={'i': i}) for i in range(10)]
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

