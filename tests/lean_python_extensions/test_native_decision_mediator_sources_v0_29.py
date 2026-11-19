"""v0.29 source-blobs and exact source-native adapter registration.

Static checking does not prove the Lean meaning matches CPython execution.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_native_decision_mediator_sources_v0_29 as check


class NativeDecisionMediatorSourceTests(unittest.TestCase):
    def test_all_original_lean_and_python_sources_are_pinned(self):
        self.assertEqual(len(check.SOURCE_BLOBS), 16)
        self.assertEqual(check.check_sources(check.ROOT), ())

    def test_all_predecessor_source_digests_still_match_exact_git_blobs(self):
        for path, pin in check.SOURCE_BLOBS.items():
            with self.subTest(path=path):
                raw, issue = check.previous.prior._read(check.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(check.previous.prior._blob(raw), pin)

    def test_original_v028_governance_still_accepted(self):
        self.assertEqual(check.previous.check_sources(check.ROOT), ())

    def test_four_actual_entrypoints_and_nine_new_files(self):
        self.assertEqual(len(check.NEW_PATHS), 9)
        self.assertEqual(len(check.ENTRYPOINTS), 4)
        self.assertEqual(set(check.inventory(check.ROOT)), set(check.TEST_CLASSES))
        self.assertEqual(check.check_sources(check.ROOT), ())

    def test_mutated_existing_python_kernel_cannot_be_accepted(self):
        path = "runtime/kuuos_decision_os_plural_kernel_v0_2.py"
        with patch.dict(check.SOURCE_BLOBS, {path: "0" * 40}):
            self.assertIn("predecessor_source_drift:" + path,
                          check.check_sources(check.ROOT))

    def test_mutated_original_lean_file_cannot_be_accepted(self):
        path = "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean"
        with patch.dict(check.SOURCE_BLOBS, {path: "0" * 40}):
            self.assertIn("predecessor_source_drift:" + path,
                          check.check_sources(check.ROOT))

    def test_missing_entrypoint_is_fail_closed(self):
        path = "runtime/kuuos_lean_python_wa_native_binding_v0_29.py"
        old = check.previous.prior._read
        def missing(root: Path, requested: str):
            if requested == path:
                return b"from __future__ import annotations\n", None
            return old(root, requested)
        with patch.object(check.previous.prior, "_read", side_effect=missing):
            self.assertIn("native_entrypoint_missing:" + path,
                          check.check_sources(check.ROOT))

    def test_missing_existing_theorem_name_fails_closed(self):
        path = "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean"
        old = check.previous.prior._read
        def broken(root: Path, requested: str):
            if requested == path:
                return b"theorem unrelated : True := by trivial\n", None
            return old(root, requested)
        with patch.object(check.previous.prior, "_read", side_effect=broken):
            found = check.check_sources(check.ROOT)
        self.assertTrue(any(x.startswith("native_theorem_name_missing:" + path)
                            for x in found))

    def test_missing_new_document_is_fail_closed(self):
        path = "docs/KUUOS_LEAN_PYTHON_NATIVE_DECISION_MEDIATOR_v0_29.md"
        with patch.object(check, "NEW_PATHS",
                          check.NEW_PATHS + ("docs/definitely_missing_v0_29.md",)):
            errors = check.check_sources(check.ROOT)
        self.assertTrue(any("new_source_missing:docs/definitely_missing" in x
                            for x in errors))
        self.assertIn(path, check.NEW_PATHS)

    def test_unknown_root_is_no_data_not_false_certification(self):
        self.assertEqual(check.check_sources(None), ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
