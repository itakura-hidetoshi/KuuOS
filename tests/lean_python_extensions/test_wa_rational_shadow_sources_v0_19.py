"""v0.19 source-preservation, additive Lean source and test declarations.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_rational_shadow_sources_v0_19 as checker
from scripts import check_kuuos_lean_python_belief_receipt_sources_v0_18 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/old_v019_fixture.py"
TEST = "tests/lean_python_extensions/test_fixture_v019.py"
FORMAL = "formal/KuuOSFormal/WaRationalBridgeV0_19.lean"
DOC = "docs/fixture-v019.md"
CLASS = "FakeV019Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v019.FakeV019Tests"
BYTE_TEST = b"import unittest\nclass FakeV019Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = b"theorem rationalIdeal_cast : True := by trivial\ntheorem two_stage_score_error_bound : True := by trivial\n"


class WaRationalShadowSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v019-pins-") as folder:
            root = Path(folder)
            for name, content in ((OLD, b"fixed\n"), (TEST, BYTE_TEST),
                                  (FORMAL, BYTE_FORMAL), (DOC, b"scope\n")):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS", {OLD: checker._BASE._git_blob(b"fixed\n")}), \
                 patch.object(checker, "REQUIRED_PATHS", (OLD, FORMAL, TEST, DOC)), \
                 patch.object(checker, "TEST_CLASSES", {TEST: CLASS}):
                yield root

    def test_actual_118_historical_pins_and_additive_six_paths(self):
        self.assertEqual(checker.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 7)
        self.assertEqual(len(prior.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(len(checker.TEST_CLASSES), 2)

    def test_actual_two_new_classes_have_unique_test_declarations(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(names for names in inventory.values()))
        self_key = "tests.lean_python_extensions.test_wa_rational_shadow_sources_v0_19.WaRationalShadowSourceTests"
        self.assertEqual(len(inventory[self_key]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_exact_unmodified_prior_checker_and_all_pins(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        for name, expected in checker.SOURCE_BLOBS.items():
            data, issue = checker._BASE._read_file(ROOT, name)
            with self.subTest(path=name):
                self.assertIsNone(issue)
                self.assertEqual(checker._BASE._git_blob(data), expected)

    def test_static_fixture_neither_executes_tests_nor_elaborates_lean(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_missing_or_modified_lean_source_is_rejected(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem unrelated : True := by trivial\n")
            self.assertIn("required_v019_proof_declarations_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v019_file_missing:" + FORMAL, checker.check_sources(root))

    def test_old_blob_drift_is_not_promoted_to_success(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"changed\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))

    def test_missing_nonregular_and_test_declaration_fail_closed(self):
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class WrongTests: pass\n")
            self.assertEqual(checker.declared_test_inventory(root), {})
            self.assertTrue(any("required_test_declarations_missing" in x
                                for x in checker.check_sources(root)))
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v019_file_missing:" + DOC, checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            (root / FORMAL).symlink_to(root / DOC)
            self.assertTrue(any(FORMAL in x for x in checker.check_sources(root)))

    def test_wrong_root_retains_no_data(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
