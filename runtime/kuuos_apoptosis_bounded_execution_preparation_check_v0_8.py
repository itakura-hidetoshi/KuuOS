#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_apoptosis_bounded_execution_preparation_v0_8 import (
    ApoptosisBoundedExecutionPreparationV08Tests,
)


def run_apoptosis_bounded_execution_preparation_v0_8() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        ApoptosisBoundedExecutionPreparationV08Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_apoptosis_bounded_execution_preparation_v0_8())
