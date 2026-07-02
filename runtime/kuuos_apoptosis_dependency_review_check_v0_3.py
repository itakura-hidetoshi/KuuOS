#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_apoptosis_dependency_review_v0_3 import (
    ApoptosisDependencyReviewV03Tests,
)


def run_apoptosis_dependency_review_v0_3() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        ApoptosisDependencyReviewV03Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_apoptosis_dependency_review_v0_3())
