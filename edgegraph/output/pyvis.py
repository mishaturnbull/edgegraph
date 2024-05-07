#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Create graphs using the PyVis framework.

.. todo::

   Document this
"""

from __future__ import annotations

try:

    from pyvis import network

except ImportError as exc:

    msg = "It appears pyvis is not installed.  Please install it before using" \
            "EdgeGraph's PyVis interactions."
    raise ImportError(msg) from exc

from edgegraph.structure import Universe
from edgegraph.traversal import helpers

def basic_pyvis(uni: Universe,
        rfunc: Callable=None):
    """
    .. todo::

       Document this.
    """

    net = network.Network()
    verts = list(uni.vertices)
    for i, vert in enumerate(verts):
        if rfunc:
            net.add_node(i, label=rfunc(vert))
        else:
            net.add_node(i, label=hex(id(vert)))

    for i, vert in enumerate(verts):
        nbs = helpers.neighbors(vert)
        for nb in nbs:
            j = verts.index(nb)
            net.add_edge(i, j)

    return net

def pyvis_render_customizable(uni: Universe,
        rfunc: Callable=None,
        show_buttons_filter_=None,
        ):
    """
    .. todo::

       Document this
    """
    net = basic_pyvis(uni, rfunc)
    net.show_buttons(filter_=None or show_buttons_filter_)
    return net

