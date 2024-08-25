#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Build graphs in the most manual form possible; taking two vertices and linking
them.

This module provides facilities for explicit, direct linking of vertices in
order to gradually build out a graph.

Most of the functions in this module are one-liners.  Seriously.  It exists to
standardize the methods by which links are associated, so that changes to the
structure classes can occur without breaking everyone's code -- instead, these
functions will get the necessary updates to match, and the API stays unchanged.
"""

from __future__ import annotations

from edgegraph.structure import Vertex, DirectedEdge, UnDirectedEdge


def link_from_to(v1: Vertex, lnktype: type, v2: Vertex, dontdup: bool = False):
    """
    Create a link of type ``lnktype`` from ``v1`` to ``v2``.

    This function instantiates a new link type (a subclass of
    :py:class:`~edgegraph.structure.twoendedlink.TwoEndedLink`.  It then
    associates both given vertices to the link instance.

    .. seealso::

       The :py:func:`link_directed` and :py:func:`link_undirected` functions
       create :py:class:`~edgegraph.structure.directededge.DirectedEdge` and
       :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`
       respectively in a similar manner to this function.

    :param v1: One end of the link.
    :param lnktype: The class of the link.
    :param v2: The other end of the link.
    :param dontdup: If set to True, performs a check for any already-existing
      links between v1 and v2.  If any are found (of any type, directed or
      undirected), no new link is created, but the already-existing one is
      returned silently.
    :return: The link instance.
    :rtype: An instance of the param ``lnktype``.
    """

    if dontdup:
        for lnk in v1.links:
            if lnk.other(v1) is v2:
                return lnk

    return lnktype(v1, v2)


def link_directed(
    v1: Vertex, v2: Vertex, dontdup: bool = False
) -> DirectedEdge:
    """
    Create a :py:class:`~edgegraph.structure.directededge.DirectedEdge` between
    the two vertices.

    This function instantiates a new
    :py:class:`~edgegraph.structure.directededge.DirectedEdge` class such that
    the given ``v1`` is the "from" vertex and the given ``v2`` is the "to"
    vertex.

    Before:

       .. uml::

          object v1
          object v2
          v1 -r[hidden]-> v2

    After:

       .. uml::

          object v1
          object v2
          v1 -r-> v2 : DirectedEdge

    :param v1: The origin end of the link.
    :param v2: The destination end of the link.
    :param dontdup: If set to True, performs a check for any already-existing
      links between v1 and v2.  If any are found (of any type, directed or
      undirected), no new link is created, but the already-existing one is
      returned silently.
    :return: The link that was created.
    """
    return link_from_to(v1, DirectedEdge, v2, dontdup=dontdup)


def link_undirected(
    v1: Vertex, v2: Vertex, dontdup: bool = False
) -> UnDirectedEdge:
    """
    Create a :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`
    between the two vertices.

    Before:

       .. uml::

          object v1
          object v2
          v1 -r[hidden]- v2

    After:

       .. uml::

          object v1
          object v2
          v1 -r- v2 : UnDirectedEdge

    :param v1: One end of the link.
    :param v2: The other end of the link.
    :param dontdup: If set to True, performs a check for any already-existing
      links between v1 and v2.  If any are found (of any type, directed or
      undirected), no new link is created, but the already-existing one is
      returned silently.
    :return: The link that was created.
    """
    return link_from_to(v1, UnDirectedEdge, v2, dontdup=dontdup)
