#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Link class.
"""

from __future__ import annotations
import warnings
from edgegraph.structure import base


class Link(base.BaseObject):
    """
    Represents an edge in the edge-vertex graph.

    .. warning::

       This object is the base class for edge types, and should not be used on
       its own.  Its meaning and semantics are undefined (it is neither a
       directed edge nor an undirected edge).

    .. seealso::

       * :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`, a
         subclass representing an undirected edge between two vertices
       * :py:class:`~edgegraph.structure.directededge.DirectedEdge`, a subclass
         representing a directed edge between two vertices

    """

    fixed_attrs: set[str] = base.BaseObject.fixed_attrs | {
        "_vertices",
        "vertices",
    }

    def __init__(
        self,
        *,
        vertices: list[Vertex] = None,
        uid: int = None,
        attributes: dict = None,
        _force_creation: bool = False,
    ):
        """
        Instantiate a new link ("edge").

        .. warning::

           Generally, creating objects of this type is a bad idea, as their
           meaning is undefined.  Instead, see the subclass types that
           implement directed or undirected edges.

        :param vertices: list of Vertex objects that this link links
        :param _force_creation: force the instantiation of this object without
           error

        .. seealso::

           * :py:meth:`edgegraph.structure.base.BaseObject.__init__`, the
             superclass constructor
        """
        super().__init__(uid=uid, attributes=attributes)

        # prevent direct usage of this class -- its meaning is undefined
        if (type(self) == Link) and not _force_creation:
            raise TypeError("Base class <Link> may not be instantiated " "directly!")

        #: Vertices that this link links
        #:
        #: This is a list of vertex objects that are linked together by this
        #: class.
        #:
        #: :type: list[Vertex]
        self._vertices = []
        if vertices is not None:
            for vert in vertices:
                self.add_vertex(vert)

    def _add_linkage(self, new: Vertex):
        """
        Adds a vertex to the internal list of vertices.

        :param new: the vertex to add to our list of vertices
        """
        self._vertices.append(new)
        self._update_vertex_linkages()

    def _update_vertex_linkages(self):
        """
        Ensure that all of our vertices know about this link.

        While this is mainly intended for internal use only, calling it
        directly shouldn't really do any harm.

        Takes no arguments and has no return.
        """
        for vert in self._vertices:
            if (vert is not None) and (self not in vert.links):
                vert._add_linkage(self)

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

    def add_vertex(self, new: Vertex):
        """
        Adds a vertex to this link.

        :param new: the vertex to add to the link
        """
        self._add_linkage(new)

    def unlink_from(self, kill: Vertex):
        """
        Remove the link association from the given vertex.

        This is effectively "unlinking" the specified vertex from this link.
        If this link is not associated with the given vertex, no action is
        taken.

        :param kill: the vertex to unlink
        """
        if kill in self._vertices:
            self._vertices.remove(kill)

            if kill is not None:
                kill.remove_from_link(self)
