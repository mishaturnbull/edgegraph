#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Contains the BaseObject class.
"""

import uuid

class BaseObject (object):
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
    fixed_attrs = (
            "_uid",
            "_attributes",
            "_universe",
            "uid",
            "universe",
            )


    def __init__(self,
                 uid=None,
                 attributes=None,
                 universe=None,
                ):
        """
        Instantiate a BaseObject.

        :param uuid: universally unique identifier of this object, or None.  If
            :python:`None`, one will automatically be generated.
        :param attributes: dictionary of attributes to apply to this object.
        :param universe: the universe that this object belongs to.
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

        #: Internal reference to the universe this object is a part of
        #:
        #: :meta private:
        self._universe = universe

    @property
    def uid(self):
        """
        Get the UID of this object.

        :rtype: int
        """
        return self._uid

    @uid.setter
    def uid(self, new):
        raise NotImplementedError("UID may not be written!")

    @property
    def universe(self):
        """
        Get the universe this object belongs to.

        :rtype: None
        """
        return self._universe
    
    @universe.setter
    def universe(self, new):
        self._universe = new

    def __getattr__(self, name):
        if name in type(self).fixed_attrs:
            return super().__getattribute__(name)

        return self._attributes[name]

    def __setattr__(self, name, val):
        if name in type(self).fixed_attrs:
            return super().__setattr__(name, val)

        self._attributes[name] = val

    def __delattr__(self, name):
        del self._attributes[name]

    def __dir__(self):
        return self._attributes.keys()

