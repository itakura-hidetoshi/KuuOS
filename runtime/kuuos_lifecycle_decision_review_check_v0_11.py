#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_decision_review_v0_11 import (
    LifecycleDecisionReviewV011Tests,
)


def run_lifecycle_decision_review_v0_11() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        LifecycleDecisionReviewV011Tests
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_decision_review_v0_11())
