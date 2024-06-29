#!python3
# -*- coding: utf-8 -*-

"""
Git driver for EdgeGraph documentation.

Provides functions and utilities for detecting Git versions while building
documentation.
"""

import subprocess
import shlex


def _run_cmd(cmd):
    """
    Run a command, capturing and returning its output.
    """
    out = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
    )
    return out.stdout.decode("ascii").strip()


def branchname():
    return _run_cmd("git rev-parse --abbrev-ref HEAD")


def is_clean():
    out = _run_cmd("git status --porcelain")
    return len(out) == 0
