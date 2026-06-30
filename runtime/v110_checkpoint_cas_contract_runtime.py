#!/usr/bin/env python3
import unittest

from runtime.v109_checkpoint_candidate_runtime import run_v109
from tests.test_kuuos_repository_checkpoint_cas_contract_v1_10 import (
    RepositoryCheckpointCasContractV110Tests,
)


def run_v110() -> int:
    if run_v109() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointCasContractV110Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
