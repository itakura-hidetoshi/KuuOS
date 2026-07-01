#!/usr/bin/env python3
import unittest

from runtime.v122_dedicated_index_runtime import run_v122
from tests.test_kuuos_repository_sandbox_worktree_accounting_v1_23 import (
    RepositorySandboxWorktreeAccountingV123Tests,
)
from tests.test_kuuos_repository_sandbox_worktree_guards_v1_23 import (
    RepositorySandboxWorktreeGuardsV123Tests,
)
from tests.test_kuuos_repository_sandbox_worktree_v1_23 import (
    RepositorySandboxWorktreeV123Tests,
)


def run_v123() -> int:
    if run_v122() != 0:
        return 1
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for case in (
        RepositorySandboxWorktreeV123Tests,
        RepositorySandboxWorktreeGuardsV123Tests,
        RepositorySandboxWorktreeAccountingV123Tests,
    ):
        suite.addTests(loader.loadTestsFromTestCase(case))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
