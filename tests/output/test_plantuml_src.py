#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.plantuml module, specifically focused on PUML sourcecode
generation.
"""

import copy
import re
import pytest
from edgegraph.structure import Vertex, DirectedEdge, Universe
from edgegraph.builder import adjlist
from edgegraph.output import plantuml


def test_plantuml_src_empty():
    """
    Ensure no sourcecode is output from an empty universe.
    """
    uni = Universe()
    src = plantuml.render_to_plantuml_src(uni, plantuml.PLANTUML_RENDER_OPTIONS)
    assert src is None, "plantuml src gen made something out of empty graph!"


def test_plantuml_quick_nonempty(graph_clrs09_22_6):
    """
    Ensure sourcecode is generated from a non-empty universe.
    """
    src = plantuml.render_to_plantuml_src(
        graph_clrs09_22_6[0], plantuml.PLANTUML_RENDER_OPTIONS
    )
    assert len(src) > 0, "PlantUML source render returns empty!"


def test_plantuml_class_option_resolution():
    """
    Exercise the vertex subclass recognition and option application.
    """

    class A(Vertex):
        """Base of inheritence chain."""

    class B(A):
        """Second object in inheritence chain."""

    class C(B):
        """Third object in inheritence chain."""

    class D(C):
        """Last object in inheritence chain."""

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
    opts[Vertex]["stereotype_skinparams"]["Vertex-STSKP-1"] = "Foo"
    opts[A]["stereotype_skinparams"]["A-STSKP-1"] = "Bar"
    opts[B]["stereotype_skinparams"]["B-STSKP-1"] = "Baz"

    src = plantuml.render_to_plantuml_src(uni, opts)

    assert (
        "Vertex-STSKP-1<<Vertex>> Foo" in src
    ), "puml src gen Vertex->Vertex lookup did not work right!"
    assert "A-STSKP-1<<A>> Bar" in src, "puml src gen A->A lookup did not work right!"
    assert "B-STSKP-1<<B>> Baz" in src, "puml src gen B->B lookup did not work right!"
    assert "B-STSKP-1<<C>> Baz" in src, "puml src gen C->B lookup did not work right!"
    assert "B-STSKP-1<<D>> Baz" in src, "puml src gen D->B lookup did not work right!"


def test_plantuml_class_option_resolution_fail(graph_clrs09_22_6):
    """
    Ensure class option resolution raises an error on invalid configuration.
    """
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    del opts[Vertex]

    with pytest.raises(ValueError):
        plantuml.render_to_plantuml_src(graph_clrs09_22_6[0], opts)


def test_plantuml_user_render_func(graph_clrs09_22_6):
    """
    Test the calling of a supplied user render function.
    """

    def urf(*args, **kwargs):
        assert len(args) == 2, "puml src gen URF was not called right!"
        assert isinstance(
            args[0], Vertex
        ), "puml src gen URF was not given vertex object!"
        assert isinstance(
            args[1], dict
        ), "puml src gen URF was not given render options!"
        return f"URF {id(args[0])}\n"

    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    opts[Vertex]["user_render_func"] = urf

    src = plantuml.render_to_plantuml_src(graph_clrs09_22_6[0], opts)
    urfcalls = [l for l in src.splitlines() if l.startswith("URF")]
    assert len(urfcalls) == len(
        graph_clrs09_22_6[1]
    ), "puml src gen URF was not called right number of times!"


def test_plantuml_no_skinparams(graph_clrs09_22_6):
    """
    Ensure no skinparams are produced when none are configured.
    """
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    del opts["skinparams"]
    src = plantuml.render_to_plantuml_src(graph_clrs09_22_6[0], opts)

    hit = re.search(r"skinparam [\w]+ [\w]+", src, re.I)
    assert hit is None, "puml src gen gave skinparams when shouldn't!"


def test_plantuml_no_stereotype_skinparams(graph_clrs09_22_6):
    """
    Ensure no stereotype skinparams are produced when unspecified.
    """
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    del opts[Vertex]["stereotype_skinparams"]
    src = plantuml.render_to_plantuml_src(graph_clrs09_22_6[0], opts)

    skps = [
        r"skinparam object {",
        r"BackgroundColor<<Vertex>>",
    ]
    hits = [re.search(skp, src) for skp in skps]
    hit = any(hits)

    assert hit is False, "puml src gen gave stereotype skinparams when shouldn't!"


def test_plantuml_title_format(graph_clrs09_22_6):
    """
    Ensure the object title format is applied correctly.
    """
    opts = copy.deepcopy(plantuml.PLANTUML_RENDER_OPTIONS)
    opts[Vertex]["title_format"] = "vertex_nondefault_title_{i}"
    src = plantuml.render_to_plantuml_src(graph_clrs09_22_6[0], opts)

    hits = re.findall(r"object vertex_nondefault_title_\d <<Vertex>> {", src)
    assert len(hits) == len(
        graph_clrs09_22_6[1]
    ), "puml src gen output wrong number of objects!"
    assert len(set(hits)) == len(hits), "puml src gen output duplicate object titles!"
