#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Depth-first search and traversal functions.

The functions here perform searches and traversals of graphs in a depth-first
manner.  For each operation (search and traverse), two implementations are
provided: one recursive, and one iterative.  The calling API is identical
between the implementations, but note that *the order of traversal frequently
differs* between them.  This is the nature of the differing approaches.

.. seealso::

   * https://en.wikipedia.org/wiki/Depth-first_search
   * [CLRS09]_, chapter 22.3; [GoTa60]_, chapter 13.2
   * :py:mod:`edgegraph.traversal.breadthfirst`: breadth-first search and
     traverse operations


The algorithm used by all the functions herein visits vertices in the following
order.  Note that the choice of which branch to take at any given node (e.g.,
visiting v3 before v6) is determined by the structure of the universe.

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
   v2 -- v3
   v3 -- v4
   v3 -- v5
   v2 -- v6
   v1 -- v7
   v1 -- v8
   v8 -- v9
   v9 -- v10
   v9 -- v11
   v8 -- v12
"""

from __future__ import annotations
from collections.abc import Callable, Iterator
from edgegraph.structure import Universe, Vertex
from edgegraph.traversal import helpers


def _df_preflight_checks(uni: Universe, start: Vertex):
    """
    Perform a few common pre-traversal sanity checks, raising ValueError if
    they fail.  For internal use only!

    :param uni: Universe to traverse/search.
    :param start: Vertex to start trav/search at.
    :raises ValueError: if the universe is empty, or if the start vertex is not
       in the given universe.
    """
    if (uni is not None) and (len(uni.vertices) == 0):
        raise ValueError("Universe is empty; cannot perform this operation!")
    if (uni is not None) and (start not in uni.vertices):
        raise ValueError("Start vertex not in specified universe!")


def _dft_recur(
    uni: Universe,
    v: Vertex,
    *,
    visited: dict[Vertex, None],
    direction_sensitive: int,
    unknown_handling: int,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> Iterator[Vertex]:
    """
    Recursion helper for :py:func:`dft_recursive`.  For internal use only!

    :meta private:

    :param uni: Universe to traverse, or ``None`` for no universe limits.
    :param v: Top of recursive tree.
    :param visited: List of vertices already visited.  Must be
       pass-by-reference!
    :return: Order of traversal of the given subtree.
    """
    visited[v] = None

    if (ff_result and ff_result(v)) or (not ff_result):
        yield v

    for w in helpers.ineighbors(
        v,
        direction_sensitive=direction_sensitive,
        unknown_handling=unknown_handling,
        filterfunc=ff_via,
    ):
        if (uni is not None) and (w not in uni.vertices):
            continue
        if w not in visited:
            yield from _dft_recur(
                uni,
                w,
                visited=visited,
                direction_sensitive=direction_sensitive,
                unknown_handling=unknown_handling,
                ff_via=ff_via,
                ff_result=ff_result,
            )


def idft_recursive(
    uni: Universe,
    start: Vertex,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> Iterator[Vertex]:
    """
    Perform a recursive depth-first traversal of the given universe, starting
    at the given vertex (generator).

    The algorithm used is detailed in [CLRS09]_, figure 22.4, and [GoTa60]_,
    Algorithm 13.6.  Slight modifications have been made due to the nature of
    EdgeGraph's data model.  This is a *recursive* implementation that returns
    a list of :py:class:`~edgegraph.structure.vertex.Vertex` objects, in the
    order of the traversal performed.

    :param uni: The universe to traverse, or ``None`` for no universe limits.
    :param start: The vertex to begin traversal at.
    :return: A generator object that yields vertices in the order of a
       recursive depth-first traversal in accordance with the set parameters.
    :raises ValueError: if the ``start`` vertex is not a member of the
       specified universe, or if the universe is empty.
    """
    _df_preflight_checks(uni, start)

    visited: dict[Vertex, None] = {}
    yield from _dft_recur(
        uni,
        start,
        visited=visited,
        direction_sensitive=direction_sensitive,
        unknown_handling=unknown_handling,
        ff_via=ff_via,
        ff_result=ff_result,
    )


def dft_recursive(
    uni: Universe,
    start: Vertex,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> list[Vertex]:
    """
    Perform a recursive depth-first traversal of the given universe, starting
    at the given vertex (**non**-generator).

    .. seealso::

       Please refer to the documentation of :py:func:`idft_recursive`!  This
       function simply wraps that one, only forcing full expansion to a list
       before returning  All parameters are exactly the same and passed through
       without alteration.

    :return: A list of vertices in order of a recursive depth-first traversal.
    :raises ValueError: if the ``start`` vertex is not a member of the
       specified universe, or if the universe is empty.
    """

    return list(
        idft_recursive(
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


def _dfs_recur(
    uni: Universe,
    v: Vertex,
    visited: dict[Vertex, None],
    attrib: str,
    val: object,
) -> Vertex | None:
    """
    Recursion helper for :py:func:`dfs_recursive`.  For internal use only!

    :meta private:

    :param uni: Universe to search in, or ``None`` for no universe limits.
    :param v: Top of the recursion subtree.
    :param visited: List of vertices already visited.  Must be
       pass-by-reference!
    :param attrib: Name of the attribute to check.
    :param val: Value of the attribute desired.
    :return: The target vertex, or None if not found in this subtree.
    """
    visited[v] = None
    for w in helpers.ineighbors(v):
        if (uni is not None) and (w not in uni.vertices):
            continue
        if w not in visited:
            # check for a match first -- then we can exit early
            if hasattr(w, attrib):
                if w[attrib] == val:
                    return w
            ret = _dfs_recur(uni, w, visited, attrib, val)
            if ret:
                return ret
    return None


def dfs_recursive(
    uni: Universe, start: Vertex, attrib: str, val: object
) -> Vertex | None:
    """
    Perform a recursive depth-first search in the given graph for a given
    attribute.

    The algorithm used is detailed in [CLRS09]_, figure 22.4, and [GoTa60]_,
    Algorithm 13.6.  Slight modifications have been made due to the nature of
    EdgeGraph's data model, and to add an early-exit condition if the desired
    vertex is found.  This is a *recursive* implementation that returns either
    the first vertex discovered matching the specified criteria, or None if no
    such vertex is found.

    Search criteria is specified via the ``attrib`` and ``val`` arguments.
    Each vertex is checked for A.) the existence of the specified attribute,
    and B.) the value of such attribute must be equal to the specified value.
    A ``==`` check is used for comparison (not ``is``).  Traversal stops as
    soon as such an attribute is found.

    :param uni: The universe to search in, or ``None`` for no universe limits.
    :param start: The vertex to start searching at.
    :param attrib: Name of the attribute to check each vertex for.
    :param val: Value to look for in the specified attribute.
    :return: The first vertex with a matching value, or ``None`` if none is
       found.
    :raises ValueError: if the ``start`` vertex is not a member of the
       specified universe, or if the universe is empty.
    """
    _df_preflight_checks(uni, start)

    if hasattr(start, attrib):
        if start[attrib] == val:
            return start

    visited: dict[Vertex, None] = {}
    return _dfs_recur(uni, start, visited, attrib, val)


def idft_iterative(
    uni: Universe,
    start: Vertex,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> Iterator[Vertex]:
    """
    Perform an iterative depth-first traversal of the given universe, starting
    at the given vertex (generator).

    This algorithm used is similar to that in [KlTa05]_, algorithm 3.12.
    Slight modifications have been made to preclude re-visited vertices in the
    final list.  This is a *iterative* implementation that returns a list of
    :py:class:`~edgegraph.structure.vertex.Vertex` objects, in the order of the
    traversal performed.

    :param uni: The universe to traverse, or ``None`` for no universe limits.
    :param start: Vertex to start searching at.
    :return: A generator object yielding vertices in the order of an iterative
       depth-first traversal, in accordance with the set parameters.
    :raises ValueError: if the ``start`` vertex is not a member of the
       specified universe, or if the universe is empty.
    """
    _df_preflight_checks(uni, start)

    stack = [start]
    discovered = []
    while len(stack) != 0:
        v = stack.pop()
        if v not in discovered:
            if (uni is not None) and (v not in uni.vertices):
                continue

            discovered.append(v)
            if (ff_result and ff_result(v)) or (not ff_result):
                yield v

            for w in helpers.ineighbors(
                v,
                direction_sensitive=direction_sensitive,
                unknown_handling=unknown_handling,
                filterfunc=ff_via,
            ):
                stack.append(w)


def dft_iterative(
    uni: Universe,
    start: Vertex,
    *,
    direction_sensitive: int = helpers.DIR_SENS_FORWARD,
    unknown_handling: int = helpers.LNK_UNKNOWN_ERROR,
    ff_via: Callable | None = None,
    ff_result: Callable | None = None,
) -> list[Vertex]:
    """
    Perform an iterative depth-first traversal of the given universe, starting at the given vertex (**non**-generator).

    .. seealso::

       Please refer to the documentation of :py:func:`idft_iterative`!  This
       function simply wraps that one, only forcing full expansion to a list
       before returning.  All parameters are exactly the same and passed
       through without alteration.

    :return: A list of vertices in the order of an iterative depth-first
       traversal.
    :raises ValueError: if the ``start`` vertex is not a member of the
       specified universe, or if the universe is empty.
    """

    return list(
        idft_iterative(
            uni,
            start,
            direction_sensitive=direction_sensitive,
            unknown_handling=unknown_handling,
            ff_via=ff_via,
            ff_result=ff_result,
        )
    )


def dfs_iterative(
    uni: Universe, start: Vertex, attrib: str, val: object
) -> Vertex | None:
    """
    Perform a non-recursive depth-first search in the given universe.

    The algorithm used is similar to that in [KlTa05]_, algorithm 3.12.  Slight
    modifications have been made for an early-exit if the desired vertex is
    discovered.  This is a *recursive* implementation that returns either the
    first vertex discovered matching the specified criteria, or None if no such
    vertex is found.

    Search criteria is specified via the ``attrib`` and ``val`` arguments.
    Each vertex is checked for A.) the existence of the specified attribute,
    and B.) the value of such attribute must be equal to the specified value.
    A ``==`` check is used for comparison (not ``is``).  Traversal stops as
    soon as such an attribute is found.

    :param uni: The universe to search in, or ``None`` for no universe limits.
    :param start: The vertex to start searching at.
    :param attrib: Name of the attribute to check each vertex for.
    :param val: Value to look for in the specified attribute.
    :return: The first vertex with a matching value, or ``None`` if none is
       found.
    :raises ValueError: if the ``start`` vertex is not a member of the
       specified universe, or if the universe is empty.
    """
    _df_preflight_checks(uni, start)

    stack = [start]
    discovered = []
    while len(stack) != 0:
        v = stack.pop()
        if (uni is not None) and (v not in uni.vertices):
            continue
        if v not in discovered:
            if hasattr(v, attrib):
                if v[attrib] == val:
                    return v
            discovered.append(v)
            for w in helpers.ineighbors(v):
                stack.append(w)
    return None
