#!/usr/bin/env python3
from __future__ import annotations

import importlib
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CHECK_MODULES = [
    "scripts.validate_kuuos_runtime_manifest_v0_1",
    "scripts.check_kuuos_example_runner_import_v0_1",
    "scripts.check_kuuos_state_io_example_v0_1",
    "scripts.check_kuuos_qi_process_tensor_example_v0_1",
    "scripts.check_kuuos_runtime_daemon_example_v0_1",
]

TEST_MODULES = [
    "tests.test_qi_process_tensor_v0_1",
    "tests.test_qi_process_tensor_downstream_v0_1",
    "tests.test_kuuos_closed_loop_v0_1",
    "tests.test_kuuos_closed_loop_driver_v0_1",
    "tests.test_kuuos_state_io_runner_v0_1",
    "tests.test_kuuos_runtime_daemon_v0_1",
    "tests.test_kuuos_runtime_daemon_status_v0_1",
    "tests.test_kuuos_runtime_daemon_qi_policy_v0_1",
    "tests.test_kuuos_runtime_daemon_qique_gauge_v0_1",
    "tests.test_kuuos_runtime_daemon_emptiness_gate_v0_1",
    "tests.test_kuuos_runtime_daemon_wa_function_v0_1",
]


def run_checks() -> list[str]:
    errors: list[str] = []
    for name in CHECK_MODULES:
        module = importlib.import_module(name)
        result = module.main()
        if result != 0:
            errors.append(f"{name} returned {result}")
    return errors


def run_unittests() -> list[str]:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for name in TEST_MODULES:
        suite.addTests(loader.loadTestsFromName(name))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        return []
    return [f"unittest failures={len(result.failures)} errors={len(result.errors)}"]


def main() -> int:
    errors = []
    errors.extend(run_checks())
    errors.extend(run_unittests())
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuuOS runtime full check v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
