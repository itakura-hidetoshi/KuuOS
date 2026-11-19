"""v0.38 exact original source pins, inherited checks and non-authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_five_store_chain_sources_v0_38 as checker


class FiveOriginalStoreChainSourceTests(unittest.TestCase):
    def test_all_inherited_v037_and_earlier_source_checks(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_seventeen_exact_original_lean_native_source_blobs(self):
        self.assertEqual(len(checker.PINNED), 17)
        for path, expected in checker.PINNED.items():
            with self.subTest(path=path):
                raw, problem = checker._read(checker.ROOT, path)
                self.assertIsNone(problem)
                self.assertEqual(checker._blob(raw), expected)

    def test_exact_five_original_lean_os_modules(self):
        paths = [path for path in checker.PINNED if path.endswith(".lean")]
        self.assertEqual(len(paths), 5)
        self.assertEqual(
            {path.rsplit("/", 2)[-2] for path in paths},
            {"PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS"},
        )

    def test_lean_plan_source_drift_blocks(self):
        path = "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v038_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_lean_learning_source_drift_blocks(self):
        path = "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v038_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_original_plan_store_source_drift_blocks(self):
        path = "runtime/kuuos_plan_os_store_v0_1.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v038_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_original_plan_act_adapter_drift_blocks(self):
        path = "runtime/kuuos_lean_python_plan_act_store_provenance_v0_34.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v038_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_original_verify_learn_adapter_drift_blocks(self):
        path = "runtime/kuuos_lean_python_verify_learn_store_compat_v0_37.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v038_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_required_new_file_missing_blocks(self):
        with patch.object(checker, "NEW", checker.NEW + ("docs/absent-v038.md",)):
            self.assertIn("v038_new_file_missing:docs/absent-v038.md",
                          checker.check_sources(checker.ROOT))

    def test_exact_two_new_testcase_classes_with_real_tests(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.CLASSES))
        self.assertGreaterEqual(len(inventory[checker.NEW[2]]), 20)
        self.assertGreaterEqual(len(inventory[checker.NEW[3]]), 8)

    def test_scoped_success_never_claims_formal_descent(self):
        from runtime.kuuos_lean_python_five_store_chain_compat_v0_38 import (
            FiveStoreChainAudit, SCOPED_COMPATIBLE,
        )
        result = FiveStoreChainAudit(SCOPED_COMPATIBLE)
        for name in (
            "formal_global_descent_proved",
            "lean_python_semantic_refinement_proved",
            "global_atomic_snapshot_proved",
            "external_activation_issuer_authenticated",
            "execution_authority_granted",
            "truth_authority_granted",
        ):
            self.assertFalse(getattr(result, name), name)

    def test_untrusted_checker_root_identity_fails_closed(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
