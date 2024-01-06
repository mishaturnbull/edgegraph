#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the UnDirectedEdge class.
"""

from __future__ import annotations
from edgegraph.structure import twoendedlink, vertex


class UnDirectedEdge (twoendedlink.TwoEndedLink):
    """
    Represents an undirected edge (v1 -- v2) in the vertex-edge graph.

    This object is intended to join two vertices in an undirected fashion; i.e.,
    neither vertex specifically points at the other.
    """

    def __init__(self,
            v1: Vertex=None,
            v2: Vertex=None,
            *,
            uid: int=None,
            attributes: dict=None,
            ):
        """
        Instantiate an undirected edge.

        :param v1: One end of the edge
        :param v2: The other end of the edge

        .. seealso::

           * :py:meth:`edgegraph.structure.link.Link.__init__`, the
             superclass constructor
        """
        super().__init__(v1, v2, uid=uid, attributes=attributes)

