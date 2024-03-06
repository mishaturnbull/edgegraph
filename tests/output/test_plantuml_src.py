#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.plantuml module.
"""

import pytest
from edgegraph.structure import Vertex, DirectedEdge, Universe
from edgegraph.builder import adjlist
from edgegraph.traversal import helpers
from edgegraph.output import plantuml

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

def test_plantuml_quick_nonempty(graph):
    src = plantuml.render_to_plantuml_src(graph[0],
            plantuml.PLANTUML_RENDER_OPTIONS)
    assert len(src) > 0, "PlantUML source render returns empty!"

def test_plantuml_out_file_format():
    with pytest.raises(ValueError):
        plantuml.render_to_image("", "out.not-a-png")

    with pytest.raises(ValueError):
        plantuml.render_to_image("", "out.jpeg")

