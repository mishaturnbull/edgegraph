# -*- coding: utf-8 -*-

"""
The bulk of general-purpose exception types, for use all across edgegraph.
"""

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
