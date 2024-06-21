#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.twoendedlink.TwoEndedLink class.
"""

import pytest
from edgegraph.structure import vertex, link, twoendedlink


def test_twoendlink_subclass():
    """
    Ensure that a TwoEndedLink looks like a Link and quacks like a Link.
    """
    assert issubclass(
        twoendedlink.TwoEndedLink, link.Link
    ), "TwoEndedLink has wrong superclass!"

    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = twoendedlink.TwoEndedLink(v1, v2, uid=-100, attributes={"fifteen": 15})

    assert e.vertices == (v1, v2), "TwoEndedLink did not pass vertices to super!"
    assert e.uid == -100, "TwoEndedLink did not pass UID to super!"
    assert e.fifteen == 15, "TwoEndedLink did not pass attributes to super!"


def test_twoendlink_init_vertices():
    """
    Ensure TwoEndedLinks can be instantiated with vertices specified.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()

    e = twoendedlink.TwoEndedLink(v1, v2)

    assert e.v1 is v1, "TwoEndedLink did not store v1!"
    assert e.v2 is v2, "TwoEndedLink did not store v2!"

    f = twoendedlink.TwoEndedLink()

    assert f.v1 is None, "TwoEndedLink did not accept v1=None!"
    assert f.v2 is None, "TwoEndedLink did not accept v2=None!"


def test_twoendlink_init_vertices_wrong():
    """
    Ensure errors are raised when passing invalid objects into two-ended links.
    """
    with pytest.raises(TypeError):
        twoendedlink.TwoEndedLink(object(), vertex.Vertex())

    with pytest.raises(TypeError):
        twoendedlink.TwoEndedLink(vertex.Vertex(), object())

    with pytest.raises(TypeError):
        twoendedlink.TwoEndedLink(object(), object())


def test_twoendedlink_other():
    """
    Ensure the other() method works as expected.
    """
    v1 = vertex.Vertex()
    v2 = vertex.Vertex()
    v3 = vertex.Vertex()
    e = twoendedlink.TwoEndedLink(v1, v2)

    assert e.other(v1) is v2, "TwoEndedLink.other took v1 and did not give v2"
    assert e.other(v2) is v1, "TwoEndedLink.other took v2 and did not give v1"
    assert e.other(v3) is None, "TwoEndedLink took <not in edge> and did not give None"
