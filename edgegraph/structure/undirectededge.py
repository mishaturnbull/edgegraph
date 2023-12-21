#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the UnDirectedEdge class.
"""

from __future__ import annotations
from edgegraph.structure import link, vertex


class UnDirectedEdge (link.Link):
    """
    Represents an undirected edge (v1 -- v2) in the vertex-edge graph.

    This object is intended to join two vertices in an undirected fashion; i.e.,
    neither vertex specifically points at the other.
    """

    fixed_attrs: set[str] = link.Link.fixed_attrs | {
            '_v1', 'v1',
            '_v2', 'v2',
            }

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
        super().__init__(vertices=[v1, v2], uid=uid, attributes=attributes)

        #: Origin vertex
        #:
        #: :type: Vertex
        self._v1 = v1
        if ((self._v1 is not None) and
                (not issubclass(type(self._v1), vertex.Vertex))):
            raise TypeError(f"v1 is not a Vertex object!  got {self._v1}")

        #: Destination vertex
        #:
        #: :type: Vertex
        self._v2 = v2
        if ((self._v2 is not None) and
                (not issubclass(type(self._v2), vertex.Vertex))):
            raise TypeError(f"v2 is not a Vertex object!  got {self._v2}")

    @property
    def v1(self) -> Vertex:
        """
        Return one vertex of this edge.
        """
        return self._v1

    @property
    def v2(self) -> Vertex:
        """
        Return the other vertex of this edge.
        """
        return self._v2

