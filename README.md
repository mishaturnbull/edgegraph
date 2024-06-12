# EdgeGraph

EdgeGraph is an object-oriented approach to network graphs.  It provides
classes to inherit from in other applications / modules, and provides
out-of-the-box operations for these classes and any subclasses of.

The intent of EdgeGraph is to allow applications to model related data with a
method closer to reality, without having to implement a custom graph module.
It provides facilities to this end, such as the base classes to allow linking
and the functions to perform it.

The base classes are also usable directly, should you wish to test-drive this
idea or study abstract graphs.

See [the docs][1] for more.

## Prealpha

At this time, this project is extremely young.  Per [semantic versioning][0],
it is in version 0.  This means that the API may be changed at any time,
without warning.

Planned features include:

* [x] Single base class for all objects, with custom data support
* [x] Vertex-edge graphs
* [x] "Universe" class to contain graphs as a single unit
* [x] Class-based edges, can associate arbitrary data with edges
* [x] Automatic edge update propagation to necessary endpoints
* [x] Adjacency list / matrix build-a-graph
* [ ] Build-an-adjlist / build-an-adjmat from graphs
* [x] Breadth-first search and traversal
* [x] Depth-first search and traversal
* [ ] Topological sorting
* [ ] Strongly connected component detection
* [ ] Universe island detection
* [ ] Shortest path detection
* [x] Graph drawing generation via PlantUML
* [x] Graph export to PyVis, ready for interactive display
* [ ] Formal automata modelling (DFA, NFA, etc)
* [ ] Operation flow graph modelling (nodes as operations instead of states)
* [ ] "Functional graphs" -- attach executable code to nodes and run a graph as
      a program
* [ ] Object serialization, save-to- and load-from-file
* [x] Singleton and semi-singleton utilities

These features, as with the API, may be changed or dropped at any time without
warning.  I do have a day job, after all :)

Sphinx documentation and full Pytest-driven unit testing coverage is expected
to match the progress of the code.

[0]: https://semver.org
[1]: https://edgegraph.readthedocs.io/en/latest/index.html

