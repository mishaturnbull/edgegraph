#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for output.plantuml module, specifically focused on interacting with
PlantUML syscalls.
"""

import os
import subprocess
import pytest
from edgegraph.output import plantuml

puml_skip = pytest.mark.skipif(
    not plantuml.is_plantuml_installed(), reason="PlantUML not installed"
)


@puml_skip
def test_plantuml_e2e(graph_clrs09_22_6, tmpdir):
    """
    Run an end-to-end shot of generating a graph and a PlantUML render of it.
    """
    src = plantuml.render_to_plantuml_src(
        graph_clrs09_22_6[0], plantuml.PLANTUML_RENDER_OPTIONS
    )
    plantuml.render_to_image(src, os.path.join(tmpdir, "out2.png"))

    files = os.listdir(tmpdir)
    assert "out2.png" in files, "final image is missing!"


@puml_skip
def test_plantuml_out_file_format():
    """
    Ensure errors are raised on unknown file formats.
    """
    with pytest.raises(ValueError):
        plantuml.render_to_image("", "out.not-a-png")

    with pytest.raises(ValueError):
        plantuml.render_to_image("", "out.jpeg")


# really, this confirms that subprocess.run errors are happening
@puml_skip
def test_plantuml_syscall_badsrc(tmpdir):
    """
    Ensure errors are raised on invalid PlantUML syntax.
    """
    bad = "@startuml\nWrong syntax!!\n@enduml"
    with pytest.raises(subprocess.CalledProcessError):
        plantuml.render_to_image(bad, os.path.join(tmpdir, "out.png"))


@puml_skip
def test_plantuml_syscall_empty(tmpdir):
    """
    Ensure we get an error when passing in empty plantuml contents.
    """
    with pytest.raises(ValueError):
        plantuml.render_to_image("", os.path.join(tmpdir, "out.png"))


def test_plantuml_detect_not_there(tmpdir):
    """
    Ensure plantuml detection does not allow a nonexistent file.
    """
    # we need a file that definitely does not exist -- so, make a tmpdir, and
    # try to call a file that we haven't created in there
    #
    # thanks, https://unix.stackexchange.com/a/643527 !
    not_there = os.path.join(tmpdir, "nothing")
    exists = plantuml.is_plantuml_installed(plantuml=not_there)
    assert exists is False, "plantuml detection false positive!"
