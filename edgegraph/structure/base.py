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
    """

    def __init__(self,
                 uid=None,
                 attributes=None,
                 universe=None,
                ):
        """
        Instantiate a BaseObject.

        :param uuid: universally unique identifier of this object, or None.  If
            :py:`None`, one will automatically be generated.
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
        self._attributes = {} or attributes

        #: Internal reference to the universe this object is a part of
        #:
        #: :meta private:
        self._universe = universe

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self):
        raise NotImplementedError("UID may not be written!")

    @property
    def universe(self):
        return self.universe

    @universe.setter
    def universe(self):
        # TODO: update universe references to objects here
        pass

