#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Contains the BaseObject class.
"""

from __future__ import annotations
import uuid


class BaseObject(object):
    """
    Top of the object inheritance tree for everything.

    That's not quite a joke -- this class is the top of the tree when it comes
    to object types.  All other objects in edgegraph inherit from this one.

    It provides a few standardized attributes and access methods:

    * Universal unique identifier
    * Dynamic attributes storage
    * Universe association

    Through the "dynamic attributes storage", this object works as a namespace
    -- it is intended for adding attributes after initialization /
    instantiation.  For example:

       >>> b = BaseObject()
       >>> dir(b)
       []
       >>> b.x = 17
       >>> b.x
       17
       >>> dir(b)
       ['x']

    The attributes provided to the ``__init__`` method also become a part of
    this operation:

       >>> b = BaseObject(attributes={"fifteen": 15})
       >>> dir(b)
       ['fifteen']
       >>> b.fifteen
       15
    """

    #: names of attributes that are *not* dynamic attributes
    fixed_attrs: set[str] = {
        "_uid",
        "_attributes",
        "_universes",
        "uid",
        "universes",
    }

    def __init__(
        self,
        *,
        uid: int = None,
        attributes: dict = None,
        # WHY does this work??  __future__ annotations??  Universe isn't
        # imported!!
        universes: set[Universe] = None,
    ):
        """
        Instantiate a BaseObject.

        :param uid: universally unique identifier of this object, or None.  If
            :python:`None`, one will automatically be generated.
        :param attributes: dictionary of attributes to apply to this object.
        :param universes: a set of universes that this object belongs to.
        :raises TypeError: if ``attributes`` argument is of invalid type
        """

        #: Internal UID value
        #:
        #: This is the *real* value -- not exposed to the outside world.  As
        #: UID's aren't really meant to change (otherwise, their uniqueness may
        #: not hold), this is protected by a getter/setter with the setter
        #: raising an exception.
        #:
        #: :type: int
        #: :meta private:
        self._uid = uid or uuid.uuid4().int

        #: Dynamic attributes that may be manipulated by operations
        #:
        #: This dictionary is the backend for attributes that are created / set
        #: after instantiation.
        #:
        #: :type: dict
        #: :meta private:
        self._attributes = attributes or {}
        if not isinstance(self._attributes, dict):
            raise TypeError(
                f"attributes argument must be dict, got " f"{type(attributes)}!"
            )

        #: Internal reference to the universes this object is a part of
        #:
        #: :meta private:
        self._universes = universes or set()
        if not isinstance(self._universes, set):
            self._universes = set(self._universes)

    @property
    def uid(self) -> int:
        """
        Get the UID of this object.
        """
        return self._uid

    @property
    def universes(self) -> frozenset[Universe]:
        """
        Get the universes this object belongs to.

        Note that this gives you a :py:class:`frozenset`; you cannot add or
        remove universes from this attribute.

        .. seealso::

           :py:meth:`~edgegraph.structure.base.BaseObject.add_to_universe`,
           :py:meth:`~edgegraph.structure.base.BaseObject.remove_from_universe`
           to add or remove this object from a given universe

        :rtype: frozenset[Universe]
        """
        return frozenset(self._universes)

    def add_to_universe(self, universe: Universe) -> None:
        """
        Adds this object to a new universe.  If it is already there, no action
        is taken.

        :param universe: the new universe to add this object to
        """
        self._universes.add(universe)

    def remove_from_universe(self, universe: Universe) -> None:
        """
        Remove this object from the specified universe.

        :param universe: the universe that this object will be removed from
        :raises KeyError: if this object is not present in the given universe
        """
        self._universes.remove(universe)

    def __dir__(self):
        """
        Called by :py:func:`dir`.
        """
        return self._attributes.keys()

    # These three control attrib access via DOTs; bobj.x; bobj.y = 7; del
    # bobj.y etc
    def __getattr__(self, name):
        """
        Called by :py:`bobj.x` to access the ``x`` attribute.
        """
        if (name in type(self).fixed_attrs) or (name.startswith("__")):
            return super().__getattribute__(name)

        try:
            return self._attributes[name]
        except KeyError as exc:
            raise AttributeError from exc

    def __setattr__(self, name, val):
        """
        Called by :py:`bobj.x = y` to set the ``x`` attribute.
        """
        if name in type(self).fixed_attrs or name.startswith('__'):
            # TODO: figure out this return statement VVV
            #
            # pylint complains about it, with good reason (inconsistent returns
            # from this method).  logically, this method sets attributes -- it
            # should not need to return anything.  yet, remove the return, and
            # try the unit test suite...  kaboom!
            #
            # pylint: disable=inconsistent-return-statements
            return super().__setattr__(name, val)

        self._attributes[name] = val

    def __delattr__(self, name):
        """
        Called by :py:`del bobj.x` to delete the ``x`` attribute.
        """
        if name in type(self).fixed_attrs:
            raise ValueError(f"Cannot delete attribute {name}; it is fixed!")
        if name.startswith('__'):
            super().__delattr__(name)
            return

        del self._attributes[name]

    # These three control attrib access via KEYS; bobj['x'], bobj['y'] = y; del
    # bobj['y']
    def __getitem__(self, name):
        """
        Called by :py:`bobj['x']` to get the ``x`` item.
        """
        if (name in type(self).fixed_attrs) or (name.startswith("__")):
            return self.__getattr__(name)

        return self._attributes[name]

    def __setitem__(self, name, val):
        """
        Called by :py:`bobj['x'] = y` to set the ``x`` item.
        """
        if (name in type(self).fixed_attrs) or (name.startswith("__")):
            self.__setattr__(name, val)
            return

        self._attributes[name] = val

    def __delitem__(self, name):
        """
        Called by :py:`del bobj['x']` to delete the ``x`` item.
        """
        if (name in type(self).fixed_attrs) or (name.startswith("__")):
            self.__delattr__(name)
        else:
            del self._attributes[name]
