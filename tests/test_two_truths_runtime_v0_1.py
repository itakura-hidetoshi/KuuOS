#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "two_truths_runtime_v0_1.py"

spec = importlib.util.spec_from_file_location("two_truths_runtime_v0_1", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
sys.modules[spec.name] = runtime
spec.loader.exec_module(runtime)


class TestTwoTruthsRuntimeV01(unittest.TestCase):
    def test_default_candidate(self) -> None:
        out = runtime.evaluate_two_truths(runtime.TwoTruthsClaim())
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertFalse(out["paramartha_objectification_allowed"])
        self.assertFalse(out["execution_authority_granted"])

    def test_ultimate_objectification_rejected(self) -> None:
        out = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(ultimate_truth_direct_objectified=True))
        self.assertEqual(out["status"], "REJECT")

    def test_conventional_truth_denial_rejected(self) -> None:
        out = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(conventional_truth_denied=True))
        self.assertEqual(out["status"], "REJECT")

    def test_collapse_rejected(self) -> None:
        out = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(collapses_ultimate_to_conventional=True))
        self.assertEqual(out["status"], "REJECT")
        out2 = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(collapses_conventional_to_ultimate=True))
        self.assertEqual(out2["status"], "REJECT")

    def test_gap_authority_rejected(self) -> None:
        out = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(treats_mass_gap_as_final_public_theorem_authority=True))
        self.assertEqual(out["status"], "REJECT")
        out2 = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(grants_execution_from_gap=True))
        self.assertEqual(out2["status"], "REJECT")

    def test_bad_bridge_held(self) -> None:
        out = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(mass_gap_bridge_input={"bridge_authority": "final_authority"}))
        self.assertEqual(out["status"], "HOLD")


if __name__ == "__main__":
    unittest.main()
