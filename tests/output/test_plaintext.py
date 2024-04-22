#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.plaintext module.
"""

import pytest
from edgegraph.structure import Vertex, DirectedEdge, Universe
from edgegraph.builder import adjlist
from edgegraph.traversal import helpers
from edgegraph.output import plaintext

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
    assert len(uni.vertices) == 10, "BFS graph setup wrong # verts??"
    return uni, verts

def test_basic_render_sorted(graph):
    uni, verts = graph
    render = plaintext.basic_render(uni, rfunc=lambda v: v.i,
            sort=lambda v: v.i)
    answer = \
"""0 -> 2, 3, 6
1 -> 4, 8
2 -> 5
3 -> 7, 8
4 -> 8
5 -> 6
6 -> 2
7 -> 9
8 -> 0
9 -> 7"""
    assert render == answer

def test_basic_render_nonsorted(graph):
    uni, verts = graph
    render = plaintext.basic_render(uni, rfunc=lambda v: v.i)

    for line in render.splitlines():
        start = verts[int(line.split(' ')[0])]
        out = set(verts[int(n.replace(',', ''))] for n in
                  line.split('->')[1].split(' ') if len(n))
        assert set(helpers.neighbors(start)) == out

def test_basic_render_norender(graph):
    uni, verts = graph
    render = plaintext.basic_render(uni, sort=lambda v: v.i)
    lines = render.splitlines()

    for i in range(len(verts)):
        vert, line = verts[i], lines[i]
        assert line.startswith(repr(vert))

        nbs = sorted(helpers.neighbors(vert), key=lambda v: v.i)
        nbs = [repr(v) for v in nbs]
        assert all(nb in line for nb in nbs)

def test_basic_render_empty():
    u = Universe()
    render = plaintext.basic_render(u)
    assert render is None

