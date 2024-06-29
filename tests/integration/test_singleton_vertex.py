#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Behavioral tests for singletons and vertices playing together.
"""

from edgegraph.structure import vertex, singleton, universe, directededge
from edgegraph.builder import adjlist
from edgegraph.traversal import breadthfirst, helpers

# this module is all about testing with classes.  the classes we define in this
# file are never exposed to users of edgegraph, nor any of the edgegraph
# module, therefore don't need:
# * any use-case besides their sole existence,
#   * sufficient public methods (R0903, too-few-public-methods)
# * docstrings (C0115, missing-class-docstring),
# * amazing formatting
#   * class Something: pass  will be allowed (C0321, multiple-statements)
#
# therefore:
# pylint: disable=R0903, C0115, C0321


def test_truesingleton_vertex():
    """
    Apply TrueSingleton to a vertex and make sure it doesn't explode.
    """

    class SingleTex(vertex.Vertex, metaclass=singleton.TrueSingleton):
        def __init__(self, i, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.i = i

    st1 = SingleTex(1)
    st2 = SingleTex(1)
    st3 = SingleTex(2)
    assert st1 is st2, "failed on same pos-arg!"
    assert st2 is st3, "failed on different pos-arg!"


def test_semisingleton_vertex():
    """
    Apply semi-singleton to a vertex and make sure it doesn't explode.
    """

    # W0612 --> unused variable.  pylint complains that hashfunc_i is unused;
    #           it most certainly is used.  not sure why this is flagged.
    # W0613 --> unused argument.  necessary here for signature matching.
    # pylint: disable-next=W0612, W0613
    def hashfunc_i(args, kwargs):
        return hash(args[0])

    class SemiSingleTex(
        vertex.Vertex, metaclass=singleton.semi_singleton_metaclass(hashfunc_i)
    ):
        def __init__(self, i, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.i = i

    uni = universe.Universe()
    verts1 = [SemiSingleTex(i, universes=[uni]) for i in range(10)]
    verts2 = [SemiSingleTex(i) for i in range(10)]
    verts3 = [SemiSingleTex(i, attributes={"j": 10 * i}) for i in range(10)]

    for i in range(10):
        assert verts1[i] is verts2[i], f"v1[i] is not v2[i] for i={i}!"
        assert verts2[i] is verts3[i], f"v2[i] is not v3[i] for i={i}!"


def test_semisingleton_vert_graphs():
    """
    Ensure that semi-singleton-ized vertices still work as a graph.
    """

    # W0612 --> unused variable.  pylint complains that hashfunc_i is unused;
    #           it most certainly is used.  not sure why this is flagged.
    # W0613 --> unused argument.  necessary here for signature matching.
    # pylint: disable-next=W0612, W0613
    def hashfunc_i(args, kwargs):
        return hash(args[0])

    class SemiSingleTex(
        vertex.Vertex, metaclass=singleton.semi_singleton_metaclass(hashfunc_i)
    ):
        def __init__(self, i, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.i = i

    # copy/paste of graph_clrs09_22_6, but with semisingleton vertices instead
    # of regular
    verts = [SemiSingleTex(i) for i in range(10)]
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
    uni = adjlist.load_adj_dict(adj, directededge.DirectedEdge)

    for v, nbs in adj.items():
        assert set(helpers.neighbors(v)) == set(
            nbs
        ), f"Vertex {v.i} neighbors are wrong!"

        m = SemiSingleTex(v.i)
        assert m is v, f"semi-singleton failed on {v.i}"
        assert helpers.neighbors(v) == helpers.neighbors(
            m
        ), "semi-singleton broke neighbors lookup"

    trav = breadthfirst.bft(uni, q)
    vals = [v.i for v in trav]

    assert vals == [0, 2, 3, 6, 5, 7, 8, 9], "SemiSingleton broke BFT!!"
