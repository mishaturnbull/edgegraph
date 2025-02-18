#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Create graphs using the PyVis framework.

This module supports exporting networks for, and shortcutting the display of,
`PyVis`_ networks / graphs.  This feature is only available if the ``pyvis``
module is installed -- otherwise, attempting to import this module will raise
an :py:exc:`ImportError` detailing this and how to install pyvis.

PyVis itself provides an interactive, HTML-based rendering of graphs.  Users
can zoom, pan around graphs, and click-and-drag the nodes themselves.  Nodes
and edges can be individually labelled, colors, sizes, and weights can be
applied, and the physics model can be optionally be changed via the UI's
customizations.  See `PyVis`_'s documentation for more information, and demos.

Generally, the usage pattern for this module is intended to be as:

.. code-block:: python
   :linenos:

   from edgegraph.builder import randgraph
   from edgegraph.output import pyvis

   uni = randgraph.randgraph()

   if you_want_customizable_ui:
       pvn = pyvis.pyvis_render_customizable(uni, rvfunc=lambda v: str(v.i))
   else:
       pvn = pyvis.make_pyvis_net(uni, rvfunc=lambda v: str(v.i))

   # notebook=False for usage outside of a Jupyter notebook.  this call will
   # block as the web browser opens to show the HTML file
   pvn.show("example.html", notebook=False)

.. _PyVis: https://pyvis.readthedocs.io/en/latest/index.html
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from collections.abc import Callable

try:

    from pyvis import network

except ImportError as exc:

    import sys

    msg = (
        "It appears pyvis is not installed.  Please install it before using"
        f" EdgeGraph's PyVis interactions.\n\n\t{sys.executable} -m pip "
        "install pyvis\n\n"
    )
    raise ImportError(msg) from exc

from edgegraph.structure import Universe, DirectedEdge

if TYPE_CHECKING:
    import pyvis


def make_pyvis_net(
    uni: Universe,
    rvfunc: Callable | None = None,
    refunc: Callable | None = None,
    network_kwargs: dict[str, Any] | None = None,
) -> pyvis.network.Network:
    """
    Convert a given Universe to a PyVis network, suitable for further use
    within PyVis.

    This function accepts a :py:class:`~edgegraph.structure.universe.Universe`
    object to a :py:class:`pyvis.network.Network` object.  The Network object
    will have all the nodes (edgegraph calls them "vertices", pyvis calls them
    "nodes", same abstract thing) from the given Universe, and all the edges
    between them.  Directionality of the edges assigned to the Network reflects
    their directionality in the Universe.

    .. seealso::

       :py:func:`pyvis_render_customizable`, which provides the same features
       as this function, but sets up a customization UI as well.

    :param uni: The universe to use as input.
    :param rvfunc: A callable object to provide the label for any given vertex
       being added to the network (short for "(R)ender (V)ertex (Func)tion").
       If supplied, it must take one argument (an instance of
       :py:class:`~edgegraph.structure.vertex.Vertex` or subclass thereof), and
       must return a :py:class:`str`.  If not provided, ``hex(id(vert))`` will
       be used.
    :param refunc: A callable object to provide the label for any given edge
       being added to the network (short for "(R)ender (E)dge (Func)tion").  If
       supplied, it must take one argument (an instance of
       :py:class:`~edgegraph.structure.twoendedlink.TwoEndedLink`, or subclass
       thereof), and must return a :py:class:`str`.  If not provided, edges
       will not be labelled.
    :param network_kwargs: An optional dictionary of keyword arguments to pass
      to :py:class:`pyvis.network.Network`.  If not supplied, the default will
      select ``"cdn_resources": "local"`` and nothing else.
    :return: A :py:class:`pyvis.network.Network` instance containing the data
       found in the given universe.
    """

    if network_kwargs is None:
        network_kwargs = {"cdn_resources": "local"}
    net = network.Network(**network_kwargs)
    verts = list(uni.vertices)
    for i, vert in enumerate(verts):
        if rvfunc:
            net.add_node(i, label=rvfunc(vert))
        else:
            net.add_node(i, label=hex(id(vert)))

        # store a temporary attribute on the object that we will use for fast
        # lookup of this vertex's index later on
        # pylint: disable-next=protected-access
        vert.__make_pyvis_net_i = i

    for i, vert in enumerate(verts):
        for edge in vert.links:

            # only draw arrows when we're at the *from* node
            if vert is edge.v2:
                continue

            other = edge.other(vert)
            try:
                # this is *much* faster than something like verts.index(other)
                # pylint: disable-next=protected-access
                j = other.__make_pyvis_net_i
            except AttributeError:
                # not a member
                continue

            # pyvis doesn't directly offer an argument in the add_edge() method
            # to specify if the arrow is directed or not.  rather, its edge
            # class is instantiated internally using the net.directed (as it
            # would know, self.directed) attribute.  therefore, by toggling
            # that attribute just before we create the edge, we can control the
            # directed-ness of the edge
            net.directed = issubclass(type(edge), DirectedEdge)

            try:
                if refunc:
                    net.add_edge(i, j, title=refunc(edge))
                else:
                    net.add_edge(i, j)
            except AssertionError:
                # AssertionError is raised by pyvis module if trying to link to
                # a non-existent vertex (node).  this should be exceedingly
                # rare in the wild, but can be triggered if a vertex already
                # has the ``__make_pyvis_net_i`` attribute that we didn't add
                # in this function (i.e. it carried it in).
                #
                # the effect of this is that the node we're trying to link to
                # doesn't exist, so skip it.
                continue

    # make sure we remove our temporary attribute
    for vert in verts:
        del vert.__make_pyvis_net_i

    return net


def pyvis_render_customizable(
    uni: Universe,
    rvfunc: Callable | None = None,
    refunc: Callable | None = None,
    show_buttons_filter: dict[str, str] | None = None,
) -> pyvis.network.Network:
    """
    Convert a given Universe to a PyVis network, suitable for further use
    within PyVis.  Then, apply a flag to it to cause the display of a
    customization UI when the network is shown in HTML.

    .. note::

       This function is *very* similar to :py:func:`make_pyvis_net`.  In fact,
       3 out of the 4 arguments given here are passed directly through to it.

    In addition to the network created by :py:func:`make_pyvis_net`, this
    function sets a flag that displays real-time adjustable options to the
    viewer of the graph.  This can include sliders to control node physics,
    colors, label visiblity, selection, and more.

    :param uni: The universe to use as input.
    :param rvfunc: A callable object to provide the label for any given vertex
       being added to the network (short for "(R)ender (V)ertex (Func)tion").
       If supplied, it must take one argument (an instance of
       :py:class:`~edgegraph.structure.vertex.Vertex` or subclass thereof), and
       must return a :py:class:`str`.  If not provided, ``hex(id(vert))`` will
       be used.
    :param refunc: A callable object to provide the label for any given edge
       being added to the network (short for "(R)ender (E)dge (Func)tion").  If
       supplied, it must take one argument (an instance of
       :py:class:`~edgegraph.structure.twoendedlink.TwoEndedLink`, or subclass
       thereof), and must return a :py:class:`str`.  If not provided, edges
       will not be labelled.
    :param show_buttons_filter: Sets the widgets that will be available in the
       customization UI displayed by Pyvis.  May be a list of strings,
       :py:obj:`True` or :py:obj:`None` to display all.

       .. seealso::

          :py:meth:`pyvis.network.Network.show_buttons`, which includes a list
          of options passable to ``show_buttons_filter``.

    :return: A :py:class:`pyvis.network.Network` instance containing the data
       found in the given universe.
    """
    net = make_pyvis_net(uni, rvfunc, refunc)
    net.show_buttons(filter_=None or show_buttons_filter)
    return net
