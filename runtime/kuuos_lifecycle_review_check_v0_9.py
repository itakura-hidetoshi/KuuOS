#!/usr/bin/env python3
from __future__ import annotations

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


class LifecycleReviewV09Checks(unittest.TestCase):
    def test_complete_audit_matrix(self) -> None:
        checks = {
            **source_audit_matrix(),
            **independence_audit_matrix(),
            **safety_audit_matrix(),
        }
        failures = sorted(name for name, passed in checks.items() if not passed)
        self.assertFalse(failures, f"failed lifecycle review checks: {failures}")
        self.assertEqual(len(checks), 19)


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
