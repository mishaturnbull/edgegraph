#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Holds the UnDirectedEdge class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from edgegraph.structure import twoendedlink

if TYPE_CHECKING:
    from edgegraph.structure.vertex import Vertex


class UnDirectedEdge(twoendedlink.TwoEndedLink):
    """
    Represents an undirected edge (v1 -- v2) in the vertex-edge graph.

    This object is intended to join two vertices in an undirected fashion; i.e.,
    neither vertex specifically points at the other.

    .. seealso::

       * To create UnDirectedEdges, see
         :py:func:`~edgegraph.builder.explicit.link_undirected` rather than
         creating these classes directly.
    """

    # pylint correctly complains about this superclass call here, citing it is
    # useless and the method should just not be overridden.  in the strictest
    # sense, it is true -- no code changes between this __init__ and the
    # super().__init__().  however, we *do* want to override the docstring to
    # specify what this method does versus the more abstract TwoEndedLink
    # parent class.  so, we do it to change the docstring.
    # pylint: disable-next=useless-parent-delegation
    def __init__(
        self,
        v1: Vertex | None = None,
        v2: Vertex | None = None,
        *,
        uid: int | None = None,
        attributes: dict | None = None,
    ):
        """
        Instantiate an undirected edge.

        :param v1: One end of the edge
        :param v2: The other end of the edge

        .. seealso::

           * :py:meth:`edgegraph.structure.link.Link.__init__`, the
             superclass constructor
        """
        super().__init__(v1, v2, uid=uid, attributes=attributes)
