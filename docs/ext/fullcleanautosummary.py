#!python3
# -*- coding: utf-8 -*-

"""
Sphinx extension that automatically detects and deletes autosummary
directories.

The approach here, after *much* trial and error, is to perform this task at the
end of the sphinx build.  There are multiple independent minutae that combine
to make this necessary:

    1. The autosummary extension calls sphinx-autogen *immediately* at the
       start of building.
    2. The autosummary extension does not emit any events that we can hook on
       to control before / after the sphinx-autogen run.
    3. The autogen files must be available *before* the `source-read` event is
       fired, so they can be parsed.  (If we run this process on source-read,
       the docutils parser crashes with a FileNotFound error)
    4. sphinx-build script does not hook into conf.py or any extensions *at
       all* when running the `clean` target.

Because of these three reasons, we cannot:

    A. Delete files on a `make clean`.
    B. Delete old files before sphinx-autogen recreates them
    C. Delete old files between sphinx-autogen and docutils parsing

Unfortunately that leaves us with:

    D. Delete the autosummary folders at the end of the build, every time, so
       that the *next* build starts off with a clean slate.

I'm not happy about this.
"""

import os
import shutil
from sphinx.util import logging

LOG = logging.getLogger(__name__)

AUTOSUMMARY_DIRECTIVE = ".. autosummary::"
TOCTREE_LINE = ":toctree:"


def wipe_autosummary_dirs(app, exception):
    """
    Search & destroy autosummary toctree directories.
    """
    # if there's been an exception, preserve what was generated for debugging
    if exception is not None:
        return

    files = app.project.docnames
    to_delete = set()

    for docname in files:

        with open(docname + ".rst", "r") as fp:
            lines = fp.readlines()

        # find all .. autosummary:: declarations
        linenos = []
        for i, line in enumerate(lines):
            if AUTOSUMMARY_DIRECTIVE in line:
                linenos.append(i)

        # for each autosummary (there could be multiple in a file), scan 5
        # lines ahead of it to find its corresponding :toctree: entry
        toctrees = []
        for lineno in linenos:
            searchin = lines[lineno : lineno + 5]
            for line in searchin:
                if TOCTREE_LINE in line:
                    toctrees.append(line)

        # we now have the :toctree: lines, do some string math to grab the
        # directory name
        basepath = os.path.split(docname)[0]
        dirs = []
        for toctree in toctrees:
            parts = toctree.split(TOCTREE_LINE)
            dirname = parts[-1].strip()
            path = os.path.join(basepath, dirname)
            if not path.endswith(os.path.sep):
                path += os.path.sep
            dirs.append(path)

        # update the kill set
        to_delete |= set(dirs)

    # MURDER
    for delete in to_delete:
        assert os.path.isdir(delete)
        LOG.warning(f"DELETING {delete}")
        shutil.rmtree(delete)


def setup(app):
    """
    Configure sphinx extension.
    """
    app.connect("build-finished", wipe_autosummary_dirs)
