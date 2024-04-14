#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Depth-first search and traversal functions.
"""

from __future__ import annotations

import collections

from edgegraph.structure import Universe, Vertex
from edgegraph.traversal import helpers

def _dft_recur(uni: Universe,
               v: Vertex,
               visited: set[Vertex]) -> list[Vertex]:
    #print(f"_dft_recur: {uni}, {v}, {visited}")
    if v in visited:
        assert "wrong!"
    else:
        visited.add(v)

    out = [v]
    for w in helpers.neighbors(v):
        if w not in visited:
            out.extend(_dft_recur(uni, w, visited))
    return out

def dft_recursive(uni: Universe,
                  start: Vertex) -> list[Vertex]:
    """
    Perform a recursive depth-first traversal of the given universe, starting
    at the given vertex.

    .. todo::

       document this
    """

    visited = set()
    return _dft_recur(uni, start, visited)

