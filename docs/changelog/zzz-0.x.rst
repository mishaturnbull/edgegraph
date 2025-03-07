.. _changelog/0.x:

v0.x
====

This section describes all 0.x.y versions of edgegraph.

.. note::

   This changelog was created after v0.10.0 was released.  Therefore, all
   entries hereafter are written after-the-fact, based on my own memory and the
   Git log.


.. _changelog/0.10.0:

v0.10.0
-------

New features:

#. ``BaseObject.universes`` is now a ``list`` object, maintaining insertion
   order.
#. ``Universe.vertices`` is now a ``list`` object, maintaining insertion order.

Bugfixes / minor changes:

#. Fixed documentation copyright year to state ``2023-x``, where ``x`` is the
   current year at build time
#. Cleaned up the unit tests' :file:`conftest.py`, moving fixtures into their
   own submodule for code cleanliness
#. Added a Sphinx extension to clean up autosummary directories after a build

.. _changelog/0.9.1:

v0.9.1
------

Bugfixes / minor changes:

#. The iterator-wrapped breadth first traversal
   (:py:func:`~edgegraph.traversal.breadthfirst.bft`) no longer returns
   ``None`` when there is no data in the traversal.  This was originally
   intentional, but I think it was a bad choice, and one bad enough to warrant
   a hotfix.

.. _changelog/0.9.0:

v0.9.0
------

New features:

#. Added generator traversal functions that yield lazy iterators (all three
   traversal functions:
   :py:func:`~edgegraph.traversal.depthfirst.idft_iterative`,
   :py:func:`~edgegraph.traversal.depthfirst.idft_recursive`, and
   :py:func:`~edgegraph.traversal.breadthfirst.ibft`)

Bugfixes / minor changes:

#. Various minute code quality, pylint, and documentation typo corrections

.. _changelog/0.8.1:

v0.8.1
------

.. note::

   With version 0.8.1, edgegraph was declared as a BETA project, no longer
   alpha.

Bugfixes / minor changes:

#. Type hinting no longer uses obsoleted ``Optional[x]`` hint; now ``x | None``
#. Community standards documentation
#. Workaround for PlantUML unit tests timing out (``workaround``, not
   ``fix``...)
#. Workaround for Python 3.7 unavailable on Ubuntu 24.04 in GitHub actions
   pipeline
#. Minor improvements to README

.. _changelog/0.8.0:

v0.8.0
------

New features:

#. Added :ref:`vertex neighbor caching <dev/performance/vert-nb-cache>`
#. Type-hinted the entire library
#. Added optional dependency specifiers: ``edgegraph[foreign]``,
   ``edgegraph[full]``

Bugfixes / minor changes:

#. Type-checker is now run on all pull requests in CI pipeline
#. PyPI upload script was improved with multiple pre-upload checks

.. _changelog/0.7.0:

v0.7.0
------

New features:

#. Added the
   :py:func:`~edgegraph.structure.singleton.drop_semi_singleton_mapping` and
   :py:func:`~edgegraph.structure.singleton.check_semi_singleton_entry_exists`
   utility functions
#. Change call signature of
   :py:func:`~edgegraph.structure.singleton.add_mapping` ( **WARNING: Breaks
   backwards compatibility!** )

.. _changelog/0.6.0:

v0.6.0
------

New features:

#. Backwards traversal options for both depth- and breadth-first traversals
#. Improved during-traversal filtering options for the same
#. Added graph deconstruction utilities (link removal, vertex removal from
   universe, etc)
#. Allow semi-singleton objects to have multiple mappings

Bugfixes / minor changes:

#. PyVIS output now uses local JS library instead of CDN resources by default

.. _changelog/0.5.0:

v0.5.0
------

This update is primarily a performance boost, at the cost of some of the
flexibility in object attribute assignments.  *Most* of this shouldn't affect
*most* users, so long as they aren't using the dict-like interfaces of the
structure.

New features:

#. Greatly improved overall performance

Removed:

#. :py:class:`~edgegraph.structure.base.BaseObject` no longer maintains an
   internal, separate, ``__dict__``-like mapping of custom attributes, instead
   now only offering dict-like attribute access with no special handling of
   ``_`` or ``__``-prefixed names.

.. _changelog.0.4.1:

v0.4.1
------

Bugfixes / minor changes:

#. :py:func:`~edgegraph.output.pyvis.make_pyvis_net` no longer fails if
   vertices link to another vertex outside a given universe.
#. Applies Black code style to all code
#. :py:class:`~edgegraph.structure.vertex.Vertex` objects now add themselves to
   :py:class:`~edgegraph.structure.universe.Universe`\ s correctly

.. _changelog/0.4.0:

v0.4.0
------

.. warning::

   The 0.4.0 release was tagged incorrectly.  If you want v0.4.0, do not ``git
   checkout v0.4.0``; instead, use ``git checkout
   64f57b51f326862e5143b081f45f253d693da122``.  (the ``v0.4.0`` tag actually
   points to the ``v0.3.0`` release)

Bugfixes / minor changes:

#. Improve documentation, catch up on doc to-dos

   #. Run documentation coverage on all PRs (py 3.12 build only) to ensure all
      functions / modules / classes / etc have documentation

#. Minor improvements to the traversal helpers module

.. _changelog/0.3.0:

v0.3.0
------

.. note::

   With version 0.3.0, the project was declared as an ALPHA project, no longer
   prealpha.

New features:

#. Added PyVIS output capability
#. Added utilities for working with singletons and semi-singletons
#. Greatly improved unit testing (code quality, documentation, quantity, and
   quality)
#. Support for Python 3.7

Bugfixes / minor changes:

#. Added an option in the explicit builder to not duplicate a link

.. _changelog/0.2.0:

v0.2.0
------

New features:

#. Added depth-first traversal and search functions
#. Added PlantUML output generator
#. Added a plain ASCII output generator

.. _changelog/0.1.0:

v0.1.0
------

Version 0.1.0 is the initial code release of edgegraph, which contained the
basic outline of the data model, breadth-first traversal and search functions,
some basic graph builders, as well as the project's infrastructure as a whole
(documentation, unit tests, Pip configuration, and more).

