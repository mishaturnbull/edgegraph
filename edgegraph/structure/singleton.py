#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provides metaclasses to assist creating singletons.

This module contains helper metaclasses to ease creating custom subclasses of
:py:class:`~edgegraph.structure.vertex.Vertex`, or anything else you might want
to singleton-ize.  It provides two helpers, one for creating a so-called "true
singleton", and one for creating so-called "semi-singletons":

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
from collections.abc import Generator, Callable, Hashable

import json

# this is one of the rare occurrances of a module-wide pylint ignore... working
# with shared-state objects, the machinery of which is private, requires
# frequent access to that private machinery.  at time of writing, this silences
# 5 pylint warnings.
# W0212 -> protected-access ("Access to a protected member [...] of a client
# class"
# pylint: disable=W0212

# MyPy's type checker does not understand dynamically-computed metaclasses,
# therefore, some operations surrounding semi-singletons have local typechecker
# silencing.  This is **NOT** applied to the entire module; it is to be used
# **locally only** on the relevant lines.
#
# See the last section of this page for more information:
# https://mypy.readthedocs.io/en/stable/metaclasses.html


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

    _TrueSingleton__singleton_instances: dict[Hashable, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._TrueSingleton__singleton_instances:
            cls._TrueSingleton__singleton_instances[cls] = super(
                TrueSingleton, cls
            ).__call__(*args, **kwargs)
        return cls._TrueSingleton__singleton_instances[cls]


def clear_true_singleton(cls: type | None = None) -> None:
    """
    Clears TrueSingleton cache for either a specified type, or all
    TrueSingleton types.

    This operation is also sometimes referred to as "resetting" a singleton
    data type.  It removes the reference to the single object that would
    otherwise be returned.

    After calling this function, the next instantiation attempt on the given
    singleton type will result in an actual re-creation and instantiation of a
    new object.  For example:

    >>> from edgegraph.structure import singleton
    >>> class S(metaclass=singleton.TrueSingleton): pass
    >>> s1 = S()
    >>> s2 = S()
    >>> s1 is s2
    True
    >>> singleton.clear_true_singleton(S)
    >>> s3 = S()
    >>> s4 = S()
    >>> s2 is s3
    False
    >>> s3 is s4
    True

    Note that this can also be used to clear *all* TrueSingleton objects by
    leaving the ``cls`` parameter empty:

    >>> from edgegraph.structure import singleton
    >>> class S(metaclass=singleton.TrueSingleton): pass
    >>> class S(metaclass=singleton.TrueSingleton): pass
    >>> s1 = S()
    >>> s2 = S()
    >>> s1 is s2
    True
    >>> r1 = R()
    >>> r2 = R()
    >>> r1 is r2
    True
    >>> singleton.clear_true_singleton()  # no argument used here
    >>> s3 = S()
    >>> s2 is s3
    False
    >>> r3 = R()
    >>> r2 is r3
    False

    :param cls: The data type to clear singleton references from.  If not
       specified, clears all TrueSingleton types.
    """
    if cls:
        if cls in TrueSingleton._TrueSingleton__singleton_instances:
            del TrueSingleton._TrueSingleton__singleton_instances[cls]

    else:
        TrueSingleton._TrueSingleton__singleton_instances = {}


# what this function actually does isn't complex, in *theory*.  however,
# metaclass hacking is some of the deeper black magic of Python -- so document
# the crap out of it.
def semi_singleton_metaclass(hashfunc: Callable | None = None) -> type:
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

    Customization of how arguments are understood to be "different" may be done
    via the ``hashfunc`` argument.  If provided, it must be a callable object:

    .. py:function:: hashfunc(args: tuple, kwargs: dict) -> Hashable
       :noindex:

       This function is given the args and kwargs of a class instantiator (a
       call to ``__init__``) and expected to return a hashable type, most
       commonly an integer.  It is the determining factor in whether two
       attempts to instantiate an object should act as a singleton or actually
       create a new object.

       :param args: Positional arguments as would be given to the class's
          ``__init__`` constructor.
       :param kwargs: Keyword arguments as would be given to the class's
          ``__init__`` constructor.
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

    .. seealso::

       * :py:func:`get_all_semi_singleton_instances`, to retrieve instances of
         a semi-singleton type
       * :py:func:`clear_semi_singleton`, to reset a given semi-singleton

    :param hashfunc: Callable object to identify unique calls to this class by
       arguments provided.
    :return: A class suitable for use as a metaclass of another class.
    """

    # by default, use a hash function to serialize all arguments
    if hashfunc is None:

        def hashfunc(args: tuple, kwargs: dict) -> int:
            """
            Default argument hash function for semi-singleton objects.  Causes
            semi-singletons to return new objects if any argument (positional
            or keyword) is different.

            :param args: Tuple of positional arguments passed to the class
              call.
            :param kwargs: Dictionary of keyword arguments passed to the class
              call.
            :return: A hash of the arguments.
            """
            jwargs = json.dumps(kwargs, sort_keys=True)
            return hash((args, jwargs))

    class _SemiSingleton(type):
        """
        Metaclass for semi-singleton types.
        """

        _SemiSingleton__semisingleton_instance_map = {}
        _SemiSingleton__semisingleton_hashfunc = hashfunc

        def __call__(cls, *args, **kwargs):
            key = hashfunc(args, kwargs)
            if key not in cls._SemiSingleton__semisingleton_instance_map:
                cls._SemiSingleton__semisingleton_instance_map[key] = super(
                    _SemiSingleton, cls
                ).__call__(*args, **kwargs)
            return cls._SemiSingleton__semisingleton_instance_map[key]

    return _SemiSingleton


def add_mapping(obj: object, *args, **kwargs):
    """
    Adds another mapping to a semi-singleton instance.

    This function can be used to add another mapping to an instance of a
    semi-singleton object.  It can be useful for situations where the same
    object can have multiple "names" (or, sets of arguments), but it is
    inefficient to implement this in the metaclass hash function.  Using this
    function instead allows a memory-time tradeoff, tipping the balance towards
    more memory usage in favor of a faster hash function (and therefore, object
    instantiation).

    >>> from edgegraph.singleton import semi_singleton_metaclass, add_mapping
    >>> class SemiSingleton(metaclass=semi_singleton_metaclass()):
    ...     def __init__(self, foo, bar=False):
    ...         self.foo = foo
    ...         self.bar = bar
    ...
    >>> s3 = SemiSingleton(37, True)  # different arguments -- different object
    >>> s3
    <__main__.SemiSingleton object at 0x01234567>
    >>> s2 is s3
    False
    >>> add_mapping(s3, 39, bar=True)
    >>> s4 = SemiSingleton(39, True)  # we get s3 again, despite different args
    >>> s4
    <__main__.SemiSingleton object at 0x01234567>
    >>> s3 is s4
    True

    :param obj: The object to map the extra identifier to.  Henceforth after
      this function, this object will be reachable by the identifier given as
      well as any others it may have already had.
    :param \\*args: Positional arguments as would normally be passed to the
      semi-singleton class instantiation.
    :param \\**kwargs: Positional arguments as would normally be passed to the
      semi-singleton class instantiation.
    """
    # get the metaclass type
    cls = type(type(obj))

    # use the metaclass's hash function to line up with existing / future
    # mappings
    # see the note at the top of the file regarding the type-checker silencing
    hashfunc = cls._SemiSingleton__semisingleton_hashfunc  # type: ignore
    hashid = hashfunc(args, kwargs)

    # store the hashed identifier in the metaclass map of hashes to instances
    cls._SemiSingleton__semisingleton_instance_map[hashid] = obj  # type: ignore


def drop_semi_singleton_mapping(cls: type, *args, **kwargs):
    """
    Remove an mapping from the specified semi-singleton instance.

    This removes a *single* mapping of a key to instance.  It may be considered
    removing a semisingleton instance, though if multiple mappings exist to
    single instance, it will still be accessible by other remaining
    identifiers.

    .. seealso::

       * :py:func:`clear_semi_singleton`, a clear-all operation instead of this
         clear-one

    >>> from edgegraph.singleton import semi_singleton_metaclass, \\
            drop_semi_singleton_mapping
    >>> class SemiSingleton(metaclass=semi_singleton_metaclass()):
    ...     def __init__(self, foo, bar=False):
    ...         self.foo = foo
    ...         self.bar = bar
    ...
    >>> s3 = SemiSingleton(37, True)  # different arguments -- different object
    >>> s3
    <__main__.SemiSingleton object at 0x01234567>
    >>> s4 = SemiSingleton(4)
    >>> s5 = SemiSingleton(5)
    >>> drop_semi_singleton_mapping(SemiSingleton, 4)  # drop s4
    >>> s4_2 = SemiSingleton(4)  # will now return a new instance
    >>> s4 is s4_2
    False
    >>> SemiSingleton(5) is s5  # other mappings unaffected
    True

    :param cls: Class to remove the mapping from.  This is typically thought of
      as ``type(some_object)``.
    :param \\*args: Positional arguments as would normally be passed to the
      semi-singleton class instantiation.
    :param \\**kwargs: Positional arguments as would normally be passed to the
      semi-singleton class instantiation.
    """
    # get the metaclass type
    mcls = type(cls)

    # use the metaclass's hash function to identify the primary key
    # see the note at the top of the file regarding the type-checker silencing
    hashfunc = mcls._SemiSingleton__semisingleton_hashfunc  # type: ignore
    hashid = hashfunc(args, kwargs)

    del mcls._SemiSingleton__semisingleton_instance_map[hashid]


def check_semi_singleton_entry_exists(cls: type, *args, **kwargs) -> object:
    """
    Test whether a semisingleton exists for the given mapping without creating
    it.

    This function allows checking whether a semisingleton instance exists for
    the provided identifier, without creating it if it does not exist.

    >>> from edgegraph.singleton import semi_singleton_metaclass, \\
            check_semi_singleton_entry_exists
    >>> class SemiSingleton(metaclass=semi_singleton_metaclass()):
    ...     def __init__(self, foo, bar=False):
    ...         self.foo = foo
    ...         self.bar = bar
    ...
    >>> s3 = SemiSingleton(37, True)  # different arguments -- different object
    >>> s3
    <__main__.SemiSingleton object at 0x01234567>
    >>> # object exists; it will be returned, but unaffected
    >>> check_semi_singleton_entry_exists(SemiSingleton, 37, bar=True)
    <__main__.SemiSingleton object at 0x01234567>
    >>> # object does not exist; None returned, such an object is *not* created
    >>> check_semi_singleton_entry_exists(128)
    >>>

    :param cls: Class to test.  This is typically thought of as
      ``type(some_object)``.
    :param \\*args: Positional arguments as would normally be passed to the
      semi-singleton class instantiation.
    :param \\**kwargs: Positional arguments as would normally be passed to the
      semi-singleton class instantiation.
    :return: The instance accessible via the given mapping if such exists; else
      ``None``.
    """
    # get the real semisingleton metaclass, not just the user type
    mcls = type(cls)

    # use the metaclass's hash function to identify the primary key
    # see the note at the top of the file regarding the type-checker silencing
    hashfunc = mcls._SemiSingleton__semisingleton_hashfunc  # type: ignore
    hashid = hashfunc(args, kwargs)

    if hashid in mcls._SemiSingleton__semisingleton_instance_map:  # type: ignore
        return mcls._SemiSingleton__semisingleton_instance_map[hashid]  # type: ignore

    return None


def get_all_semi_singleton_instances(cls: type) -> Generator[object]:
    """
    Get all instances belonging to a given semi-singleton type.

    This is a simple operation, in concept:  it retrieves all the unique
    instances of the specified semi-singleton type.  It may best be explained
    by example:

    >>> from edgegraph.structure import singleton
    >>> class SemiSingle(metaclass=singleton.semi_singleton_metaclass()): pass
    >>> instances = [SemiSingle(i) for i in range(10)]  # all unique instances
    >>> checked = singleton.get_all_semi_singleton_instances(SemiSingle)
    >>> set(checked) == set(instances)  # use sets -- order may not be same
    True

    .. note::

       Internally, references to these instances are kept as the *value* side
       of a dictionary, which maintains insertion order.  Therefore, some
       semblence of order may be present, but it shouldn't be relied upon.

    .. seealso::

       * :py:func:`semi_singleton_metaclass`, for more info about
         semi-singletons
       * :py:func:`clear_semi_singleton`, to reset a given semi-singleton

    :param cls: Data type to check singleton instances for.
    :return: Generator expression yielding semi-singleton instances.
    """
    yield from type(cls)._SemiSingleton__semisingleton_instance_map.values()  # type: ignore


def clear_semi_singleton(cls: type) -> None:
    """
    Clears a specified semi-singleton.

    This operation is also sometimes referred to as "resetting" a
    (semi-)singleton data type.  It clears the internal hashmap (dictionary)
    relating hashed arguments to their instance.  It may be best explained by
    example:

    >>> from edgegraph.structure import singleton
    >>> class SemiSingle(metaclass=singleton.semi_singleton_metaclass()): pass
    >>> instances = [SemiSingle(i) for i in range(10)]  # all unique instances
    >>> s = SemiSingle(7)
    >>> s is instances[7]
    True
    >>> singleton.clear_semi_singleton(SemiSingle)
    >>> s2 = SemiSingle(7)  # will now give us a new object
    >>> s is s2  # see, different from the old one!
    False

    Note that this operation does not outright delete all the old objects.
    Normal garbage collection rules apply.

    .. seealso::

       * :py:func:`semi_singleton_metaclass`, for more info about
         semi-singletons
       * :py:func:`get_all_semi_singleton_instances`, to retrieve instead of
         clear the semi-singleton instances

    :param cls: Class to clear semisingleton states from.
    """
    type(cls)._SemiSingleton__semisingleton_instance_map = {}  # type: ignore
