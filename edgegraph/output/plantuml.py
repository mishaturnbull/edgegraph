#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Print graphs to an ASCII format.  (Not ASCII "art"!)

This module *mostly* does not require PlantUML installed to operate.  It only
needs PlantUML installed to actually generate the images -- for only sourcecode
generation, it does not need to be installed.

.. seealso::

   PlantUML's homepage: https://plantuml.com/
"""

from __future__ import annotations

import functools
import os
import re
import subprocess
import tempfile

from edgegraph.structure import Universe, Vertex, DirectedEdge, UnDirectedEdge
from edgegraph.traversal import helpers

#: rendering options, based on type
#:
#: keys:
#:
#:   * ``"type"``: the plantuml type used (default ``"object"``)
#:   * ``"stereotype"``: stereotype definition
#:   * ``"show_attrs"``: list of regex of attribute names to show.  passed to
#:     :py:func:`re.match`.
#:   * ``"user_render_func"``: function to call instead of performing builtin
#:     rendering
#:   * ``"title_format"``: format string for object title.
PLANTUML_RENDER_OPTIONS = {
        Vertex: {
            "type": "object",
            "stereotype": "",
            "show_attrs": [".+"],
            "title_format": "$id",
        },
        DirectedEdge: {
            "v1side": "",
            "v2side": ">",
        },
        UnDirectedEdge: {
            "v1side": "",
            "v2side": "",
        },
    }

def _resolve_options(clas, options):
    search = clas
    mro_idx = 0

    while search not in options:
        # we did not find the thing we were looking for
        mro_idx += 1
        search = clas.__mro__[mro_idx]

    # TODO: replace EAFP with LBYL in while loop?
    try:
        opts = options[search]
    except KeyError:
        return None

    # combine into a super-regex to use only one
    if "show_attrs" in opts and not isinstance(opts['show_attrs'], re.Pattern):
        superrgx = '(' + ')|('.join(opts['show_attrs']) + ')'
        opts['show_attrs'] = re.compile(superrgx)

    return opts

def _vertex_title(vertex, opts):
    attr_rgx = opts['show_attrs']
    attributes = [a for a in dir(vertex) if attr_rgx.match(a)]
    if opts['title_format'] == '$id':
        title = hex(id(vertex))
    else:
        title = opts['title_format'].format(**{a: vertex[a] for a in attributes})
    return title

def _one_vert_to_puml(vertex, options):
    opts = _resolve_options(type(vertex), options)

    if 'user_render_func' in opts:
        return opts['user_render_func'](vertex, options)
    
    # identify and match the attributes described in the show_attrs tag
    attr_rgx = opts['show_attrs']
    attributes = [a for a in dir(vertex) if attr_rgx.match(a)]

    title = _vertex_title(vertex, opts)
    hdrline = f"{opts['type']} {title} <<{type(vertex).__name__}>> {{\n"

    attrlines = []
    for attr in attributes:
        attrlines += f"    {{field}} {attr} = {vertex[attr]}\n"

    ftrline = "}\n"

    return hdrline + ''.join(attrlines) + ftrline

def _one_link_to_puml(lnk, options):
    opts = _resolve_options(type(lnk), options)
    v1, v2 = lnk.v1, lnk.v2
    v1ops = _resolve_options(type(v1), options)
    v2ops = _resolve_options(type(v2), options)
    v1puml = _vertex_title(v1, v1ops)
    v2puml = _vertex_title(v2, v2ops)
    v1e = opts["v1side"]
    v2e = opts["v2side"]

    out = f"{v1puml} {v1e}--{v2e} {v2puml}\n"
    return out

def render_to_plantuml_src(uni: Universe,
                           options: dict) -> str:
    """
    Render a universe to PlantUML source.

    .. todo::
    
       document this

    """

    if len(uni.vertices) == 0:
        return None

    components = ["@startuml\n"]
    links = set()
    for vert in uni.vertices:
        vertcomp = _one_vert_to_puml(vert, options)
        components.append(vertcomp)
        links |= set(vert.links)

    try:
        for link in links:
            components.append(_one_link_to_puml(link, options))
    except Exception as e:
        import pdb; pdb.post_mortem()

    components.append("@enduml\n")
    return ''.join(components)

def render_to_image(src: str,
                    out_file: str,
                    plantuml: str="plantuml") -> bool:
    """
    Accept string PlantUML source, and create an image.

    .. todo::

       document this
    """
    srcfile = tempfile.mkstemp(prefix="edgegraph_puml_renderer_")
    with open(srcfile[1], 'w') as wfp:
        wfp.write(src)
   
    args = [plantuml, "-pipe", '-charset', "utf-8", "-filename", srcfile]
    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    os.remove(srcfile[1])

