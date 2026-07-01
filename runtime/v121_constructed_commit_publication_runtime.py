#!/usr/bin/env python3
import unittest

from runtime.v120_tree_commit_runtime import run_v120

TEST_MODULES = (
    "tests.test_kuuos_repository_constructed_commit_publication_v1_21",
    "tests.test_kuuos_repository_constructed_commit_publication_guards_v1_21",
    "tests.test_kuuos_repository_constructed_commit_publication_accounting_v1_21",
)


def run_v121() -> int:
    prior_status = run_v120()
    if prior_status:
        return prior_status
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if outcome.wasSuccessful() else 1
