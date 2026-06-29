#!/usr/bin/env python3
from __future__ import annotations

import unittest

from scripts.check_kuuos_live_v096 import main as check_live_contract
from scripts.run_kuuos_runtime_full_check_v0_55 import main as run_previous_frontier
from tests.test_kuuos_repository_reference_update_authorization_v0_96 import (
    RepositoryReferenceUpdateAuthorizationV096Tests,
)


def main() -> int:
    if check_live_contract() != 0:
        return 1
    if run_previous_frontier() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryReferenceUpdateAuthorizationV096Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
