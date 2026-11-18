"""v0.24 additive source-pin and declared-test inventory regressions.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_upper_clip_sources_v0_24 as checker
from scripts import check_kuuos_lean_python_wa_normalized_score_sources_v0_23 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/pinned_v024_old.py"
FORMAL = "formal/KuuOSFormal/WaUpperClipV0_24.lean"
TEST = "tests/lean_python_extensions/test_fixture_v024.py"
DOC = "docs/fixture-v024.md"
CLASS = "FakeV024Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v024.FakeV024Tests"
BYTE_TEST = b"import unittest\nclass FakeV024Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = (
    b"theorem rational_normalized_wa_ideal_in_unit : True := by trivial\n"
    b"theorem native_clipped_upper_final_wa_real : True := by trivial\n"
)


class WaUpperClipSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v024-source-") as folder:
            root = Path(folder)
            for path, raw in ((OLD, b"original\n"), (FORMAL, BYTE_FORMAL),
                              (TEST, BYTE_TEST), (DOC, b"scope\n")):
                f = root / path
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_bytes(raw)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS",
                              {OLD: checker._BASE._git_blob(b"original\n")}), \
                 patch.object(checker, "REQUIRED_PATHS",
                              (OLD, FORMAL, TEST, DOC)), \
                 patch.object(checker, "TEST_CLASSES", {TEST: CLASS}):
                yield root

    def test_actual_149_predecessor_pins_and_six_additive_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 6)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_real_new_test_classes_uniquely_declared(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(methods for methods in inventory.values()))
        me = "tests.lean_python_extensions.test_wa_upper_clip_sources_v0_24.WaUpperClipSourceTests"
        self.assertEqual(len(inventory[me]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_original_v023_blob_hashes_are_preserved(self):
        for path, sha in checker.SOURCE_BLOBS.items():
            raw, error = checker._BASE._read_file(ROOT, path)
            with self.subTest(path=path):
                self.assertIsNone(error)
                self.assertEqual(checker._BASE._git_blob(raw), sha)

    def test_static_fixture_has_no_runtime_or_lean_execution(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_mutated_old_source_is_blocked(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"altered\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))

    def test_missing_or_mutated_lean_declarations_are_blocked(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem ignored : True := by trivial\n")
            self.assertIn("required_v024_proof_declaration_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v024_file_missing:" + FORMAL,
                          checker.check_sources(root))

    def test_missing_doc_or_suppressed_tests_are_blocked(self):
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v024_file_missing:" + DOC,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class Wrong: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in x
                                for x in checker.check_sources(root)))

    def test_untrusted_root_is_not_certified(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
