#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.pyvis module.
"""

import logging
from edgegraph.structure import Vertex
from edgegraph.builder import explicit
from edgegraph.output import pyvis
from edgegraph.traversal import helpers

LOG = logging.getLogger(__name__)


def test_pyvis_makes_net_default_args(graph_clrs09_22_6):
    """
    Ensure default-arguments make net call makes a net.
    """
    uni, verts = graph_clrs09_22_6
    pvn = pyvis.make_pyvis_net(uni)
    assert len(verts) == len(
        pvn.get_nodes()
    ), "Did not get the right number of vertices back!"


def test_pyvis_makes_net(graph_clrs09_22_6):
    """
    Ensure the PyVis network creation is working.
    """
    uni, verts = graph_clrs09_22_6
    nodes_expected = {str(v.i) for v in verts}

    pvn = pyvis.make_pyvis_net(
        uni,
        rvfunc=lambda v: str(v.i),
        refunc=lambda e: f"{e.v1.i} --> {e.v2.i}",
    )

    nodes_present = pvn.get_nodes()
    nodes_found = set()
    for nodei in nodes_present:
        LOG.info(f"TPMN iloop: nodei={nodei}, pvn={pvn.get_node(nodei)}")
        node = pvn.get_node(nodei)
        nodes_found.add(node["label"])

    assert (
        nodes_expected == nodes_found
    ), "Did not retrieve expected nodes from pyvis network!"

    edges = set()
    for vert in verts:
        edges.update(vert.links)

    edges_found = pvn.get_edges()

    for found in edges_found:
        title = found["title"]
        # this will break if there are more than 10 verts fed in to the network
        v1 = verts[int(title[0])]
        v2 = verts[int(title[6])]

        assert v2 in helpers.neighbors(v1)


def test_pyvis_customizable(graph_clrs09_22_6):
    """
    Ensure that UI customizability can be enabled.
    """
    uni, _ = graph_clrs09_22_6

    pvn = pyvis.make_pyvis_net(
        uni,
        rvfunc=lambda v: str(v.i),
        refunc=lambda e: f"{e.v1.i} --> {e.v2.i}",
    )

    assert not pvn.conf, "Customizability was enabled by default!"

    pvn = pyvis.pyvis_render_customizable(
        uni,
        rvfunc=lambda v: str(v.i),
        refunc=lambda e: f"{e.v1.i} --> {e.v2.i}",
    )

    assert pvn.conf, "Customizability was not enabled!"


def test_pyvis_vert_outside_uni(graph_clrs09_22_6):
    """
    Ensure that make_pyvis_net can handle vertices outside the given universe.
    """
    uni, verts = graph_clrs09_22_6
    extra = Vertex()
    explicit.link_directed(verts[0], extra)

    pvn = pyvis.make_pyvis_net(uni)

    nodes_present = pvn.get_nodes()
    assert len(nodes_present) == len(
        verts
    ), "Extra vertex detected in PyVIS network"


def test_pyvis_vert_outside_uni_hard(graph_clrs09_22_6):
    """
    See what happens in a worst-case scenario with the __make_pyvis_net_i
    attribute already defined.
    """
    uni, verts = graph_clrs09_22_6
    extra = Vertex()
    # inject the variable used to track cross-vertex linking
    # pylint: disable-next=protected-access
    extra.__make_pyvis_net_i = len(verts)
    explicit.link_directed(verts[0], extra)

    pvn = pyvis.make_pyvis_net(uni)

    nodes_present = pvn.get_nodes()
    assert len(nodes_present) == len(
        verts
    ), "Extra vertex detected in PyVIS network"


def test_pyvis_create_with_options(graph_clrs09_22_6):
    """
    Ensure Pyvis network kwargs passthru works.
    """
    uni, _ = graph_clrs09_22_6

    default = pyvis.make_pyvis_net(uni)
    assert default.cdn_resources == "local", "Wrong default CDN resources!"

    modded = pyvis.make_pyvis_net(
        uni, network_kwargs={"cdn_resources": "remote"}
    )
    assert modded.cdn_resources == "remote", "Wrong modified CDN resources!"
