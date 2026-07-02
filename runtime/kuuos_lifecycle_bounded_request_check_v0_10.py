#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest

from tests.test_kuuos_lifecycle_bounded_request_v0_10 import (
    LifecycleBoundedRequestV010Tests,
)


def run_lifecycle_bounded_request_v0_10() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        LifecycleBoundedRequestV010Tests
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_lifecycle_bounded_request_v0_10())
