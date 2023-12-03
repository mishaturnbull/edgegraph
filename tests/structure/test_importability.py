#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests to ensure module structure is operable.
"""

import pytest

def test_full_qual_imports():
    import edgegraph.structure.base
    import edgegraph.structure.vertex
    import edgegraph.structure.universe

def test_structure_imports():
    from edgegraph.structure import BaseObject, Vertex, Universe

