.. _dev/practices:

Development Practices
=====================

As a project, Edgegraph intends to use the most up-to-date, complete Python
development practices.  This includes :ref:`unit testing <dev/testing>`,
:ref:`documentation <dev/docs>`, and code formatting and quality standards.  It
is expected to perform flawlessly on all supported versions of Python at any
given moment, and if only trivial changes are required to support EOL'd
versions of Python, limited effort may be made to do so.

Formatting
----------

`Black`_ is employed to automatically format code in-place, alongside `pylint`_
for further code quality checks.  Both are automatically invoked during GitHub
Actions runs on pull requests and certain branches; but neither (Black
especially) are configured to automatically commit any changes.  Black *will*
cause the actions run to fail if files are not formatted; the developer is
expected to perform this formatting locally before pushing code.  Pylint checks
are provided for information only, and do not have a failure threshold --
however, the maintainer of Edgegraph reserves the right to reject pull requests
if they are sufficiently detrimental in the pylint scorecard :)

You can run these checks locally on your machine with the following invocations:

* :samp:`black --check edgegraph tests docs` to *only check*, without applying
  any edits, which files (if any) Black will want formatted.
* :samp:`black edgegraph tests docs` to *apply* Black formatting changes.
* :samp:`pylint edgegraph tests` to check Pylint results

.. _dev/vcs:

Version Control
---------------

Git provides version control for the Edgegraph project, and GitHub is the
primary collaboration point.  Core maintainers (should there ever be more than
one...) are expected to follow the `Git Flow`_ model on branching within the
repository with a minor change to the widely accepted model.  Instead of
release branches merging directly into both ``master`` and ``develop``, release
branches are merged into ``master`` which is then in turn merged into
``develop``.  This approach ensures the version number-tagged commit is present
in ``develop``'s history as well as ``master``.

Contributions from anyone are always welcome; please utilize the GitHub Flow
(also sometimes known as the "fork-and-pull") model, targeting pull requests to
the ``develop`` branch.

+-----------------------+-----------------------------------------------------+
| Branch name pattern   | Usage                                               |
+=======================+=====================================================+
| ``master``            | Formally released, tagged, version numbered         |
|                       | releases are here.  This branch is merge commits    |
|                       | only; and only from ``release`` or ``hotfix``       |
|                       | branches.                                           |
+-----------------------+-----------------------------------------------------+
| ``release/v\d.\d.\d`` | Release integration, final quality checks, readme   |
|                       | and documentation finalizations happen here.        |
|                       | Release branches are branched *from* ``develop``    |
|                       | and merge *into* ``master``.                        |
+-----------------------+-----------------------------------------------------+
| ``hotfix/.*``         | Hotfix branches focus, again, on eliminating bugs.  |
|                       | However, it is permissible for hotfix branches to   |
|                       | fix multiple bugs, should it be most sensible.      |
|                       | Unlike ``bugfix`` branches, ``hotfix`` branches     |
|                       | branch from and merge into ``master``; therefore,   |
|                       | they necessitate a patch-level version increment.   |
+-----------------------+-----------------------------------------------------+
| ``develop``           | Long-running feature integration and shakeout.      |
|                       | This branch is also sometimes known as the          |
|                       | "nightly" version, and stability is not guaranteed. |
+-----------------------+-----------------------------------------------------+
| ``bugfix/.*``         | Bugfix branches are focused on eliminating a single |
|                       | bug.  They branch from and merge into develop.      |
+-----------------------+-----------------------------------------------------+
| ``feature/.*``        | Each feature branch is focused on, well, a single   |
|                       | feature.  These branch from and merge into          |
|                       | ``develop``.                                        |
+-----------------------+-----------------------------------------------------+
| ``sandbox/.*``        | Sandbox branches may be used for testing of ideas,  |
|                       | large-scale refactors or changes, what-if analyses, |
|                       | etc..  They are used identically to ``feature``     |
|                       | branches, but with less guarantee of stability or   |
|                       | eventual closure.                                   |
+-----------------------+-----------------------------------------------------+

Release Procedure
-----------------

Every versioned release of Edgegraph is expected to undergo the following
steps.  Some differences are naturally driven by the difference between the
normal release route, and more urgent hotfixes.  Much effort has been given to
automating as much of this process as possible, and such efforts are expected
to continue.  However, some aspects of the release process *should* involve
human intervention and authority; notably, merging of the releasing pull
request and upload to PyPI.

#. A version number is identified.  This number shall increment in accordance
   with :ref:`Edgegraph's versioning standard <versioning>`.
#. Create a new branch from ``develop``, named :samp:`release/v{version
   number}`.  For example, ``release/v0.4.0`` would be correct.
#. Create a new branch:

   #. For normal releases (that is, major and minor releases), branch from
      ``develop``.  The branch name should be of the form ``release/vX.Y.Z``.
   #. For urgent hotfixs (that is, patch releases), branch from ``master``.
      The branch name should be of the form :samp:`hotfix/{issue}`.

#. Update the release number in :file:`edgegraph/version.py` as needed.  This
   is the ONLY place where the version number is kept.
#. Ensure all applicable documentation for new features, bugfixes, etc. is
   created, and all prior existing documentation is updated with any relevant
   changes.  Ensure the :file:`README.md` feature list is up to date.
#. Commit these changes, and push.  GitHub Actions will ensure that all unit
   tests pass, code coverage is at 100%, and documentation build is working.
   Ensure the actual documentation product is as you expect on ReadTheDocs.
#. Open a GitHub pull request into the ``master`` branch.

   #. At this point, the normal peer review cycle takes place, with reviewers
      (hopefully) leaving comments.  GitHub Actions will continue to perform
      its automated checks.

#. Once all reviews are satisfied, merge the pull request.
#. Tag the commit on the master branch with the applicable version number.

   #. On your machine, ensure you pull the latest ``master`` branch.
   #. :samp:`git tag v{X.Y.Z}`
   #. :samp:`git push origin master`

#. Back-merge the release into the master branch.

   #. :samp:`git checkout develop`
   #. :samp:`git merge master`

#. Upload the build to PyPI.

   #. Switch back to the master branch; more specifically the version tagged
      commit (:samp:`git checkout v{X.Y.Z}`).
   #. If the :file:`dist` folder exists, delete it and any of its contents.
   #. Run :samp:`scripts/pypi.sh`

.. _Black: https://black.readthedocs.io/en/stable/
.. _pylint: https://www.pylint.org/
.. _git flow: https://nvie.com/posts/a-successful-git-branching-model/

