"""Static identity and declared test inventory tests for v0.15.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from scripts import check_kuuos_lean_python_wa_evaluation_sources_v0_15 as checker
from scripts import check_kuuos_lean_python_wa_gate_sources_v0_14 as prior

ROOT = Path(__file__).resolve().parents[2]
FAKE_SOURCE = "runtime/source.py"
FAKE_TEST = "tests/lean_python_extensions/test_source.py"
FAKE_DOC = "docs/required.md"
FAKE_KLASS = "RequiredTests"
FAKE_TEST_CLASS = "tests.lean_python_extensions.test_source.RequiredTests"
FAKE_TEST_BYTES = (
    b"import unittest\nclass RequiredTests(unittest.TestCase):\n"
    b"    def test_one(self):\n        pass\n"
)


class WaEvaluationSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v015-static-") as directory:
            root = Path(directory)
            for path, data in ((FAKE_SOURCE, b"hello\n"), (FAKE_TEST, FAKE_TEST_BYTES),
                               (FAKE_DOC, b"documentation\n")):
                location = root / path
                location.parent.mkdir(parents=True, exist_ok=True)
                location.write_bytes(data)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS", {FAKE_SOURCE: prior._git_blob(b"hello\n")}), \
                 patch.object(checker, "REQUIRED_PATHS", (FAKE_SOURCE, FAKE_TEST, FAKE_DOC)), \
                 patch.object(checker, "TEST_CLASSES", {FAKE_TEST: FAKE_KLASS}):
                yield root

    def test_actual_sources_are_pinned_and_required(self):
        self.assertEqual(checker.check_sources(ROOT), ())
        self.assertEqual(len(prior.SOURCE_BLOBS), 83)
        self.assertEqual(len(checker.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.REQUIRED_PATHS), 7)
        self.assertTrue(set(prior.REQUIRED_PATHS).issubset(checker.SOURCE_BLOBS))

    def test_all_three_new_test_classes_have_declared_methods(self):
        inventory = checker.declared_test_inventory(ROOT)
        expected = {
            "tests.lean_python_extensions.test_wa_evaluation_guard_v0_15.WaEvaluationGuardTests",
            "tests.lean_python_extensions.test_wa_evaluation_native_cycle_v0_15.WaEvaluationNativeCycleTests",
            "tests.lean_python_extensions.test_wa_evaluation_sources_v0_15.WaEvaluationSourceTests",
        }
        self.assertEqual(set(inventory), expected)
        self.assertTrue(all(methods for methods in inventory.values()))
        own = "tests.lean_python_extensions.test_wa_evaluation_sources_v0_15.WaEvaluationSourceTests"
        self.assertEqual(len(inventory[own]), unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_preserved_v014_source_hashes_are_verified_independently(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        for relative, expected in checker.SOURCE_BLOBS.items():
            raw, problem = prior._read_file(ROOT, relative)
            with self.subTest(path=relative):
                self.assertIsNone(problem)
                self.assertEqual(prior._git_blob(raw), expected)

    def test_actual_test_declarations_are_not_executed_by_static_check(self):
        with self.fixture() as root:
            self.assertEqual(checker.declared_test_inventory(root), {FAKE_TEST_CLASS: ("test_one",)})
            self.assertEqual(checker.check_sources(root), ())

    def test_original_blob_drift_is_detected(self):
        with self.fixture() as root:
            source = root / FAKE_SOURCE
            source.write_bytes(b"changed\n")
            self.assertIn("source_byte_drift:" + FAKE_SOURCE, checker.check_sources(root))

    def test_original_missing_symlink_and_directory_are_rejected(self):
        for kind in ("missing", "symlink", "directory"):
            with self.subTest(kind=kind), self.fixture() as root:
                source = root / FAKE_SOURCE
                source.unlink()
                if kind == "symlink":
                    source.symlink_to(root / FAKE_DOC)
                elif kind == "directory":
                    source.mkdir()
                problem = {"missing": "missing", "symlink": "symlink_not_allowed",
                           "directory": "not_regular_file"}[kind]
                self.assertIn("source_" + problem + ":" + FAKE_SOURCE, checker.check_sources(root))

    def test_required_new_file_and_test_are_required_when_invoked(self):
        for relative in (FAKE_DOC, FAKE_TEST):
            with self.subTest(path=relative), self.fixture() as root:
                (root / relative).unlink()
                self.assertIn("required_v015_file_missing:" + relative, checker.check_sources(root))

    def test_missing_or_duplicate_direct_test_declarations_are_blocked(self):
        for source in (
            b"class RequiredTests:\n    pass\n",
            b"class RequiredTests:\n    def test_one(self): pass\n"
            b"    def test_one(self): pass\n",
            b"class DifferentTests:\n    def test_one(self): pass\n",
            b"def test_one(): pass\n",
            b"class RequiredTests:\n    def test_not_closed(self):\n",
        ):
            with self.subTest(source=source), self.fixture() as root:
                (root / FAKE_TEST).write_bytes(source)
                self.assertEqual(checker.declared_test_inventory(root), {})
                self.assertIn("required_test_declarations_missing_or_invalid:" + FAKE_TEST_CLASS,
                              checker.check_sources(root))

    def test_non_path_root_fails_closed(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
