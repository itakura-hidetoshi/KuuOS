#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_operation_approval_stage_order_v0_13 import (
    LifecycleOperationApprovalStageOrderV013Tests,
)
from tests.test_kuuos_lifecycle_operation_approval_v0_13 import (
    LifecycleOperationApprovalV013Tests,
)


def run_lifecycle_operation_approval_v0_13() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(LifecycleOperationApprovalV013Tests),
            loader.loadTestsFromTestCase(
                LifecycleOperationApprovalStageOrderV013Tests
            ),
        )
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_operation_approval_v0_13())
