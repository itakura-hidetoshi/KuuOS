#!/usr/bin/env python3
import unittest

from runtime.v112_checkpoint_validated_cas_intake_runtime import run_v112
from tests.test_kuuos_repository_checkpoint_cas_coherence_v1_13 import RepositoryCheckpointCasCoherenceV113Tests


def run_v113() -> int:
    if run_v112() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RepositoryCheckpointCasCoherenceV113Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
