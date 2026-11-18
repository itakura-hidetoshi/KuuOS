"""v0.23 additive source-pin and static declaration regression tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_normalized_score_sources_v0_23 as checker
from scripts import check_kuuos_lean_python_wa_normalization_sources_v0_22 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/pinned_v023_old.py"
FORMAL = "formal/KuuOSFormal/WaNormalizedScoreV0_23.lean"
TEST = "tests/lean_python_extensions/test_fixture_v023.py"
DOC = "docs/fixture-v023.md"
CLASS = "FakeV023Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v023.FakeV023Tests"
BYTE_TEST = b"import unittest\nclass FakeV023Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = (
    b"theorem rational_ideal_weighted_contraction : True := by trivial\n"
    b"theorem certified_products_normalized_final_wa_real : True := by trivial\n"
)


class WaNormalizedScoreSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v023-source-pins-") as folder:
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

    def test_actual_143_predecessor_pins_and_six_additive_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 6)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_real_two_new_test_class_declarations(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(methods for methods in inventory.values()))
        me = "tests.lean_python_extensions.test_wa_normalized_score_sources_v0_23.WaNormalizedScoreSourceTests"
        self.assertEqual(len(inventory[me]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_v022_exact_blobs_preserved(self):
        for path, sha in checker.SOURCE_BLOBS.items():
            raw, error = checker._BASE._read_file(ROOT, path)
            with self.subTest(file=path):
                self.assertIsNone(error)
                self.assertEqual(checker._BASE._git_blob(raw), sha)

    def test_fixture_does_not_execute_runtime_or_elaborate_lean(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_changed_lean_theorem_source_cannot_look_certified(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem irrelevant : True := by trivial\n")
            self.assertIn("required_v023_proof_declaration_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v023_file_missing:" + FORMAL,
                          checker.check_sources(root))

    def test_mutated_predecessor_source_is_blocked(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"rewritten\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))

    def test_test_suppression_or_missing_doc_is_blocked(self):
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class Wrong: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in x
                                for x in checker.check_sources(root)))
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v023_file_missing:" + DOC,
                          checker.check_sources(root))

    def test_untrusted_root_keeps_no_data(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
