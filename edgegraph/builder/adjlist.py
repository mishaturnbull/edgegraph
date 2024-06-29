#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Build graphs from adjacency lists.

This module provides helper functions to construct a graph from a given
adjacency list structure, as is common in graph algorithms and software.

.. seealso::

   * https://en.wikipedia.org/wiki/Adjacency_list
"""

from __future__ import annotations

from edgegraph.structure import Universe, UnDirectedEdge
from edgegraph.builder import explicit


def load_adj_dict(
    adjdict: dict,
    linktype: type = UnDirectedEdge,
) -> Universe:
    """
    Load an "adjacency dictionary" to create a
    :py:class:`~edgegraph.structure.universe.Universe` object.

    The input structure is expected to be of the following structure:

    .. code-block:: python

       adjdict = {
           v0: [v1, v2, v3],  # these don't have to be *lists* --
           v1: [v2, v3, v4],  # only iterable objects
           v2: [v3, v4, v5],
           v3: [v3],          # origin in list -> self-edge
           v5: []             # empty list -> no edges
           }

    where all :samp:`v{x}` values are
    :py:class:`~edgegraph.structure.vertex.Vertex` instances (or subclasses
    thereof).  The given example will produce the following structure:

    .. uml::

       object v0
       object v1
       object v2
       object v3
       object v4
       object v5

       v0 -- v1
       v0 -- v2
       v0 -- v3
       v1 -- v2
       v1 -- v3
       v1 -- v4
       v2 -- v3
       v2 -- v4
       v2 -- v5
       v3 -- v3

    Existing links between vertices are not checked or altered.  If, in the
    above example, ``v0`` was already linked to ``v2``, this function would
    create *another* link between those vertices.

    .. attention::

       This process has side effects on the vertices that are a part of the
       adjacency dictionary!  They are all added to a new universe and linked
       to the other vertices given.

    :param adjdict: Adjacency dictionary as described above
    :param linktype: Class of links to use in creation.  May be any subclass of
       :py:class:`~edgegraph.structure.twoendedlink.TwoEndedLink`; default is
       :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.
    :return: a Universe containing the graph described in ``adjdict``.
    """
    uni = Universe()
    for v1, v2s in adjdict.items():
        v1.add_to_universe(uni)
        for v2 in v2s:
            explicit.link_from_to(v1, linktype, v2)
            v2.add_to_universe(uni)
    return uni
