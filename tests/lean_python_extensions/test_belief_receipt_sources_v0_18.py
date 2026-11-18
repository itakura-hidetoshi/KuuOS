"""Retained source pins, fail-closed source drift and declaration checks v0.18.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_belief_receipt_sources_v0_18 as checker
from scripts import check_kuuos_lean_python_decision_evidence_sources_v0_17 as prior

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = "runtime/belief-source-fixture.py"
TEST = "tests/lean_python_extensions/test_belief_fixture.py"
DOC = "docs/gerbe-fixture.md"
CLASS = "FakeBeliefTests"
NAME = "tests.lean_python_extensions.test_belief_fixture.FakeBeliefTests"
SOURCE = b"import unittest\nclass FakeBeliefTests(unittest.TestCase):\n def test_one(self): pass\n"


class BeliefReceiptSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v018-sources-") as directory:
            root = Path(directory)
            for name, contents in ((ORIGINAL, b"unchanged\n"), (TEST, SOURCE), (DOC, b"scope\n")):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(contents)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS", {
                     ORIGINAL: prior.prior.prior.prior._git_blob(b"unchanged\n")}), \
                 patch.object(checker, "REQUIRED_PATHS", (ORIGINAL, TEST, DOC)), \
                 patch.object(checker, "TEST_CLASSES", {TEST: CLASS}):
                yield root

    def test_all_111_selected_original_git_blobs_and_new_regular_paths(self):
        self.assertEqual(checker.check_sources(ROOT), ())
        self.assertEqual(len(prior.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.REQUIRED_PATHS), 7)
        self.assertTrue(set(prior.REQUIRED_PATHS).issubset(checker.SOURCE_BLOBS))

    def test_three_ordinary_new_classes_have_actual_declarations(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 3)
        self.assertTrue(all(tests for tests in inventory.values()))
        own = "tests.lean_python_extensions.test_belief_receipt_sources_v0_18.BeliefReceiptSourceTests"
        self.assertEqual(len(inventory[own]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_preexisting_v017_sources_exact_and_original_checker_passes(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        for relative, original in checker.SOURCE_BLOBS.items():
            raw, issue = prior.prior.prior.prior._read_file(ROOT, relative)
            with self.subTest(relative=relative):
                self.assertIsNone(issue)
                self.assertEqual(prior.prior.prior.prior._git_blob(raw), original)

    def test_synthetic_checker_only_declares_tests_does_not_execute(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root), {NAME: ("test_one",)})

    def test_source_bytes_missing_symlink_and_directory_are_refused(self):
        with self.fixture() as root:
            (root / ORIGINAL).write_bytes(b"changed\n")
            self.assertIn("source_byte_drift:" + ORIGINAL, checker.check_sources(root))
        for kind in ("missing", "directory", "symlink"):
            with self.subTest(kind=kind), self.fixture() as root:
                path = root / ORIGINAL
                path.unlink()
                if kind == "directory":
                    path.mkdir()
                if kind == "symlink":
                    path.symlink_to(root / DOC)
                self.assertTrue(any(ORIGINAL in issue for issue in checker.check_sources(root)))

    def test_unparseable_wrong_duplicate_or_missing_declared_test_fails(self):
        for wrong in (b"class OtherTests:\n pass\n",
                      b"class FakeBeliefTests:\n pass\n",
                      b"class FakeBeliefTests:\n def test_a(self): pass\n def test_a(self): pass\n",
                      b"class FakeBeliefTests:\n def test_a(self):\n"):
            with self.subTest(content=wrong), self.fixture() as root:
                (root / TEST).write_bytes(wrong)
                self.assertEqual(checker.declared_test_inventory(root), {})
                self.assertTrue(any("required_test_declarations_missing" in x
                                    for x in checker.check_sources(root)))

    def test_root_and_required_new_paths_cannot_be_missing(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})
        for name in (DOC, TEST):
            with self.subTest(path=name), self.fixture() as root:
                (root / name).unlink()
                self.assertIn("required_v018_file_missing:" + name, checker.check_sources(root))


if __name__ == "__main__":
    unittest.main()
