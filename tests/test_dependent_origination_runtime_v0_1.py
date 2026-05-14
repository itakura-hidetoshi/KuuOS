#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "dependent_origination_runtime_v0_1.py"

spec = importlib.util.spec_from_file_location("dependent_origination_runtime_v0_1", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(runtime)


class TestDependentOriginationRuntimeV01(unittest.TestCase):
    def test_default_is_candidate(self) -> None:
        out = runtime.evaluate_dependent_origination(runtime.DependentOriginationClaim())
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertFalse(out["self_origin_allowed"])
        self.assertFalse(out["execution_authority_granted"])

    def test_self_origin_rejected(self) -> None:
        out = runtime.evaluate_dependent_origination(runtime.DependentOriginationClaim(claims_self_origin=True))
        self.assertEqual(out["status"], "REJECT")

    def test_independent_essence_rejected(self) -> None:
        out = runtime.evaluate_dependent_origination(runtime.DependentOriginationClaim(claims_independent_essence=True))
        self.assertEqual(out["status"], "REJECT")

    def test_missing_context_observe(self) -> None:
        out = runtime.evaluate_dependent_origination(runtime.DependentOriginationClaim(has_context=False))
        self.assertEqual(out["status"], "OBSERVE")

    def test_missing_gluing_witness_hold(self) -> None:
        out = runtime.evaluate_dependent_origination(runtime.DependentOriginationClaim(gluing_witness_ok=False))
        self.assertEqual(out["status"], "HOLD")


if __name__ == "__main__":
    unittest.main()
