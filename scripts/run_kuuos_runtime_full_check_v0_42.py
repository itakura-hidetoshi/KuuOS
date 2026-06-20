#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_qi_world_cross_cycle_blocker_v1_5 import (
    main as check_qi_world_v15,
)
from scripts.check_qi_world_indra_transport_request_v1_6 import (
    main as check_qi_world_v16,
)
from scripts.check_world_gauge_categorical_indra_net_bridge_v0_42 import (
    main as check_v042,
)
from scripts.run_kuuos_runtime_full_check_v0_41 import main as run_v041_full_check


def _run_qi_world_tests() -> int:
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in (
        "tests.test_qi_world_cross_cycle_blocker_v1_5",
        "tests.test_qi_world_indra_transport_request_v1_6",
    ):
        suite.addTests(loader.loadTestsFromName(module))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main() -> int:
    for check in (check_v042, check_qi_world_v15, check_qi_world_v16):
        if check() != 0:
            return 1
    if _run_qi_world_tests() != 0:
        return 1
    return run_v041_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
