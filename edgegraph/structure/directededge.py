#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the DirectedEdge class.
"""

from __future__ import annotations
from edgegraph.structure import link, vertex


class DirectedEdge (link.Link):
    """
    Represents a directed edge (v1 --> v2) in the vertex-edge graph.

    This object is intended to join two vertices in a directed fashion; i.e.,
    one vertex directs to the other.
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
        Instantiate a directed edge.

        :param v1: The first vertex in the edge (the link will be *FROM* this
           one)
        :param v2: The second vertex in the edge (thie link will be *TO* this
           one)

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
        Return the origin vertex of this edge.

        This edge comes *FROM* this object: v1 --> v2.
        """
        return self._v1

    @property
    def v2(self) -> Vertex:
        """
        Return the destination vertex of this edge.

        This edge goes *TO* this object: v1 --> v2.
        """
        return self._v2

