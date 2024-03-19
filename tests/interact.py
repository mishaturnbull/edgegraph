#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Quickly enter an interactive session with an example graph already
instantiated.

Designed for interactive testing and development, not unit tests!
"""

import code

from edgegraph.builder import randgraph
from edgegraph.output import plaintext, plantuml as pu

def main():
    graph = randgraph.randgraph()
    print(plaintext.basic_render(graph, rfunc=lambda v: v.i, sort=lambda v: v.i))

    with open('out2.puml', 'w') as wfp:
        wfp.write(pu.render_to_plantuml_src(graph, pu.PLANTUML_RENDER_OPTIONS))

    code.interact(local={**locals(), **globals()})


if __name__ == '__main__':
    main()

