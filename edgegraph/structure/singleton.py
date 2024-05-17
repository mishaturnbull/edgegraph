#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provides metaclasses to assist creating singletons.

This module contains helper metaclasses to ease creating custom subclasses of
:py:class:`~edgegraph.structure.vertex.Vertex`.  It provides two helpers, one
for creating a so-called "true singleton", and one for creating so-called
"semi-singletons":

* Global singleton: there can be *only one* instance of global singletons.
* Semi-singletons: there can be multiple instances of semi-singleton classes,
   but they are designated with some unique primary key.  Only one instance
   with a given primary key can exist.

.. todo::

   add code examples to this
"""

from __future__ import annotations

import json

class TrueSingleton(type):
    """
    Metaclass for true singletons.

    .. seealso::

       The design of this metaclass is taken directly from this *excellent*
       StackOverflow answer by user @agf.  Thanks!!

       https://stackoverflow.com/a/6798042
    """

    __singleton_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__singleton_instances:
            cls.__singleton_instances[cls] = \
                    super(TrueSingleton, cls).__call__(*args, **kwargs)
        return cls.__singleton_instances[cls]


def semi_singleton_metaclass(hashfunc=None):
    """
    Generate and return a metaclass for semi-singletons.

    .. seealso::

       The design of this metaclass is heavily inspiried by this *excellent*
       StackOverflow answer by user @agf@.  Thanks!!

       https://stackoverflow.com/a/6798042

       The default hash function also uses an approach for dictionary hashing
       from StackOverflow user Jack O'Connor.  Thanks!!

       https://stackoverflow.com/a/22003440
    """

    # by default, use a hash function to serialize all arguments
    if hashfunc is None:

        def hashfunc(args, kwargs):
            kwargs = json.dumps(kwargs, sort_keys=True)
            return hash((args, kwargs))

    class _SemiSingleton(type):

        __semisingleton_instance_map = {}

        def __call__(cls, *args, **kwargs):
            key = hashfunc(args, kwargs)
            if key not in cls.__semisingleton_instance_map:
                cls.__semisingleton_instance_map[key] = \
                        super(_SemiSingleton, cls).__call__(*args, **kwargs)
            return cls.__semisingleton_instance_map[key]

    return _SemiSingleton

