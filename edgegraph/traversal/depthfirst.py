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
               visited: dict[Vertex, None]) -> list[Vertex]:
    if v in visited:
        assert "wrong!"
    else:
        visited[v] = None

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

    visited = {}
    return _dft_recur(uni, start, visited)

def dft_iterative(uni: Universe,
                  start: Vertex) -> list[Vertex]:
    """
    Perform an iterative depth-first traversal of the given universe, starting
    at the given vertex.

    .. todo::
    
       document this too
    """

    stack = [start]
    discovered = []
    while len(stack):
        v = stack.pop()
        if v not in discovered:
            discovered.append(v)
            for w in helpers.neighbors(v):
                stack.append(w)
    return discovered

