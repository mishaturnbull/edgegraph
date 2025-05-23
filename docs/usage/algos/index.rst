.. _usage/algos:

Algorithms
==========

One of EdgeGraph's most fundamental goals is to provide implementations of all
the "interesting" algorithms that you might want to use on your data.  This
section goes into more detail about the algorithms available, their
limitations, and may help you select exactly which you want to use for a given
problem.

It is intentionally separate from the API documentation, as this page discusses
more theoretical matters, such as limitations of Dijkstra's algorithm vs. a
uniform cost search; while exact details on how to call the implementations of
these algorithms is in the API documentation.  (though, cross-references
between the two are frequent!)

Note, though, that this section is not intended to replace your data structures
and algorithms textbook.  My goal here is to capture the gotchas and
performance tradeoffs of Edgegraph and the operations it provides, not to teach
CSCI 242.

.. toctree::
   :maxdepth: 2
   :caption: Type
   :glob:

   *

