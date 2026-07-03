#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_authorization_decision_v0_12 import (
    LifecycleAuthorizationDecisionV012Tests,
)


def run_lifecycle_authorization_decision_v0_12() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        LifecycleAuthorizationDecisionV012Tests
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_authorization_decision_v0_12())
