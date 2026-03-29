# -*- coding: utf-8 -*-

"""
General-purpose exceptions for use across all of edgegraph.

This module contains all exception types which will be thrown by edgegraph.
"""

# Under the hood, break up exceptions into submodules to keep __init__ tidy.

# Do a bit of magic to manage __all__ without having to re-type everything.
# We'll compare the dir() before and after all the imports, and any differences
# go into __all__.
_dir_before = set(dir())

# That does mean we have some code above imports, which ruff doesn't like, but
# it doesn't get the big picture here.
# ruff: noqa: E402, F403

from edgegraph.exceptions._general_purpose import *

_dir_after = set(dir())
_all = _dir_after - _dir_before - {"_dir_after", "_dir_before"}

# Ruff does not seem to realize that sorted() does actually return a list.
__all__ = sorted(_all)  # noqa: PLE0605
