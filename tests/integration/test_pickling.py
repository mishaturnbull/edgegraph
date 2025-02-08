#!python3
# -*- coding: utf-8 -*-

"""
Unit tests that ensure all Edgegraph objects are pickleable and unpickleable.
"""

import pickle
import sys
import logging

import dill
import pytest

from edgegraph.structure import singleton, vertex, universe, singleton
from edgegraph.traversal import breadthfirst
from edgegraph.builder import randgraph
from edgegraph.output import nrpickler

# similarly to the singleton tests, this module tests *a lot* of custom
# classes.  the classes defined here are never exposed to users of edgegraph,
# nor any of the edgegraph module, therefore don't need:
# * any use-case besides their sole existence,
#   * sufficient public methods (R0903, too-few-public-methods)
# * docstrings (C0115, missing-class-docstring),
# * amazing formatting
#   * class Something: pass  will be allowed (C0321, multiple-statements)
#
# therefore:
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=multiple-statements

LOG = logging.getLogger(__name__)


def test_p_up_smoketest():
    """
    Quick it's-still-in-dev smoketest for just pickling and unpickling a
    vertex.
    """

    prepickle = randgraph.randgraph()

    serial = nrpickler.dumps(prepickle)
    postpickle = pickle.loads(serial)

    assert prepickle is not postpickle, "same object returned from P/UP"
    assert isinstance(serial, bytes), "pickle didn't pickle!"

    pre_v0 = [v for v in prepickle.vertices if v.i == 0][0]
    trav_pr = [v.i for v in breadthfirst.bft(prepickle, pre_v0)]

    post_v0 = [v for v in postpickle.vertices if v.i == 0][0]
    trav_po = [v.i for v in breadthfirst.bft(postpickle, post_v0)]

    assert trav_pr == trav_po, "traversal order wrong after P/UP"


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_up_large(straightline_graph_1k_directed, protocol):
    """
    Ensure large graphs don't cause recursion errors.
    """

    orig_rcr_depth = sys.getrecursionlimit()
    LOG.debug(f"orig_rcr_depth = {orig_rcr_depth}")

    # set a lower recursion limit than the graph size by a good amount, to
    # ensure we'll hit a recursion limit if there exists any such issues
    sys.setrecursionlimit(500)

    test_rcr_depth = sys.getrecursionlimit()
    LOG.debug(f"test_rcr_depth = {test_rcr_depth}")

    uni, verts = straightline_graph_1k_directed

    try:
        serial = nrpickler.dumps(uni, protocol=protocol)
        postpickle = pickle.loads(serial)

        assert len(uni.vertices) == len(
            postpickle.vertices
        ), "Did not serialize all vertices!"

    finally:
        # ...but also restore the earlier recursion depth for tests which come
        # after us (even in the event of a failure)
        sys.setrecursionlimit(orig_rcr_depth)


class SingleTex(vertex.Vertex, metaclass=singleton.TrueSingleton):
    def __init__(self, i, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = i


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_singleton(protocol):
    """
    Ensure singleton objects can be pickled.
    """

    st1 = SingleTex(1)
    st2 = SingleTex(2)

    serial = nrpickler.dumps([st1, st2], protocol=protocol)
    postpickle = pickle.loads(serial)

    assert postpickle[0].i == 1, "Post-pickle singleton has wrong .i"
    assert postpickle[1].i == 1, "Post-pickle singleton has wrong .i"
    assert postpickle[0] is not st1, "Post-pickle singleton *IS* pre-pickle!"
    assert postpickle[1] is not st2, "Post-pickle singleton *IS* pre-pickle!"
    assert postpickle[0] is postpickle[1], "Post-pickle singletons differ!"
    assert isinstance(
        postpickle[0], SingleTex
    ), "Class defined in module level didn't unpickle to the same"


class MultiTex(vertex.Vertex, metaclass=singleton.semi_singleton_metaclass()):
    def __init__(self, i, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = i


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_semisingleton(protocol):
    """
    Ensure semisingleton objects can be pickled.
    """

    mt1a = MultiTex(1)
    mt1b = MultiTex(1)
    mt2a = MultiTex(2)
    mt2b = MultiTex(2)

    serial = nrpickler.dumps([mt1a, mt1b, mt2a, mt2b], protocol=protocol)
    postpickle = pickle.loads(serial)

    assert postpickle[0].i == 1, "Post-pickle semisingleton has wrong .i"
    assert postpickle[1].i == 1, "Post-pickle semisingleton has wrong .i"
    assert postpickle[2].i == 2, "Post-pickle semisingleton has wrong .i"
    assert postpickle[3].i == 2, "Post-pickle semisingleton has wrong .i"
    assert (
        postpickle[0] is postpickle[1]
    ), "Post-pickle semisingleton *IS NOT* expected!"
    assert (
        postpickle[1] is not postpickle[2]
    ), "Post-pickle semisingleton *IS NOT* expected!"
    assert (
        postpickle[2] is postpickle[3]
    ), "Post-pickle semisingleton *IS NOT* expected!"
    assert postpickle[0] is not mt1a, "Post-pickle semisingleton IS pre-pickle!"
    assert postpickle[1] is not mt1b, "Post pickle semisingleton IS pre-pickle!"
    assert isinstance(
        postpickle[0], MultiTex
    ), "Class defined in module level didn't unpickle to the same"


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_runtime_attributes(protocol):
    """
    Test pickling procedure saves and restores arbitrary defined-at-runtime
    attributes.
    """

    v1 = vertex.Vertex()
    v1.i = 7
    v1.j = 12
    v2 = vertex.Vertex()
    v2.i = 9001
    v2.other_one = v1
    v2.this_one = v2
    v2.words = "words"

    serial = nrpickler.dumps([v1, v2], protocol=protocol)
    postpickle = pickle.loads(serial)
    p1, p2 = postpickle

    assert p1 is not v1, "Post-pickle vertex IS pre-pickle!"
    assert p2 is not v2, "Post-pickle vertex IS pre-pickle!"
    assert p1 is not p2, "Post-pickle vertices are the same???"
    assert p1.i == 7, "Post-pickle v1.i is wrong"
    assert p1.j == 12, "Post-pickle v1.j is wrong"
    assert p2.i == 9001, "Post-pickle v2.i is wrong"
    assert p2.other_one is p1, "Post-picle v2.other_one is wrong"
    assert p2.this_one is p2, "Post-pickle v2.this_one is wrong"
    assert p2.words == "words", "Post-pickle v2.words is wrong"


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_subclasses(protocol):
    """
    Ensure the pickling approach works with various subclass structures.
    """

    class VertType1(vertex.Vertex):
        pass

    class VertType2(vertex.Vertex):
        pass

    class VertType3(VertType2):
        pass

    class VertType4(VertType3, VertType1):
        pass

    v1 = VertType1()
    v2 = VertType2()
    v3 = VertType3()
    v4 = VertType4()
    v5 = vertex.Vertex()

    serial = nrpickler.dumps([v1, v2, v3, v4, v5], protocol=protocol)
    postpickle = pickle.loads(serial)
    p1, p2, p3, p4, p5 = postpickle

    assert isinstance(p5, vertex.Vertex), "Post-pickle vertex is the wrong type"

    # p5 works, as seen above
    # but since the VertTypeX classes are created dynamically, they can't be
    # pickled at the module level, and so are unpickled as identical, but
    # different, type instances.  therefore, we can't do isinstance() or is
    # checks on them, this is the next best thing

    assert (
        type(v1).__qualname__ == type(p1).__qualname__
    ), "post-pickle vt1 wrong qn"
    assert (
        type(v2).__qualname__ == type(p2).__qualname__
    ), "post-pickle vt2 wrong qn"
    assert (
        type(v3).__qualname__ == type(p3).__qualname__
    ), "post-pickle vt3 wrong qn"
    assert (
        type(v4).__qualname__ == type(p4).__qualname__
    ), "post-pickle vt4 wrong qn"

    with pytest.raises(AssertionError):
        assert isinstance(
            p1, VertType1
        ), "p1 not expected to be real instance of VT1"
    with pytest.raises(AssertionError):
        assert isinstance(
            p2, VertType2
        ), "p2 not expected to be real instance of VT2"
    with pytest.raises(AssertionError):
        assert isinstance(
            p3, VertType3
        ), "p3 not expected to be real instance of VT3"
    with pytest.raises(AssertionError):
        assert isinstance(
            p4, VertType4
        ), "p4 not expected to be real instance of VT4"


def _main_func_foo(x):
    """
    Main module-level test function for pickling purposes.
    """
    return x * 4


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_executable_nonlocal(protocol):
    """
    Ensure that instances with extra non-local code can be pickled.
    """

    v1 = vertex.Vertex()
    v1.func = _main_func_foo

    assert v1.func(4) == 16, "precondition wrong!"

    serial = nrpickler.dumps(v1, protocol=protocol)
    p1 = pickle.loads(serial)

    assert p1 is not v1, "unpickling gave the same instance"
    assert p1.func is v1.func, "did not pickle function by ref"
    assert p1.func(3) == 12, "3*4 did not equal 12"


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_executable_local(protocol):
    """
    Ensure that instances with extra code attached can be pickled.
    """

    def foo(bar):
        return 2 * bar

    v1 = vertex.Vertex()
    v1.somefunc = foo

    assert v1.somefunc(2) == 4, "precondition wrong!"

    serial = nrpickler.dumps(v1, protocol=protocol)
    p1 = pickle.loads(serial)

    assert p1.somefunc(2) == 4, "2*2 did not equal 4"
    assert p1 is not v1, "unpickling gave the same instance"
    assert p1.somefunc is not v1.somefunc, "unpickling returned same function"


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_p_up_file(protocol, tmp_path, straightline_graph_1k_directed):
    """
    Ensure pickle data can actually be written to / read from a real file.
    """
    uni, verts = straightline_graph_1k_directed

    fname = tmp_path / "store.pkl"
    with open(fname, "wb") as wfp:
        nrpickler.dump((uni, verts), wfp)

    with open(fname, "rb") as rfp:
        puni, pverts = pickle.load(rfp)

    assert len(pverts) == len(verts), "Wrong length of vertices"


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL)))
def test_up_with_dill(protocol, straightline_graph_1k_directed):
    """
    Ensure that the nonrecursive pickler data can be deserialized by dill.
    """
    uni, verts = straightline_graph_1k_directed
    serial = nrpickler.dumps((uni, verts), protocol=protocol)
    p1 = dill.loads(serial)

    assert p1[0] is not uni, "Dill deserialized same object!"

    for i in range(len(verts)):
        assert p1[1][i].i == verts[i].i, "dill deserialized wrong order!"
