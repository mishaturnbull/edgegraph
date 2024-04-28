#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.plaintext module.
"""

from edgegraph.structure import Universe
from edgegraph.traversal import helpers
from edgegraph.output import plaintext

def test_basic_render_sorted(graph_clrs09_22_6):
    """
    Test the basic render approach with a sort and render function.
    """
    uni, _ = graph_clrs09_22_6
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

def test_basic_render_nonsorted(graph_clrs09_22_6):
    """
    Test the basic render approach without a sort function, but with a render
    function.
    """
    uni, verts = graph_clrs09_22_6
    render = plaintext.basic_render(uni, rfunc=lambda v: v.i)

    for line in render.splitlines():
        start = verts[int(line.split(' ')[0])]
        out = set(verts[int(n.replace(',', ''))] for n in
                  line.split('->')[1].split(' ') if len(n))
        assert set(helpers.neighbors(start)) == out

def test_basic_render_norender(graph_clrs09_22_6):
    """
    Test the basic render approach with a sort function but no render function.
    """
    uni, verts = graph_clrs09_22_6
    render = plaintext.basic_render(uni, sort=lambda v: v.i)
    lines = render.splitlines()

    for i, vert in enumerate(verts):
        line = lines[i]
        assert line.startswith(repr(vert))

        nbs = sorted(helpers.neighbors(vert), key=lambda v: v.i)
        nbs = [repr(v) for v in nbs]
        assert all(nb in line for nb in nbs)

def test_basic_render_empty():
    """
    Test the basic render function with an empty universe.
    """
    u = Universe()
    render = plaintext.basic_render(u)
    assert render is None

