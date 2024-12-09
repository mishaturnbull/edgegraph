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
:file:`docs/` folder.  Ensure you have the following prerequisites:

#. PlantUML installed (see https://plantuml.com/ )
#. Pip prerequisites: :samp:`pip install .[development]`

Then, simply run :samp:`make clean html` to build docs locally.  Output will be
placed in :file:`docs/_build/`.  You may also inspect the output of :samp:`make
help` to show additional formats that can be built.

Coverage assessment
^^^^^^^^^^^^^^^^^^^

Documentation-of-code coverage is also assessed by Sphinx, using the coverage
extension.  Though this is run by GitHub Actions against all pull requests, you
may also assess coverage locally by using :samp:`make coverage`.  A file
:file:`_build/coverage/python.txt` will be created; this contains the coverage
table.  Ensure that the bottom row (``TOTAL``) is marked as ``100.00%``.

.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _ReadTheDocs: https://about.readthedocs.com/

