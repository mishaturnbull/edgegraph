#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit testing for PyVis not being installed.  Maybe...
"""

import os
import sys
import importlib
import logging
import pytest

# this test module does a few unorthodox imports -- but, that's the point of
# this single test isolated in its own module.  we don't want the "gonna break
# everything" test to, well, break everything *else*
# C0415 = Import outside toplevel
# W0611 = Unused import
# pylint: disable=C0415, W0611

LOG = logging.getLogger(__name__)


def test_pyvis_not_installed(monkeypatch):
    """
    Ensure that when PyVis is not installed, the appropriate error message is
    thrown, and the rest of the program continues to operate without error.
    """
    testroot = os.path.split(os.path.split(__file__)[0])[0]
    badmods = os.path.join(testroot, "testfiles", "badmodules")

    LOG.info(f"Adding {badmods} to sys.path (prepend): {sys.path}")
    monkeypatch.syspath_prepend(badmods)

    restore_mods = {}

    LOG.debug("Flushing package caches...")
    for mod in list(sys.modules.keys()):
        if mod.startswith("pyvis") or mod.startswith("edgegraph"):
            LOG.debug(f"Deleting {mod} from sys.modules")
            restore_mods[mod] = sys.modules[mod]
            del sys.modules[mod]
    importlib.invalidate_caches()

    # ensure the error message includes instructions on how to install pyvis
    with pytest.raises(ImportError, match="pip install pyvis"):
        import edgegraph.output.pyvis

    # and now do a quick smoketest to make sure this hasn't broken the other
    # parts of the module
    from edgegraph.builder import randgraph

    uni = randgraph.randgraph()

    try:
        assert len(uni.vertices) > 0
    finally:
        # restore the earlier modules to not break tests which might come after
        # us, even in the event of a failure
        for modname, module in restore_mods.items():
            sys.modules[modname] = module
