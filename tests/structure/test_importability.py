#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests to ensure module structure is operable.
"""

# disable import-related checks; everything imported here is unused.  that's
# fine.
# ruff: noqa: F401


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
