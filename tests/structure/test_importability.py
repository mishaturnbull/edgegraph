#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests to ensure module structure is operable.
"""

# W0611 is unused-import.  The entire objective of these tests is to ensure we
# can import the objects; their usage is tested elsewhere.
# C0415 is import-outside-toplevel.  We don't perform unit tests at the module
# scope.
# pylint: disable=W0611, C0415

def test_full_qual_imports():
    """
    Ensure we can import structure container modules as fully-qualified
    modules.
    """
    import edgegraph.structure.base
    import edgegraph.structure.vertex
    import edgegraph.structure.universe

def test_structure_imports():
    """
    Ensure we can import structure objects directly from the structure module.
    """
    from edgegraph.structure import BaseObject, Vertex, Universe

