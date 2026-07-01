#!/usr/bin/env python3
import unittest

from runtime.v117_checkpoint_live_git_preflight_runtime import run_v117
from tests.test_kuuos_repository_checkpoint_live_ref_cas_v1_18 import (
    RepositoryCheckpointLiveRefCasV118Tests,
)


def run_v118() -> int:
    if run_v117() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointLiveRefCasV118Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
