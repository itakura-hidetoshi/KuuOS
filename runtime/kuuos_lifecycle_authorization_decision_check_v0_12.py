#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_authorization_decision_stage_order_v0_12 import (
    LifecycleAuthorizationDecisionStageOrderV012Tests,
)
from tests.test_kuuos_lifecycle_authorization_decision_v0_12 import (
    LifecycleAuthorizationDecisionV012Tests,
)


def run_lifecycle_authorization_decision_v0_12() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(LifecycleAuthorizationDecisionV012Tests),
            loader.loadTestsFromTestCase(
                LifecycleAuthorizationDecisionStageOrderV012Tests
            ),
        )
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_authorization_decision_v0_12())
