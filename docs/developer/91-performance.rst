.. _dev/performance:

Performance and optimizing
==========================

The primary downside to object-oriented graphs is that performance is *awful*
compared to traditional data structure approaches.  Edgegraph does attempt to
bake in some optimizations using efficiently-implemented algorithms and general
operations, but the fact that OOP code simply uses more memory and processor
time is, in the end, unavoidable.  Therefore, some effort has been given to
allow the user of Edgegraph to tune some optimization knobs for their usage
patterns.  This is expected to continue as the library becomes more capable and
more performance pain-points are identified.

.. _dev/performance/vert-nb-cache:

Vertex neighbor caching
-----------------------

**Problem**: The :py:func:`edgegraph.traversal.helpers.neighbors` function is
slow, and when called many times, can cause tremendous performance hits.  This
function is called by many (at time of writing, *all*) traversal functions, so
traversing the same graph many times is unnecessarily slow.

This performance hit is felt most commonly when implementing a
create-then-traverse usage pattern, wherein a graph is created first, and then
after creation is done, the graph is traversed many times.

**Solution**: The :py:class:`~edgegraph.structure.vertex.Vertex` object can
work in tandem with the :py:func:`~edgegraph.traversal.helpers.neighbors`
function to cache results for the neighbors function, similar in effect to
:py:func:`functools.cache` but in a safe manner.

**The bottom line to use this is to set**
:py:attr:`edgegraph.structure.vertex.Vertex.NEIGHBOR_CACHING` to ``True`` **any
time before graph traversals begin.**

Unfortunately, using a standard :py:func:`functools.lru_cache` or
:py:func:`functools.cache` on the
:py:func:`~edgegraph.traversal.helpers.neighbors` is unsafe, as the vertex may
change neighbors, and the cache function would erroneously not know this and
return stale data.  Consider the following:

.. code-block:: python
   :linenos:

   #!python3

   from edgegraph.structure import Vertex
   from edgegraph.builder import explicit
   from edgegraph.traversal import helpers

   v1 = Vertex()
   v2 = Vertex()

   helpers.neighbors(v1)
   # --> []

   explicit.link_directed(v1, v2)

   helpers.neighbors(v1)
   # --> [v2]

On the second call to ``neighbors``, the same arguments were provided; so
out-of-the-box caching functions would erroneously return ``[]``.

Instead, with vertex neighbor caching, the cache is stored in the ``Vertex``
object.  The ``neighbors`` function checks for cache availability based on the
provided arguments; if available, it returns the cached data immediately.

To solve the stale data problem, the cache is invalidated any time the relevant
``Vertex`` instance is modified; linked or unlinked to/from any other vertex.
Then, the next time ``neighbors`` is called, it finds no cached data; so it
reevaluates the most up-to-date information available and inserts it into the
cache for future reuse.

