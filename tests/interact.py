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

    src = pu.render_to_plantuml_src(graph, pu.PLANTUML_RENDER_OPTIONS)
    with open("out.puml", 'w') as fp:
        fp.write(src)

    code.interact(local={**locals(), **globals()})


if __name__ == '__main__':
    main()

