"""v0.44 exact original semantic-bridge source and finite proof inventory.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_python_finite_evidence_sources_v0_44 as checker


class FiniteEvidenceSourceTests(unittest.TestCase):
    def test_original_and_inherited_sources_are_unchanged(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_retained_middle_way_formal_source_is_exact(self):
        path = "formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v044_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_retained_python_join_runtime_source_is_exact(self):
        path = "runtime/kuuos_lean_python_middle_way_semantic_bridge_v0_43.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v044_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_previous_source_pin_checker_is_pinned(self):
        path = "scripts/check_kuuos_lean_python_middle_way_semantic_sources_v0_43.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v044_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_formal_v044_proof_has_four_model_definitions_and_nine_theorems(self):
        raw, issue = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(issue)
        lines = tuple(line.strip() for line in raw.decode("utf-8").splitlines())
        self.assertEqual(len(checker.LEAN_DEFINITIONS), 4)
        self.assertEqual(len(checker.LEAN_DECLARATIONS), 9)
        for name in checker.LEAN_DEFINITIONS + checker.LEAN_DECLARATIONS:
            self.assertTrue(any(
                line == name or line.startswith(name + " ")
                or line.startswith(name + ":") for line in lines
            ), name)

    def test_v044_lean_source_uses_correct_original_import(self):
        raw, issue = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(issue)
        lines = raw.decode("utf-8").splitlines()
        for item in checker.LEAN_IMPORTS:
            self.assertIn(item, lines)
        self.assertNotIn("sorry", lines)
        self.assertNotIn("axiom", lines)

    def test_no_missing_new_test_or_lean_file_can_be_accepted(self):
        missing = "formal/KUOS/Architecture/AbsentEvidenceWitnessV0_44.lean"
        with patch.object(checker, "NEW", checker.NEW + (missing,)):
            self.assertIn("v044_new_file_missing:" + missing,
                          checker.check_sources(checker.ROOT))

    def test_real_regression_tests_discoverable_without_duplicate_classes(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.TEST_CLASSES))
        main_tests = inventory[checker.NEW[3]]
        self.assertIn("test_original_python_three_status_pairs_all_nine",
                      main_tests)
        self.assertIn("test_native_real_nine_stores_with_model_is_locally_usable",
                      main_tests)
        self.assertIn("test_original_join_mutation_cannot_pass_finite_model",
                      main_tests)
        self.assertGreaterEqual(len(main_tests), 20)

    def test_root_hooks_are_never_invoked(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("unexpected root hook")
        for root in (None, str(checker.ROOT), HostileRoot()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(root), {})

    def test_parent_traversal_blocks_in_static_checker(self):
        root = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(checker.check_sources(root),
                         ("root:trusted_path_required",))
        self.assertEqual(checker.test_inventory(root), {})

    def test_original_source_symlink_and_parent_symlink_are_untrusted(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias),
                             ("root:trusted_path_required",))
            alias.unlink()
            alias.symlink_to(checker.ROOT.parent, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias / checker.ROOT.name),
                             ("root:trusted_path_required",))


if __name__ == "__main__":
    unittest.main()
