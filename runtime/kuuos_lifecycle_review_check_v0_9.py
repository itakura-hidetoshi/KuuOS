#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from runtime.kuuos_lifecycle_review_audit_independence_v0_9 import (
    independence_audit_matrix,
)
from runtime.kuuos_lifecycle_review_audit_safety_v0_9 import (
    safety_audit_matrix,
)
from runtime.kuuos_lifecycle_review_audit_source_v0_9 import (
    source_audit_matrix,
)
from tests.kuuos_lifecycle_review_fixture_v0_9 import LifecycleReviewFixtureV09


class LifecycleReviewV09Checks(unittest.TestCase):
    def test_complete_audit_matrix(self) -> None:
        checks = {
            **source_audit_matrix(),
            **independence_audit_matrix(),
            **safety_audit_matrix(),
        }
        failures = sorted(name for name, passed in checks.items() if not passed)
        if failures:
            fixture = LifecycleReviewFixtureV09(methodName="runTest")
            fixture.setUp()
            record = fixture.review()
            diagnostic = {
                "status": record.status,
                "reason": record.reason,
                "false_checks": sorted(
                    name for name, passed in record.checks.items() if not passed
                ),
                "audit_failures": failures,
            }
            print(json.dumps(diagnostic, indent=2, sort_keys=True))
        self.assertFalse(failures, f"failed lifecycle review checks: {failures}")
        self.assertEqual(len(checks), 19)


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
