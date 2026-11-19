"""v0.37 exact original source integrity and cumulative audit tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_verify_learn_store_sources_v0_37 as checker


class NativeVerifyLearnStoreSourceTests(unittest.TestCase):
    def test_v036_and_all_previous_pins_are_unchanged(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_fourteen_original_lean_native_source_blobs(self):
        self.assertEqual(len(checker.PINNED), 14)
        for path, expected in checker.PINNED.items():
            with self.subTest(path=path):
                raw, problem = checker._read(checker.ROOT, path)
                self.assertIsNone(problem)
                self.assertEqual(checker._blob(raw), expected)

    def test_lean_future_only_learning_source_drift_blocks(self):
        path = "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v037_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_native_learn_source_adapter_drift_blocks(self):
        path = "runtime/kuuos_lean_python_learn_native_binding_v0_28.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v037_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_original_learn_store_drift_blocks(self):
        path = "runtime/kuuos_learn_os_store_v0_1.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v037_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_original_verify_kernel_drift_blocks(self):
        path = "runtime/kuuos_verify_os_kernel_v0_1.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v037_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_new_file_missing_blocks(self):
        with patch.object(checker, "NEW", checker.NEW + ("docs/absent-v037.md",)):
            self.assertIn(
                "v037_new_file_missing:docs/absent-v037.md",
                checker.check_sources(checker.ROOT),
            )

    def test_two_independent_case_classes_without_duplicating_others(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.CLASSES))
        self.assertGreaterEqual(len(inventory[checker.NEW[2]]), 20)

    def test_scoped_result_never_activates_or_grants_authority(self):
        from runtime.kuuos_lean_python_verify_learn_store_compat_v0_37 import (
            NativeVerifyLearnStoreAudit, SCOPED_COMPATIBLE,
        )
        report = NativeVerifyLearnStoreAudit(SCOPED_COMPATIBLE)
        self.assertFalse(report.learning_activated_now)
        self.assertFalse(report.learning_is_truth)
        self.assertFalse(report.memory_overwrite_authority_granted)
        self.assertFalse(report.whole_program_lean_python_refinement_proved)
        self.assertFalse(report.global_descent_proved)
        self.assertFalse(report.execution_authority_granted)

    def test_root_without_verified_identity_is_not_passed(self):
        self.assertEqual(
            checker.check_sources(None), ("root:trusted_path_required",),
        )


if __name__ == "__main__":
    unittest.main()
