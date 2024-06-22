#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Ensure the versioning constants are valid.
"""

import re
from edgegraph import version


def test_version():
    """
    Test version attributes are accessible.

    These are constants... this test is mostly to ensure 100% code coverage is
    actually reachable.
    """

    for attr in [
        version.VERSION_MAJOR,
        version.VERSION_MINOR,
        version.VERSION_PATCH,
    ]:
        assert isinstance(attr, int)
        assert attr >= 0

    # 5 is the minimum possible length, of "0.0.0"
    assert len(version.__version__) >= 5


def test_python_version_compliance():
    """
    Test version attribute is complaint with PyPA standard.

    See
    https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers
    """

    ptrn = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)"'
        r"(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$"
    )
    assert re.match(ptrn, version.__version__)
