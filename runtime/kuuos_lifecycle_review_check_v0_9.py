#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.kuuos_lifecycle_review_fixture_v0_9 import LifecycleReviewFixtureV09


class LifecycleReviewV09Checks(LifecycleReviewFixtureV09):
    def test_valid_case_is_read_only(self) -> None:
        record = self.review()
        self.assertTrue(record.review_record_issued)
        self.assertTrue(record.effect_free)
        self.assertTrue(record.read_only)


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
