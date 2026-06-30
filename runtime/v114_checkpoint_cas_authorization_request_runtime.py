#!/usr/bin/env python3
import unittest

from runtime.v113_checkpoint_cas_coherence_runtime import run_v113
from tests.test_kuuos_repository_checkpoint_cas_authorization_request_v1_14 import (
    RepositoryCheckpointCasAuthorizationRequestV114Tests,
)


def run_v114() -> int:
    if run_v113() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointCasAuthorizationRequestV114Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
