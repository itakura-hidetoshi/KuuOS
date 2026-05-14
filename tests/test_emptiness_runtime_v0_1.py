#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "emptiness_runtime_v0_1.py"

spec = importlib.util.spec_from_file_location("emptiness_runtime_v0_1", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(runtime)


class TestEmptinessRuntimeV01(unittest.TestCase):
    def test_default_is_candidate(self) -> None:
        out = runtime.evaluate_emptiness(runtime.EmptinessClaim())
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertFalse(out["direct_K_observable"])
        self.assertFalse(out["execution_authority_granted"])

    def test_k_objectification_rejected(self) -> None:
        out = runtime.evaluate_emptiness(runtime.EmptinessClaim(names_k_as_object=True))
        self.assertEqual(out["status"], "REJECT")

    def test_k_nothingness_requires_repair(self) -> None:
        out = runtime.evaluate_emptiness(runtime.EmptinessClaim(treats_k_as_nothingness=True))
        self.assertEqual(out["status"], "REPAIR")

    def test_k_kperp_collapse_holds(self) -> None:
        out = runtime.evaluate_emptiness(runtime.EmptinessClaim(collapses_k_and_kperp=True))
        self.assertEqual(out["status"], "HOLD")

    def test_missing_lineage_observe(self) -> None:
        out = runtime.evaluate_emptiness(runtime.EmptinessClaim(has_lineage=False))
        self.assertEqual(out["status"], "OBSERVE")


if __name__ == "__main__":
    unittest.main()
