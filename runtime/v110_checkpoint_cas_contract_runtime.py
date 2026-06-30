#!/usr/bin/env python3
import unittest

from tests.test_kuuos_repository_checkpoint_cas_contract_v1_10 import (
    RepositoryCheckpointCasContractV110Tests,
)


def run_v110() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointCasContractV110Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
