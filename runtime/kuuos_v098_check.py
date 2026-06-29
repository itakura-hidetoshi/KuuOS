#!/usr/bin/env python3
from __future__ import annotations

import unittest

from runtime.kuuos_v097_check import main as run_previous_frontier
from scripts.check_kuuos_live_v098 import main as check_live_contract
from tests.test_kuuos_repository_reference_update_receipt_v0_98 import (
    RepositoryReferenceUpdateReceiptV098Tests,
)


def main() -> int:
    if check_live_contract() != 0:
        return 1
    if run_previous_frontier() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryReferenceUpdateReceiptV098Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
