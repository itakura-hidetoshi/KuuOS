#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_v101_check import main as run_previous_frontier
from scripts.check_kuuos_live_v102 import main as check_live_contract
from tests.test_kuuos_repository_atomic_checkpoint_creation_v1_02 import (
    RepositoryAtomicCheckpointCreationV102Tests,
)


def main() -> int:
    if check_live_contract() != 0:
        return 1
    if run_previous_frontier() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryAtomicCheckpointCreationV102Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
