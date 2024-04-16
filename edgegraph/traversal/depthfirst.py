#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Depth-first search and traversal functions.
"""

from __future__ import annotations

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

def _dfs_recur(uni: Universe,
               v: Vertex,
               visited: dict[Vertex, None],
               attrib: str,
               val: object) -> Vertex:
    visited[v] = None
    for w in helpers.neighbors(v):
        if (uni is not None) and (w not in uni.vertices):
            continue
        if w not in visited:
            # check for a match first -- then we can exit early
            if hasattr(w, attrib):
                print(f"checking {w.i} for {attrib}={val}...", end='')
                if w[attrib] == val:
                    print("HIT!")
                    return w
                print("nope")
            ret = _dfs_recur(uni, w, visited, attrib, val)
            if ret:
                return ret
    return None

def dfs_recursive(uni: Universe,
                  start: Vertex,
                  attrib: str,
                  val: object) -> Vertex:
    """
    Perform a recursive depth-first search in the given graph for a given
    attribute.

    .. todo::
      
       document this
    """
    if len(uni.vertices) == 0:
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    visited = {}
    return _dfs_recur(uni, start, visited, attrib, val)

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
    while len(stack) != 0:
        v = stack.pop()
        if v not in discovered:
            if (uni is not None) and (v not in uni.vertices):
                continue
            discovered.append(v)
            for w in helpers.neighbors(v):
                stack.append(w)
    return discovered

def dfs_iterative(uni: Universe,
                  start: Vertex,
                  attrib: str,
                  val: object) -> Vertex:
    """
    Perform a non-recursive depth-first search in the given universe.

    .. todo::

       document this

    .. danger::

       I'm fairly certain this isn't working right just yet.  It searches, but
       re-visits vertices.
    """
    if len(uni.vertices) == 0:
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    stack = [start]
    discovered = []
    while len(stack) != 0:
        v = stack.pop()
        if hasattr(v, attrib):
            print(f"checking {v[attrib]} for {attrib}={val}...", end='')
            if v[attrib] == val:
                print("HIT!")
                return v
            print("nope")
        if v not in discovered:
            if (uni is not None) and (v not in uni.vertices):
                continue
            discovered.append(v)
            for w in helpers.neighbors(v):
                stack.append(w)
    return None

