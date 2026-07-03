#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_operation_completion_stage_order_v0_15 import (
    LifecycleOperationCompletionStageOrderV015Tests,
)
from tests.test_kuuos_lifecycle_operation_completion_v0_15 import (
    LifecycleOperationCompletionV015Tests,
)


def run_lifecycle_operation_completion_v0_15() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(
                LifecycleOperationCompletionV015Tests
            ),
            loader.loadTestsFromTestCase(
                LifecycleOperationCompletionStageOrderV015Tests
            ),
        )
    )
    result = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=2
    ).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_operation_completion_v0_15())
