#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Vertex class.
"""

from __future__ import annotations
from edgegraph.structure import base

class Vertex (base.BaseObject):
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

    def __init__(self, *,
            links: list=None,
            uid: int=None,
            attributes: dict=None,
            universes: set[Universe]=None,
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
        #: :type: list
        self._links = links or []
        if not isinstance(self._links, list):
            self._links = list(self._links)

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
    def links(self):
        """
        Return a tuple of links that are attached to this object.

        A tuple is given specifically to prevent the addition or removal of
        link objects using this attribute; it is intended to be immutable.

        :rtype: tuple[Link]
        """
        return tuple(self._links)

