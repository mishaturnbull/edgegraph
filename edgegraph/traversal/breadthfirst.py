#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Breadth-first search and traversal functions.

The functions here perform searches and traversals of graphs in a breadth-first manner.  The implementations are iterative.

.. seealso::

   * [CLRS09]_, chapter 22.2; [GoTa60]_, chapter 13.3
   * https://en.wikipedia.org/wiki/Breadth-first_search
   * :py:mod:`edgegraph.traversal.depthfirst`: depth-first search and traverse
     operations

The algorithm used by all the functions herein visits vertices in the following
order.  Note that the choice of which branch to take at any given node (e.g.,
visiting v9 before v10) is determined by the structure of the universe.

.. uml::

   object v1
   object v2
   object v3
   object v4
   object v5
   object v6
   object v7
   object v8
   object v9
   object v10
   object v11
   object v12

   v1 -- v2
   v1 -- v3
   v1 -- v4
   v2 -- v5
   v2 -- v6
   v4 -- v7
   v4 -- v8
   v5 -- v9
   v5 -- v10
   v7 -- v11
   v7 -- v12

"""

from __future__ import annotations

import collections

from edgegraph.structure import Universe, Vertex
from edgegraph.traversal import helpers

# TODO: add (to both these fn's) passthru kwargs to neighbors() options


def bfs(uni: Universe, start: Vertex, attrib: str, val: object) -> Vertex:
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
    if (uni is not None) and (len(uni.vertices) == 0):
        # empty!
        return None
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    if hasattr(start, attrib):
        if start[attrib] == val:
            return start

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


def ibft(uni: Universe, start: Vertex) -> list[Vertex]:
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
    if (uni is not None) and (len(uni.vertices) == 0):
        # empty!
        return
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    visited = set()
    queue = collections.deque([start])
    visited.add(start)
    yield start

    while queue:
        u = queue.popleft()
        for v in helpers.neighbors(u):

            if (uni is not None) and (v not in uni.vertices):
                continue

            # make sure we don't re-visit as a duplicate
            if v not in visited:
                visited.add(v)
                queue.append(v)
                yield v


def bft(uni: Universe, start: Vertex) -> list[Vertex]:
    out = list(ibft(uni, start))
    if out == []:
        return None
    return out

