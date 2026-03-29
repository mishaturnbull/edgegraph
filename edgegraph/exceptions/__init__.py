# -*- coding: utf-8 -*-

"""
General-purpose exceptions for use across all of edgegraph.

This module contains all exception types which will be thrown by edgegraph.
"""

# Under the hood, break up exceptions into submodules to keep __init__ tidy.
# Typically, this is bad practice; but these modules behave well in managing
# their __all__'s, so I'll allow it here.
# ruff: noqa: F403

from edgegraph.exceptions._general_purpose import *
