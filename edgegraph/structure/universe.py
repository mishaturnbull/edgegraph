#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the Universe class.
"""

from __future__ import annotations
import types
import edgegraph.structure.base as base
import edgegraph.structure.vertex as vertex

class UniverseLaws (base.BaseObject):
    """
    Defines the rules that apply to a universe.

    This class is effectively a namespace that controls the rules / constraints
    that a universe must obey.
    """

    fixed_attrs: set[str] = base.BaseObject.fixed_attrs | {
            "edge_whitelist",
            "mixed_links",
            "cycles",
            "multipath",
            "multiverse",
            "universe",
            }

    def __init__(self,
            edge_whitelist: dict=None,
            mixed_links: bool=False,
            cycles: bool=True,
            multipath: bool=True,
            multiverse: bool=False,
            universe: Universe=None
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
        :param universe: the universe these laws apply to
        """
        super().__init__()

        #: edge types allowed
        self._edge_whitelist = edge_whitelist

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
        self._universe = universe

    @property
    def edge_whitelist(self):
        """
        Returns an immutable copy of the edge whitelist rules.

        .. todo::

           fix the warning with ``type`` type in this docstring's ``rtype``.
           See https://stackoverflow.com/a/30624034 and link to a Python bug
           in that answer.

        :rtype: types.MappingProxyType[type: types.MappingProxyType[type: type]]
        """
        out = types.MappingProxyType({
            l: types.MappingProxyType({v1: v2 for v1, v2 in linkset}) \
                    for l, linkset in self._edge_whitelist
            })
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
    def universe(self) -> Universe:
        """
        Returns the universe that these laws apply to.
        """
        return self._universe

    @universe.setter
    def universe(self, new: Universe):
        """
        Set the universe these laws apply to.
        """
        if new is self._universe:
            return

        self._universe = new
        self._universe.laws = self

class Universe (vertex.Vertex):
    """
    Represents a universe that can contain vertices and links.
    """
    
    fixed_attrs: set[str] = vertex.Vertex.fixed_attrs | {
            "_vertices",
            "vertices",
            "_laws",
            "laws",
            }

    def __init__(self, *,
            vertices: set[vertex.Vertex]=None,
            laws: UniverseLaws=None,
            uid: int=None,
            attributes: dict=None,
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

        #: Internal set of vertices
        #:
        #: :type: set[vertex.Vertex]
        self._vertices = vertices or set()
        if not isinstance(self._vertices, set):
            self._vertices = set(self._vertices)

        #: Laws of the universe
        #:
        #: :type: UniverseLaws
        self._laws = laws
        if self._laws is None:
            self._laws = UniverseLaws(universe=self)
        self._laws.universe = self

    @property
    def laws(self) -> UniverseLaws:
        """
        Get the laws of this universe.
        """
        return self._laws

    @laws.setter
    def laws(self, new: UniverseLaws):
        """
        Set the laws of this universe.
        """
        if new is self._laws:
            return

        self._laws = new
        self._laws.universe = self

