#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_transition_decision_stage_order_v0_18 import (
    LifecycleTransitionDecisionStageOrderV018Tests,
)
from tests.test_kuuos_lifecycle_transition_decision_v0_18 import (
    LifecycleTransitionDecisionV018Tests,
)


def run_lifecycle_transition_decision_v0_18() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        (
            loader.loadTestsFromTestCase(LifecycleTransitionDecisionV018Tests),
            loader.loadTestsFromTestCase(
                LifecycleTransitionDecisionStageOrderV018Tests
            ),
        )
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_transition_decision_v0_18())
