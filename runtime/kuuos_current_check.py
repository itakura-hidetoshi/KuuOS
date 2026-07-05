#!/usr/bin/env python3
from __future__ import annotations

import importlib
import unittest

from runtime.kuuos_current_root_sequence_v0_77 import CURRENT_ROOT_STEPS

CURRENT_RUNTIME_ROOT = "runtime/kuuos_current_check.py"
CURRENT_ROOT_SEQUENCE_FRONTIER = "kuuos_current_root_sequence_v0_77"


def _run_unittest_module(module_name: str) -> int:
    suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def _run_callable(target: str) -> int:
    module_name, function_name = target.split(":", 1)
    module = importlib.import_module(module_name)
    outcome = getattr(module, function_name)()
    return int(outcome)


def _run_step(runner: str, target: str) -> int:
    if runner == "unittest":
        return _run_unittest_module(target)
    if runner == "callable":
        return _run_callable(target)
    raise ValueError("unknown_current_root_runner:" + runner)


def run_current() -> int:
    for step in CURRENT_ROOT_STEPS:
        status = _run_step(step.runner, step.target)
        if status != 0:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(run_current())
