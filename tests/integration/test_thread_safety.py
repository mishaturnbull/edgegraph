# -*- coding: utf-8 -*-

"""
Ensure graph operations are thread-safe.
"""

import os
import sys
import threading
import time
from concurrent import futures

import pytest

from edgegraph.builder import explicit
from edgegraph.structure import BaseObject, DirectedEdge, Universe
from edgegraph.traversal import breadthfirst, depthfirst, helpers

travs = [
    depthfirst.dft_recursive,
    depthfirst.dft_iterative,
    breadthfirst.bft,
]

if sys.version_info >= (3, 13):
    N_WORKERS = min(32, (os.process_cpu_count() or 1) + 4)
else:
    N_WORKERS = min(32, len(os.sched_getaffinity(0)))
NANO = 1_000_000_000


def barricaded_call(barrier, func, *args, **kwargs):
    """
    Simple wrapper around a barricaded function call.
    """
    barrier.wait()
    return func(*args, **kwargs)


def routine_cft(graph_clrs09_22_6, trav, singlethread_answer):
    """
    Test routine for concurrent-futures-trav tests.  Isolated into its own
    function for easier variability in how many times this routine is run per
    unit test.
    """
    uni, verts = graph_clrs09_22_6
    all_futures = []

    with futures.ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
        # use a barrier to ensure all threads are started at the same time
        # -- increase concurrent accesses
        barrier = threading.Barrier(N_WORKERS)

        for _ in range(N_WORKERS):
            future = executor.submit(
                barricaded_call, barrier, trav, uni, verts[0]
            )
            all_futures.append(future)

        for future in futures.as_completed(all_futures):
            data = future.result()
            assert data == singlethread_answer, (
                "Did not get the same answer as single-threaded run!"
            )


@pytest.mark.timeout(10)
@pytest.mark.parametrize("trav", travs)
def test_concurrent_futures_trav_fast(graph_clrs09_22_6, trav):
    """
    Ensure reading from a graph is safe across many threads concurrently for 5
    seconds.

    Creates a graph, then tries to traverse it in a multi-threaded manner many
    times to induce any simultaneous-access issues.
    """
    uni, verts = graph_clrs09_22_6
    singlethread_answer = trav(uni, verts[0])
    t_start = time.monotonic_ns()

    while time.monotonic_ns() - t_start < 5 * NANO:
        routine_cft(graph_clrs09_22_6, trav, singlethread_answer)


@pytest.mark.slow
@pytest.mark.parametrize("trav", travs)
def test_concurrent_futures_trav_slow(graph_clrs09_22_6, trav):
    """
    Ensure reading from a graph is safe across many threads concurrently, 512
    times.

    Creates a graph, then tries to traverse it in a multi-threaded manner many
    times to induce any simultaneous-access issues.
    """
    uni, verts = graph_clrs09_22_6

    n_tries = 512
    singlethread_answer = trav(uni, verts[0])

    for _ in range(n_tries):
        routine_cft(graph_clrs09_22_6, trav, singlethread_answer)


def routine_cfb(graph_clrs09_22_6):
    """
    Test routine for concurrent-futures-build tests.  Isolated into its own
    function for easier variability in how many times this routine is run per
    unit test.
    """
    _, verts = graph_clrs09_22_6

    def proc(barrier):
        barrier.wait()
        explicit.link_from_to(verts[0], DirectedEdge, verts[1])
        helpers.neighbors(verts[0])
        assert verts[1] in helpers.neighbors(verts[0])

    all_futures = []

    with futures.ThreadPoolExecutor(max_workers=N_WORKERS * 2) as executor:
        # use a barrier to ensure all threads are started at the same time
        # -- increase concurrent accesses
        barrier = threading.Barrier(N_WORKERS * 2)

        for _ in range(N_WORKERS * 2):
            future = executor.submit(proc, barrier)
            all_futures.append(future)

        links = []
        for future in futures.as_completed(all_futures):
            data = future.result()
            links.append(data)

    assert len(links) == N_WORKERS * 2, (
        "Did not create correct amount of links!"
    )


@pytest.mark.timeout(10)
def test_concurrent_futures_build_fast(graph_clrs09_22_6):
    """
    Ensure writing to a graph is safe across many threads concurrently for 5
    seconds.
    """
    t_start = time.monotonic_ns()
    while time.monotonic_ns() - t_start < 5 * NANO:
        routine_cfb(graph_clrs09_22_6)


@pytest.mark.slow
def test_concurrent_futures_build_slow(graph_clrs09_22_6):
    """
    Ensure writing to a graph is safe across many threads concurrently 128
    times.
    """
    n_tries = 128
    for _ in range(n_tries):
        routine_cfb(graph_clrs09_22_6)


def routine_universes():
    """
    Test routine for baseobject-in-universe thread safety.
    """
    uni = Universe()
    bos = [BaseObject()] * 32

    def proc_add(barrier_add, uni, bos):
        barrier_add.wait()
        for bo in bos:
            bo.add_to_universe(uni)

    def proc_rem(barrier_rem, uni, bos):
        barrier_rem.wait()
        for bo in bos:
            bo.remove_from_universe(uni)

    all_futures = []

    with futures.ThreadPoolExecutor(max_workers=N_WORKERS * 2) as executor:
        barrier_add = threading.Barrier(N_WORKERS * 2)
        barrier_rem = threading.Barrier(N_WORKERS * 2)

        for _ in range(N_WORKERS * 2):
            future = executor.submit(proc_add, barrier_add, uni, bos)
            all_futures.append(future)

        for future in futures.as_completed(all_futures):
            future.result()

        for bo in bos:
            assert bo.universes == [uni], "Did not add correctly!"

        all_futures = []
        for _ in range(N_WORKERS * 2):
            future = executor.submit(proc_rem, barrier_rem, uni, bos)
            all_futures.append(future)

        for future in futures.as_completed(all_futures):
            future.result()

    for bo in bos:
        assert bo.universes == [], "Wrong universes!"


@pytest.mark.timeout(10)
def test_concurrent_futures_universe_fast():
    """
    Ensure BaseObject and Universe linkages are handled in a thread-safe
    manner, concurreently for 5 seconds (this is the fast version of the test).
    """
    t_start = time.monotonic_ns()
    while time.monotonic_ns() - t_start < 5 * NANO:
        routine_universes()


@pytest.mark.slow
def test_concurrent_futures_universe_slow():
    """
    Ensure BaseObject and Universe linkages are safe across many threads
    concurrently; test runs 128 times.
    """
    n_tries = 128
    for _ in range(n_tries):
        routine_universes()
