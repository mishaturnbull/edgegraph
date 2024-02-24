#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Print graphs to an ASCII format.  (Not ASCII "art"!)
"""

from __future__ import annotations

from edgegraph.structure import Universe, Vertex
from edgegraph.traversal import helpers

def basic_render(uni: Universe,
                 rfunc: Callable=None,
                 sort: Callable=None) -> str:
    """
    Perform a very basic rendering of a graph into a string.

    This function does not do any proper graph traversals; instead, simply
    works down the list of vertices in the given universe.

    If specified, ``rfunc`` should be a callable object accepting one argument
    and returning a string.  It will be given each vertex, and expected to
    return the user's choice of how they wish that vertex to be rendered.
    Likewise, if specified, ``sort`` should be a callable accepting one
    argument and returning a comparison key for use in :py:func:`sorted`.

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
            nbs = sorted(helpers.neighbors(vert), key=sort)
        else:
            nbs = helpers.neighbors(vert)
        for end in nbs:
            if rfunc:
                node = rfunc(end)
            else:
                node = repr(end)
            line += f"{node}, "

        # remove trailing comma & space
        line = line[:-2]
        lines.append(line)

    return '\n'.join(lines)

