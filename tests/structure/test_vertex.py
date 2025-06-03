# -*- coding: utf-8 -*-

"""
Unit tests for structure.vertex.Vertex class.
"""

from edgegraph.structure import base, link, universe, vertex

# W0212 is protected-access, or, access to a protected member (starting with a
# _) of a client class.  In this case, the test objectives require we inspect
# internal state of the objects, so we need to read these attributes.
# pylint: disable=W0212


def test_vertex_subclass():
    """
    Ensure Vertex trees up to correct subclass and attributes are operating
    correctly.
    """
    assert issubclass(vertex.Vertex, base.BaseObject)

    unis = [universe.Universe(), universe.Universe()]

    v = vertex.Vertex(
        uid=-100,
        attributes={"fifteen": 15},
        universes=unis,
    )

    assert v.uid == -100
    assert v.fifteen == 15
    assert unis[0] in v.universes
    assert unis[1] in v.universes
    assert len(v.universes) == 2


def test_vertex_creation():
    """
    Ensure we can create Vertices with default options.
    """
    v = vertex.Vertex()

    assert len(v.links) == 0, "vertex init'd with links!!"


def test_vertex_create_with_links():
    """
    Ensure we can create vertices with base Link objects in a list.
    """
    links = [link.Link(_force_creation=True) for _ in range(3)]

    v1 = vertex.Vertex(links=links)
    assert v1._links == links, "vertex did not accept list of links!"
    assert v1.links == tuple(links), "vertex did not return tuple of links!"


def test_vertex_create_with_links_set():
    """
    Ensure we can create vertices with base Link objects in a set.
    """
    links = set()
    for _ in range(3):
        links.add(link.Link(_force_creation=True))

    v2 = vertex.Vertex(links=links)
    # sets are unordered, can't just compare to a list
    for obj in v2.links:
        assert obj in links, "found unexpected linkin vertex links!"
    assert len(v2.links) == len(links), "vertex links is not expected length!"
    assert isinstance(v2.links, tuple), "vertex links is not correct type!"


def test_vertex_create_with_tuple():
    """
    Ensure we can create vertices with base Link objects in a tuple.
    """
    links = [link.Link(_force_creation=True) for _ in range(3)]
    links = tuple(links)

    v3 = vertex.Vertex(links=links)
    assert v3.links == links, "vertex .links did not equal expected!"
    assert isinstance(v3.links, tuple), "vertex links is not correct type!"


def test_vertex_create_with_generator():
    """
    Ensure we can create vertices with base Link objects in a genexpr.
    """
    links = [link.Link(_force_creation=True) for _ in range(3)]

    def gen():
        yield from links

    v4 = vertex.Vertex(links=gen())
    assert v4.links == tuple(links), "vertex .links did not equal expected!"
    assert isinstance(v4.links, tuple), "vertex links is not correct type!"


def test_vert_add_to_uni():
    """
    Ensure we can add a Vertex to multiple universes.
    """
    v = vertex.Vertex()

    unis = []
    for _ in range(50):
        unis.append(universe.Universe())
        v.add_to_universe(unis[-1])

    assert len(v.universes) == 50, "vertex .universes has wrong # elements!"
    for uni in unis:
        assert v in uni.vertices, "vertex add_to_universe did not back-ref!"


def test_vert_rem_from_uni():
    """
    Ensure we can remove a Vertex from universes.
    """
    v = vertex.Vertex()

    unis = []
    for _ in range(50):
        unis.append(universe.Universe())
        v.add_to_universe(unis[-1])

    remove = unis[0 : len(unis) : 2]
    stay = unis[1 : len(unis) : 2]

    for uni in remove:
        v.remove_from_universe(uni)

        assert uni not in v.universes, (
            "remove_from_universe did not remove vert-side!"
        )
        assert v not in uni.vertices, (
            "remove_from_universes did not remove uni-side!"
        )

    for uni in stay:
        assert uni in v.universes, (
            "remove_from_universe altered unrequested uni, vert-side!"
        )
        assert v in uni.vertices, (
            "remove_from_universe altered unrequested uni, uni-side!"
        )


def test_vert_init_with_uni():
    """
    Ensure vertices init'd with universes are members of them.
    """
    unis = [universe.Universe() for _ in range(50)]

    v1 = vertex.Vertex(universes=[unis[0]])

    assert v1.universes == [unis[0]], (
        "vertex .universes does not match what was given to init!"
    )
    assert v1 in unis[0].vertices, "vertex did not register itself in universe!"

    v2 = vertex.Vertex(universes=unis)
    assert v2.universes == unis, (
        "vertex .universes does not match what was given to init!"
    )
    for uni in unis:
        assert v2 in uni.vertices, (
            "vertex did not register itself in universes!"
        )
