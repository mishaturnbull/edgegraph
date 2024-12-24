# EdgeGraph

EdgeGraph is an object-oriented approach to network graphs.  It provides
classes to inherit from in other applications / modules, and provides
out-of-the-box operations for these classes and any subclasses of.

The intent of EdgeGraph is to allow applications to model related data with a
method closer to reality, without having to implement a custom graph module.
It provides facilities to this end, such as the base classes to allow linking
and the functions to perform it.

The base classes are also usable directly, should you wish to test-drive this
idea or study abstract graphs.

See [the docs][1] for more!

## Beta

At this time, this project is still rather young.  Per [semantic
versioning][0], it is in version 0.  This means that the API may be changed at
any time, without warning.

Planned features include can be viewed at the [features list milestone][2].

These features, as with the API, may be changed or dropped at any time without
warning.  I do have a day job, after all :)

Sphinx documentation and full Pytest-driven unit testing coverage is expected
to match the progress of the code.

## Installation and quickstart

Edgegraph can be installed via pip with `pip install edgegraph`.

A few optional dependencies are available:

* `pip install edgegraph[foreign]` for all the other libraries that edgegraph
  can interact with
* `pip install edgegraph[full]` to install all the above (at the time of
  writing, only the one.  But, this "metapackage" exists for future-proofing)

You can start right out building graphs:

```python
from edgegraph.builder import randgraph
from edgegraph.traversal import breadthfirst

uni = randgraph.randgraph(count=10)
print(breadthfirst.bft(uni, uni.vertices[0]))
```

[0]: https://semver.org
[1]: https://edgegraph.readthedocs.io/en/latest/index.html
[2]: https://github.com/mishaturnbull/edgegraph/milestone/2

