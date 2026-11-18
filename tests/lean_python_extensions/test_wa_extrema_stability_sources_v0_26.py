"""v0.26 immutable source pin and test inventory checks.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_extrema_stability_sources_v0_26 as checker
from scripts import check_kuuos_lean_python_wa_finite_extrema_sources_v0_25 as prior

ROOT = Path(__file__).resolve().parents[2]
OLD = "runtime/v026_previous_fixture.py"
FORMAL = "formal/KuuOSFormal/WaExtremaStabilityV0_26.lean"
TEST = "tests/lean_python_extensions/test_v026_fixture.py"
DOC = "docs/v026_fixture.md"
CLASS = "V026FixtureTests"
CLASS_ID = "tests.lean_python_extensions.test_v026_fixture.V026FixtureTests"
BYTE_TEST = b"import unittest\nclass V026FixtureTests(unittest.TestCase):\n def test_one(self): pass\n"
BYTE_FORMAL = b"".join(
    ("theorem " + name + " : True := by trivial\n").encode("utf-8")
    for name in (
        "rational_ideal_weakest_nonexpansive",
        "rational_ideal_alert_nonexpansive",
        "rational_ideal_two_extrema_stability",
        "observed_wa_with_extrema_error",
        "native_normalized_wa_with_extrema_error",
        "native_normalized_wa_with_extrema_real",
    )
)


class WaExtremaStabilitySourceTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with TemporaryDirectory(prefix="kuuos-v026-sources-") as folder:
            root = Path(folder)
            for path, raw in ((OLD, b"previous\n"), (FORMAL, BYTE_FORMAL),
                              (TEST, BYTE_TEST), (DOC, b"scope\n")):
                f = root / path
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_bytes(raw)
            with patch.object(prior, "check_sources", return_value=()), \
                 patch.object(checker, "SOURCE_BLOBS",
                              {OLD: checker._BASE._git_blob(b"previous\n")}), \
                 patch.object(checker, "REQUIRED_PATHS",
                              (OLD, FORMAL, TEST, DOC)), \
                 patch.object(checker, "TEST_CLASSES", {TEST: CLASS}):
                yield root

    def test_all_161_predecessor_source_pins_and_six_additive_paths(self):
        self.assertEqual(prior.check_sources(ROOT), ())
        self.assertEqual(len(checker.SOURCE_BLOBS), 6)
        self.assertEqual(len(checker.REQUIRED_PATHS), 6)
        self.assertEqual(checker.check_sources(ROOT), ())

    def test_unique_declared_new_test_classes_are_registered(self):
        inventory = checker.declared_test_inventory(ROOT)
        self.assertEqual(len(inventory), 2)
        self.assertTrue(all(methods for methods in inventory.values()))
        key = "tests.lean_python_extensions.test_wa_extrema_stability_sources_v0_26.WaExtremaStabilitySourceTests"
        self.assertEqual(len(inventory[key]),
                         unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases())

    def test_all_v025_blob_identities_are_preserved(self):
        for path, sha in checker.SOURCE_BLOBS.items():
            raw, issue = checker._BASE._read_file(ROOT, path)
            with self.subTest(path=path):
                self.assertIsNone(issue)
                self.assertEqual(checker._BASE._git_blob(raw), sha)

    def test_pure_fixture_static_source_check_has_no_runtime_effect(self):
        with self.fixture() as root:
            self.assertEqual(checker.check_sources(root), ())
            self.assertEqual(checker.declared_test_inventory(root),
                             {CLASS_ID: ("test_one",)})

    def test_mutated_predecessor_source_is_detected(self):
        with self.fixture() as root:
            (root / OLD).write_bytes(b"rewritten\n")
            self.assertIn("source_byte_drift:" + OLD,
                          checker.check_sources(root))

    def test_missing_or_mutated_lean_theorem_markers_block(self):
        with self.fixture() as root:
            (root / FORMAL).write_bytes(b"theorem unrelated : True := by trivial\n")
            self.assertIn("required_v026_proof_declaration_missing:" + FORMAL,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / FORMAL).unlink()
            self.assertIn("required_v026_file_missing:" + FORMAL,
                          checker.check_sources(root))

    def test_missing_doc_or_suppressed_tests_are_not_accepted(self):
        with self.fixture() as root:
            (root / DOC).unlink()
            self.assertIn("required_v026_file_missing:" + DOC,
                          checker.check_sources(root))
        with self.fixture() as root:
            (root / TEST).write_bytes(b"class Wrong: pass\n")
            self.assertTrue(any("required_test_declarations_missing" in x
                                for x in checker.check_sources(root)))

    def test_untrusted_root_remains_no_data(self):
        self.assertEqual(checker.check_sources(None), ("root:trusted_path_required",))
        self.assertEqual(checker.declared_test_inventory(None), {})


if __name__ == "__main__":
    unittest.main()
