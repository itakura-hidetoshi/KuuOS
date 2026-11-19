"""Native CodeAI original-source and Lean theorem signature pins v0.30.

Original source frozen, added module tested by real native CodeAI
fixtures. Source markers are not proof elaboration, compiler results,
external evidence authenticity, or host effect receipts.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_codeai_native_selection_sources_v0_30 as check


class CodeAINativeSourceBindingTests(unittest.TestCase):
    def test_all_older_proof_pins_and_new_exact_source_still_match(self):
        self.assertEqual(check.prior.check_sources(check.ROOT), ())
        self.assertEqual(check.check_sources(check.ROOT), ())
        self.assertEqual(len(check.ORIGINAL_BLOBS), 10)

    def test_all_ten_actual_original_codeai_source_blobs_are_unchanged(self):
        for path, sha in check.ORIGINAL_BLOBS.items():
            with self.subTest(path=path):
                raw, error = check._read(check.ROOT, path)
                self.assertIsNone(error)
                self.assertEqual(check._blob(raw), sha)

    def test_two_new_classes_include_real_test_methods(self):
        inventory = check.inventory(check.ROOT)
        self.assertEqual(set(inventory), set(check.TEST_CLASSES))
        self.assertTrue(all(len(x) > 5 for x in inventory.values()))

    def test_missing_source_is_not_treated_as_a_negative_proof(self):
        altered = check.NEW_FILES + ("docs/unavailable-codeai-v0_30.md",)
        with patch.object(check, "NEW_FILES", altered):
            errors = check.check_sources(check.ROOT)
        self.assertIn("v030_new_source_missing:docs/unavailable-codeai-v0_30.md",
                      errors)

    def test_drift_of_original_codeai_selector_fails_closed(self):
        path = "runtime/kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py"
        with patch.dict(check.ORIGINAL_BLOBS, {path: "0" * 40}):
            self.assertIn("v030_original_source_drift:" + path,
                          check.check_sources(check.ROOT))

    def test_theorem_signature_markers_cannot_be_omitted(self):
        path = "formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean"
        original = check._read

        def replace(root: Path, item: str):
            if item == path:
                return b"theorem irrelevant : True := by trivial\n", None
            return original(root, item)
        with patch.object(check, "_read", side_effect=replace):
            problems = check.check_sources(check.ROOT)
        self.assertIn("v030_lean_declaration_missing:highScoreCannotOverrideInadmissible",
                      problems)

    def test_original_score_does_not_create_lean_certification(self):
        from runtime.kuuos_lean_python_codeai_native_selection_v0_30 import (
            audit_native_codeai_selection, NO_DATA,
        )
        result = audit_native_codeai_selection(None, None, None)
        self.assertEqual(result.status, NO_DATA)
        self.assertFalse(result.lean_proof_term_constructed)
        self.assertFalse(result.source_issuer_authenticated)
        self.assertFalse(result.execution_authority_granted)

    def test_untrusted_root_is_no_data(self):
        self.assertEqual(check.check_sources(None), ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
