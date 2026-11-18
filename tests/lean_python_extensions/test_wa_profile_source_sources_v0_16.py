"""Selected v0.16 source pins, inventory and static declaration tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from scripts import check_kuuos_lean_python_wa_profile_source_sources_v0_16 as checker
from scripts import check_kuuos_lean_python_wa_evaluation_sources_v0_15 as prior

ROOT = Path(__file__).resolve().parents[2]
FAKE_ORIGINAL = "runtime/fixed.py"
FAKE_TEST = "tests/lean_python_extensions/test_fixture.py"
FAKE_DOC = "docs/fixed-v016.md"
FAKE_CLASS = "FixtureTests"
FAKE_NAME = "tests.lean_python_extensions.test_fixture.FixtureTests"
FAKE_BYTES = (
    b"import unittest\nclass FixtureTests(unittest.TestCase):\n"
    b"    def test_one(self):\n        pass\n"
)


class WaProfileSourceSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v016-pins-") as directory:
            root = Path(directory)
            for relative, value in ((FAKE_ORIGINAL, b"hello\n"),
                                    (FAKE_TEST, FAKE_BYTES),
                                    (FAKE_DOC, b"source witness\n")):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(value)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS",
                              {FAKE_ORIGINAL: prior.prior._git_blob(b"hello\n")}), \
                 patch.object(checker, "REQUIRED_PATHS",
                              (FAKE_ORIGINAL, FAKE_TEST, FAKE_DOC)), \
                 patch.object(checker, "TEST_CLASSES", {FAKE_TEST: FAKE_CLASS}):
                yield root

    def test_actual_original_sources_are_retained_and_all_new_files_present(self):
        self.assertEqual(checker.check_sources(ROOT), ())
        self.assertEqual(len(prior.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.SOURCE_BLOBS), 7)
        self.assertEqual(len(checker.REQUIRED_PATHS), 7)
        self.assertEqual(len(prior.prior.SOURCE_BLOBS), 83)
        self.assertTrue(set(prior.REQUIRED_PATHS).issubset(checker.SOURCE_BLOBS))

    def test_three_new_classes_have_ordinary_declared_test_methods(self):
        inventory = checker.declared_test_inventory(ROOT)
        expected = {
            "tests.lean_python_extensions.test_wa_profile_source_guard_v0_16.WaProfileSourceGuardTests",
            "tests.lean_python_extensions.test_wa_profile_source_native_cycle_v0_16.WaProfileSourceNativeCycleTests",
            "tests.lean_python_extensions.test_wa_profile_source_sources_v0_16.WaProfileSourceSourceTests",
        }
        self.assertEqual(set(inventory), expected)
        self.assertTrue(all(methods for methods in inventory.values()))
        own = "tests.lean_python_extensions.test_wa_profile_source_sources_v0_16.WaProfileSourceSourceTests"
        self.assertEqual(len(inventory[own]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_prior_checker_and_all_seven_v015_pins_are_unmodified(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        for relative, original_blob in checker.SOURCE_BLOBS.items():
            raw, issue = prior.prior._read_file(ROOT, relative)
            with self.subTest(path=relative):
                self.assertIsNone(issue)
                self.assertEqual(prior.prior._git_blob(raw), original_blob)

    def test_static_fixture_passes_without_importing_or_running_test_code(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root), {FAKE_NAME: ("test_one",)})

    def test_original_blob_drift_is_rejected(self):
        with self.fixture() as root:
            target = root / FAKE_ORIGINAL
            target.write_bytes(b"modified\n")
            self.assertIn("source_byte_drift:" + FAKE_ORIGINAL, checker.check_sources(root))

    def test_missing_source_and_symlink_are_rejected(self):
        for kind in ("missing", "symlink", "directory"):
            with self.subTest(kind=kind), self.fixture() as root:
                target = root / FAKE_ORIGINAL
                target.unlink()
                if kind == "symlink":
                    target.symlink_to(root / FAKE_DOC)
                elif kind == "directory":
                    target.mkdir()
                code = {"missing": "missing", "symlink": "symlink_not_allowed",
                        "directory": "not_regular_file"}[kind]
                self.assertIn("source_" + code + ":" + FAKE_ORIGINAL, checker.check_sources(root))

    def test_new_file_and_new_test_must_exist_when_checker_is_invoked(self):
        for name in (FAKE_DOC, FAKE_TEST):
            with self.subTest(name=name), self.fixture() as root:
                (root / name).unlink()
                self.assertIn("required_v016_file_missing:" + name, checker.check_sources(root))

    def test_duplicate_or_invalid_ast_class_cannot_be_accepted(self):
        for case in (
            b"class WrongTests:\n def test_one(self): pass\n",
            b"class FixtureTests:\n def test_one(self): pass\n def test_one(self): pass\n",
            b"class FixtureTests:\n pass\n",
            b"class FixtureTests:\n def test_not_finished(self):\n",
        ):
            with self.subTest(case=case), self.fixture() as root:
                (root / FAKE_TEST).write_bytes(case)
                self.assertEqual(checker.declared_test_inventory(root), {})
                self.assertIn("required_test_declarations_missing_or_invalid:" + FAKE_NAME,
                              checker.check_sources(root))

    def test_wrong_root_is_no_data_not_silent_success(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})

    def test_every_pin_detects_local_drift_when_original_checker_runs(self):
        with TemporaryDirectory(prefix="kuuos-v016-all-pins-") as directory:
            root = Path(directory)
            for relative in checker.SOURCE_BLOBS:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "REQUIRED_PATHS", ()), \
                 patch.object(checker, "TEST_CLASSES", {}):
                self.assertEqual(checker.check_sources(root), ())
                for relative in checker.SOURCE_BLOBS:
                    target = root / relative
                    before = target.read_bytes()
                    try:
                        target.write_bytes(before + b" altered\n")
                        self.assertIn("source_byte_drift:" + relative, checker.check_sources(root))
                    finally:
                        target.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
