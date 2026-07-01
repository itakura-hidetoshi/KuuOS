#!/usr/bin/env python3
import unittest

from runtime.v116_checkpoint_atomic_cas_transition_runtime import run_v116
from tests.test_kuuos_repository_checkpoint_live_git_preflight_v1_17 import (
    RepositoryCheckpointLiveGitPreflightV117Tests,
)


def run_v117() -> int:
    if run_v116() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCheckpointLiveGitPreflightV117Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
