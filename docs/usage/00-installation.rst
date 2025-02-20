.. _install:

Installation
============

Installation of EdgeGraph is rather simple via Pip:

:samp:`$ pip install edgegraph`

Details of the Pip package can be found on Pip at
https://pypi.org/project/edgegraph/ .

.. _install/extras:

Extras
------

Edgegraph's pip definition contains some optional extra components:

* :samp:`$ pip install edgegraph[foreign]` for all the foreign Python modules
  edgegraph can interface with
* :samp:`$ pip install edgegraph[full]` for all the above options
* :samp:`$ pip install edgegraph[development]` for the full devops packages
  needed to develop, test, document, build, and publish edgegraph itself (this
  includes `edgegraph[full]`)

.. _versioning:

Versioning
----------

Edgegraph follows a subset of semantic versioning that is compatible with
PyPI's version specification.  Version numbers are formatted as ``X.Y.Z``,
where:

* ``X`` is the "major" version number, incrementing when backwards-incompatible
  changes are made
* ``Y`` is the "minor" version number, incrementing when backwards-compatible
  new features are added
* ``Z`` is the "patch" version number, incrementing when minute changes and/or
  bugfix-only changes are made

.. seealso::

   * https://semver.org , the Semantic Versioning standard
   * https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers ,
     the PyPI version specification

To maintain easy compatibility between these version standards, SemVer
pre-release or build metadata are not used.

Development versions
--------------------

EdgeGraph can also be "installed" by cloning the repository and adding it to
your Python module path (though, be sure to add the ``edgegraph`` folder within
the repo, and not the repo itself).  You may check out any of the branches you
wish, though note that only the ``master`` branch is *guaranteed* to be stable
at any given moment.

You can also use Pip's repository installation:

:samp:`$ pip install git+https://github.com/mishaturnbull/edgegraph@{branch}`

The repository is tagged for each versioned release; the tag names are the
version prefixed with a ``v``.  For example, ``v0.2.0`` is the tag name for
version ``0.2.0``.

.. seealso::

   More information about branches can be found here: :ref:`dev/vcs`.

