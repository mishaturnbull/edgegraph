.. _usage/algos/pathfinding:

Pathfinding
===========

Pathfinding algorithms are those which answer the question "how do I get from
this vertex to that vertex."  Many allow consideration of arbitrary edge
weights, or costs (where two vertices that are one edge apart may have a "cost"
of more than one), and there are, as usual, certain "gotchas" to avoid.  This
section attempts to summarize the options available in Edgegraph.

.. seealso::

   Edgegraph's primary pathfinding API is the
   :py:func:`edgegraph.pathfinding.shortestpath` module.

Dijkstra's Algorithm
--------------------

Named for its creator (Edsgar W. Dijkstra), Dijkstra's algorithm provides the
shortest path from any given node to *all other nodes*.  It works for edge
weights of any positive value, and graphs which contain loops.

.. warning::

   Dijkstra's algorithm does not work with graphs containing negative or zero
   edge weights.  Its behavior is dependent on the graph; it will likely
   **silently** fail to find the correct shortest path.

   Only use it on data you are certain does not contain zero or negative weight
   edges!

To select this solver in Edgegraph, where implemented, you will typically use
``method="dijkstra"`` parameter.

.. seealso::

   More information on Dijkstra's algorithm is widely available on the
   internet.  some sources are given:

   * On NIST: https://xlinux.nist.gov/dads/HTML/dijkstraalgo.html
   * On Wikipedia: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

At this time, no other implementations are available.  Check back soon!

