#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Build graphs from adjacency matrices.

This module provides helper functions to construct a graph from a given
adjacency matrix structure, as is common in graph algorithms and software.

.. seealso::

   * https://en.wikipedia.org/wiki/Adjacency_matrix
"""

from __future__ import annotations

from edgegraph.structure import Universe, Vertex, DirectedEdge
from edgegraph.builder import explicit


def load_adj_matrix(
    matrix: list[list[bool]],
    vertices: list[Vertex],
    linktype: type = DirectedEdge,
) -> Universe:
    """
    Loads an adjacency matrix to create a graph structure.

    The input structure is expected to be a list of list of booleans.  A "side
    array" is also required, to denote the vertices.  Inputting of the
    following matrix is given:

    +----+----+----+----+----+----+----+
    |    | v0 | v1 | v2 | v3 | v4 | v5 |
    +----+----+----+----+----+----+----+
    | v0 | 0  | 1  | 1  | 1  | 0  | 0  |
    +----+----+----+----+----+----+----+
    | v1 | 0  | 0  | 1  | 1  | 1  | 0  |
    +----+----+----+----+----+----+----+
    | v2 | 0  | 0  | 0  | 1  | 1  | 1  |
    +----+----+----+----+----+----+----+
    | v3 | 0  | 0  | 0  | 1  | 0  | 0  |
    +----+----+----+----+----+----+----+
    | v4 | 0  | 0  | 0  | 0  | 0  | 0  |
    +----+----+----+----+----+----+----+
    | v5 | 0  | 0  | 0  | 0  | 0  | 0  |
    +----+----+----+----+----+----+----+


    .. code-block:: python
       :linenos:

       # define the "side array"
       vertices = [v0, v1, v2, v3, v4, v5]

       # and the matrix
       matrix = [
           [0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 0, 0],
           [0] * 6,
           [0] * 6
           ]

       universe = load_adj_matrix(matrix, vertices)

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

       v0 --> v1
       v0 --> v2
       v0 --> v3
       v1 --> v2
       v1 --> v3
       v1 --> v4
       v2 --> v3
       v2 --> v4
       v2 --> v5
       v3 --> v3

    Existing links between vertices are not checked or altered.  If, in the
    above example, ``v0`` was already linked to ``v2``, this function would
    create *another* link between those vertices.

    .. attention::

       This process has side effects on the vertices that are a part of the
       adjacency dictionary!  They are all added to a new universe and linked
       to the other vertices given.

    .. note::

       If you select an un-directed edge type for the ``linktype`` param, a
       graph algorithms textbook would have you believe these matrices should
       be symmetrical across the diagonal.  This is great in theory -- but
       here, EITHER of the cells :math:`a_{ij}` or :math:`a_{ji}` being truthy
       will set the link.

       This is an implementation detail, not a part of the API specification,
       and may be changed without notice!

    :param matrix: The adjacency matrix.  Each individual "cell" is tested for
       truthy-ness -- if :py:`bool(x)` would return ``True``, a link is
       created.
    :param vertices: The "side array" defining the vertices that run along the
       sides of the matrix.  Must be an iterable object containing
       :py:class:`~edgegraph.structure.vertex.Vertex` objects (or subclasses
       thereof).
    :param linktype: Class of links to use in creation.  May be any subclass of
       :py:class:`~edgegraph.structure.twoendedlink.TwoEndedLink`; default is
       :py:class:`~edgegraph.structure.directededge.DirectedEdge`.
    """

    # some sanity checks up front
    # make sure the side array is the same size as the matrix
    matrixlen = len(matrix)
    if len(vertices) != matrixlen:
        raise ValueError(
            "load_adj_matrix needs len(vertices) to be matrix len!"
        )
    # and make sure that the matrix is a square
    for i, row in enumerate(matrix):
        if len(row) != matrixlen:
            raise ValueError(
                f"given matrix was not a square!  row {i} had "
                f"len {len(row)}, should have {matrixlen}"
            )
    # okay, good enough!

    uni = Universe()

    for vert in vertices:
        vert.add_to_universe(uni)

    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                explicit.link_from_to(vertices[i], linktype, vertices[j])

    return uni
