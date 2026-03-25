.. _usage/algos/sorting:

Sorting & Ordering
==================

Sorting algorithms put a collection of items in a specific order.  Typically,
this ordering is defined by some "key" attribute of the items, such as a list
of numbers (which are their own keys, traditionally sorted numerically), but
there are other orderings as well when sorting a graph.  This section attempts
to summarize the sorting and ordering options available in Edgegraph.

.. _usage/algos/sorting/toposort:

Topological Sorts
-----------------

Topological sorting algorithms are those which order the vertices of a graph
based on the graph structure itself.  Toposorts are most commonly seen in
dependency ordering, where a vertex represents a particular requirement or
state which must have dependencies (other requirements or states) satisfied
before it can be met.

.. seealso::

   Edgegraph's primary topological sorting API is the
   :py:func:`edgegraph.sorting.toposort.topological_ordering` function.

Kahn's Algorithm
^^^^^^^^^^^^^^^^

A. B. Kahn described a process which topologically orders large graphs in 1962 [Kahn62]_.
Kahn's algorithm is similar to a modified breadth-first search (BFS), and can
be used to order graphs in a non-recursive fashion.  
 
To select this solver in Edgegraph, you will typically use the
``method="kahn"`` parameter.

.. seealso::

   More information on Kahn's algorithm is widely available on the internet.
   Some sources are given:

   * On Wikipedia: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
   * A. B. Kahn's original paper: https://dl.acm.org/doi/abs/10.1145/368996.369025

Modified Depth-First Search
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another approach to topological sorting consists of a modified depth-first
search (DFS).  Such algorithms can be found in [CLRS09]_ and may provide a
faster runtime at the expense of recursive function calls (limiting potential
usefulness on large graphs).

To select this solver in Edgegraph, use the ``method="dfs"`` option in the
topological sorting API.

