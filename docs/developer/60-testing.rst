.. _dev/testing:

Testing Practices
=================

Edgegraph follows a strict rule of unit testing and code coverage.  ***All
code*** is to be covered by unit testing, with exceptions only made for cases
which are well and truly needed (and justification is documented).  The
brilliant `PyTest`_ framework is used to drive unit testing, and `Coverage.py`_
provides coverage analysis.  `pytest-cov`_ links the two together, and
`pytest-randomly`_ is also employed to ensure order of unit tests does not
impact the tests.

Tests are written in the ``tests/`` directory of the project, and are *not*
bundled with the module to end users.  Nonetheless, standards for documentation
and code quality are enforced on all unit tests.  The entire directory is
scanned with PyLint on all GitHub pull requests.

Running tests
-------------

From the command line, you can run all tests with a simple :command:`pytest`
command issued from the project root.  Ideally, all tests will be executed and
pass.  PyTest can be integrated with numerous IDEs probably including yours,
though configuring that is outside the scope of this documentation (probably
found in your IDE docs).

By default, some slower stress tests will be executed as well.  These tests are
marked as slow, and can be excluded by passing ``-m "not slow"`` as an argument
to PyTest, for example :command:`pytest -m "not slow"`.  This flag is set in the
GitHub actions invocation of tests, and therefore, **100% code coverage must be
achieved without slow testing**.

Coverage analysis
^^^^^^^^^^^^^^^^^

The included :file:`scripts/ut_cov.sh` shell script executes all unit tests and
performs coverage analysis.  The invocation used here is identical to that in
the GitHub actions pipeline; therefore, this script accurately matches the
behavior of the pipeline.  This is useful for testing changes locally before
pushing to GitHub.

The script places an HTML report in the ``docs/_build/htmlcov`` folder; after
running it, open :file:`docs/_build/htmlcov/index.html` in your browser to see
results in an interactive format showing exactly what lines / branches were
missed.

Writing tests
-------------

Writing unit tests is an essential part of adding, changing, or removing
functionality from EdgeGraph.  Organization of the tests closely mirrors
organization of the sourcecode they test, and all tests relevant to any given
module should be in a test subdirectory easily apparent to match the code which
it tests.  An extra test subdirectory, :py:mod:`tests.integration`, is used for
testing activities which combine functionality of multiple sourcecode modules.

The following testing practices are kept:

* Unit tests should be kept relatively small where possible (i.e., they should
  test "a single unit of code.")
* All assertions are provided a message to indicate in plain English what
  failed, should the assertion fail
* All unit tests must provide at least a short docstring to summarize what the
  test tests.
* All test modules must provide at least a short docstring to summarize the
  overall topic of the tests contained.
* PyLint messages may be ignored at the module level, if needed.  Justification
  must be provided in a code comment near to the pylint disable flag.  (This is
  NOT a freebie to write bad code -- only ignore messages that are truly
  unavoidable.  W0212 is a common offender.)

For convenience and code cleanliness, test authors may wish to familiarize
themselves with the :py:mod:`tests.conftest` module.  This module contains
PyTest fixtures available to all test modules (automatically, no import
needed!).  Commonly-used graph constructors can be found here.  See the module
documentation for more info.

Test List
---------

You can find an API-like summary & description of all unit tests here:

.. autosummary::
   :toctree: _autosummary_tests
   :template: custom-mod-template.rst
   :recursive:

   tests

.. _PyTest: https://docs.pytest.org/en/latest/contents.html
.. _Coverage.py: https://coverage.readthedocs.io/en/latest/
.. _pytest-cov: https://pytest-cov.readthedocs.io/en/latest/index.html
.. _pytest-randomly: https://github.com/pytest-dev/pytest-randomly

