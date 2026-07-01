#!/usr/bin/env python3
import unittest

from runtime.v119_bounded_blob_runtime import run_v119


def run_v120() -> int:
    if run_v119() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromNames(
        (
            "tests.test_kuuos_repository_bounded_tree_commit_v1_20",
            "tests.test_kuuos_repository_bounded_tree_commit_guards_v1_20",
        )
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
