"""Original MemoryOS/WORLD v0.32 source blob and regression inventory.

Exact source fingerprints and runtime booleans do not constitute
Lean proof of global descent or external authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from pathlib import Path
from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_memory_world_local_compat_sources_v0_32 as checker


class NativeMemoryWorldCompatibilitySourceTests(unittest.TestCase):
    def test_all_predecessor_pins_and_exact_v032_source_paths(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())
        self.assertEqual(len(checker.NEW), 5)

    def test_all_nine_original_native_and_lean_blobs_unchanged(self):
        self.assertEqual(len(checker.PINNED), 9)
        for path, sha in checker.PINNED.items():
            with self.subTest(path=path):
                raw, issue = checker._read(checker.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(checker._blob(raw), sha)

    def test_v031_memory_native_blob_change_blocks(self):
        path = "runtime/kuuos_lean_python_memory_native_binding_v0_31.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v032_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_v031_world_native_blob_change_blocks(self):
        path = "runtime/kuuos_lean_python_world_native_binding_v0_31.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v032_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_source_file_is_not_silent_success(self):
        fake = "docs/no-such-memory-world-v032.md"
        with patch.object(checker, "NEW", checker.NEW + (fake,)):
            self.assertIn("v032_new_file_missing:" + fake,
                          checker.check_sources(checker.ROOT))

    def test_missing_compatibility_entrypoint_fails(self):
        path = checker.NEW[0]
        original_read = checker._read

        def missing(root: Path, name: str):
            if name == path:
                return b"from __future__ import annotations\n", None
            return original_read(root, name)

        with patch.object(checker, "_read", side_effect=missing):
            self.assertIn("v032_local_compatibility_entrypoint_missing",
                          checker.check_sources(checker.ROOT))

    def test_direct_fixture_testcase_import_is_statically_forbidden(self):
        # Regression for PR CI #44467037785 duplicate_extension_test_id:
        # imported unittest.TestCase fixture classes are rediscovered.
        path = checker.NEW[2]
        original = checker._read

        def imported_fixture(root: Path, selected: str):
            if selected == path:
                return (
                    b"from tests.test_authorized_atomic_world_commit_v0_34 "
                    b"import AuthorizedAtomicWorldCommitV034Test\n",
                    None,
                )
            return original(root, selected)

        with patch.object(checker, "_read", side_effect=imported_fixture):
            failures = checker.check_sources(checker.ROOT)
        self.assertIn("v032_direct_fixture_testcase_import_forbidden", failures)

    def test_full_two_class_regression_inventory(self):
        x = checker.inventory(checker.ROOT)
        self.assertEqual(set(x), set(checker.CLASSES))
        self.assertGreaterEqual(len(x[checker.NEW[2]]), 10)

    def test_unknown_root_remains_no_data(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))

    def test_static_compatibility_never_asserts_authority(self):
        from runtime.kuuos_lean_python_memory_world_local_compat_v0_32 import (
            LocalCompatibilityAudit, SCOPED_COMMIT,
        )
        x = LocalCompatibilityAudit(SCOPED_COMMIT)
        self.assertFalse(x.formal_descent_certified)
        self.assertFalse(x.global_gluing_proved)
        self.assertFalse(x.execution_authority_granted)
        self.assertFalse(x.complete_external_issuer_authenticated)


if __name__ == "__main__":
    unittest.main()
