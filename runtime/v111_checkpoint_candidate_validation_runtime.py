#!/usr/bin/env python3
import unittest

from runtime.v110_checkpoint_cas_contract_runtime import run_v110
from tests.test_kuuos_checkpoint_candidate_validation_v1_11 import (
    CheckpointCandidateValidationV111Tests,
)


def run_v111() -> int:
    if run_v110() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        CheckpointCandidateValidationV111Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
