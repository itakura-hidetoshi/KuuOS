#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_post_operation_review_stage_order_v0_16 import (
    LifecyclePostOperationReviewStageOrderV016Tests,
)
from tests.test_kuuos_lifecycle_post_operation_review_v0_16 import (
    LifecyclePostOperationReviewV016Tests,
)


def run_lifecycle_post_operation_review_v0_16() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(
                LifecyclePostOperationReviewV016Tests
            ),
            loader.loadTestsFromTestCase(
                LifecyclePostOperationReviewStageOrderV016Tests
            ),
        )
    )
    result = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=2
    ).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_post_operation_review_v0_16())
