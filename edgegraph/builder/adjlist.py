# -*- coding: utf-8 -*-

"""
Build graphs from adjacency lists.

This module provides helper functions to construct a graph from a given
adjacency list structure, as is common in graph algorithms and software.

.. seealso::

   * https://en.wikipedia.org/wiki/Adjacency_list
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from edgegraph.builder import explicit
from edgegraph.structure import DirectedEdge, UnDirectedEdge, Universe

if TYPE_CHECKING:
    from edgegra.structure.vertex import Vertex


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

    .. seealso::

       The :py:func:`create_adj_dict` function is more-or-less the inverse of
       this one, accepting a Universe as an argument and returning an adjacency
       dictionary.

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


def create_adj_dict(
    uni: Universe,
) -> dict[Vertex, list[Vertex]]:
    """
    Create an adjacency dict from a graph.  Effectively the reverse of
    :py:func:`load_adj_dict`.

    This function returns an adjacency dictionary from a graph.  This
    dictionary lists all unique vertices as the keys, and then all vertices
    which they link to are given as a list in the value.  For example, consider
    the following graph:

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

    The adjacency dictionary returned would look like:

    .. code-block:: python

       {
       v0: [v1, v2, v3],
       v1: [v0, v2, v3, v4],
       v2: [v0, v1, v3, v4, v5],
       v3: [v0, v1, v2, v3],      # origin in list -> self-edge
       v4: [v1, v2],
       v5: [v2],
       }

    Directed edges (:py:class:`~edgegraph.structure.directededge.DirectedEdge`
    and subclasses thereof) are respected, and a vertex will only be considered
    linked to another if it follows the forward direction.  Undirected edges
    (:py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge` and
    subclasses thereof) are considered linked in either direction.

    .. note::

       You may assume that ``create_adj_dict(load_adj_dict(d))`` returns
       exactly ``d`` for some adjacency dict ``d``.  However, this is **NOT
       ALWAYS TRUE**, especially when dealing with undirected edges!!  This
       function adds all reachable vertices to the list for each vertex; which
       means for an undirected edge, both vertices will be listed in the
       adjacency entries for each of them.

       This is expected and desired behavior.

    .. seealso::

       The :py:func:`load_adj_dict` function is more-or-less the inverse of
       this one, accepting the adjacency dictionary as an argument and
       returning a formed graph.

    :param uni: The Universe graph container to analyze.
    :return: A dictionary containing adjacency information for the given
       universe.
    """
    out = {}

    for vert in uni.vertices:
        out[vert] = []

        for link in vert.links:
            if isinstance(link, DirectedEdge) and vert is link.v1:
                out[vert].append(link.v2)

            elif isinstance(link, UnDirectedEdge):
                out[vert].append(link.other(vert))

    return out
