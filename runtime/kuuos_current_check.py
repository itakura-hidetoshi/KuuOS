#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.v124_checkpoint_reflog_runtime import run_v124

CURRENT_RUNTIME_ROOT = "runtime/kuuos_current_check.py"
REPOSITORY_MUTATION_ROOT = "runtime/kuuos_v124_check.py"
LIFECYCLE_COMPLETION_TEST = "tests.test_kuuos_lifecycle_completion_v0_36"
LIFECYCLE_FRONTIER = "kuuos_lifecycle_completion_v0_36"


def _run_unittest_module(module_name: str) -> int:
    suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def run_current() -> int:
    repository_status = run_v124()
    if repository_status != 0:
        return repository_status
    return _run_unittest_module(LIFECYCLE_COMPLETION_TEST)


if __name__ == "__main__":
    raise SystemExit(run_current())
