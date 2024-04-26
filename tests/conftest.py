#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provides fixtures and PyTest hooks for all testing usage.

See:
https://docs.pytest.org/en/7.1.x/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import pytest

from edgegraph.structure import Vertex, DirectedEdge
from edgegraph.builder import adjlist

@pytest.fixture
def graph_clrs09_22_6():
    """
    The graph generated in this function is taken from [CLRS09]_, figure 22.6.

    .. uml::

       object q
       object r
       object s
       object t
       object u
       object v
       object w
       object x
       object y
       object z

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
    """
    verts = [Vertex(attributes={'i': i}) for i in range(10)]
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
    return uni, verts



