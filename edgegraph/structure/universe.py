#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Universe class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import types
from edgegraph.structure import base, vertex

if TYPE_CHECKING:
    Vertex = vertex.Vertex


class UniverseLaws(base.BaseObject):
    """
    Defines the rules that apply to a universe.

    This class is effectively a namespace that controls the rules / constraints
    that a universe must obey.

    Pay close attention to the difference in meaning between the
    :py:attr:`applies_to` and :py:attr:`universes` attributes.  The former
    (applies_to) refers to the universe that these laws apply to.  This object
    is not necessarily a vertex / object present in that universe.  The latter
    (universes) is the set of universes this object *appears in*; see also
    :py:attr:`edgegraph.structure.base.BaseObject.universes`, where the latter
    (universes) is inherited from.

    Likewise, the :py:meth:`add_to_universe` and
    :py:meth:`remove_from_universe` are inherited from
    :py:meth:`edgegraph.structure.base.BaseObject.add_to_universe` and
    :py:meth:`edgegraph.structure.base.BaseObject.remove_from_universe`.
    """

    def __init__(
        self,
        edge_whitelist: dict | None = None,
        mixed_links: bool = False,
        cycles: bool = True,
        multipath: bool = True,
        multiverse: bool = False,
        applies_to: Universe | None = None,
    ):
        """
        Instantiate a set of universal laws.

        .. important::

           After creation / instantiation, the attributes of this object become
           read-only!

        :param edge_whitelist: dictionary of types of links allowed
        :param mixed_links: whether or not mixed link types are allowed
        :param cycles: whether or not cycles are allowed
        :param multipath: whether or not multiple paths between nodes are
            allowed (not necessarily cycles)
        :param multiverse: whether or not universes may be connected inside
            this universe
        :param applies_to: the universe these laws apply to
        """
        super().__init__()

        #: edge types allowed
        self._edge_whitelist = edge_whitelist
        try:
            self.edge_whitelist
        except (ValueError, AttributeError) as exc:
            # re-raise, but with a more clear message of what's happening
            raise ValueError(
                "Given edge_whitelist is of incorrect structure!"
            ) from exc

        #: whether or not mixed link types are allowed
        #:
        #: TODO: is this functionality covered by edge_whitelist ??
        self._mixed_links = mixed_links

        #: whether or not cycles are allowed
        self._cycles = cycles

        #: whether or not multipaths are allowed
        self._multipath = multipath

        #: whether or not universes may be vertices in this universe
        self._multiverse = multiverse

        #: the universe these laws apply to
        self._applies_to = applies_to

    @property
    def edge_whitelist(self):
        """
        Returns an immutable copy of the edge whitelist rules.

        :rtype: types.MappingProxyType[type, types.MappingProxyType[type, type]] or None
        """
        if self._edge_whitelist is None:
            return None

        out = types.MappingProxyType(
            {
                t: types.MappingProxyType(dict(linkset.items()))
                for t, linkset in self._edge_whitelist.items()
            }
        )
        return out

    @property
    def mixed_links(self) -> bool:
        """
        Returns whether or not mixed types of links are allowed here.
        """
        return self._mixed_links

    @property
    def cycles(self) -> bool:
        """
        Returns whether or not cycles are allowed in this universe.
        """
        return self._cycles

    @property
    def multipath(self) -> bool:
        """
        Returns whether or not multiple paths between nodes are allowed in this
        universe.
        """
        return self._multipath

    @property
    def multiverse(self) -> bool:
        """
        Returns whether ot not this is a "multiverse" -- that is, whether other
        Universes are allowed to be vertices in this graph.
        """
        return self._multiverse

    @property
    def applies_to(self) -> Universe | None:
        """
        Returns the universe that these laws apply to.
        """
        return self._applies_to

    @applies_to.setter
    def applies_to(self, new: Universe):
        """
        Set the universe these laws apply to.
        """
        if new is self._applies_to:
            return

        self._applies_to = new

        if self._applies_to is not None:
            self._applies_to.laws = self


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
        laws: UniverseLaws | None = None,
        uid: int | None = None,
        attributes: dict | None = None,
    ):
        """
        Instantiate a Universe.

        :param vertices: a set of vertices to link to this universe
        :param laws: the laws of nature that apply to this universe

        .. seealso::

           * :py:meth:`edgegraph.structure.vertex.Vertex.__init__`, the
             superclass constructor
        """
        super().__init__(uid=uid, attributes=attributes)

        #: Laws of the universe
        self._laws: UniverseLaws | None = laws
        if self._laws is None:
            self._laws = UniverseLaws(applies_to=self)
        self._laws.applies_to = self

        #: Internal set of vertices
        self._vertices: list[Vertex] = []
        if vertices is not None:
            for v in vertices:
                self.add_vertex(v)

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
        return list(self._vertices)

    def add_vertex(self, vert: vertex.Vertex):
        """
        Adds a new vertex to this universe.

        The vertex in question will automatically have its universes updated to
        include this one, if needed.  If the vertex is already present, no
        action is taken.

        .. seealso::

           :py:attr:`vertices` to see what vertices are present in this
           universe, and :py:meth:`remove_vertex` to remove a vertex.

        :param vert: the vertex to be added
        """
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
        self._vertices.remove(vert)
        if self in vert.universes:
            vert.remove_from_universe(self)

    @property
    def laws(self) -> UniverseLaws | None:
        """
        Get the laws of this universe.
        """
        return self._laws

    @laws.setter
    def laws(self, new: UniverseLaws):
        """
        Set the laws of this universe.
        """
        # covers the None-and-None case as well as already-assigned
        if new is self._laws:
            return

        # deassignment
        if self._laws is not None and new is None:
            # pylint (rightfully) complains about the access to a private
            # member here -- but, since we're still within the library, this is
            # allowed.  it would, however, be an issue if a user of edgegraph
            # were accessing this
            # pylint: disable-next=protected-access
            self._laws._applies_to = None
            self._laws = None

        # new- and re-assignment
        else:
            # mypy can't seem to figure out the type-narrowing here.  in this
            # else clause, self._laws won't be none
            self._laws.applies_to = None  # type: ignore

            self._laws = new
            self._laws.applies_to = self
