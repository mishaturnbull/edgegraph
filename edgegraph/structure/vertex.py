#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Vertex class.
"""

from __future__ import annotations
from edgegraph.structure import base


class Vertex(base.BaseObject):
    """
    Represents a vertex in an edge-vertex graph.

    This class is a base class for anything that needs to "relate to" something
    else -- another instance, or completely different types (as long as they
    both subclass this one, at some level).
    """

    NEIGHBOR_CACHING = False
    _QA_NB_INVALID = object()
    CACHE_STATS = {}

    @classmethod
    def total_cache_stats(cls):

        lines = []

        if cls.NEIGHBOR_CACHING:

            totals = [0, 0, 0, 0]
            for _, stat in cls.CACHE_STATS.items():
                totals[0] += stat[0]
                totals[1] += stat[1]
                totals[2] += stat[2]
                totals[3] += stat[3]

            lines.append(f"=== CACHE STATISTICS OVERALL ===")
            lines.append(f"Size:          {len(Vertex.CACHE_STATS)}")
            lines.append(f"Hits:          {totals[0]}")
            lines.append(f"Misses:        {totals[1]}")
            lines.append(f"Invalidations: {totals[2]}")
            lines.append(f"Insertions:    {totals[3]}")

        else:
            lines.append("Neighbor caching is DISABLED")

        return '\n'.join(lines)

    def __init__(
        self,
        *,
        links: list[Link] = None,
        uid: int = None,
        attributes: dict = None,
        universes: set[Universe] = None,
    ):
        """
        Creates a new vertex.

        Unlike BaseObject, the Vertex class will add itself to Universes
        provided to this method.

        :param links: iterable of link objects to associate this vertex with

        .. seealso::

           * :py:meth:`edgegraph.structure.base.BaseObject.__init__`, the
             superclass constructor
        """
        super().__init__(uid=uid, attributes=attributes, universes=universes)

        self.CACHE_STATS.update({self.uid: [0, 0, 0, 0]})

        #: Links that this vertex is associated with
        #:
        #: This is a list of links that include this vertex as one of the
        #: linked vertices.
        #:
        #: :type: list[Link]
        self._links = []
        if links is not None:
            for link in links:
                self.add_to_link(link)

        # ensure that we add ourselves to the universes given
        for uni in self.universes:
            uni.add_vertex(self)

        self.__qa_nb_cache = {}

    def add_to_universe(self, universe: Universe) -> None:
        """
        Adds this object to a new universe.  If it is already there, no action
        is taken.

        In addition to the action(s) taken by the superclass
        (:py:meth:`~edgegraph.structure.base.BaseObject.add_to_universe`), this
        method also adds this vertex to the universes' reference of vertices,
        if needed.

        :param universe: the new universe to add this object to
        """
        super().add_to_universe(universe)
        if self not in universe.vertices:
            universe.add_vertex(self)

    @property
    def links(self) -> tuple[Link]:
        """
        Return a tuple of links that are attached to this object.

        A tuple is given specifically to prevent the addition or removal of
        link objects using this attribute; it is intended to be immutable.
        """
        return tuple(self._links)

    def _qa_neighbors_get(self, *args):
        if not self.NEIGHBOR_CACHING:
            return self._QA_NB_INVALID

        if args in self.__qa_nb_cache:
            self.CACHE_STATS[self.uid][0] += 1
                
            return self.__qa_nb_cache[args]

        self.CACHE_STATS[self.uid][1] += 1
        return self._QA_NB_INVALID

    def _qa_neighbors_invalidate(self):
        if not self.NEIGHBOR_CACHING:
            return
        self.CACHE_STATS[self.uid][2] += 1
        self.__qa_nb_cache = {}

    def _qa_neighbors_insert(self, answer, *args):
        if not self.NEIGHBOR_CACHING:
            return
        self.CACHE_STATS[self.uid][3] += 1
        self.__qa_nb_cache[args] = answer

    def add_to_link(self, link: Link):
        """
        Add this vertex to a link.

        Roughly equivalent to calling the
        :py:class:`~edgegraph.structure.link.Link`'s
        :py:meth:`~edgegraph.structure.link.Link.add_vertex` with this object
        as an argument.

        If the given link is already associated with this vertex, no action is taken.

        .. attention::

           Duplicate links ARE allowed!  However, the **same** link twice is
           not.  The difference is that of a ``==`` vs ``is`` comparison.  ``==``
           duplicate links are allowed, ``is`` duplicate links are ignored.

        :param link: the link to add this vertex to
        """
        if link not in self._links:
            self._links.append(link)
            if self not in link.vertices:
                link.add_vertex(self)

        self._qa_neighbors_invalidate()

    def remove_from_link(self, link: Link):
        """
        Remove this vertex from a link.

        :param link: the link to remove this vertex from.
        """

        if link in self._links:
            self._links.remove(link)
            link.unlink_from(self)

        self._qa_neighbors_invalidate()

    def remove_from_universe(self, universe: Universe) -> None:
        """
        Remove this vertex from the specified universe.

        In addition to the superclass method, also removes the vertex from the
        universe's record of vertices as well as simply removing the universe
        from this vertices' record of universes if necessary.

        :param universe: the universe that this vertex will be removed from
        :raises KeyError: if this object is not present in the given universe
        """
        super().remove_from_universe(universe)
        if self in universe.vertices:
            universe.remove_vertex(self)
