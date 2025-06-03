#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Helper functions for graph traversals.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generator
from edgegraph.structure import (
    Vertex,
    Link,
    DirectedEdge,
    UnDirectedEdge,
)

#: Unknown edge classes treated as non-neighbors.
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
LNK_UNKNOWN_NONNEIGHBOR = 0

#: Unknown edge classes treated as neighbors.
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
LNK_UNKNOWN_NEIGHBOR = 1

#: Unknown edge classes raise an exception.
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
LNK_UNKNOWN_ERROR = 2

#: Follow links forward
#:
#: This option specifies that links between vertices should be followed in
#: their direction (that is, normally).
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
DIR_SENS_FORWARD = 0

#: Follow links regardless of directionality
#:
#: This option specifies that links between vertices should be followed no
#: matter what direction they point in (i.e., forwards or backwards).
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
DIR_SENS_ANY = 1

#: Follow links backwards
#:
#: This option specifies that links between vertices should be followed only
#: against their directionality (backwards).
#:
#: .. seealso::
#:
#:    :py:func:`neighbors`
DIR_SENS_BACKWARD = 2


def ineighbors(
    vert: Vertex,
    direction_sensitive: int = DIR_SENS_FORWARD,
    unknown_handling: int = LNK_UNKNOWN_ERROR,
    filterfunc: Callable | None = None,
) -> Generator[Vertex, None, None]:
    """
    Identify the neighbors of a given vertex (generator).

    This function checks the edges associated with the given vertex, identifies
    the vertices on the other end of those edges, and returns them.  It
    respects edge directionality if/when necessary, and can handle arbitrary
    edge types given they are subclasses of either
    :py:class:`~edgegraph.structure.directededge.DirectedEdge` or
    :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.

    For example, with the given graph:

    .. uml::

       object v1
       object v2
       object v3
       object v4

       v1 --> v2
       v1 --> v3
       v2 --> v3
       v3 --> v4
       v4 --> v1

    the function would operate as:

    >>> list(ineighbors(v1))
    [v2, v3]
    >>> list(ineighbors(v1, direction_sensitive=DIR_SENS_FORWARD))
    [v2, v3, v4]
    >>> list(ineighbors(v4))
    [v1]
    >>> list(ineighbors(v4, direction_sensitive=DIR_SENS_ANY))
    [v1, v3]

    If supplied, the ``filterfunc`` argument should be to a callable object
    (function or otherwise) that will return either :py:obj:`True` or
    :py:obj:`False`.  This function is used to determine if a given vertex
    should be included in the returned neighbors.  It must have the following
    signature:

    .. py:function:: filterfunc(e, v2)
       :noindex:

       Determines if a given vertex (``v2``) should be included in the
       neighbors of ``v``.  Because ``v2`` may be reachable from ``v1`` via
       multiple edges, the edge currently being considered is given as well.

       :param e: The edge connecting ``v1`` to ``v2``.
       :param v2: The vertex under consideration.
       :return: Whether or not ``v2`` should be considered a neighbor of ``v``,
          when reached via ``e``.

    For example, one may wish to only consider vertices if a given attribute
    meets some criteria:

    >>> list(ineighbors(v1))
    [v2, v3]
    >>> list(ineighbors(v1, filterfunc=lambda e, v2: v2.i >= 3))
    [v3]

    .. note::

       The ``filterfunc`` parameter operates **in addition to** the
       ``direction_sensitive`` parameter!

    .. seealso::

       If you find yourself calling this function a lot on vertices that
       haven't changed nieghbors, you may wish to read about
       :ref:`dev/performance/vert-nb-cache`.  This technique allows this
       function to work in tandem with the Vertex class to cache neighbor
       lookups in a safe manner, drastically improving performance in some
       scenarios.

    :param vert: The vertex to identify neighbors of.
    :param direction_sensitive: How to handle directional edges as they are
       encountered.  :py:const:`DIR_SENS_FORWARD` will indicates "normal"
       usages, where edges will only be followed outwards from the given
       vertex.  :py:const:`DIR_SENS_ANY` will follow *any* edge, regardless of
       whether it points to or from this vertex.  :py:const:`DIR_SENS_BACKWARD`
       will follow only edges inbound to this vertex.
    :param unknown_handling: What to do with edges whose class is not
       recognized (not a subclass / instance of either
       :py:class:`~edgegraph.structure.directededge.DirectedEdge` or
       :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`).
       Options are :py:const:`LNK_UNKNOWN_NONNEIGHBOR` to treat unknown edges
       as non-neighbors, :py:const:`LNK_UNKNOWN_NEIGHBOR` to treat unknown
       edges *as* neighbors, or :py:const:`LNK_UNKNOWN_ERROR` to raise a
       :py:exc:`NotImplementedError` if such an edge is encountered.
    :param filterfunc: Callable object to determine whether the given edge /
       vertex should be included in the neighbors output.
    :raises NotImplementedError: if kwarg ``unknown_handling`` is set to
       :py:const:`LNK_UNKNOWN_ERROR` and an unknown edge class is enountered.
    :return: A generator object which yields
       :py:class:`~edgegraph.structure.vertex.Vertex` objects representing
       neighbors of the specified vertex.
    """

    # pylint complains about this operation, with fairly good reason -- we're
    # accessing a private member of a client class.  however, since this is
    # still edgegraph-internal code, this is ok; it would be a problem were the
    # consumer of edgegraph doing this, though.
    # pylint: disable-next=protected-access
    cached = vert._qa_neighbors_get(
        direction_sensitive, unknown_handling, filterfunc
    )
    # pylint: disable-next=protected-access
    if cached is not Vertex._QA_NB_INVALID:
        yield from cached
        return

    cache = []

    for link in vert.links:

        v2 = link.other(vert)

        if direction_sensitive == DIR_SENS_FORWARD:
            # undirected edges don't matter
            if issubclass(type(link), UnDirectedEdge):

                # we'll use boolean short-circuiting to prevent an unnecessary
                # call into a default filterfunc if one is not provided.  such
                # a default would always return True, but be an unnecessary
                # call context switch.
                # so, we'll first check if filterfunc is None -- if so, good
                # enough, we can add this to the neighbors.  otherwise, it was
                # in fact specified, and we should check its decision.
                # this goes for all three places filterfunc() is used in this
                # neighbors function
                if filterfunc is None or filterfunc(link, v2):
                    if Vertex.NEIGHBOR_CACHING:
                        cache.append(v2)
                    yield v2
                else:

                    # this is not detectable by coverage.py, due to a ~~bug~~
                    # side effect of the python peephole optimizer.  continue
                    # statements inside else: blocks are often skipped /
                    # replaced with a jump opcode.  see
                    # https://github.com/nedbat/coveragepy/issues/198#issuecomment-399705984
                    # for more info.  for proof that this IS run, uncomment:
                    # raise Exception("look, ma!  this happened!")
                    # and re-run unit tests.  You'll get that exception.
                    continue  # pragma: no cover

            # for directed edges, only add the neighbor if vert is the origin
            elif issubclass(type(link), DirectedEdge) and (link.v1 is vert):

                # see above notes on short-circuiting filterfunc() if it's not
                # provided
                if filterfunc is None or filterfunc(link, v2):
                    if Vertex.NEIGHBOR_CACHING:
                        cache.append(v2)
                    yield v2
                else:
                    # see comment on the above else: continue block for
                    # explanation of this no-cover statement.
                    continue  # pragma: no cover

            # we're looking at v2 -- the destination
            elif issubclass(type(link), DirectedEdge) and (link.v2 is vert):
                pass

            else:
                if unknown_handling == LNK_UNKNOWN_NONNEIGHBOR:
                    continue

                if unknown_handling == LNK_UNKNOWN_NEIGHBOR:
                    yld = link.other(vert)

                    if Vertex.NEIGHBOR_CACHING:
                        cache.append(yld)
                    yield yld
                else:
                    raise NotImplementedError(
                        f"Unknown link class {type(link)}"
                    )

        elif direction_sensitive == DIR_SENS_BACKWARD:

            if issubclass(type(link), UnDirectedEdge):

                if filterfunc is None or filterfunc(link, v2):
                    if Vertex.NEIGHBOR_CACHING:
                        cache.append(v2)
                    yield v2
                else:
                    # see comment on the above else: continue block for
                    # explanation of this no-cover statement.
                    continue  # pragma: no cover

            # for directed edges, only add the neighbor if vert is the origin
            elif issubclass(type(link), DirectedEdge) and (link.v2 is vert):

                # see above notes on short-circuiting filterfunc() if it's not
                # provided
                if filterfunc is None or filterfunc(link, v2):
                    if Vertex.NEIGHBOR_CACHING:
                        cache.append(v2)
                    yield v2
                else:
                    # see comment on the above else: continue block for
                    # explanation of this no-cover statement.
                    continue  # pragma: no cover

            # we're looking at v2 -- the destination
            elif issubclass(type(link), DirectedEdge) and (link.v1 is vert):
                pass

            else:
                if unknown_handling == LNK_UNKNOWN_NONNEIGHBOR:
                    continue

                if unknown_handling == LNK_UNKNOWN_NEIGHBOR:
                    yld = link.other(vert)

                    if Vertex.NEIGHBOR_CACHING:
                        cache.append(yld)
                    yield yld
                else:
                    raise NotImplementedError(
                        f"Unknown link class {type(link)}"
                    )

        elif direction_sensitive == DIR_SENS_ANY:
            # see above notes on short-circuiting filterfunc() if it's not
            # provided
            if filterfunc is None or filterfunc(link, v2):
                if Vertex.NEIGHBOR_CACHING:
                    cache.append(v2)
                yield v2

        else:
            raise ValueError(
                f"Unknown option for direction_sensitive = {direction_sensitive}"
            )

    vert._qa_neighbors_insert(
        cache, direction_sensitive, unknown_handling, filterfunc
    )


def neighbors(
    vert: Vertex,
    direction_sensitive: int = DIR_SENS_FORWARD,
    unknown_handling: int = LNK_UNKNOWN_ERROR,
    filterfunc: Callable | None = None,
) -> list[Vertex]:
    """
    Identify the neighbors of a given vertex (**non**-generator).

    This function checks the edges associated with the given vertex, identifies
    the vertices on the other end of those edges, and returns them.  It
    respects edge directionality if/when necessary, and can handle arbitrary
    edge types given they are subclasses of either
    :py:class:`~edgegraph.structure.directededge.DirectedEdge` or
    :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.

    .. seealso::

       Please refer to the documentation of :py:func:`ineighbors`!  This
       function simply wraps that one, only forcing full expansion to a list
       before returning.  All parameters are exactly the same and passed
       through without alteration.

    :return: A list of  :py:class:`~edgegraph.structure.vertex.Vertex` objects
       representing neighbors of the specified vertex.
    """
    return list(
        ineighbors(vert, direction_sensitive, unknown_handling, filterfunc)
    )


def find_links(
    v1: Vertex,
    v2: Vertex,
    direction_sensitive: bool = True,
    unknown_handling: int = LNK_UNKNOWN_ERROR,
    filterfunc: Callable | None = None,
) -> set[Link]:
    """
    Find the link(s) that connect v1 to v2.

    This function returns links that connect v1 and v2.  If multiple
    links/edges connect the given vertices, they are all returned in a list.
    It respects edge directionality if/when necessary, and can handle arbitrary
    edge types given they are subclasses of either
    :py:class:`~edgegraph.structure.directededge.DirectedEdge` or
    :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.

    For example, with the given graph:

    .. uml::

       object v1
       object v2
       object v3
       object v4

       v1 --> v2 : e1
       v1 --> v3 : e2
       v2 --> v3 : e3
       v3 --> v4 : e4
       v4 --> v1 : e5
       v1 --> v4 : e6

    the function would operate as:

    >>> find_links(v1, v2)
    {e1}
    >>> find_links(v1, v4)
    {e6}
    >>> find_links(v1, v4, direction_sensitive=False)
    {e6, e5}

    If supplied, the ``filterfunc`` argument should be a callable object
    (function or otherwise) that will return either :py:obj:`True` or
    :py:obj:`False`.  This function is used to determine if a given edge should
    be included in the returned set.  It must have the following signature:

    .. py:function:: filterfunc(e)
       :noindex:

       Determines if a given edge (``e``) should be included in the returned
       set of edges between ``v1`` and ``v2``.

       :param e: The edge under consideration.
       :return: Whether or not ``e`` should be returned as part of the set of
          edges connecting ``v1`` and ``v2``.

    :param v1: First vertex to find links from.  In a directed edge, this is
       consiered the "from" vertex.
    :param v2: Second vertex to find links from.  In a directed edge, this is
       consiered the "to" vertex.
    :param direction_sensitive: Whether or not to respect edge directionality.
       If True (default), edges direcetd from v2 to v1 are ignored.  If False,
       such edges are collected and returned.
    :param unknown_handling: How to deal with classes that are subclasses of
       neither :py:class:`~edgegraph.structure.directededge.DirectedEdge` nor
       :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`.

       * :py:const:`LNK_UNKNOWN_ERROR` (default): Raise a
         :py:exc:`NotImplementedError` when such an edge is encountered.
       * :py:const:`LNK_UNKNOWN_NEIGHBOR`: Skip unknown edges.
       * :py:const:`LNK_UNKNOWN_NONNEIGHBOR`: Collect and return unknown edges.

    :param filterfunc: Callable object that returns whether or not a given link
       should be included in the output.
    """

    links = set()
    for link in v1.links:

        # no matter what the other options are, don't care!
        if link.other(v1) is not v2:
            continue

        if direction_sensitive:

            if issubclass(type(link), UnDirectedEdge):

                # short-circuit operation, just like in neighbors()
                if filterfunc is None or filterfunc(link):
                    links.add(link)
                else:
                    # see comment on the else: continue block in neighbors()
                    # for explanation of this no-cover statement.
                    continue  # pragma: no cover

            elif issubclass(type(link), DirectedEdge):

                if link.v1 is not v1:
                    # this is a link from v2 to v1, not the way we want
                    continue

                if filterfunc is None or filterfunc(link):
                    links.add(link)
                else:
                    # see comment on the else: continue block in neighbors()
                    # for explanation of this no-cover statement.
                    continue  # pragma: no cover

            else:
                if unknown_handling == LNK_UNKNOWN_NONNEIGHBOR:
                    continue
                if unknown_handling == LNK_UNKNOWN_NEIGHBOR:
                    links.add(link)
                else:
                    raise NotImplementedError(
                        f"Unknown link class {type(link)}"
                    )

        else:
            # see above notes on short-circuiting filterfunc() if it's not
            # provided
            if filterfunc is None or filterfunc(link):
                links.add(link)

    return links
