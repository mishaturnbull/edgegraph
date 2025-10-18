# -*- coding: utf-8 -*-

"""
Define version information for edgegraph.

This is the ONLY place version information should be updated!!
"""

# Take a snapshot of the directory before, to be used for determining what
# names are added
_dir_before = set(dir())

#: major version number (the X in vX.Y.Z)
#:
#: :type: int
VERSION_MAJOR = 0

#: minor version number (the Y in vX.Y.Z)
#:
#: :type: int
VERSION_MINOR = 11

#: patch version number (the Z in vX.Y.Z)
#:
#: :type: int
VERSION_PATCH = 0

__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

# Figure out what variables have been added, and export them to __all__
_dir_after = set(dir())
_all = _dir_after - _dir_before - {"_dir_before", "_dir_after"}
__all__ = list(_all)
