#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for Universe object.
"""

import pytest
from edgegraph import version

def test_version():
    """
    Test version attributes are accessible.

    These are constants... this test is mostly to ensure 100% code coverage is
    actually reachable.
    """

    for attr in [version.VERSION_MAJOR,
                 version.VERSION_MINOR,
                 version.VERSION_PATCH]:
        assert isinstance(attr, int)
        assert attr >= 0

    assert version.VERSION_PREREL is not None
    assert version.VERSION_BUILD is not None

    # 5 is the minimum possible length, of "0.0.0"
    assert len(version.__version__) >= 5

