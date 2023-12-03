#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for Universe object.
"""

import pytest
from edgegraph.structure import base, vertex, universe

def test_universe_subclass():
    assert issubclass(universe.Universe, vertex.Vertex)

    u = universe.Universe(
            uid=-100,
            attributes={"thirteen": 13},
            )

    assert u.uid == -100
    assert u.thirtteen == 13

