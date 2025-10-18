# -*- coding: utf-8 -*-

"""
Build graphs from adjacency matrices.

This module provides helper functions to construct a graph from a given
adjacency matrix structure, as is common in graph algorithms and software.

.. seealso::

   * https://en.wikipedia.org/wiki/Adjacency_matrix
"""

from __future__ import annotations

from collections.abc import Callable

from edgegraph.builder import explicit
from edgegraph.structure import DirectedEdge, UnDirectedEdge, Universe, Vertex


def load_adj_matrix(
    matrix: list[list[bool]],
    vertices: list[Vertex],
    linktype: type = DirectedEdge,
) -> Universe:
    """
    Load an adjacency matrix to create a graph structure.

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

    .. seealso::

       :py:func:`create_adj_matrix` is more-or-less the inverse of this
       function, producing an adjacency matrix form an already-formed graph.

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
        msg = "load_adj_matrix needs len(vertices) to be matrix len!"
        raise ValueError(msg)

    # and make sure that the matrix is a square
    for i, row in enumerate(matrix):
        if len(row) != matrixlen:
            msg = (
                f"given matrix was not a square!  row {i} had len {len(row)}"
                ",should have {matrixlen}"
            )
            raise ValueError(msg)
    # okay, good enough!

    uni = Universe()

    for vert in vertices:
        vert.add_to_universe(uni)

    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                explicit.link_from_to(vertices[i], linktype, vertices[j])

    return uni


def create_adj_matrix(uni: Universe, sort_key: Callable[[Vertex], int]) -> list[list[bool]]:
    """
    Create an adjacency matrix from a given universe.

    This function creates and returns an adjacency matrix from a given
    already-formed graph.  The structure and meaning of the matrix is the same
    as in :py:func:`load_adj_matrix`.

    Note that this function requires not only the universe graph container, but
    also a sort key.  This sort key controls the order of rows and columns
    within the output matrix.  Consider the following matrix, which clearly
    labels rows and columns:

    +----+-------+-------+-------+-------+-------+-------+
    |    | v0    | v1    | v2    | v3    | v4    | v5    |
    +----+-------+-------+-------+-------+-------+-------+
    | v0 | False | True  | True  | True  | False | False |
    +----+-------+-------+-------+-------+-------+-------+
    | v1 | False | False | True  | True  | True  | False |
    +----+-------+-------+-------+-------+-------+-------+
    | v2 | False | False | False | True  | True  | True  |
    +----+-------+-------+-------+-------+-------+-------+
    | v3 | False | False | False | True  | False | False |
    +----+-------+-------+-------+-------+-------+-------+
    | v4 | False | False | False | False | False | False |
    +----+-------+-------+-------+-------+-------+-------+
    | v5 | False | False | False | False | False | False |
    +----+-------+-------+-------+-------+-------+-------+

    Now, if this is the matrix you wish to get out of this function, you must
    tell it which vertex is v0, which is v1, which is v2, etc..  This is what
    the sort_key argument is for.  It is passed directly to the builtin
    :py:func:`sorted`'s ``key`` argument.

    Note that if you are using a custom subclass of
    :py:class:`~edgegraph.structure.vertex.Vertex` which implements rich
    comparison methods, you may pass ``None`` to this argument to relegate
    sorting to these rich comparisons.

    .. seealso::

       * Python rich comparison methods:
         https://docs.python.org/3/reference/datamodel.html#object.__lt__
       * :py:func:`sorted` builtin, which is used internally in this method

    .. note::

        In some scenarios, with the right arguments, this function and
        :py:func:`load_adj_matrix` can perform exactly inverse operations.  The
        requirements for this to occur are:

        #. The ``sort_key`` parameter given here excatly replicates the order
           of vertices given in the ``vertices`` argument to
           :py:func:`load_adj_matrix`
        #. Either:

           #. Directed edges are used throughout the graph, or
           #. Both:

              #. Undirected edges are used throughout the graph
              #. The matrix given to :py:func:`load_adj_matrix` is symmetric
                 over the diagonal

        In all other cases, it is **NOT GUARANTEED** that these two functions
        perform precisely inverse operations.  This may return matrices that
        are slightly different, especially when using undirected edges.

        This is expected and desired behavior.

    .. seealso::

       The :py:func:`load_adj_matrix` function is *nearly* the inverse of this
       one.

    :param uni: The Universe graph container to analyze.
    :param sort_key: A function of one argument which specifies a comparison
       key for each vertex in the given universe.  It may be set to ``None`` if
       the vertices are of a custom subtype which implements rich comparison
       operators.
    :return: A square 2-dimensional array (matrix), representing adjacency
       within the graph.  The elements are set to either ``True`` or ``False``
       to indicate a link.
    """
    sorted_verts = sorted(uni.vertices, key=sort_key)
    matrix = []

    for vert in sorted_verts:
        row = [False] * len(sorted_verts)
        matrix.append(row)
        for link in vert.links:
            if isinstance(link, DirectedEdge) and vert is link.v1:
                row[sorted_verts.index(link.v2)] = True

            elif isinstance(link, UnDirectedEdge):
                row[sorted_verts.index(link.other(vert))] = True

    return matrix
