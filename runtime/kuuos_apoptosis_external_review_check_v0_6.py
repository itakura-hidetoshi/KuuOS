#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_apoptosis_external_review_v0_6 import (
    ApoptosisExternalReviewV06Tests,
)


def run_apoptosis_external_review_v0_6() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        ApoptosisExternalReviewV06Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_apoptosis_external_review_v0_6())
