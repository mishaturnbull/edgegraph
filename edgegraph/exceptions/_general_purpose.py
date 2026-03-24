# -*- coding: utf-8 -*-

"""
The bulk of general-purpose exception types, for use all across edgegraph.
"""

_dir_before = dir()


class GraphContainsCyclesError(Exception):
    """
    A graph under examination contains a cycle and is being used in a process
    which cannot process such graphs.

    For example, topological sorting operations cannot order cyclic graphs.
    """


_dir_after = dir()
_all_objs = set(_dir_after) - set(_dir_before) - {"_dir_after", "_dir_before"}
__all__ = list(_all_objs)
