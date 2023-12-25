#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the DirectedEdge class.
"""

from __future__ import annotations
from edgegraph.structure import undirectededge, vertex


class DirectedEdge (undirectededge.UnDirectedEdge):
    """
    Represents a directed edge (v1 --> v2) in the vertex-edge graph.

    This object is intended to join two vertices in a directed fashion; i.e.,
    one vertex directs to the other.
    """

    # to be completely honest, this class is IDENTICAL in implementation to
    # UnDirectedEdge.  however, it's still getting its own type -- makes it
    # much easier for graph algos to spot the difference (as opposed to a
    # simple TwoEndedEdge.directed == True flag), and this approach allows us
    # to document the directed edge in a much cleaner manner.

    def __init__(self,
            v1: Vertex=None,
            v2: Vertex=None,
            *,
            uid: int=None,
            attributes: dict=None,
            ):
        """
        Instantiate a directed edge.

        :param v1: The first vertex in the edge (the link will be *FROM* this
           one)
        :param v2: The second vertex in the edge (thie link will be *TO* this
           one)

        .. seealso::

           * :py:meth:`edgegraph.structure.undirectededge.UnDirectedEdge.__init__`,
             the superclass constructor
        """
        super().__init__(v1=v1, v2=v2, uid=uid, attributes=attributes)

    @property
    def v1(self) -> Vertex:
        """
        Return the origin vertex of this edge.

        This edge comes *FROM* this object: v1 --> v2.
        """
        return super().v1

    @property
    def v2(self) -> Vertex:
        """
        Return the destination vertex of this edge.

        This edge goes *TO* this object: v1 --> v2.
        """
        return super().v2

