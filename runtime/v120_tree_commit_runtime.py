#!/usr/bin/env python3
import unittest
from runtime.v119_bounded_blob_runtime import run_v119

TEST_MODULES = (
    "tests.test_kuuos_repository_tree_commit_v1_20",
    "tests.test_kuuos_repository_tree_commit_guards_v1_20",
    "tests.test_kuuos_repository_tree_commit_accounting_v1_20",
)


def run_v120() -> int:
    prior_status = run_v119()
    if prior_status:
        return prior_status
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if outcome.wasSuccessful() else 1
