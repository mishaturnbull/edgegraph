.. _dev/threadsafety:

Thread Safety
=============

Edgegraph's internal structure is thread-safe; meaning it can be used (read and
written) from multiple threads within the same process simulatenously without
the following categories of issues:

#. Data race conditions, in which thread A may read partial data from object
   state that thread B is currently writing to; and
#. Deadlock, in which two threads may wait infinitely for the same resource,
   guarding it from each other

This statement applies to the internal graph structure of the
:py:class:`~edgegraph.structure.vertex.Vertex` and
:py:class:`~edgegraph.structure.link.Link` objects, and therefore is inherited
by all subclasses of them which properly call their superclass methods for
graph operations (establishing and removing links between vertices).

**However:**

This thread safety is implemented with a series of locks that guard critical
object state relating to the "joints" of vertices and links.  It does **NOT**
extend automatically to all user-created instance variables in a subclass of
any of Edgegraph's classes.

**You as the user of edgegraph are responsible for the thread-safety of your
own instance variables!**

The developer of edgegraph cannot know what you intend to do with the module,
and therefore cannot adequately place guardrails for any potential use.  It is
impossible for me to know how you will use the subclasses of Vertex.

For example, consider the following:

.. code-block:: python
   :linenos:

   from edgegraph.structure import Vertex
   from edgegraph.builder import randgraph

   class MyData (Vertex):
       '''Represents a piece of data.'''

       def __init__(self, data):
           '''Set up this piece of data.'''
           super().__init__(self)  # <-- object is thread-safe; no worries here

           self.data = data  # <-- this is NOT thread safe!  guard it!

.. note::

   If you intend to guard custom instance variables within Edgegraph vertices,
   you may often need to use reentrant locks (RLocks).

   In addition, if you intend to pickle objects containing RLocks, be aware
   that it doesn't seem to work in conjunction with edgegraph's
   :py:mod:`non-recursive pickler <edgegraph.output.nrpickler>`.  Internally,
   edgegraph faces this very problem - and uses ``threading._PyRLock`` to work
   around it.  It's not a good practice, but seems to be necessary.  See
   https://github.com/mishaturnbull/edgegraph/issues/118.

Async and Multiprocessing
-------------------------

Edgegraph does not take measures to guard resources while working with Python's
async routines or multiprocessing capabilities.  It is up to the user to ensure
their usage of async / multiprocessing is done in a safe manner.

For the async side, Python's implementation of async leads to a pattern where
context switches only happen at points explicitly defined by the user.
Therefore, Edgegraph recommends not switching contexts while a graph update
operation is happening.

"Multiprocessing safety" is not considered by Edgegraph, as shared memory
between operating system *processes* requires much more manual setup and
synchronization by the user compared to threading models.  Further, Python's
implementation of multiprocessing leads to patterns of data serialization for
exchange between processes, meaning the same object references are not shared
directly.  Ergo, the typical threading problems discussed above are not
relevant.

.. seealso::

   If you do wish to exchange Edgegraph structures between *processes*,
   consider the custom pickler: :py:mod:`edgegraph.output.nrpickler`.

