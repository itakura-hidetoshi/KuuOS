#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "dependent_origination_sheaf_gauge_runtime_v0_2.py"

spec = importlib.util.spec_from_file_location("dependent_origination_sheaf_gauge_runtime_v0_2", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(runtime)


class TestSheafGaugeDependentOriginationRuntimeV02(unittest.TestCase):
    def test_default_is_candidate(self) -> None:
        out = runtime.evaluate_sheaf_gauge_dependent_origination(runtime.SheafGaugeDependentOriginationClaim())
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertFalse(out["graph_only_model_allowed"])
        self.assertTrue(out["site_cover_required"])
        self.assertTrue(out["gauge_connection_required"])

    def test_flat_graph_collapse_rejected(self) -> None:
        out = runtime.evaluate_sheaf_gauge_dependent_origination(runtime.SheafGaugeDependentOriginationClaim(collapses_to_flat_graph=True))
        self.assertEqual(out["status"], "REJECT")

    def test_missing_cover_observed(self) -> None:
        out = runtime.evaluate_sheaf_gauge_dependent_origination(runtime.SheafGaugeDependentOriginationClaim(has_cover_family=False))
        self.assertEqual(out["status"], "OBSERVE")

    def test_missing_cocycle_holds(self) -> None:
        out = runtime.evaluate_sheaf_gauge_dependent_origination(runtime.SheafGaugeDependentOriginationClaim(cocycle_condition_ok=False))
        self.assertEqual(out["status"], "HOLD")

    def test_missing_gauge_connection_holds(self) -> None:
        out = runtime.evaluate_sheaf_gauge_dependent_origination(runtime.SheafGaugeDependentOriginationClaim(has_gauge_connection=False))
        self.assertEqual(out["status"], "HOLD")

    def test_missing_curvature_observed(self) -> None:
        out = runtime.evaluate_sheaf_gauge_dependent_origination(runtime.SheafGaugeDependentOriginationClaim(curvature_exposed=False))
        self.assertEqual(out["status"], "OBSERVE")


if __name__ == "__main__":
    unittest.main()
