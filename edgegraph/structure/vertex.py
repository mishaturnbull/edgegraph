#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Vertex class.
"""

from __future__ import annotations
import edgegraph.structure.base as base

class Vertex (base.BaseObject):
    """
    Represents a vertex in an edge-vertex graph.

    This class is a base class for anything that needs to "relate to" something
    else -- another instance, or completely different types (as long as they
    both subclass this one, at some level).
    """

    fixed_attrs: set[str] = base.BaseObject.fixed_attrs | {
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
        self.links = links or []
        if not isinstance(self.links, list):
            self.links = list(self.links)

