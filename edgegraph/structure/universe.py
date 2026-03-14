# -*- coding: utf-8 -*-

"""
Holds the Universe class.
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from edgegraph.structure import vertex

if TYPE_CHECKING:
    Vertex = vertex.Vertex


class Universe(vertex.Vertex):
    """
    Represents a universe that can contain vertices and links.

    This is the container of vertices.  It may also reasonably be called a
    "graph" object -- the collection of all edges and vertices under
    examination at any given moment.  However, it is more flexible in
    implementation, and can actually contain any subclass of
    :py:class:`~edgegraph.structure.base.BaseObject` (though they may not
    appear in graph-related operations, such as traversals or searches, if they
    do not subclass :py:class:`~edgegraph.structure.vertex.Vertex`.)

    Pay attention that this class itself is a subclass of
    :py:class:`~edgegraph.structure.vertex.Vertex`; this means that while
    containing an entire graph (or more) on its own, this object can also be
    treated as a vertex inside another universe.  In this way, you can create
    graphs *of other graphs*, even recursively if you like.  Whether or not
    this is a good idea greatly depends on the situation, but the
    implementation allows it (this is a *feature*, not an implementation
    detail).
    """

    def __init__(
        self,
        *,
        vertices: set[vertex.Vertex] | None = None,
        uid: int | None = None,
        attributes: dict | None = None,
    ):
        """
        Instantiate a Universe.

        :param vertices: a set of vertices to link to this universe

        .. seealso::

           * :py:meth:`edgegraph.structure.vertex.Vertex.__init__`, the
             superclass constructor
        """
        super().__init__(uid=uid, attributes=attributes)

        self._verts_lock = threading.RLock()

        #: Internal set of vertices
        self._vertices: list[Vertex] = []
        if vertices is not None:
            for v in vertices:
                self.add_vertex(v)

    def __getstate__(self) -> dict:
        data = self.__dict__.copy()
        data.pop("_verts_lock")
        return data

    def __setstate__(self, value: dict) -> None:
        self.__dict__.update(value)
        self.__dict__["_verts_lock"] = threading.RLock()

    @property
    def vertices(self) -> list[vertex.Vertex]:
        """
        Return a list of vertices that this universe contains.

        Note that the returned copy is just that, a copy.  Modifications to the
        list that you may make will have no impact to the universe.

        .. seealso::

           :py:meth:`add_vertex` can be used to add a vertex, and
           :py:meth:`remove_vertex` can be used to remove one.

        :return: vertices belonging to this universe, ordered by insertion
           order.
        """
        with self._verts_lock:
            return list(self._vertices)

    def add_vertex(self, vert: vertex.Vertex):
        """
        Add a new vertex to this universe.

        The vertex in question will automatically have its universes updated to
        include this one, if needed.  If the vertex is already present, no
        action is taken.

        .. seealso::

           :py:attr:`vertices` to see what vertices are present in this
           universe, and :py:meth:`remove_vertex` to remove a vertex.

        :param vert: the vertex to be added
        """
        with self._verts_lock:
            if vert in self._vertices:
                return

            self._vertices.append(vert)
            if self not in vert.universes:
                vert.add_to_universe(self)

    def remove_vertex(self, vert: vertex.Vertex):
        """
        Remove a vertex from this universe.

        The vertex in question will be removed from this universe's record of
        vertices.  If necessary. this universe will then be removed from the
        vertices' record of universes as well.

        :param vert: the vertex to be removed
        """
        with self._verts_lock:
            self._vertices.remove(vert)
            if self in vert.universes:
                vert.remove_from_universe(self)
