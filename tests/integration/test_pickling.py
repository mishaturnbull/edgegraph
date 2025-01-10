#!python3
# -*- coding: utf-8 -*-

"""
Unit tests that ensure all Edgegraph objects are pickleable and unpickleable.
"""

import pickle
import sys

import logging
import pytest

from edgegraph.structure import singleton, vertex, universe
from edgegraph.traversal import breadthfirst
from edgegraph.builder import randgraph
from edgegraph.output import nrpickler

# https://stackoverflow.com/a/65318623
import __main__
__main__.universe = universe

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


# NOTE: this test has been observed to fail with --randomly-seed=3991981975
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

    # replace the normal `set()`-typed uni._vertices with the list from the
    # graph contructor.  this way, the vertices are always ordered -- starting
    # at v0 and increasing to v999 -- which is necessary to trigger the
    # recursion error every time.  if we leave it as the set, then the "first"
    # vertex the pickler encounters may be halfway down the list, which will
    # cause intermittent unexpected passes (*not* running out of recursion
    # depth)
    uni._vertices = verts

    # troubleshooting!!!
    LOG.debug(f"{id(universe.Universe)=}")
    LOG.debug(f"{id(__main__.universe.Universe)=}")

    try:
        serial = nrpickler.dumps(uni, protocol=protocol)
        postpickle = pickle.loads(serial)

        assert len(uni.vertices) == len(postpickle.vertices)

    finally:
        sys.setrecursionlimit(orig_rcr_depth)
    
