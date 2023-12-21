#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Link class.
"""

from __future__ import annotations
from edgegraph.structure import base

class Link (base.BaseObject):
    """
    Represents an edge in the edge-vertex graph.

    This object is the base class for edge types, and should not be used on its
    own.  Its meaning and semantics are undefined (it is neither a directed
    edge nor an undirected edge).

    .. seealso::

       :py:cls:`~edgegraph.structure.directededge.DirectedEdge`
       :py:cls:`~edgegraph.structure.undirectededge.UnDirectedEdge`

    """

    fixed_attrs: set[str] = base.BaseObject.fixed_attrs | {
            '_vertices',
            'vertices',
            }

    def __init__(self, *,
            vertices: list[Vertex]=None,
            uid: int=None,
            attributes: dict=None,
            ):
        """
        Instantiate a new link ("edge").

        .. warning::

           Generally, creating objects of this type is a bad idea, as their
           meaning is undefined.  Instead, see the subclass types that
           implement directed or undirected edges.

        :param vertices: list of Vertex objects that this link links

        .. seealso::

           * :py:meth:`edgegraph.structure.base.BaseObject.__init__`, the
             superclass constructor
        """
        super().__init__(uid=uid, attributes=attributes)

        #: Vertices that this link links
        #:
        #: This is a list of vertex objects that are linked together by this
        #: class.
        #:
        #: :type: list[Vertex]
        self._vertices = vertices or []
        if not isinstance(self._vertices, list):
            self._vertices = list(self._vertices)

    @property
    def vertices(self):
        """
        Return a tuple of vertices this edge connects.

        A tuple object is given because the addition or removal of vertex
        objects using this attribute is not intended; it is meant to be
        immutable.

        :rtype: tuple[Vertex]
        """
        return tuple(self._vertices)

