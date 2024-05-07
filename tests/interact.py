#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Quickly enter an interactive session with an example graph already
instantiated.

Designed for interactive testing and development, not unit tests!

Invoke as ``python -m tests.interact``.  A random graph will be generated, its
structure printed to the console, and the universe is available as the
``graph`` global (of type :py:class:`~edgegraph.structure.universe.Universe`).
"""

import code

from edgegraph.builder import randgraph
from edgegraph.output import plaintext, plantuml as pu, pyvis

def main():
    """
    Main routine.
    """
    graph = randgraph.randgraph(count=100)
    print(plaintext.basic_render(graph, rfunc=lambda v: v.i, sort=lambda v: v.i))

    with open('out2.puml', 'w', encoding='utf-8') as wfp:
        wfp.write(pu.render_to_plantuml_src(graph, pu.PLANTUML_RENDER_OPTIONS))

    code.interact(local={**locals(), **globals()})


if __name__ == '__main__':
    main()

