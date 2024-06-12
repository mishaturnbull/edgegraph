Concept
=======

EdgeGraph's concept of operations is vertex-edge graphs implemented with
object-oriented programming (OOP).  It represents vertices (and edges) as
first-class objects, which brings several advantages over more common,
quick-to-implement approaches such as dictionaries or matricies:

- Vertices can have arbitrary attributes, assigned on-the-fly, without any
  changes in graph handling code
- Edges can *also* have arbitrary attributes, again assigned on-the-fly,
  without any changes in graph handling code
- Every vertex carries with it full information of edges that interact with it
  (outbound *and* inbound)
- Every edge carries with it full information of the vertices it connects
- Vertices may be members of multiple graphs (EdgeGraph calls them
  :py:class:`~edgegraph.structure.universe.Universe`\ s)
- Vertices (and edges) can be inherited from with ease in a program that uses
  EdgeGraph, automatically making program data into a fully-fledged graph with
  no extra effort

The last bullet is really the true selling point of EdgeGraph.  All of the
traversal, graph-building, rendering, etc. functionality works with subclasses
of :py:class:`~edgegraph.structure.vertex.Vertex` -- all you need to do is
subclass that, and now you have a graph backend.

However, no lunch is free, so keep these points in mind.  I haven't benchmarked
EdgeGraph against the more famed graph libraries for Python (NetworkX and co),
so I don't have hard numbers to give you yet.  I do expect, though:

- OOP approaches may consume more memory to represent the same graph structure
  as non-OOP methods
- OOP approaches may consume more processing time to operate on than non-OOP
  methods
- EdgeGraph is not application-specific.  If you have existing knowledge of the
  data structure your application trends towards, EdgeGraph has no idea and
  won't be able to take advantage of it.  However, it does provide the building
  blocks to create your own traversal functions quickly.

For example, consider an application that represents many interlinked pieces of
data:

.. code-block:: python
   :linenos:

   #!python3

   from edgegraph.structure import Vertex
   from edgegraph.builder import explicit
   from edgegraph.traversal import breadthfirst

   class MyData (Vertex):
       '''
       Represents a piece of data.
       '''

       def __init__(self, value):
           '''
           Set up this piece of data.
           '''
           super().__init__(attributes={'value': value})

   def load_data():
       d1 = MyData(1)
       d2 = MyData(5)
       d3 = MyData(100)

       explicit.link_directed(d1, d2)
       explicit.link_directed(d1, d3)
       explicit.link_directed(d3, d2)

       return Universe(vertices=[d1, d2, d3]), d1

   def main():
       uni, d1 = load_data()

       print(breadfirst.bft(uni, d1))

   if __name__ == '__main__':
       main()


There it is -- a complete example of loading some (admittedly, small) data and
doing a bread-first traversal.  Note that

#. We defined our own data type
#. We used it as a vertex in a graph
#. We used an out-of-the-box traversal on a graph of our own data type
#. *No* traversal code was implemented here

and yet, we have all the benefits of a graph backend.

