"""v0.21 additive source pins and proof/test declaration regression.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_weighted_sum_sources_v0_21 as checker
from scripts import check_kuuos_lean_python_wa_binary64_midpoint_sources_v0_20 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/old_v021_fixture.py"
FORMAL = "formal/KuuOSFormal/WaWeightedSumV0_21.lean"
TEST = "tests/lean_python_extensions/test_fixture_v021.py"
DOC = "docs/fixture-v021.md"
CLASS = "FakeV021Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v021.FakeV021Tests"
BYTE_TEST = b"import unittest\nclass FakeV021Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = (
    b"theorem list_abs_sum_le_sum_abs : True := by trivial\n"
    b"theorem weighted_sum_observed_real_error : True := by trivial\n"
)


class WaWeightedSumSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v021-pins-") as folder:
            root = Path(folder)
            for path, data in ((OLD, b"original\n"),
                               (FORMAL, BYTE_FORMAL),
                               (TEST, BYTE_TEST),
                               (DOC, b"scope\n")):
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(data)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS",
                              {OLD: checker._BASE._git_blob(b"original\n")}), \
                 patch.object(checker, "REQUIRED_PATHS",
                              (OLD, FORMAL, TEST, DOC)), \
                 patch.object(checker, "TEST_CLASSES", {TEST: CLASS}):
                yield root

    def test_actual_131_prior_blob_pins_and_six_additive_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_both_new_test_classes_are_uniquely_declared(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(names for names in inventory.values()))
        self_id = "tests.lean_python_extensions.test_wa_weighted_sum_sources_v0_21.WaWeightedSumSourceTests"
        self.assertEqual(len(inventory[self_id]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_original_v020_blobs_byte_preserved(self):
        for path, expected in checker.SOURCE_BLOBS.items():
            raw, issue = checker._BASE._read_file(ROOT, path)
            with self.subTest(path=path):
                self.assertIsNone(issue)
                self.assertEqual(checker._BASE._git_blob(raw), expected)

    def test_static_fixture_does_not_execute_python_or_compile_lean(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_missing_or_altered_proof_declaration_blocks(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem unrelated : True := by trivial\n")
            self.assertIn("required_v021_proof_declaration_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v021_file_missing:" + FORMAL, checker.check_sources(root))

    def test_mutated_historical_bytes_are_rejected(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"changed\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))

    def test_suppressed_tests_or_missing_doc_are_rejected(self):
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class WrongTests: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in x
                                for x in checker.check_sources(root)))
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v021_file_missing:" + DOC,
                          checker.check_sources(root))

    def test_invalid_root_keeps_no_data(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
