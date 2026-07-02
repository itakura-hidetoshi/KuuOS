#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_apoptosis_quiescence_review_v0_5 import (
    ApoptosisQuiescenceReviewV05Tests,
)


def run_apoptosis_quiescence_review_v0_5() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        ApoptosisQuiescenceReviewV05Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_apoptosis_quiescence_review_v0_5())
