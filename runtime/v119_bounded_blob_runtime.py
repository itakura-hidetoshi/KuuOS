#!/usr/bin/env python3
import unittest

from runtime.v118_checkpoint_live_ref_cas_runtime import run_v118
from tests.test_kuuos_repository_bounded_blob_v1_19 import (
    RepositoryBoundedBlobV119Tests,
)


def run_v119() -> int:
    if run_v118() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryBoundedBlobV119Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
