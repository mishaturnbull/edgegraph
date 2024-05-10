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

    import sys
    msg = "It appears pyvis is not installed.  Please install it before using" \
            f" EdgeGraph's PyVis interactions.\n\n\t{sys.executable} -m pip " \
            "install pyvis\n\n"
    raise ImportError(msg) from exc

from edgegraph.structure import Universe, DirectedEdge

def make_pyvis_net(uni: Universe,
        rvfunc: Callable=None,
        refunc: Callable=None):
    """
    .. todo::

       Document this.
    """

    net = network.Network()
    verts = list(uni.vertices)
    for i, vert in enumerate(verts):
        if rvfunc:
            net.add_node(i, label=rvfunc(vert))
        else:
            net.add_node(i, label=hex(id(vert)))

    for i, vert in enumerate(verts):
        for edge in vert.links:

            # only draw arrows when we're at the *from* node
            if vert is not edge.v1:
                continue

            j = verts.index(edge.other(vert))

            # pyvis doesn't directly offer an argument in the add_edge() method
            # to specify if the arrow is directed or not.  rather, its edge
            # class is instantiated internally using the net.directed (as it
            # would know, self.directed) attribute.  therefore, by toggling
            # that attribute just before we create the edge, we can control the
            # directed-ness of the edge
            net.directed = issubclass(type(edge), DirectedEdge)

            if refunc:
                net.add_edge(i, j, title=refunc(edge))
            else:
                net.add_edge(i, j)

    return net

def pyvis_render_customizable(uni: Universe,
        rvfunc: Callable=None,
        refunc: Callable=None,
        show_buttons_filter_=None,
        ):
    """
    .. todo::

       Document this
    """
    net = make_pyvis_net(uni, rvfunc, refunc)
    net.show_buttons(filter_=None or show_buttons_filter_)
    return net

