"""v0.25 additive source pin and test-inventory regression checks.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_finite_extrema_sources_v0_25 as checker
from scripts import check_kuuos_lean_python_wa_upper_clip_sources_v0_24 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/pinned_v025_old.py"
FORMAL = "formal/KuuOSFormal/WaFiniteExtremaV0_25.lean"
TEST = "tests/lean_python_extensions/test_fixture_v025.py"
DOC = "docs/fixture-v025.md"
CLASS = "FakeV025Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v025.FakeV025Tests"
BYTE_TEST = b"import unittest\nclass FakeV025Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = (
    b"theorem rational_min_unit : True := by trivial\n"
    b"theorem rational_max_unit : True := by trivial\n"
    b"theorem rational_finite_extrema_wa_ideal_in_unit : True := by trivial\n"
    b"theorem observed_finite_extrema_ideal_identity : True := by trivial\n"
)


class WaFiniteExtremaSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v025-source-pins-") as folder:
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

    def test_actual_155_predecessor_pins_and_six_additive_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 6)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_new_real_test_class_inventory_is_declared(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(methods for methods in inventory.values()))
        me = "tests.lean_python_extensions.test_wa_finite_extrema_sources_v0_25.WaFiniteExtremaSourceTests"
        self.assertEqual(len(inventory[me]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_v024_exact_blob_hashes_are_preserved(self):
        for path, sha in checker.SOURCE_BLOBS.items():
            raw, error = checker._BASE._read_file(ROOT, path)
            with self.subTest(path=path):
                self.assertIsNone(error)
                self.assertEqual(checker._BASE._git_blob(raw), sha)

    def test_fixture_static_does_not_execute_runtime_or_elaborate_lean(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_mutated_predecessor_blob_fails_closed(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"mutated\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))

    def test_missing_or_mutated_lean_declarations_are_blocked(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem irrelevant : True := by trivial\n")
            self.assertIn("required_v025_proof_declaration_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v025_file_missing:" + FORMAL,
                          checker.check_sources(root))

    def test_missing_doc_and_suppressed_tests_fail_closed(self):
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v025_file_missing:" + DOC,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class Wrong: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in p
                                for p in checker.check_sources(root)))

    def test_unknown_root_is_not_certified(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
