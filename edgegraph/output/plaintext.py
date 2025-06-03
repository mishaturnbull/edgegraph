#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Print graphs to an ASCII format.  (Not ASCII "art"!)

This module provides functionality to "print" a graph.  At present time, only
one format is supported.  See the sole function for more information.  More
formats may be added in the future.

.. important::

   Nothing in this module is intended to be *parsed* by anyone, for any reason.
   If you are trying to persistently store graphs, or exchange them between
   processes, or something else, see the :py:mod:`output.nrpickler
   <edgegraph.output.nrpickler>` module.
"""

from __future__ import annotations
from collections.abc import Callable
from edgegraph.structure import Universe
from edgegraph.traversal import helpers


def basic_render(
    uni: Universe,
    rfunc: Callable | None = None,
    sort: Callable | None = None,
) -> str | None:
    """
    Perform a very basic rendering of a graph into a string.

    This function does not do any proper graph traversals; instead, simply
    works down the list of vertices in the given universe.

    If specified, ``rfunc`` should be a callable object accepting one argument
    and returning a string.  It will be given each vertex, and expected to
    return the user's choice of how they wish that vertex to be rendered.
    Likewise, if specified, ``sort`` should be a callable accepting one
    argument and returning a comparison key for use in :py:func:`sorted`.

    The intended usage is as follows:

    >>> from edgegraph.builder import randgraph
    >>> from edgegraph.output import plaintext
    >>> graph = randgraph.randgraph()
    >>> asci = plaintext.basic_render(graph)
    >>> print(asci, rfunc=lambda v: v.i)
    7 -> 5
    4 -> 6
    14 -> 14, 7, 13
    11 -> 1, 11, 4
    8 -> 14, 8
    0 -> 12
    3 -> 5
    5 -> 0
    12 -> 3, 1
    1 -> 8
    9 -> 4
    6 -> 7
    2 -> 13
    10 -> 7, 10, 8
    13 -> 7

    .. todo::

       figure out what to do to make this pass doctest... if graph is
       randomized, graph is different every time --> test fails

    :param uni: The universe to render.
    :param rfunc: Callable render function, if any.
    :param sort: Callable sorting key function, if any.
    :return: Multi-line output of the rendering operation, or ``None`` if the
       universe is empty.
    """
    if len(uni.vertices) == 0:
        # empty!
        return None

    lines = []
    start, node = "", ""
    if sort:
        verts = sorted(uni.vertices, key=sort)
    else:
        verts = uni.vertices
    for vert in verts:
        line = ""
        if rfunc:
            start = rfunc(vert)
        else:
            start = repr(vert)

        line += f"{start} -> "

        if sort:
            nbs = sorted(helpers.ineighbors(vert), key=sort)
        else:
            nbs = helpers.ineighbors(vert)
        for end in nbs:
            if rfunc:
                node = rfunc(end)
            else:
                node = repr(end)
            line += f"{node}, "

        # remove trailing comma & space
        line = line[:-2]
        lines.append(line)

    return "\n".join(lines)
