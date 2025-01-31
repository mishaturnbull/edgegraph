#!python3
# -*- coding: utf-8 -*-

"""
Non-recursive pickler / "diller" implementation to be used for serializing
edgegraph objects.

This module contains a non-recursive implementation of a pickler that is
suggested for use when serializing edgegraph objects.  This overcomes a
limitation of the default builtin pickler, which struggles with highly
recursive data structures -- edgegraph's internal linkage structure is indeed
very recursive, and graphs even a fraction of :py:func:`the recursion limit
<sys.getrecursionlimit>` will often cause ``RecursionError``\\ s when being
pickled.  Even :py:mod:`dill` uses a recursive implementation, so this is
necessary for use with ``dill`` as well.

.. danger::

   Like Python's default pickler, this module is **not secure**.  Only pickle /
   unpickle data you trust.

   See the warning at the top of :py:mod:`pickle` documentation for more
   information!

.. seealso::

   The first mention of the non-recursive pickler used here was by Daniel
   Darabos (cyhawk) on https://bugs.python.org/issue2480 .  I stole it
   shamelessly, only making minor changes for Python 3.x, dill compatibility,
   and readability / formatting.  Thank you, Daniel!

Usage of this pickler should be similar to the built-in one::

   >>> from edgegraph.builder import randgraph
   >>> from edgegraph.output import nrpickler
   >>> import pickle
   >>> graph = randgraph.randgraph(count=100)
   >>> serial = nrpickler.dumps(graph)
   >>> serial
   b'\\x80\\x04\\x8c\\x1cedgegraph.structure.universe\\x94\\x8c\\x08...'
   >>> unpacked = pickle.loads(serial)  # use the regular pickle module to unpack
   >>> unpacked is graph
   False
   >>> len(unpacked.vertices) == len(graph.vertices)
   True

At this point, the ``unpacked`` object is a Universe identical in every way to
``graph``, except it is a different instance.  All of its vertices, links, and
any attributes of have all been unpacked.
"""

import io
import pickle
import dill


class _LazySave(object):
    """
    Out of band marker for lazy saves among lazy writes.
    """

    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return f"<_LazySave {self.obj}>"  # pragma: no cover


class _LazyMemo(object):
    """
    Out of band marker for lazy memos among lazy writes.
    """

    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return f"<_LazyMemo {self.obj}>"  # pragma: no cover


class NonrecursivePickler(dill.Pickler):
    """
    Non-recursive pickler class.

    This class subclasses :py:cls`dill.Pickler`, and overrides its ``dumps``
    method with a non-recursive implementation, making it safe to use with
    arbitrary edgegraph objects regardless of the size of graphs they may be a
    part of.

    This class it not *really* intended for direct usage; see also
    :py:func:`dumps` for a better interface.  For unpickling, use the regular
    built-in :py:mod:`pickle` module (nonrecursive specialties are only needed
    on the pickling side, not the unpickling side).
    """

    def __init__(self, file, **kwargs):
        dill.Pickler.__init__(self, file, **kwargs)
        self.lazywrites = []
        self.realwrite = file.write

        # TODO: this creates a reference loop and prevents gc
        self.write = self.lazywrite

    def lazywrite(self, *args):
        """
        Lazily write an object to the memo.
        """
        if self.lazywrites:
            self.lazywrites.append(args)
        else:
            self.realwrite(*args)

    def save(self, obj):
        """
        Lazy-save the given object (that is, add it to the queue for writing
        later).
        """
        self.lazywrites.append(_LazySave(obj))

    #: Alias to the true :py:meth:`dill.Pickler.save`.
    realsave = dill.Pickler.save

    def lazymemoize(self, obj):
        """Store an object in the memo."""
        if self.lazywrites:
            self.lazywrites.append(_LazyMemo(obj))
        else:
            self.realmemoize(obj)

    memoize = lazymemoize
    realmemoize = dill.Pickler.memoize

    def dump(self, obj):
        """Write a pickled representation of obj to the open file."""
        if self.proto >= 2:
            self.write(pickle.PROTO + chr(self.proto).encode("ascii"))
        self.realsave(obj)
        while self.lazywrites:
            lws = self.lazywrites
            self.lazywrites = []
            while lws:
                lw = lws.pop(0)
                if type(lw) is _LazySave:
                    self.realsave(lw.obj)
                    if self.lazywrites:
                        self.lazywrites.extend(lws)
                        break
                elif type(lw) is _LazyMemo:
                    self.realmemoize(lw.obj)
                else:
                    self.realwrite(*lw)
        self.realwrite(pickle.STOP)


def dumps(
    obj,
    protocol=pickle.DEFAULT_PROTOCOL,
    byref=None,
    fmode=None,
    recurse=None,
    **kwargs,
):
    """
    Module-level interface to the non-recursive pickler ``dumps``.

    This is intended to mirror :py:func:`pickle.dumps` in functionality, but is
    safe to use with edgegraph objects (i.e. will not cause recursion
    problems).
    """
    f = io.BytesIO()
    p = NonrecursivePickler(
        f,
        protocol=protocol,
        byref=byref,
        fmode=fmode,
        recurse=recurse,
        **kwargs,
    )
    p.dump(obj)
    return f.getvalue()
