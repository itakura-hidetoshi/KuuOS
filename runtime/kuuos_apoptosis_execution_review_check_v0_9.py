#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_apoptosis_execution_review_v0_9 import (
    ApoptosisExecutionReviewV09Tests,
)


def run_apoptosis_execution_review_v0_9() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        ApoptosisExecutionReviewV09Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_apoptosis_execution_review_v0_9())
