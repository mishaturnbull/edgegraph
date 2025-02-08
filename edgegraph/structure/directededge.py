#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the DirectedEdge class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from edgegraph.structure import twoendedlink

if TYPE_CHECKING:
    from edgegraph.structure.vertex import Vertex


class DirectedEdge(twoendedlink.TwoEndedLink):
    """
    Represents a directed edge (v1 --> v2) in the vertex-edge graph.

    This object is intended to join two vertices in a directed fashion; i.e.,
    one vertex directs to the other.

    .. seealso::

       * To create DirectedEdges, see
         :py:func:`~edgegraph.builder.explicit.link_directed` rather than
         creating these classes directly.
    """

    def __init__(
        self,
        v1: Vertex | None = None,
        v2: Vertex | None = None,
        *,
        uid: int | None = None,
        attributes: dict | None = None,
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

    @v1.setter
    def v1(self, new: Vertex):
        """
        Set the origin vertex of this edge.

        This edge comes *FROM* this object: v1 --> v2.

        :param new: the new vertex to associate as the start of this edge
        """
        super()._set_v1(new)

    @property
    def v2(self) -> Vertex:
        """
        Return the destination vertex of this edge.

        This edge goes *TO* this object: v1 --> v2.
        """
        return super().v2

    @v2.setter
    def v2(self, new: Vertex):
        """
        Set the destination vertex of this edge.

        This edge goes *TO* this object: v1 --> v2.

        :param new: the new vertex to associate as the destination of this edge.
        """
        super()._set_v2(new)
