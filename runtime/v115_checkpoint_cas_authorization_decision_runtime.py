#!/usr/bin/env python3
import unittest

from runtime.v114_checkpoint_cas_authorization_request_runtime import run_v114
from tests.test_kuuos_repository_checkpoint_cas_authorization_decision_v1_15 import (
    RepositoryCheckpointCasAuthorizationDecisionV115Tests,
)


def run_v115() -> int:
    if run_v114() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointCasAuthorizationDecisionV115Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
