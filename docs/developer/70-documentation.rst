.. _dev/docs:

Documentation practices
=======================

EdgeGraph follows a strict rule of 100% documentation-of-code coverage, plus
any necessary narrative documentation.  `Sphinx`_ is used to build
documentation, which is hosted on `ReadTheDocs`_.  GitHub Actions deploys
documentation builds automatically.

Documentation of code is kept as close to the code as possible -- in Python
docstrings for the relevant modules, classes, and functions.  These are written
in reStructuredText format, with Sphinx extensions available.  Narrative
documentation (along with docs configuration and indexing) is kept in the
:file:`docs/` folder.

Building documentation
----------------------

Documentation can be built locally using the Sphinx makefile in the
:file:`docs/` folder.  Simply run :samp:`make clean html` to view docs locally.
Output will be placed in :file:`docs/_build/`.

.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _ReadTheDocs: https://about.readthedocs.com/

