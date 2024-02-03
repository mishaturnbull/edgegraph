#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Helper functions for graph traversals.
"""

from __future__ import annotations

from edgegraph.structure import Vertex, DirectedEdge, UnDirectedEdge

#: Unknown edge classes treated as non-neighbors.
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
LNK_UNKNOWN_NONNEIGHBOR = 0

#: Unknown edge classes treated as neighbors.
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
LNK_UNKNOWN_NEIGHBOR = 1

#: Unknown edge classes raise an exception.
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
LNK_UNKNOWN_ERROR = 2

def neighbors(vert: Vertex,
        direction_sensitive: bool=True,
        unknown_handling: int=LNK_UNKNOWN_ERROR,
        ) -> list[Vertex]:
    """
    Identify the neighbors of a given vertex.

    This function checks the edges associated with the given vertex, identifies
    the vertices on the other end of those edges, and returns them.  It
    respects edge directionality if/when necessary, and can handle arbitrary
    edge types given they are subclasses of either
    :py:class:`~edgegraph.structure.directededge.DirectedEdge` or
    :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.

    For example, with the given graph:

    .. uml::

       object v1
       object v2
       object v3
       object v4

       v1 --> v2
       v1 --> v3
       v2 --> v3
       v3 --> v4
       v4 --> v1

    the function would operate as:

       >>> neighbors(v1)
       [v2, v3]
       >>> neighbors(v1, direction_sensitive=False)
       [v2, v3, v4]
       >>> neighbors(v4)
       [v1]
       >>> neighbors(v4, direction_sensitive=False)
       [v1, v3]

    :param vert: The vertex to identify neighbors of.
    :param direction_sensitive: Enables handling of directional links.  If set
       to ``False``, any subclasses / instances of
       :py:class:`~edgegraph.structure.directededge.DirectedEdge` are treated
       as if they were instead subclasses / instances of
       :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.
    :param unknown_handling: What to do with edges whose class is not
       recognized (not a subclass / instance of either
       :py:class:`~edgegraph.structure.directededge.DirectedEdge` or
       :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`).
       Options are :py:const:`LNK_UNKNOWN_NONNEIGHBOR` to treat unknown edges
       as non-neighbors, :py:const:`LNK_UNKNOWN_NEIGHBOR` to treat unknown
       edges *as* neighbors, or :py:const:`LNK_UNKNOWN_ERROR` to raise a
       :py:exc:`NotImplementedError` if such an edge is encountered.
    :raises NotImplementedError: if kwarg ``unknown_handling`` is set to
       :py:const:`LNK_UNKNOWN_ERROR` and an unknown edge class is enountered.
    :return: A list of :py:class:`~edgegraph.structure.vertex.Vertex` objects
       representing neighbors of the specified vertex.
    """

    nbs = []
    for link in vert.links:

        if direction_sensitive:
            # undirected edges don't matter
            if issubclass(type(link), UnDirectedEdge):
                nbs.append(link.other(vert))

            # for directed edges, only add the neighbor if vert is the origin
            elif issubclass(type(link), DirectedEdge) and (link.v1 is vert):
                nbs.append(link.other(vert))

            # we're looking at v2 -- the destination
            # TODO: is it more time efficient to move the v1/v2 comparison into
            # an if nested under the directededge check?
            elif issubclass(type(link), DirectedEdge) and (link.v2 is vert):
                pass

            else:
                if unknown_handling == LNK_UNKNOWN_NONNEIGHBOR:
                    continue

                if unknown_handling == LNK_UNKNOWN_NEIGHBOR:
                    nbs.append(link.other(vert))
                else:
                    raise NotImplementedError(f"Unknown link class {type(link)}")

        else:
            nbs.append(link.other(vert))

    return nbs

