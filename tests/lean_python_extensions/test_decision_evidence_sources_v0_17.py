"""v0.17 predecessor source pins, declaration inventory and drift tests.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from scripts import check_kuuos_lean_python_decision_evidence_sources_v0_17 as checker
from scripts import check_kuuos_lean_python_wa_profile_source_sources_v0_16 as prior

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = "runtime/original_fixture.py"
NEW_TEST = "tests/lean_python_extensions/fixture.py"
NEW_DOC = "docs/v017-fixture.md"
TEST_CLASS = "TemporaryEvidenceTests"
TEST_NAME = "tests.lean_python_extensions.fixture.TemporaryEvidenceTests"
BYTES = b"import unittest\nclass TemporaryEvidenceTests(unittest.TestCase):\n def test_one(self): pass\n"


class DecisionEvidenceSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v017-static-") as directory:
            root = Path(directory)
            for name, value in ((ORIGINAL, b"original\n"), (NEW_TEST, BYTES), (NEW_DOC, b"boundary\n")):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(value)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS", {
                     ORIGINAL: prior.prior.prior._git_blob(b"original\n")}), \
                 patch.object(checker, "REQUIRED_PATHS", (ORIGINAL, NEW_TEST, NEW_DOC)), \
                 patch.object(checker, "TEST_CLASSES", {NEW_TEST: TEST_CLASS}):
                yield root

    def test_all_104_selected_historical_blobs_retained_and_new_files_present(self):
        self.assertEqual(checker.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 7)
        self.assertEqual(len(prior.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.REQUIRED_PATHS), 7)
        self.assertTrue(set(prior.REQUIRED_PATHS).issubset(checker.SOURCE_BLOBS))

    def test_three_test_classes_have_nonempty_unique_ast_declarations(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 3)
        self.assertTrue(all(methods for methods in inventory.values()))
        own = "tests.lean_python_extensions.test_decision_evidence_sources_v0_17.DecisionEvidenceSourceTests"
        self.assertEqual(len(inventory[own]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_original_predecessor_checker_and_exact_blobs_unchanged(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        for name, sha in checker.SOURCE_BLOBS.items():
            raw, issue = prior.prior.prior._read_file(ROOT, name)
            with self.subTest(name=name):
                self.assertIsNone(issue)
                self.assertEqual(prior.prior.prior._git_blob(raw), sha)

    def test_static_fixture_is_only_declaration_not_execution(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root), {TEST_NAME: ("test_one",)})

    def test_source_drift_missing_and_symlink_rejected(self):
        with self.fixture() as root:
            path = root / ORIGINAL
            path.write_bytes(b"changed\n")
            self.assertIn("source_byte_drift:" + ORIGINAL, checker.check_sources(root))
        for case in ("missing", "directory", "symlink"):
            with self.subTest(case=case), self.fixture() as root:
                path = root / ORIGINAL
                path.unlink()
                if case == "directory":
                    path.mkdir()
                if case == "symlink":
                    path.symlink_to(root / NEW_DOC)
                self.assertTrue(any(ORIGINAL in issue for issue in checker.check_sources(root)))

    def test_unparseable_or_duplicate_declared_test_class_is_rejected(self):
        for content in (b"class Wrong:\n pass\n", b"class TemporaryEvidenceTests:\n pass\n",
                        b"class TemporaryEvidenceTests:\n def test_x(self): pass\n def test_x(self): pass\n"):
            with self.subTest(data=content), self.fixture() as root:
                (root / NEW_TEST).write_bytes(content)
                self.assertEqual(checker.declared_test_inventory(root), {})
                self.assertTrue(any("required_test_declarations_missing" in p
                                    for p in checker.check_sources(root)))

    def test_missing_new_file_and_bad_root_fail_closed(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        for name in (NEW_DOC, NEW_TEST):
            with self.subTest(name=name), self.fixture() as root:
                (root / name).unlink()
                self.assertIn("required_v017_file_missing:" + name, checker.check_sources(root))


if __name__ == "__main__":
    unittest.main()
