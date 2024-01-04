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
        if ((v1 is not None) and (not issubclass(type(v1), vertex.Vertex))):
            raise TypeError(f"v1 is not a Vertex object!  got {v1}")

        if ((v2 is not None) and (not issubclass(type(v2), vertex.Vertex))):
            raise TypeError(f"v2 is not a Vertex object!  got {v2}")

        super().__init__(vertices=[v1, v2], uid=uid, attributes=attributes)

    @property
    def v1(self) -> Vertex:
        """
        Return one vertex of this edge.
        """
        return self.vertices[0]

    def _set_v1(self, new: Vertex):
        """
        Helper method to set v1.
        """
        v2 = self.v2
        self.unlink_from(self.v1)
        self._vertices = []
        self.add_vertex(new)
        self._vertices.append(v2)

    @v1.setter
    def v1(self, new: Vertex):
        """
        Sets one vertex of this edge.
        """
        self._set_v1(new)

    @property
    def v2(self) -> Vertex:
        """
        Return the other vertex of this edge.
        """
        return self.vertices[1]

    def _set_v2(self, new: Vertex):
        """
        Helper method to set v2.
        """
        v1 = self.v1
        self.unlink_from(self.v2)
        self._vertices = [v1]
        self.add_vertex(new)

    @v2.setter
    def v2(self, new: Vertex):
        """
        Sets the other end of this edge.
        """
        self._set_v2(new)

