#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_apoptosis_authority_review_v0_4 import (
    ApoptosisAuthorityReviewV04Tests,
)


def run_apoptosis_authority_review_v0_4() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        ApoptosisAuthorityReviewV04Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_apoptosis_authority_review_v0_4())
