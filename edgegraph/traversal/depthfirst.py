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
    visited[v] = None
    out = [v]
    for w in helpers.neighbors(v):
        if (uni is not None) and (w not in uni.vertices):
            continue
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
    if len(uni.vertices) == 0:
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

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
    if len(uni.vertices) == 0:
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    stack = [start]
    discovered = []
    while len(stack):
        v = stack.pop()
        if v not in discovered:
            if (uni is not None) and (v not in uni.vertices):
                continue
            discovered.append(v)
            for w in helpers.neighbors(v):
                stack.append(w)
    return discovered

