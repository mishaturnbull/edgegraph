#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file defines version information for edgegraph.

This is the ONLY place version information should be updated!!
"""

#: major version number (the X in vX.Y.Z)
#:
#: :type: int
VERSION_MAJOR = 0

#: minor version number (the Y in vX.Y.Z)
#:
#: :type: int
VERSION_MINOR = 0

#: patch version number (the Z in vX.Y.Z)
#:
#: :type: int
VERSION_PATCH = 0

#: prerelease version text
#:
#: if not blank, this is appended to the version identifier after a dash.  for
#: example, setting this to ``prealpha`` will add a ``-prealpha`` appended to
#: the end of the version ``vX.Y.Z`` string.
VERSION_PREREL = "prealpha"

#: build metadata text
#:
#: if not blank, defines extra information appended to the version identifier
#: after a plus.  for example, setting this to ``12345`` will add a ``+12345``
#; appended to the end of the version ``vX.Y.Z`` string.
VERSION_BUILD = ""

__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
if VERSION_PREREL:
    __version__ += '-' + VERSION_PREREL
if VERSION_BUILD:
    __version__ += '+' + VERSION_BUILD

