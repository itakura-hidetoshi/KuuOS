"""v0.22 additive source-pin and declaration regression tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_normalization_sources_v0_22 as checker
from scripts import check_kuuos_lean_python_wa_weighted_sum_sources_v0_21 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/old_v022_fixture.py"
FORMAL = "formal/KuuOSFormal/WaNormalizationV0_22.lean"
TEST = "tests/lean_python_extensions/test_fixture_v022.py"
DOC = "docs/fixture-v022.md"
CLASS = "FakeV022Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v022.FakeV022Tests"
BYTE_TEST = b"import unittest\nclass FakeV022Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = (
    b"theorem rational_normalization_shift_bound : True := by trivial\n"
    b"theorem observed_native_tolerance_to_normalized_real : True := by trivial\n"
)


class WaNormalizationSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v022-pins-") as folder:
            root = Path(folder)
            for path, data in ((OLD, b"original\n"), (FORMAL, BYTE_FORMAL),
                               (TEST, BYTE_TEST), (DOC, b"scope\n")):
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

    def test_actual_137_prior_blob_pins_and_six_additive_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 6)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_both_new_test_classes_uniquely_declared(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(names for names in inventory.values()))
        self_id = "tests.lean_python_extensions.test_wa_normalization_sources_v0_22.WaNormalizationSourceTests"
        self.assertEqual(len(inventory[self_id]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_original_v021_blobs_byte_preserved(self):
        for path, expected in checker.SOURCE_BLOBS.items():
            raw, problem = checker._BASE._read_file(ROOT, path)
            with self.subTest(path=path):
                self.assertIsNone(problem)
                self.assertEqual(checker._BASE._git_blob(raw), expected)

    def test_fixture_static_detection_does_not_execute_or_elaborate(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_missing_or_modified_lean_declaration_blocked(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem unrelated : True := by trivial\n")
            self.assertIn("required_v022_proof_declaration_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v022_file_missing:" + FORMAL,
                          checker.check_sources(root))

    def test_source_byte_drift_and_missing_test_blocked(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"changed\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class WrongTests: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in error
                                for error in checker.check_sources(root)))

    def test_missing_doc_and_nonregular_file_blocked(self):
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v022_file_missing:" + DOC, checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            (root / FORMAL).symlink_to(root / TEST)
            self.assertTrue(any(FORMAL in x for x in checker.check_sources(root)))

    def test_unknown_root_returns_no_data(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
