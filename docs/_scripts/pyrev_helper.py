#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
Helper script for generating pyreverse-driven UML diagrams.
"""

import os

DOCS_PATH = os.path.split(os.path.split(__file__)[0])[0]
PROJ_PATH = os.path.split(DOCS_PATH)[0]

DEFAULT_OPTS = [
    "--output plantuml",
    f"--output-directory {DOCS_PATH}/_auto/uml/",
]

CALLS = [
    "pyreverse {options} -A -s0 -my --colorized edgegraph",
]


def call_one(call):
    """
    Print and make a syscall.
    """
    call = call.format(options=" ".join(DEFAULT_OPTS))
    print(call)
    os.system(call)


def main():
    """
    Call all necessary pyrev options to generate diagrams.
    """
    orig_path = os.getcwd()
    os.chdir(PROJ_PATH)
    for call in CALLS:
        call_one(call)
    os.chdir(orig_path)


if __name__ == "__main__":
    main()
