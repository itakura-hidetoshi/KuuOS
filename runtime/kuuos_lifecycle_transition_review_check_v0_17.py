#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_transition_review_stage_order_v0_17 import (
    LifecycleTransitionReviewStageOrderV017Tests,
)
from tests.test_kuuos_lifecycle_transition_review_v0_17 import (
    LifecycleTransitionReviewV017Tests,
)


def run_lifecycle_transition_review_v0_17() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(LifecycleTransitionReviewV017Tests),
            loader.loadTestsFromTestCase(
                LifecycleTransitionReviewStageOrderV017Tests
            ),
        )
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_transition_review_v0_17())
