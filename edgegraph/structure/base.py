#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Contains the BaseObject class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Iterator
import uuid

if TYPE_CHECKING:
    from edgegraph.structure.universe import Universe


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

    def __init__(
        self,
        *,
        uid: int | None = None,
        attributes: dict | None = None,
        universes: Iterator[Universe] | None = None,
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

        if attributes is not None:
            if not isinstance(attributes, dict):
                raise TypeError(
                    f"`attributes` must be a dictionary; got {type(attributes)}"
                )
            for key, val in attributes.items():
                setattr(self, key, val)

        #: Internal reference to the universes this object is a part of
        #:
        #: :meta private:
        self._universes: list[Universe] = (
            list(universes) if universes is not None else []
        )

        # deduplicate it while keeping order
        # https://stackoverflow.com/a/17016257
        self._universes = [*dict.fromkeys(self._universes)]

    @property
    def uid(self) -> int:
        """
        Get the UID of this object.
        """
        return self._uid

    @property
    def universes(self) -> list[Universe]:
        """
        Get the universes this object belongs to.

        Note that the copy returned is just that, a copy.  Modifications to
        this list that you may make will have no effect on the object.

        .. seealso::

           :py:meth:`~edgegraph.structure.base.BaseObject.add_to_universe`,
           :py:meth:`~edgegraph.structure.base.BaseObject.remove_from_universe`
           to add or remove this object from a given universe
        """
        return list(self._universes)

    def add_to_universe(self, universe: Universe) -> None:
        """
        Adds this object to a new universe.  If it is already there, no action
        is taken.

        :param universe: the new universe to add this object to
        """
        # do not accept duplicates
        if universe in self._universes:
            return

        self._universes.append(universe)

    def remove_from_universe(self, universe: Universe) -> None:
        """
        Remove this object from the specified universe.

        :param universe: the universe that this object will be removed from
        :raises ValueError: if this object is not present in the given universe
        """
        self._universes.remove(universe)

    # These three control attrib access via KEYS; bobj['x'], bobj['y'] = y; del
    # bobj['y']
    def __getitem__(self, name):
        """
        Called by :py:`bobj['x']` to get the ``x`` item.
        """
        return getattr(self, name)

    def __setitem__(self, name, val):
        """
        Called by :py:`bobj['x'] = y` to set the ``x`` item.
        """
        setattr(self, name, val)

    def __delitem__(self, name):
        """
        Called by :py:`del bobj['x']` to delete the ``x`` item.
        """
        delattr(self, name)
