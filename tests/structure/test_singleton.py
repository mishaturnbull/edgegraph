#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Unit tests for structure.singleton metaclasses.

This'll be fun!!
"""

import pytest

from edgegraph.structure import singleton

# this module is all about testing with classes.  the classes we define in this
# file are never exposed to users of edgegraph, nor any of the edgegraph
# module, therefore don't need:
# * any use-case besides their sole existence,
#   * sufficient public methods (R0903, too-few-public-methods)
# * docstrings (C0115, missing-class-docstring),
# * amazing formatting
#   * class Something: pass  will be allowed (C0321, multiple-statements)
#
# therefore:
# pylint: disable=R0903, C0115, C0321

def test_true_singleton_smoketest():
    """
    Quick it's-still-in-dev smoketest for true singletons.
    """

    class Counter(object):
        a = 0
        b = 0

    class A(object):
        def __init__(self, *args):
            Counter.a += 1

    class B(metaclass=singleton.TrueSingleton):
        def __init__(self, *args):
            Counter.b += 1

    a1 = A()
    a2 = A()

    assert a1 is not a2, "Regular objects are returning the same instance!!"
    assert Counter.a == 2, "Regular objects not calling __init__!"

    b1 = B()
    b2 = B()

    assert b1 is b2, "TrueSingleton didn't work!"
    assert Counter.b == 1, "TrueSingleton re-called __init__!"

def test_semi_singleton_smoketest():
    """
    Quick it's-still-in-dev smoketest for semisingletons.
    """
    class Counter(object):
        c = 0

    class C(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            Counter.c += 1

    c1 = C()
    c2 = C()

    assert c1 is c2, "SemiSingleton failed with zero args!"
    assert Counter.c == 1, "SemiSingleton re-called __init__!"

    Counter.c = 0
    c3 = C(1, 2, 3)
    c4 = C(1, 2, 3)
    c5 = C(3, 2, 1)

    assert c3 is c4, "SemiSingleton failed with *args!"
    assert c4 is not c5, "SemiSingleton failed with re-ordered *args!"
    assert Counter.c == 2, "SemiSingleton called init wrong # of times!"

    Counter.c = 0
    c6 = C(i=4, j=5)
    c7 = C(j=5, i=4)
    c8 = C(i=5, j=4)

    assert c6 is c7, "SemiSingleton failed with **kwargs (order)!"
    assert c7 is not c8, "SemiSingleton failed with different kwargs!"
    assert Counter.c == 2, "SemiSingleton called init wrong # of times!"

def test_true_singleton_arg_patterns():
    """
    Exercise TrueSingleton's response to class argument patterns.
    """

    class NoArgs(metaclass=singleton.TrueSingleton):
        def __init__(self):
            pass

    class PosArgs(metaclass=singleton.TrueSingleton):
        def __init__(self, *args):
            self.args = args

    class KwArgs(metaclass=singleton.TrueSingleton):
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class BothArgs(metaclass=singleton.TrueSingleton):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    n1 = NoArgs()
    n2 = NoArgs()
    assert n1 is n2, "TrueSingleton failed no-args"

    p1 = PosArgs(1, 2, 3, 4, 5)
    p2 = PosArgs(5, 4, 3, 2, 1, 8, 2, 17)
    assert p1 is p2, "TrueSingleton reassigned with new args"
    assert p2.args == (1, 2, 3, 4, 5), "TrueSingleton re-assigned arguments"

    k1 = KwArgs(i=1, j=2)
    k2 = KwArgs(i=17, j=-1, t=True)
    assert k1 is k2, "TrueSingleton reassigned with new kwargs"
    assert k2.kwargs == {'i': 1, 'j': 2}, "TrueSingleton re-assigned arguments"

    b1 = BothArgs(1, 2, i=1)
    b2 = BothArgs(4, 5, j=3)
    assert b1 is b2, "TrueSingleton reassigned with new args"
    assert b2.args == (1, 2), "TrueSingleton re-assigned arguments"
    assert b2.kwargs == {'i': 1}, "TrueSingleton re-assigned kwargs"

def test_semi_singleton_noarg_default_hashfunc():
    """
    Exercise semi-singleton's response to no-argument classes using default
    hashfunc.
    """

    class NoArgs(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self):
            pass

    n1 = NoArgs()
    n2 = NoArgs()
    assert n1 is n2, "SemiSingleton failed no-args"

def test_semi_singleton_args_pattern_default_hashfunc():
    """
    Exercise semi-singleton's response to ``*args`` pattern using default
    hashfunc.
    """

    class PosArgs(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self, *args):
            self.args = args

    p1 = PosArgs(1)
    p2 = PosArgs(1)
    p3 = PosArgs(2)
    p4 = PosArgs(1, 2, 3)
    p5 = PosArgs(1, 2, 3)
    p6 = PosArgs(3, 2, 1)
    assert p1 is p2, "SemiSingleton failed same pos-arg"
    assert p2 is not p3, "SemiSingleton failed different pos-arg"
    assert p4 is p5, "SemiSingleton failed same multiple pos-arg"
    assert p5 is not p6, "SemiSingleton failed different multiple pos-arg"

def test_semi_singleton_kwargs_patterns_default_hashfunc():
    """
    Exercise semi-singleton's response to ``**kwargs`` pattern using default
    hashfunc.
    """

    class KwArgs(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    k1 = KwArgs(i=1)
    k2 = KwArgs(i=1)
    k3 = KwArgs(i=2)
    k4 = KwArgs(i=3, j=4)
    k5 = KwArgs(j=4, i=3)
    k6 = KwArgs(i=4, j=3)
    assert k1 is k2, "SemiSingleton failed same kw-arg"
    assert k2 is not k3, "SemiSingleton failed different kw-arg"
    assert k4 is k5, "SemiSingleton failed same (reordered) kw-arg"
    assert k5 is not k6, "SemiSingleton failed different kw-arg"

def test_semi_singleton_bothargs_patterns_default_hashfunc():
    """
    Exercise semi-singleton's response to ``*args, **kwargs`` pattern using
    default hashfunc.
    """

    class BothArgs(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    b1 = BothArgs(1, 2, i=3)
    b2 = BothArgs(1, 2, i=3)
    b3 = BothArgs(3, 4, i=3)
    b4 = BothArgs(1, 2, i=4)
    b5 = BothArgs(1, 2)
    b6 = BothArgs(1, 2)
    b7 = BothArgs(i=3)
    b8 = BothArgs(i=3)
    assert b1 is b2, "Failed same both-arg"
    assert b2 is not b3, "Failed different both-arg"
    assert b3 is not b4, "Failed different pos-arg"
    assert b4 is not b5, "Failed missing kw-arg"
    assert b5 is b6, "Failed same pos-arg"
    assert b6 is not b7, "Failed pos- vs kw-arg"
    assert b7 is b8, "Failed same kw-arg"

def test_semi_singleton_custom_hashfunc():
    """
    Exercise usage of custom hashfuncs for semi-singleton identification.
    """
    # W0612 --> unused variable.  pylint complains that ign_kw is unused; it
    #           most certainly is used.  not sure why this is flagged.
    # W0613 --> unused argument.  necessary here for signature matching.
    # pylint: disable-next=W0612, W0613
    def ign_kw(args, kwargs):
        return hash(args)

    class PosOnlyArgs(metaclass=singleton.semi_singleton_metaclass(ign_kw)):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    po1 = PosOnlyArgs(1, 2, 3)
    po2 = PosOnlyArgs(1, 2, 3)
    po3 = PosOnlyArgs(1, 2, 3, i=4, j=5)
    po4 = PosOnlyArgs(1, 2, 3, i=512, j=False)
    po5 = PosOnlyArgs(4, 5, 6, i=4, j=5)
    po6 = PosOnlyArgs(4, 5, 6, i=512, j=False)
    assert po1 is po2, "Failed same pos-arg"
    assert po2 is po3, "Failed additional kw-arg"
    assert po3 is po4, "Failed different kw-arg"
    assert po4 is not po5, "Failed different pos-arg"
    assert po5 is po6, "Failed different kw-arg"

@pytest.mark.slow
def test_true_singleton_access_stresstest():
    """
    Access a TrueSingleton object *a lot*.
    """
    class Singleton(metaclass=singleton.TrueSingleton):
        pass

    prev = None
    for i in range(1000000):
        s = Singleton()
        if prev:
            assert s is prev, f"Did not get the same object on iter {i}!"
        prev = s

@pytest.mark.slow
def test_true_singleton_create_stresstest():
    """
    Create and access a TrueSingleton object *a lot*.
    """
    prev = None
    for i in range(10000):

        class Singleton(metaclass=singleton.TrueSingleton):
            pass

        s1 = Singleton()
        s2 = Singleton()
        assert s1 is s2, f"Failed singleton on iter {i}!"

        if prev:
            # this looks a little weird, that we're not getting the same
            # singleton object every loop (after all, what else is the point of
            # a singleton??).  it works, though, because we make *an entirely
            # new class* every loop, not just an instance of it.
            assert s1 is not prev, "Object not recreated after loop!"
        prev = s1

@pytest.mark.slow
def test_semi_singleton_access_stresstest():
    """
    Access a semi-singleton *a lot*.
    """
    class SemiSingleton(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self, *args):
            self.args = args

    prev = None
    for i in range(1000000):
        s = SemiSingleton(1, 2, 3)
        if prev:
            assert s is prev, f"Did not get the same object on iter {i}!"
        prev = s

@pytest.mark.slow
def test_semi_singleton_create_stresstest():
    """
    Create and access a semi-singleton object *a lot*.
    """
    prev = None
    for i in range(10000):

        class SemiSingleton(metaclass=singleton.semi_singleton_metaclass()):
            def __init__(self, *args):
                self.args = args

        s1 = SemiSingleton(1, 2, 3)
        s2 = SemiSingleton(1, 2, 3)
        assert s1 is s2, f"Failed semi-singleton on iter {i}!"

        if prev:
            # again, this looks a little weird -- but the same reason as the
            # truesingleton version of this test; we make a new *class* every
            # loop, not just an instance of it.
            assert s1 is not prev, "Object not recreated after loop!"
        prev = s1

def test_true_singleton_clear():
    """
    Ensure TrueSingletons can all be cleared.
    """
    class A(metaclass=singleton.TrueSingleton): pass
    class B(metaclass=singleton.TrueSingleton): pass
    class C(metaclass=singleton.TrueSingleton): pass

    a1 = A()
    b1 = B()
    c1 = C()

    singleton.clear_true_singleton()

    a2 = A()
    b2 = B()
    c2 = C()

    assert a1 is not a2, "Did not clear-all TrueSingletons"
    assert b1 is not b2, "Did not clear-all TrueSingletons"
    assert c1 is not c2, "Did not clear-all TrueSingletons"

def test_true_singleton_clear_specific():
    """
    Ensure TrueSingletons can be cleared individually.
    """
    class A(metaclass=singleton.TrueSingleton): pass
    class B(metaclass=singleton.TrueSingleton): pass
    class C(metaclass=singleton.TrueSingleton): pass

    a1 = A()
    b1 = B()
    c1 = C()

    singleton.clear_true_singleton(B)

    a2 = A()
    b2 = B()
    c2 = C()

    assert a1 is a2, "Cleared all TrueSingletons instead of only B"
    assert b1 is not b2, "Did not clear right TrueSingleton"
    assert c1 is c2, "Cleared all TrueSingletons instead of only B"

def test_true_singleton_clear_specific_not_present():
    """
    Ensure calling clear on an un-set singleton is safe.
    """
    class A(metaclass=singleton.TrueSingleton): pass

    singleton.clear_true_singleton(A)

    a1 = A()
    a2 = A()
    assert a1 is a2, "Clearing empty singleton broke singletons!"

def test_semi_singleton_clear():
    """
    Ensure semi-singletons can be cleared.
    """

    class A(metaclass=singleton.semi_singleton_metaclass()): pass
    class B(metaclass=singleton.semi_singleton_metaclass()): pass
    class C(metaclass=singleton.semi_singleton_metaclass()): pass

    a1 = A()
    b1 = B()
    c1 = C()

    singleton.clear_semi_singleton(B)

    a2 = A()
    b2 = B()
    c2 = C()

    assert a1 is a2, "Cleared wrong semi-singleton type!"
    assert b1 is not b2, "Did not clear semi-singleton!"
    assert c1 is c2, "Cleared wrong semi-singleton type!"

def test_semi_singleton_get():
    """
    Ensure we can get all the values of semi-singletons.
    """
    class SemiSingle(metaclass=singleton.semi_singleton_metaclass()):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    insts = [SemiSingle(i) for i in range(10)]

    check = singleton.get_all_semi_singleton_instances(SemiSingle)

    assert set(insts) == set(check), \
            "Did not get expected semi-singleton insts!"


