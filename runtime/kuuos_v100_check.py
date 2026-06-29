#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_v099_check import main as run_previous_frontier
from scripts.check_kuuos_live_v100 import main as check_live_contract
from tests.test_kuuos_repository_local_frontier_finality_v1_00 import (
    RepositoryLocalFrontierFinalityV100Tests,
)


def main() -> int:
    if check_live_contract() != 0:
        return 1
    if run_previous_frontier() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryLocalFrontierFinalityV100Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
