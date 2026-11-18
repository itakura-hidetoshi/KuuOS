"""v0.20 independent additive source-pins and declaration tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_binary64_midpoint_sources_v0_20 as checker
from scripts import check_kuuos_lean_python_wa_rational_shadow_sources_v0_19 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/old_v020_fixture.py"
TEST = "tests/lean_python_extensions/test_fixture_v020.py"
FORMAL_A = "formal/KuuOSFormal/WaGridRoundingV0_20.lean"
FORMAL_B = "formal/KuuOSFormal/WaNeighborMidpointV0_20.lean"
DOC = "docs/fixture-v020.md"
CLASS = "FakeV020Tests"
CLASS_ID = "tests.lean_python_extensions.test_fixture_v020.FakeV020Tests"
BYTE_TEST = b"import unittest\nclass FakeV020Tests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_A = b"theorem gridRound_half_quantum : True := by trivial\n"
BYTE_B = b"theorem observed_neighbor_midpoint_error : True := by trivial\n"


class WaBinary64MidpointSourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v020-pins-") as folder:
            root = Path(folder)
            for name, content in ((OLD, b"fixed\n"), (TEST, BYTE_TEST),
                                  (FORMAL_A, BYTE_A), (FORMAL_B, BYTE_B),
                                  (DOC, b"scope\n")):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS", {OLD: checker._BASE._git_blob(b"fixed\n")}), \
                 patch.object(checker, "REQUIRED_PATHS", (OLD, FORMAL_A, FORMAL_B, TEST, DOC)), \
                 patch.object(checker, "TEST_CLASSES", {TEST: CLASS}):
                yield root

    def test_actual_124_predecessor_blob_pins_and_seven_new_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 6)
        self.assertEqual(len(checker.REQUIRED_PATHS), 7)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_actual_two_new_test_classes_have_unique_declarations(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(value for value in inventory.values()))
        self_key = "tests.lean_python_extensions.test_wa_binary64_midpoint_sources_v0_20.WaBinary64MidpointSourceTests"
        self.assertEqual(len(inventory[self_key]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_six_v019_original_blobs_are_byte_preserved(self):
        for path, sha in checker.SOURCE_BLOBS.items():
            data, issue = checker._BASE._read_file(ROOT, path)
            with self.subTest(path=path):
                self.assertIsNone(issue)
                self.assertEqual(checker._BASE._git_blob(data), sha)

    def test_static_fixture_does_not_execute_tests_or_elaborate_lean(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root), {CLASS_ID: ("test_one",)})

    def test_missing_or_drifted_lean_declaration_blocks(self):
        with self.fixture() as root:
            (root / FORMAL_B).write_bytes(b"theorem unrelated : True := by trivial\n")
            self.assertIn("required_v020_proof_declaration_missing:" + FORMAL_B,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL_A).unlink()
            self.assertIn("required_v020_file_missing:" + FORMAL_A, checker.check_sources(root))

    def test_changed_historical_source_and_missing_test_block(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"drift\n")
            self.assertIn("source_byte_drift:" + OLD, checker.check_sources(root))
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class WrongTests: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in x
                                for x in checker.check_sources(root)))

    def test_unknown_root_yields_no_data(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
