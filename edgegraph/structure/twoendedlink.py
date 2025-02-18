#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the TwoEndedLink class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from edgegraph.structure import link, vertex

if TYPE_CHECKING:
    from edgegraph.structure.vertex import Vertex


class TwoEndedLink(link.Link):
    """
    Represents an two-ended edge (v1 and v2) in the vertex-edge graph.  It is
    neither undirected nor directed, and not intended for explicit use.

    .. seealso::

       You may want one of these subclasses of links, which *are* intended for
       explicit use:

       * :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`
       * :py:class:`~edgegraph.structure.directededge.DirectedEdge`
    """

    def __init__(
        self,
        v1: Vertex | None = None,
        v2: Vertex | None = None,
        *,
        uid: int | None = None,
        attributes: dict | None = None,
    ):
        """
        Instantiate an two-ended edge.

        :param v1: One end of the edge
        :param v2: The other end of the edge

        .. seealso::

           * :py:meth:`edgegraph.structure.link.Link.__init__`, the
             superclass constructor
        """
        if (v1 is not None) and (not issubclass(type(v1), vertex.Vertex)):
            raise TypeError(f"v1 is not a Vertex object!  got {v1}")

        if (v2 is not None) and (not issubclass(type(v2), vertex.Vertex)):
            raise TypeError(f"v2 is not a Vertex object!  got {v2}")

        # mypy complains about the vertices list below, that it may contain
        # None if the v1 or v2 arguments were not specified in our constructor
        # here.  however, that scenario is prevented by the TypeError checks
        # above; mypy just doesn't seem to recognize it as type narrowing.
        super().__init__(vertices=[v1, v2], uid=uid, attributes=attributes)  # type: ignore

    @property
    def v1(self) -> Vertex:
        """
        Return one vertex of this edge.

        Setting this attribute automatically handles link-vertex assocation
        updates; no extra effort is necessary.
        """
        return self.vertices[0]

    @v1.setter
    def v1(self, new: Vertex):
        """
        Sets one vertex of this edge.
        """
        self._set_v1(new)

    def _set_v1(self, new: Vertex):
        """
        Helper method to set v1.

        Why does this method exist, you ask, instead of just doing it in
        @v1.setter ?  Good question!  I want to use this same code in
        subclasses, but :py:`super` does not support attribute assignment.  See
        https://github.com/python/cpython/issues/59170.

        So, instead, this method exists -- then subclasses can call
        ``super()._set_v1(new)`` from their implementation of @v1.setter, and
        all is well.  Except the access to a private method... but it seems the
        least bad option, IMO.
        """
        v2 = self.v2
        self.unlink_from(self.v1)
        self._vertices = []
        self.add_vertex(new)
        self._vertices.append(v2)

    @property
    def v2(self) -> Vertex:
        """
        Return the other vertex of this edge.

        Setting this attribute automatically handles link-vertex assocation
        updates; no extra effort is necessary.
        """
        return self.vertices[1]

    @v2.setter
    def v2(self, new: Vertex):
        """
        Sets the other end of this edge.
        """
        self._set_v2(new)

    def _set_v2(self, new: Vertex):
        """
        Helper method to set v2.

        For a brief on why this exists, see
        :py:meth:`~edgegraph.structure.TwoEndedLink._set_v1`.
        """
        v1 = self.v1
        self.unlink_from(self.v2)
        self._vertices = [v1]
        self.add_vertex(new)

    def other(self, end: Vertex) -> Vertex | None:
        """
        Identify and return the other end of this edge.

        This is mainly a convience method -- it accepts one vertex as an
        argument, figures out whether it's v1 or v2 of this edge, and returns
        v2 or v1 respectively.

        Should the given vertex not be a part of this edge, ``None`` is
        returned.

        :param end: one end of this edge
        :return: the other end of this edge, or None
        """
        if end is self.v1:
            return self.v2
        if end is self.v2:
            return self.v1

        return None
