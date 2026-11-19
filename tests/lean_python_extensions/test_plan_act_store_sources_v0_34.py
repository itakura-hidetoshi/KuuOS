"""v0.34 source-exact native Plan→Act and Lean integrity checks.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_plan_act_store_sources_v0_34 as checker


class NativePlanActStoreSourceTests(unittest.TestCase):
    def test_inherited_prior_source_integrity(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_ten_exact_original_source_blobs(self):
        self.assertEqual(len(checker.PINNED), 10)
        for path, expected in checker.PINNED.items():
            with self.subTest(path=path):
                raw, issue = checker._read(checker.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(checker._blob(raw), expected)

    def test_act_lean_source_pin_drift_blocks(self):
        path = "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v034_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_act_store_source_pin_drift_blocks(self):
        path = "runtime/kuuos_act_os_store_v0_1.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v034_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_new_file_is_no_success(self):
        with patch.object(checker, "NEW", checker.NEW + ("docs/no-such-v034.md",)):
            self.assertIn("v034_new_file_missing:docs/no-such-v034.md",
                          checker.check_sources(checker.ROOT))

    def test_new_test_class_inventory_has_no_duplicate(self):
        a = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(a), set(checker.CLASSES))
        self.assertGreaterEqual(len(a[checker.NEW[2]]), 12)

    def test_no_success_result_promotes_formal_authority(self):
        from runtime.kuuos_lean_python_plan_act_store_provenance_v0_34 import (
            NativePlanActStoreAudit, SCOPED_COMPATIBLE,
        )
        x = NativePlanActStoreAudit(SCOPED_COMPATIBLE)
        self.assertFalse(x.whole_act_lean_conditions_certified)
        self.assertFalse(x.formal_descent_certified)
        self.assertFalse(x.execution_authority_granted)

    def test_unknown_root_is_unverified(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
