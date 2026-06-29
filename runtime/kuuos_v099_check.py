#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_v098_check import main as run_previous_frontier
from scripts.check_kuuos_live_v099 import main as check_live_contract
from tests.test_kuuos_repository_reference_stability_v0_99 import (
    RepositoryReferenceStabilityV099Tests,
)


def main() -> int:
    if check_live_contract() != 0:
        return 1
    if run_previous_frontier() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryReferenceStabilityV099Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
