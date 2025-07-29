# -*- coding: utf-8 -*-

"""
Ensure graph operations are thread-safe.
"""

from concurrent import futures
import os
import threading
import time

import pytest

from edgegraph.traversal import helpers, breadthfirst, depthfirst, breadthfirst
from edgegraph.structure import DirectedEdge
from edgegraph.builder import explicit

travs = [
    depthfirst.dft_recursive,
    depthfirst.dft_iterative,
    breadthfirst.bft,
]

N_WORKERS = min(32, (os.process_cpu_count() or 1) + 4)
NANO = 1_000_000_000


def barricaded_call(barrier, func, *args, **kwargs):
    """
    Simple wrapper around a barricaded function call.
    """
    barrier.wait()
    return func(*args, **kwargs)

def routine_cft(graph_clrs09_22_6, trav, singlethread_answer):
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
            try:
                data = future.result()
            except Exception as exc:
                raise exc
            else:
                assert data == singlethread_answer, (
                    "Did not get the same answer as single-threaded run!"
                )

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
    uni, verts = graph_clrs09_22_6

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
            try:
                data = future.result()
            except Exception as exc:
                raise exc
            else:
                links.append(data)

    assert len(links) == N_WORKERS * 2, (
        "Did not create correct amount of links!"
    )

def test_concurrent_futures_build_fast(graph_clrs09_22_6):
    """
    Ensure writing to a graph is safe across many threads concurrently for 5
    seconds.
    """
    uni, verts = graph_clrs09_22_6
    t_start = time.monotonic_ns()
    while time.monotonic_ns() - t_start < 5 * NANO:
        routine_cfb(graph_clrs09_22_6)

@pytest.mark.slow
def test_concurrent_futures_build_slow(graph_clrs09_22_6):
    """
    Ensure writing to a graph is safe across many threads concurrently 128
    times.
    """
    uni, verts = graph_clrs09_22_6
    n_tries = 128
    for _ in range(n_tries):
        routine_cfb(graph_clrs09_22_6)
