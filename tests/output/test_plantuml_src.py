#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.plantuml module.
"""

import pytest
import copy
import re
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

def test_plantuml_src_empty():
    uni = Universe()
    src = plantuml.render_to_plantuml_src(uni,
            plantuml.PLANTUML_RENDER_OPTIONS)
    assert src is None

def test_plantuml_quick_nonempty(graph):
    src = plantuml.render_to_plantuml_src(graph[0],
            plantuml.PLANTUML_RENDER_OPTIONS)
    assert len(src) > 0, "PlantUML source render returns empty!"

def test_plantuml_out_file_format():
    with pytest.raises(ValueError):
        plantuml.render_to_image("", "out.not-a-png")

    with pytest.raises(ValueError):
        plantuml.render_to_image("", "out.jpeg")

def test_plantuml_class_option_resolution():
    class A(Vertex): pass
    class B(A): pass
    class C(B): pass
    class D(C): pass

    v = [Vertex(), A(), B(), C(), D()]
    adj = {
            v[0]: [v[0]],
            v[1]: [v[0]],
            v[2]: [v[0]],
            v[3]: [v[0]],
            v[4]: [v[0]],
        }
    uni = adjlist.load_adj_dict(adj, DirectedEdge)
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    opts[A] = copy.deepcopy(opts[Vertex])
    opts[B] = copy.deepcopy(opts[Vertex])
    opts[Vertex]['stereotype_skinparams']['Vertex-STSKP-1'] = "Foo"
    opts[A]['stereotype_skinparams']['A-STSKP-1'] = "Bar"
    opts[B]['stereotype_skinparams']['B-STSKP-1'] = "Baz"

    src = plantuml.render_to_plantuml_src(uni, opts)

    assert "Vertex-STSKP-1<<Vertex>> Foo" in src
    assert "A-STSKP-1<<A>> Bar" in src
    assert "B-STSKP-1<<B>> Baz" in src
    assert "B-STSKP-1<<C>> Baz" in src
    assert "B-STSKP-1<<D>> Baz" in src

def test_plantuml_class_option_resolution_fail(graph):
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    del opts[Vertex]

    with pytest.raises(ValueError):
        src = plantuml.render_to_plantuml_src(graph[0], opts)

def test_plantuml_user_render_func(graph):
    def urf(*args, **kwargs):
        assert len(args) == 2
        assert isinstance(args[0], Vertex)
        assert isinstance(args[1], dict)
        return f"URF {id(args[0])}\n"

    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    opts[Vertex]['user_render_func'] = urf

    src = plantuml.render_to_plantuml_src(graph[0], opts)
    urfcalls = [l for l in src.splitlines() if l.startswith("URF")]
    assert len(urfcalls) == len(graph[1])

def test_plantuml_no_skinparams(graph):
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    del opts['skinparams']
    src = plantuml.render_to_plantuml_src(graph[0], opts)

    hit = re.search(r"skinparam [\w]+ [\w]+", src, re.I)
    assert hit is None

def test_plantuml_no_stereotype_skinparams(graph):
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    del opts[Vertex]['stereotype_skinparams']
    src = plantuml.render_to_plantuml_src(graph[0], opts)

    skps = [
            r"skinparam object {",
            r"BackgroundColor<<Vertex>>",
        ]
    hits = [re.search(skp, src) for skp in skps]
    hit = any(hits)

    assert hit is False

def test_plantuml_title_format(graph):
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    opts[Vertex]['title_format'] = "vertex_nondefault_title_{i}"
    src = plantuml.render_to_plantuml_src(graph[0], opts)

    hits = re.findall(r"object vertex_nondefault_title_\d <<Vertex>> {", src)
    assert len(hits) == len(graph[1])
    assert len(set(hits)) == len(hits)

