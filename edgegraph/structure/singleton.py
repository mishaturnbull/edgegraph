#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provides metaclasses to assist creating singletons.

This module contains helper metaclasses to ease creating custom subclasses of
:py:class:`~edgegraph.structure.vertex.Vertex`.  It provides two helpers, one
for creating a so-called "true singleton", and one for creating so-called
"semi-singletons":

* Global singleton: there can be *only one* instance of global singletons.  See
  :py:class:`TrueSingleton`.
* Semi-singletons: there can be multiple instances of semi-singleton classes,
  but they are designated with some unique primary key.  Only one instance
  with a given primary key can exist.  See
  :py:func:`semi_singleton_metaclass`.

**Consider carefully how you intend to use these tools!**

Some disclaiming about singleton usage (anti-)patterns is worthwile.  Many
people feel that singletons in general violate good OOP practices, and often
with good reason.  The purpose of OOP is to provide instances of objects that
behave independently of each other -- singletons violate this.

Nonetheless, I (and many others) argue that in moderation, singletons can be
used to good effect.  There are some use-cases that see frequent singletons
(loggers and global configuration containers, for example) and improve code
quality with it.  How exactly you intend to apply this logic to ... graphs ...
is up to you -- but edgegraph will happily supply the foot-gun.

In order to sustain the law of least astonishment, these helpers take the form
of metaclasses.  There are several ways to implement singletons in Python, but
after some surveying (Googling) I decided that metaclasses approach gave:

* Cleanest implementation
* Most straightforward to use ("pythonic")
* Best expression of intent
"""

from __future__ import annotations

import json

class TrueSingleton(type):
    """
    Metaclass for true singletons.

    .. seealso::

       The design of this metaclass is taken directly from this *excellent*
       StackOverflow answer by user @agf.  This answer is also perhaps the
       clearest explanation of metaclasses I've ever seen in the wild.
       Thanks!!

       https://stackoverflow.com/a/6798042

    .. danger::
    
       If you find yourself using this with
       :py:class:`~edgegraph.structure.vertex.Vertex`, something will probably
       go wrong.  Though it will, technically speaking, *work*, the effects of
       true-singleton vertices have little real-world purpose, and their use
       may have side effects far beyond what you predict.  If you think "yes, I
       really do need a singleton vertex," it is probably a sign that something
       else has gone horribly wrong and you should refactor whatever you're
       doing.

       You may wish to read about :py:func:`semi_singleton_metaclass` for an
       alternative, less-probably-a-bad-idea approach.

    Using this metaclass allows creation of a truly global singleton object.
    Only one of them can ever be created, observing the following rules:

    #. Instances of such classes can only be created once
    #. instances of such classes will only have their ``__init__`` called once,
       no matter what arguments (same or different) may be passed in on a
       future attempt
    #. All attempts to create a new instance of the given class will return the
       One True Instance

    For example:

    >>> from edgegraph.structure import singleton
    >>> class MySingleton(metaclass=singleton.TrueSingleton):
    ...     def __init__(self, foo, bar=False):
    ...         self.foo = foo
    ...         self.bar = bar
    ... 
    >>> s1 = MySingleton(8, True)
    >>> s1
    <__main__.MySingleton object at 0xdeadbeef>
    >>> s2 = MySingleton(8, True)
    >>> s2
    <__main__.MySingleton object at 0xdeadbeef>
    >>> s1 is s2
    True
    >>> s3 = MySingleton(512, 2**32)
    >>> s3
    <__main__.MySingleton object at 0xdeadbeef>
    >>> s2 is s3
    True
    >>> s3.foo = 9001
    >>> s1.foo
    9001
    >>> s2.foo = 18002
    >>> s3.foo
    18002

    We can see here that, no matter whether you give the class the same or
    different arguments, the first-ever instance is always what you get.  Note
    the use of the ``is`` operator here -- this checks that the two objects
    given are the same *reference*, not just of the same value.

    Furthermore, changing attributes of the one instance affects all other
    copies of the singleton floating around, because they're all shallow
    references to the original.
    """

    __singleton_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__singleton_instances:
            cls.__singleton_instances[cls] = \
                    super(TrueSingleton, cls).__call__(*args, **kwargs)
        return cls.__singleton_instances[cls]

def clear_true_singleton(cls=None):
    """
    Clears TrueSingleton cache for either a specified type, or all
    TrueSingleton types.

    .. todo::

       document this!
    """
    if cls:
        if cls in TrueSingleton._TrueSingleton__singleton_instances:
            del TrueSingleton._TrueSingleton__singleton_instances[cls]

    else:
        TrueSingleton._TrueSingleton__singleton_instances = {}

# what this function actually does isn't complex, in *theory*.  however,
# metaclass hacking is some of the deeper black magic of Python -- so document
# the crap out of it.
def semi_singleton_metaclass(hashfunc: Callable=None) -> type:
    """
    Generate and return a metaclass for semi-singletons.

    .. seealso::

       The design of this metaclass is heavily inspired by this *excellent*
       StackOverflow answer by user @agf.  Thanks!!

       https://stackoverflow.com/a/6798042

       The default hash function also uses an approach for dictionary hashing
       from StackOverflow user Jack O'Connor.  Thanks!!

       https://stackoverflow.com/a/22003440

    .. danger::

       Though *potentially less bad* than true singletons, usage of this
       metaclass alongside a :py:class:`~edgegraph.structure.vertex.Vertex` can
       lead to surprising side-effects.  As a quick example, creating a vertex
       under one universe may actually return you a reference to a pre-existing
       vertex from elsewhere.  This will be completely silent, and probably
       *very* hard to debug.

       **Be careful!**

    This function creates metaclasses for so-called semi-singletons; classes
    that act as if they have an instantiation cache.  In other words, creating
    *duplicate* instances of these classes is not possible, but creating
    *different* instances is (as determined by their arguments).  This may be
    easiest to explain with an example:

    >>> from edgegraph.singleton import semi_singleton_metaclass
    >>> class SemiSingleton(metaclass=semi_singleton_metaclass()):
    ...     def __init__(self, foo, bar=False):
    ...         self.foo = foo
    ...         self.bar = bar
    ... 
    >>> s1 = SemiSingleton(1, False)
    >>> s1
    <__main__.SemiSingleton object at 0xdeadbeef>
    >>> s2 = SemiSingleton(1, False)  # same arguments -- we'll get same object
    >>> s2
    <__main__.SemiSingleton object at 0xdeadbeef>
    >>> s1 is s2
    True
    >>> s3 = SemiSingleton(37, True)  # different arguments -- different object
    >>> s3
    <__main__.SemiSingleton object at 0x01234567>
    >>> s2 is s3
    False

    Cuztomization of how arguments are understood to be "different" may be done
    via the ``hashfunc`` argument.  If provided, it must be a callable object:

    .. py:function:: hashfunc(args: tuple, kwargs: dict) -> Hashable:
       :noindex:

       This function is given the args and kwargs of a class instantiator (a
       call to ``__init__``) and expected to return a hashable type, most
       commonly an integer.  It is the determining factor in whether two
       attempts to instantiate an object should act as a singleton or actually
       create a new object.

       :param args: A tuple containing the positional arguments given.  Often
          seen as ``*args``, though not starred in this case (you get the
          actual tuple).
       :param kwargs: A dictionary containing keyword arguments given.  Often
          seen as ``**kwargs``, though not starred in this case (you get the
          actual dictionary).
       :return: Some hashable data time.  Most often, an :py:class:`int`.

    If not specified, the default hashfunc inspects all positional and keyword
    arguments, and hashes them all.  This causes a new object to be created if
    *any* argument is different.  So long as they have the same value, order of
    keyword arguments is not accounted for.

    .. note::

       Python :py:class:`dict` is not a hashable data type; therefore, special
       care must often be taken when hashing ``kwargs``.  The default hashfunc
       uses :py:func:`json.dumps` to accomplish this, transforming
       (recursively) the dictionary into a string, which *is* hashable.  This
       has some side effects, though:

       * All the keys of the dictionary must be strings (which is the case with
         ``kwargs``, but may *not* be the case if passing another dictionary
         into a keyword argument)
       * The JSON encoder may handle character escaping differently on
         different platforms and/or Python versions.  I believe this to be a
         nonissue for the semi-singleton application, but attempting to pickle
         and unpickle these objects may have undefined behavior.
       * Passing non-JSON-ify-able data types may cause issues (things other
         than strings, ints, bools, and lists/dictionaries of them)
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

def get_all_semi_singleton_instances(cls):
    """
    Get all instances belonging to a given semi-singleton type.
    """
    yield from type(cls)._SemiSingleton__semisingleton_instance_map.values()

def clear_semi_singleton(cls):
    """
    Clears a specified semi-singleton.
    """
    type(cls)._SemiSingleton__semisingleton_instance_map = {}

