#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Vertex class.
"""

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from collections.abc import Iterator
from edgegraph.structure import base

if TYPE_CHECKING:
    from edgegraph.structure.link import Link
    from edgegraph.structure.universe import Universe


class Vertex(base.BaseObject):
    """
    Represents a vertex in an edge-vertex graph.

    This class is a base class for anything that needs to "relate to" something
    else -- another instance, or completely different types (as long as they
    both subclass this one, at some level).
    """

    #: Enable / disable neighbor caching program-wide.
    #:
    #: .. seealso::
    #:
    #:    :ref:`dev/performance/vert-nb-cache` for more information on usage
    NEIGHBOR_CACHING: bool = False

    _QA_NB_INVALID: object = object()
    _CACHE_STATS: dict[int, list[int]] = {}

    @classmethod
    def total_cache_stats(cls) -> str:
        """
        Return a ready-to-print summary of caching statistics.

        This function can be used to get human-readable cache statistics for
        the quick-access neighbor caching.  It returns a string intended to be
        printed, logged, or written to file (it does not do anything other than
        build the string on its own).

        .. seealso::

           * :ref:`dev/performance/vert-nb-cache` for more on caching
           * :py:attr:`NEIGHBOR_CACHING` to enable / disable it

        :return: Human-readable string indicating size, hits, misses,
           invalidations, and insertions to the vertex neighbor cache.
        """
        lines = []

        if cls.NEIGHBOR_CACHING:

            totals = [0, 0, 0, 0]
            for _, stat in cls._CACHE_STATS.items():
                totals[0] += stat[0]
                totals[1] += stat[1]
                totals[2] += stat[2]
                totals[3] += stat[3]

            lines.append("=== CACHE STATISTICS OVERALL ===")
            lines.append(f"Size:          {len(Vertex._CACHE_STATS)}")
            lines.append(f"Hits:          {totals[0]}")
            lines.append(f"Misses:        {totals[1]}")
            lines.append(f"Invalidations: {totals[2]}")
            lines.append(f"Insertions:    {totals[3]}")

        else:
            lines.append("Neighbor caching is DISABLED")

        return "\n".join(lines)

    def __init__(
        self,
        *,
        links: list[Link] | None = None,
        uid: int | None = None,
        attributes: dict | None = None,
        universes: Iterator[Universe] | None = None,
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

        self._CACHE_STATS.update({self.uid: [0, 0, 0, 0]})

        #: Links that this vertex is associated with
        #:
        #: This is a list of links that include this vertex as one of the
        #: linked vertices.
        self._links: list[Link] = []
        if links is not None:
            for link in links:
                self.add_to_link(link)

        # ensure that we add ourselves to the universes given
        for uni in self.universes:
            uni.add_vertex(self)

        self.__qa_nb_cache: dict[tuple[Any, ...], list[Vertex]] = {}

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
    def links(self) -> tuple[Link, ...]:
        """
        Return a tuple of links that are attached to this object.

        A tuple is given specifically to prevent the addition or removal of
        link objects using this attribute; it is intended to be immutable.
        """
        return tuple(self._links)

    def _qa_neighbors_get(self, *args):
        """
        Check for and return quick-access neighbors cache data.

        **FOR INTERNAL USE ONLY!!**

        This function is to be used for checking for and returning (if
        available) cached neighbor data.  If no such data is available (or
        caching is disabled), :py:attr:`_QA_NB_INVALID` is returned instead as
        a sentinel.

        :param args: Arguments passed to neighbors() function.
        :return: Cached data if available, else :py:attr:`_QA_NB_INVALID`.
        """
        if not self.NEIGHBOR_CACHING:
            return self._QA_NB_INVALID

        if args in self.__qa_nb_cache:
            self._CACHE_STATS[self.uid][0] += 1

            return self.__qa_nb_cache[args]

        self._CACHE_STATS[self.uid][1] += 1
        return self._QA_NB_INVALID

    def _qa_neighbors_invalidate(self):
        """
        Invalidate the quick-access neighbor caching.

        **FOR INTERNAL USE ONLY!!**

        This function invalidates any cached neighbor data for this vertex.
        This MUST be called when the vertex's neighbors are modified in any way
        -- linked, unlinked, or anything else, to maintain cache integrity and
        prevent stale data.
        """
        if not self.NEIGHBOR_CACHING:
            return
        self._CACHE_STATS[self.uid][2] += 1
        self.__qa_nb_cache = {}

    def _qa_neighbors_insert(self, answer, *args):
        """
        Insert data into the quick-access neighbor cache.

        **FOR INTERNAL USE ONLY!!**

        This function inserts the "answer" into the neighbor cache for this
        object, with a key of ``*args``.

        :param answer: the neighbors of this object
        :param *args: Arguments passed to the neighbors() function
        """
        if not self.NEIGHBOR_CACHING:
            return
        self._CACHE_STATS[self.uid][3] += 1
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
