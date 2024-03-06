#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Create PlantUML sourcecode for a graph.

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
import shutil
import tempfile
import datetime

from edgegraph.structure import Universe, Vertex, DirectedEdge, UnDirectedEdge
from edgegraph.traversal import helpers
from edgegraph import version

PLANTUML_AUTOGEN_NOTE = f"""
note as n1
    PlantUML source generated by
    edgegraph on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
end note
"""

#: Default options for PlantUML rendering.
#:
#: Keys as follows:
#:
#: * ``"skinparams"``: :py:class:`dict`, controls diagram-wide skinparams.
#:
#:   * ``"dpi"``: :py:class:`str`, controls DPI skinparam (dots per inch)
#:
#: * :py:class:`~edgegraph.structure.vertex.Vertex`: (yes, the actual Vertex
#:   *class*): controls rendering for the Vertex class and any subclasses
#:   thereof
#:
#:   * ``"type"``: :py:class:`str` (default ``"object"``), PlantUML class used
#:   * ``"stereotype_skinparams"``: :py:class:`dict`, controls skinparams
#:     applied to relevant objects in the diagram
#:
#:     * Any stereotype-specific skinparam can go here, and it'll be applied
#:       automatically.  For example:
#:     * ``"BackgroundColor": "White"`` causes the skinparam
#:       ``BackgroundColor<<Vertex>> White`` to be applied diagram-wide.
#:
#:   * ``"show_attrs"``: :py:class:`list` of :py:class:`str`, representing
#:     regular expressions.  if any match an instance attribute's name, that
#:     attribute (name and value) are included on the diagram.
#:   * ``"title_format"``: :py:class:`str`, format string used to create the
#:     object title.  if set to ``"$id"``, will result in ``hex(id(obj))``.
#:     all instance attributes are available to this format string.
#:
#: * :py:class:`~edgegraph.structure.directededge.DirectedEdge`: (yes, the
#:   actual *class*): controls rendering for DirectedEdges and any subclasses
#:   thereof.
#:
#:   * ``"v1side"``: :py:class:`str`, controls the ending of the arrow at the
#:     :py:attr:`~edgegraph.structure.directededge.DirectedEdge.v1` end of the
#:     link.  default ``""``.
#:   * ``"v2side"``: :py:class:`str`, controls the ending of the arrow at the
#:     :py:attr:`~edgegraph.structure.directededge.DirectedEdge.v2` end of the
#:     link.  default ``">"``.
#:
#: * :py:class:`~edgegraph.structure.undirectededge.UnDirectedEdge`: (yes, the
#:   actual *class*): controls rendering for UnDirectedEdges and any subclasses
#:   thereof.
#:
#:   * ``"v1side"``: :py:class:`str`, controls the ending of the arrow at the
#:     :py:attr:`~edgegraph.structure.undirectededge.UnDirectedEdge.v1` end of
#:     the link.  default ``""``.
#:   * ``"v2side"``: :py:class:`str`, controls the ending of the arrow at the
#:     :py:attr:`~edgegraph.structure.undirectededge.UnDirectedEdge.v2` end of
#:     the link.  default ``""``.
PLANTUML_RENDER_OPTIONS = {
        "skinparams": {
            "dpi": "300",
        },
        Vertex: {
            "type": "object",
            "stereotype_skinparams": {
                "BackgroundColor": "White",
                "FontColor": "Black",
                "StereotypeFontColor": "Black",
            },
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

def is_plantuml_installed(plantuml: str="plantuml") -> bool:
    """
    Checks if PlantUML is installed and usable on this system.

    This function checks if the PlantUML program is available for use on the
    current system.  If so, it returns ``True``.  If not, ``False``.

    .. seealso::

       It may be useful to check this function before trying to use
       :py:func:`render_to_image`.  If this function returns ``True``, that one
       should be safe to use!

    :param plantuml: PlantUML syscall invocation to use.
    :return: Whether or not PlantUML is usable.
    """
    try:
        subprocess.run([plantuml, '--version'], check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def _resolve_options(clas, options):
    search = clas
    mro_idx = 0

    while search not in options:
        # we did not find the thing we were looking for
        mro_idx += 1
        if mro_idx >= len(clas.__mro__):
            raise ValueError(f"Cannot identify useful superclass of {clas}!")
        search = clas.__mro__[mro_idx]

    opts = options[search]

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

def _one_vert_to_skinparam(vert, options):
    opts = _resolve_options(type(vert), options)
    if 'stereotype_skinparams' not in opts:
        return []

    stereo = opts['stereotype_skinparams']
    typename = type(vert).__name__
    output = []
    for key, val in stereo.items():
        output.append(f"{key}<<{typename}>> {val}\n")
    return output

def render_to_plantuml_src(uni: Universe,
                           options: dict) -> str:
    """
    Render a universe to PlantUML source.

    This function creates a PlantUML object diagram sourcecode to represent the
    given universe.  Vertices are treated as objects, and a number of thematic
    options can be applied based on their types, attributes, and the supplied
    options.

    .. seealso::

       This function works smoothly with :py:func:`render_to_image`.

    :param uni: The universe to render.
    :param options: Rendering options and customizations.
    :return: A (multi-line) string, representing PlantUML code.
    """

    if len(uni.vertices) == 0:
        return None

    components = ["@startuml\n"]
    links = set()
    skinparams = set()
    vertex_comps = []
    for vert in uni.vertices:
        vertex_comps.append(_one_vert_to_puml(vert, options))
        links |= set(vert.links)
        skinparams |= set(_one_vert_to_skinparam(vert, options))

    # these are the overall, diagram-wide skinparams
    if 'skinparams' in options and len(options['skinparams']):
        for spkey, spval in options['skinparams'].items():
            components.append(f"skinparam {spkey} {spval}\n")

    # these are the per-object skinparams
    if len(skinparams):
        components.append("skinparam object {\n")
        components.extend('    ' + s for s in skinparams)
        components.append("}\n")

    components.append(PLANTUML_AUTOGEN_NOTE)

    components.extend(vertex_comps)
    for link in links:
        components.append(_one_link_to_puml(link, options))

    

    components.append("@enduml\n")
    return ''.join(components)

def render_to_image(src: str,
                    out_file: str,
                    plantuml: str="plantuml"):
    """
    Accept string PlantUML source, and create an image.

    This function accepts a string and a desired output filename, and invokes
    PlantUML to create the image from the given PlantUML sourcecode.

    .. seealso::

       * This function works smoothly with :py:func:`render_to_plantuml_src`.
         Feed that function's output into this one!
       * The :py:func:`is_plantuml_installed` function can tell you if PlantUML
         is installed on your system at runtime -- it may be beneficial to
         check that function before trying to call this one.

    For this function to work, PlantUML must be installed on the system.  Only
    PNG output is supported at this time.  Specifying an output filename not
    ending in ``"png"`` will raise an exception.

    :param src: The PlantUML sourcecode to create a diagram from.
    :param out_file: The output filename you want the image to appear at.
    :param plantuml: The command to invoke PlantUML with.
    :raises ValueError: If the specified filename is invalid.
    """
    if not out_file.endswith('.png'):
        raise ValueError("Only PNG's are supported at the moment!")
    if not len(src):
        raise ValueError("Cannot render PlantUML image with empty string src!")

    tmpdir = tempfile.mkdtemp(prefix="edgegraph_puml_renderer_")
    
    # do all the stuff inside a try/finally, to make sure the tempdir always
    # gets cleaned up whether or not an exception happens
    try:
        srcfile = os.path.join(tmpdir, "in.puml")
        outfile = os.path.join(tmpdir, "in.png")
        with open(srcfile, 'w') as wfp:
            wfp.write(src)

        # https://plantuml.com/command-line
        subprocess.run([plantuml, srcfile], capture_output=True, check=True)
        shutil.move(outfile, out_file)
    except Exception:
        raise
    finally:
        shutil.rmtree(tmpdir)

