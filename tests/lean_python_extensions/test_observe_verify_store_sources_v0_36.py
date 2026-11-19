"""v0.36: source pins and append-only regression inventory.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_observe_verify_store_sources_v0_36 as checker


class NativeObserveVerifyStoreSourceTests(unittest.TestCase):
    def test_inherited_v035_and_earlier_pins(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_eleven_unmodified_original_sources(self):
        self.assertEqual(len(checker.PINNED), 11)
        for path, expected in checker.PINNED.items():
            with self.subTest(path=path):
                raw, problem = checker._read(checker.ROOT, path)
                self.assertIsNone(problem)
                self.assertEqual(checker._blob(raw), expected)

    def test_original_lean_verify_evidence_source_drift_blocks(self):
        path = "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v036_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_original_verify_store_drift_blocks(self):
        path = "runtime/kuuos_verify_os_store_v0_1.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v036_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_native_verify_adapter_drift_blocks(self):
        path = "runtime/kuuos_lean_python_verify_native_binding_v0_28.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v036_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_new_file_missing_blocks(self):
        with patch.object(
            checker, "NEW", checker.NEW + ("docs/absent-v036.md",),
        ):
            self.assertIn(
                "v036_new_file_missing:docs/absent-v036.md",
                checker.check_sources(checker.ROOT),
            )

    def test_exact_two_independent_testcase_classes(self):
        observed = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(observed), set(checker.CLASSES))
        self.assertGreaterEqual(len(observed[checker.NEW[2]]), 18)

    def test_checked_local_success_keeps_non_authority(self):
        from runtime.kuuos_lean_python_observe_verify_store_compat_v0_36 import (
            NativeObserveVerifyStoreAudit, SCOPED_COMPATIBLE,
        )
        result = NativeObserveVerifyStoreAudit(SCOPED_COMPATIBLE)
        self.assertFalse(result.verification_is_truth)
        self.assertFalse(result.causal_attribution_authority_granted)
        self.assertFalse(result.whole_program_lean_python_refinement_proved)
        self.assertFalse(result.global_descent_proved)
        self.assertFalse(result.execution_authority_granted)

    def test_untrusted_root_identity_is_not_accepted(self):
        self.assertEqual(
            checker.check_sources(None),
            ("root:trusted_path_required",),
        )


if __name__ == "__main__":
    unittest.main()
