#!/usr/bin/env python3
import unittest

from runtime.v123_sandbox_worktree_runtime import run_v123
from tests.test_kuuos_repository_checkpoint_reflog_accounting_v1_24 import (
    RepositoryCheckpointReflogAccountingV124Tests,
)
from tests.test_kuuos_repository_checkpoint_reflog_guards_v1_24 import (
    RepositoryCheckpointReflogGuardsV124Tests,
)
from tests.test_kuuos_repository_checkpoint_reflog_v1_24 import (
    RepositoryCheckpointReflogV124Tests,
)


def run_v124() -> int:
    if run_v123() != 0:
        return 1
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for case in (
        RepositoryCheckpointReflogV124Tests,
        RepositoryCheckpointReflogGuardsV124Tests,
        RepositoryCheckpointReflogAccountingV124Tests,
    ):
        suite.addTests(loader.loadTestsFromTestCase(case))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
