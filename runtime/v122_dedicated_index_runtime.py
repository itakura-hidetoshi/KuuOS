#!/usr/bin/env python3
import unittest

from runtime.v121_constructed_commit_publication_runtime import run_v121
from tests.test_kuuos_repository_dedicated_index_accounting_v1_22 import RepositoryDedicatedIndexAccountingV122Tests
from tests.test_kuuos_repository_dedicated_index_guards_v1_22 import RepositoryDedicatedIndexGuardsV122Tests
from tests.test_kuuos_repository_dedicated_index_v1_22 import RepositoryDedicatedIndexV122Tests


def run_v122() -> int:
    if run_v121() != 0:
        return 1
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for case in (
        RepositoryDedicatedIndexV122Tests,
        RepositoryDedicatedIndexGuardsV122Tests,
        RepositoryDedicatedIndexAccountingV122Tests,
    ):
        suite.addTests(loader.loadTestsFromTestCase(case))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
