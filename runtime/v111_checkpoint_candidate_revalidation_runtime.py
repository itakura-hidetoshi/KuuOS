#!/usr/bin/env python3
import unittest

from tests.test_kuuos_repository_checkpoint_candidate_revalidation_v1_11 import (
    RepositoryCheckpointCandidateRevalidationV111Tests,
)


def run_v111() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointCandidateRevalidationV111Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
