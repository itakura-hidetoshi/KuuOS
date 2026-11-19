"""v0.35 native ActOS→ObserveOS source integrity and inherited pins.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_act_observe_store_sources_v0_35 as checker


class NativeActObserveStoreSourceTests(unittest.TestCase):
    def test_previous_v034_and_earlier_pins(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_nine_unchanged_original_lean_native_blobs(self):
        self.assertEqual(len(checker.PINNED), 9)
        for path, sha in checker.PINNED.items():
            with self.subTest(path=path):
                raw, issue = checker._read(checker.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(checker._blob(raw), sha)

    def test_lean_observe_source_drift_blocks(self):
        path = "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v035_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_observe_store_source_drift_blocks(self):
        path = "runtime/kuuos_observe_os_store_v0_1.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v035_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_required_v035_source_blocks(self):
        with patch.object(checker, "NEW", checker.NEW + ("docs/absent-v035.md",)):
            self.assertIn("v035_new_file_missing:docs/absent-v035.md",
                          checker.check_sources(checker.ROOT))

    def test_exact_two_testcase_classes_without_duplicates(self):
        observed = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(observed), set(checker.CLASSES))
        self.assertGreaterEqual(len(observed[checker.NEW[2]]), 12)

    def test_source_checker_cannot_grant_global_authority(self):
        from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
            NativeActObserveStoreAudit, SCOPED_COMPATIBLE,
        )
        x = NativeActObserveStoreAudit(SCOPED_COMPATIBLE)
        self.assertFalse(x.whole_program_lean_python_refinement_proved)
        self.assertFalse(x.observation_is_verification)
        self.assertFalse(x.global_descent_proved)
        self.assertFalse(x.execution_authority_granted)

    def test_root_without_verified_identity_is_unverified(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
