# -*- coding: utf-8 -*-

"""
Git driver for EdgeGraph documentation.

Provides functions and utilities for detecting Git versions while building
documentation.
"""

import shlex
import subprocess


def _run_cmd(cmd):
    """
    Run a command, capturing and returning its output.
    """
    out = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        check=True,
    )
    return out.stdout.decode("ascii").strip()


def branchname():
    """
    Check and return the current repository branch name.
    """
    return _run_cmd("git rev-parse --abbrev-ref HEAD")


def is_clean():
    """
    Determine whether the repository is currently 'clean' or not; that is, no
    uncommitted changes or untracked files.
    """
    out = _run_cmd("git status --porcelain")
    return len(out) == 0
