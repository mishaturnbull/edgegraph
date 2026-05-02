# -*- coding: utf-8 -*-

"""
General-purpose exceptions for use across all of edgegraph.

This module contains all exception types which will be thrown by edgegraph.
"""

# Do a bit of magic to manage __all__ without having to re-type everything.
# We'll compare the dir() before and after all the imports, and any differences
# go into __all__.
_dir_before = set(dir())


class GraphContainsCyclesError(Exception):
    """
    A graph under examination contains a cycle and is being used in a process
    which cannot process such graphs.

    For example, topological sorting operations cannot order cyclic graphs.
    """


_dir_after = set(dir())
_all = _dir_after - _dir_before - {"_dir_after", "_dir_before"}

# Ruff does not seem to realize that sorted() does actually return a list.
__all__ = sorted(_all)  # noqa: PLE0605
