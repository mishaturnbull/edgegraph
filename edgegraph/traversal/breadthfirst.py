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
from collections.abc import Callable, Iterator

from edgegraph.structure import Universe, Vertex
from edgegraph.traversal import helpers


def bfs(
    uni: Universe, start: Vertex, attrib: str, val: object
) -> Vertex | None:
    """
    Perform a breadth-first search.

    This function performs a breadth-first search within ``uni``, starting at
    ``start``, looking for a vertex such that ``vert[attrib] == val``.

    This algorithm is detailed in pseudocode in [CLRS09]_, figure 22.3, and
    [GoTa60]_, Algorithm 13.8.  Slight modifications have been made to break
    early when the desired value is found.

    :param uni: The universe to search in.  Set to ``None`` for no limitations.
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
        for v in helpers.ineighbors(u):

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


def ibft(
    uni: Universe,
    start: Vertex,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> Iterator[Vertex]:
    """
    Perform a breadth-first traversal (generator).

    This function performs a breadth-first traversal within ``uni``, starting
    at ``start``, and returns the vertices visited in a list.

    This algorithm is detailed in pseudocode in [CLRS09]_, figure 22.3, and
    [GoTa60]_, Algorithm 13.8.

    :param uni: The universe to search in.  Set to ``None`` for no limiations.
    :param start: The vertex to start searching at.
    :param direction_sensitive: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors`.  This may be one of:

       * :py:const:`~edgegraph.traversal.helpers.DIR_SENS_FORWARD` (default),
         to follow edges only forward (when directed),
       * :py:const:`~edgegraph.traversal.helpers.DIR_SENS_ANY`, to follow edges
         regardless of their direction,
       * :py:const:`~edgegraph.traversal.helpers.DIR_SENS_BACKWARD`, to only
         follow edges backwards (when directed).

    :param unknown_handling: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors`.  This may be one of:

       * :py:const:`~edgegraph.traversal.helpers.LNK_UNKNOWN_ERROR` (default),
         to throw an exception,
       * :py:const:`~edgegraph.traversal.helpers.LNK_UNKNOWN_NEIGHBOR`, to
         treat such edges as neighbors (and take the edge),
       * :py:const:`~edgegraph.traversal.helpers.LNK_UNKNOWN_NONNEIGHBOR`, to
         treat such edges as non-neighbors (do not take the edge).

    :param ff_via: Directly passed through to
       :py:func:`~edgegraph.traversal.helpers.neighbors` function's
       ``filterfunc`` argument.

       .. py:function:: ff_via(e, v2)
          :noindex:

          Determines if an edge (``e``) from a given vertex to another (``v2``)
          should be followed.  If not, that entire section of the graph will
          not be traversed (assuming no other entries to that area).

          :param e: The edge connecting ``v1`` to ``v2``.
          :param v2: The vertex under consideration.
          :return: Whether or not ``v2`` should be considered a neighbor of
             ``v``, when reached via ``e``.

    :param ff_result: Callable used to filter the final output, after traversal
       has been completed.

       .. py:function:: ff_result(v)
          :noindex:

          Determines if a vertex should be returned during the final output.
          This can be useful if you want to mask certain vertices in the
          result, but still traverse across them.

          :param v: Vertex to be considered
          :return: Whether or not ``v`` should be part of the output.

    :return: A generator object that yields vertices in the order of a
       breadth-first traversal in accordance with the set parameters.
    """
    if (uni is not None) and (len(uni.vertices) == 0):
        # empty!
        return
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")

    visited = set()
    queue = collections.deque([start])
    visited.add(start)

    if (ff_result and ff_result(start)) or (not ff_result):
        yield start

    while queue:
        u = queue.popleft()
        for v in helpers.ineighbors(
            u,
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            filterfunc=ff_via,
        ):

            if (uni is not None) and (v not in uni.vertices):
                continue

            # make sure we don't re-visit as a duplicate
            if v not in visited:
                visited.add(v)
                queue.append(v)

                if (ff_result and ff_result(v)) or (not ff_result):
                    yield v


def bft(
    uni: Universe,
    start: Vertex,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> list[Vertex]:
    """
    Perform a breadth-first traversal (**non**-generator).

    .. seealso::

       Please refer to the documentation of :py:func:`ibft`!  This function
       simply wraps that one, only forcing full expansion to a list before
       returning.  All parameters are exactly the same and passed through
       without alteration.

    :return: A list of vertices in order of a breadth-first traversal.
    """

    out = list(
        ibft(
            # multiple functions have the same arguments... not a duplicate!
            # pylint: disable=duplicate-code
            uni,
            start,
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            ff_via=ff_via,
            ff_result=ff_result,
        )
    )
    return out
