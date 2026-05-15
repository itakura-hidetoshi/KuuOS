#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "emptiness_dependent_origination_two_truths_runtime_v0_1.py"

spec = importlib.util.spec_from_file_location("emptiness_dependent_origination_two_truths_runtime_v0_1", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
sys.modules[spec.name] = runtime
spec.loader.exec_module(runtime)


class TestEmptinessDependentOriginationTwoTruthsRuntimeV01(unittest.TestCase):
    def test_default_candidate(self) -> None:
        out = runtime.evaluate_ku_string_emptiness_do_two_truths(runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim())
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertFalse(out["K_is_object_allowed"])
        self.assertFalse(out["flat_graph_dependent_origination_allowed"])
        self.assertFalse(out["paramartha_samvrti_collapse_allowed"])

    def test_emptiness_objectification_rejected(self) -> None:
        out = runtime.evaluate_ku_string_emptiness_do_two_truths(
            runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim(emptiness_claim={"names_k_as_object": True})
        )
        self.assertEqual(out["status"], "REJECT")

    def test_flat_graph_dependent_origination_rejected(self) -> None:
        out = runtime.evaluate_ku_string_emptiness_do_two_truths(
            runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim(dependent_origination_claim={"collapses_to_flat_graph": True})
        )
        self.assertEqual(out["status"], "REJECT")

    def test_two_truths_collapse_rejected(self) -> None:
        out = runtime.evaluate_ku_string_emptiness_do_two_truths(
            runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim(two_truths_claim={"collapses_ultimate_to_conventional": True})
        )
        self.assertEqual(out["status"], "REJECT")

    def test_string_or_brane_as_k_rejected(self) -> None:
        out = runtime.evaluate_ku_string_emptiness_do_two_truths(
            runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim(treats_string_or_brane_as_k=True)
        )
        self.assertEqual(out["status"], "REJECT")

    def test_missing_gap_reference_holds(self) -> None:
        out = runtime.evaluate_ku_string_emptiness_do_two_truths(
            runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim(gap_stabilizer_33_20_reference=False)
        )
        self.assertEqual(out["status"], "HOLD")


if __name__ == "__main__":
    unittest.main()
