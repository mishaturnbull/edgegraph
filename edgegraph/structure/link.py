#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Link class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from edgegraph.structure import base

if TYPE_CHECKING:
    from edgegraph.structure.vertex import Vertex


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

    def __init__(
        self,
        *,
        vertices: list[Vertex] | None = None,
        uid: int | None = None,
        attributes: dict | None = None,
        _force_creation: bool | None = False,
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
        # pylint complains about this being unidiomatic, and suggests
        # isinstance() instead.  however, isinstance() also returns True when
        # the given object is a *subclass* of the type -- which we don't want
        # here.  no flag or option is available to disable this; and no
        # alternative instance-but-not-subclass function is available, so here
        # we are.
        # pylint: disable-next=unidiomatic-typecheck
        if (type(self) == Link) and not _force_creation:
            raise TypeError(
                "Base class <Link> may not be instantiated directly!"
            )

        #: Vertices that this link links
        #:
        #: This is a list of vertex objects that are linked together by this
        #: class.
        self._vertices: list[Vertex] = []
        if vertices is not None:
            for vert in vertices:
                self.add_vertex(vert)

    @property
    def vertices(self) -> tuple[Vertex, ...]:
        """
        Return a tuple of vertices this edge connects.

        A tuple object is given because the addition or removal of vertex
        objects using this attribute is not intended; it is meant to be
        immutable.
        """
        return tuple(self._vertices)

    def add_vertex(self, new: Vertex):
        """
        Adds a vertex to this link.

        :param new: the vertex to add to the link
        """
        self._vertices.append(new)
        if (new is not None) and (self not in new.links):
            new.add_to_link(self)

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
