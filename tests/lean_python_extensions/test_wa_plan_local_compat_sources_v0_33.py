"""Exact-source v0.33 Wa->Plan native source and Lean pins.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_wa_plan_local_compat_sources_v0_33 as checker


class NativeWaPlanLocalCompatibilitySourceTests(unittest.TestCase):
    def test_original_v032_inherited_source_pins(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_exact_eight_original_native_and_lean_blobs(self):
        self.assertEqual(len(checker.PINNED), 8)
        for path, expected in checker.PINNED.items():
            with self.subTest(path=path):
                raw, issue = checker._read(checker.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(checker._blob(raw), expected)

    def test_original_wa_projection_drift_is_blocked(self):
        path = "runtime/kuuos_lean_python_wa_native_binding_v0_29.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v033_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_original_plan_theorem_drift_is_blocked(self):
        path = "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v033_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_new_python_file_is_blocked(self):
        with patch.object(checker, "NEW", checker.NEW + ("docs/absent-v033.md",)):
            self.assertIn("v033_new_file_missing:docs/absent-v033.md",
                          checker.check_sources(checker.ROOT))

    def test_source_entrypoint_inventory(self):
        methods = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(methods), set(checker.CLASSES))
        self.assertGreaterEqual(len(methods[checker.NEW[2]]), 10)

    def test_no_local_compatibility_to_global_authority(self):
        from runtime.kuuos_lean_python_wa_plan_local_compat_v0_33 import (
            NativeWaPlanLocalAudit, SCOPED_COMPATIBLE,
        )
        report = NativeWaPlanLocalAudit(SCOPED_COMPATIBLE)
        self.assertFalse(report.global_gluing_proved)
        self.assertFalse(report.formal_descent_certified)
        self.assertFalse(report.complete_lean_python_refinement_proved)
        self.assertFalse(report.execution_authority_granted)

    def test_wrong_root_kept_unverified(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
