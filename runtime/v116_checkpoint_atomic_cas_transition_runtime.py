#!/usr/bin/env python3
import unittest

from runtime.v115_checkpoint_cas_authorization_decision_runtime import run_v115
from tests.test_kuuos_repository_checkpoint_atomic_cas_transition_v1_16 import (
    RepositoryCheckpointAtomicCasTransitionV116Tests,
)


def run_v116() -> int:
    if run_v115() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointAtomicCasTransitionV116Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
