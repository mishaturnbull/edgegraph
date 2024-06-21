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

    fixed_attrs: set[str] = base.BaseObject.fixed_attrs | {
        "_links",
        "links",
    }

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

        :param links: iterable of link objects to associate this vertex with

        .. seealso::

           * :py:meth:`edgegraph.structure.base.BaseObject.__init__`, the
             superclass constructor
        """
        super().__init__(uid=uid, attributes=attributes, universes=universes)

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

    def _add_linkage(self, new: Link):
        """
        Adds a linkage to the internal list of links.

        :param new: the link to add to our list of links
        """
        if new not in self._links:
            self._links.append(new)
            self._update_link_linkages()

    def _update_link_linkages(self):
        """
        Ensure that all of our links know about that this vertex is an
        endpoint.

        Takes no arguments and has no return.
        """
        for link in self._links:
            if self not in link.vertices:
                link._add_linkage(self)

    @property
    def links(self) -> tuple[Link]:
        """
        Return a tuple of links that are attached to this object.

        A tuple is given specifically to prevent the addition or removal of
        link objects using this attribute; it is intended to be immutable.
        """
        return tuple(self._links)

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
        self._add_linkage(link)

    def remove_from_link(self, link: Link):
        """
        Remove this vertex from a link.

        :param link: the link to remove this vertex from.
        """

        if link in self._links:
            self._links.remove(link)
            link.unlink_from(self)
