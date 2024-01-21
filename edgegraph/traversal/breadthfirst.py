#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Breadth-first search and traversal functions.
"""

from __future__ import annotations

import collections

from edgegraph.structure import Universe, Vertex, DirectedEdge, UnDirectedEdge
from edgegraph.traversal import helpers

def bfs(uni: Universe,
        start: Vertex,
        attrib: str,
        val: object) -> Vertex:
    """
    Perform a breadth-first search.

    This function performs a breadth-first search within ``uni``, starting at
    ``start``, looking for a vertex such that ``vert[attrib] == val``.

    This algorithm is detailed in pseudocode in [CLRS09]_, figure 22.3, and
    [GoTa60]_, Algorithm 13.8.  Slight modifications have been made to break
    early when the desired value is found.

    :param uni: The universe to search in.
    :param start: The vertex to start searching at.
    :param attrib: The attribute name to check for each vertex.
    :param val: The value to check for in the aforementioned attribute.
    :return: The vertex which first matched the specified attribute value.
    """
    if len(uni.vertices) == 0:
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    visited = set()
    queue = collections.deque([start])
    visited.add(start)

    while queue:
        u = queue.popleft()
        for v in helpers.neighbors(u):

            if (uni is not None) and (v not in uni.vertices):
                continue

            # check for a match first -- then we can exit early
            if hasattr(v, attrib):
                if v[attrib] == val:
                    return v

            # make sure we don't re-visit as a duplicate
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return None

def bft(uni: Universe,
        start: Vertex) -> list[Vertex]:
    """
    Perform a breadth-first traversal.

    This function performs a breadth-first traversal within ``uni``, starting
    at ``start``, and returns the vertices visited in a list.

    This algorithm is detailed in pseudocode in [CLRS09]_, figure 22.3, and
    [GoTa60]_, Algorithm 13.8.

    :param uni: The universe to search in.
    :param start: The vertex to start searching at.
    :return: The vertices visited during traversal.
    """
    if len(uni.vertices) == 0:
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    visited = []
    queue = collections.deque([start])
    visited.append(start)

    while queue:
        u = queue.popleft()
        for v in helpers.neighbors(u):

            if (uni is not None) and (v not in uni.vertices):
                continue

            # make sure we don't re-visit as a duplicate
            if v not in visited:
                visited.append(v)
                queue.append(v)

    return visited

