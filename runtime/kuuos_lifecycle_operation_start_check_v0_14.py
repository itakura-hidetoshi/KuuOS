#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_operation_start_stage_order_v0_14 import (
    LifecycleOperationStartStageOrderV014Tests,
)
from tests.test_kuuos_lifecycle_operation_start_v0_14 import (
    LifecycleOperationStartV014Tests,
)


def run_lifecycle_operation_start_v0_14() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(LifecycleOperationStartV014Tests),
            loader.loadTestsFromTestCase(LifecycleOperationStartStageOrderV014Tests),
        )
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_operation_start_v0_14())
