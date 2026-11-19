"""v0.41 original Decision and Belief source pin regression.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_decision_store_origin_sources_v0_41 as checker,
)


class NativeDecisionStoreOriginSourceTests(unittest.TestCase):
    def test_new_and_inherited_source_pins_pass(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_original_decision_kernel_store_and_constructor_are_pinned(self):
        for path in (
            "runtime/kuuos_decision_os_store_v0_1.py",
            "runtime/kuuos_decision_os_state_v0_1.py",
            "runtime/kuuos_decision_os_kernel_v0_1.py",
            "runtime/kuuos_decision_os_types_v0_1.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v041_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_lean_decision_history_source_drift_blocks(self):
        path = "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v041_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_belief_receipt_type_and_digest_source_drift_blocks(self):
        path = "runtime/kuuos_belief_os_gerbe_types_v0_3.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v041_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_retained_plural_auditor_and_source_checker_are_immutable(self):
        for path in (
            "runtime/kuuos_lean_python_plural_store_origin_v0_40.py",
            "scripts/check_kuuos_lean_python_plural_store_origin_sources_v0_40.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v041_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_missing_new_file_is_blocked(self):
        path = "runtime/absent-v041-file.py"
        with patch.object(checker, "NEW", checker.NEW + (path,)):
            self.assertIn("v041_new_file_missing:" + path,
                          checker.check_sources(checker.ROOT))

    def test_inventory_has_actual_suffix_and_timing_obstruction_tests(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.TEST_CLASSES))
        tests = inventory[checker.NEW[2]]
        self.assertIn("test_real_suffix_history_is_native_valid_but_not_original_genesis",
                      tests)
        self.assertIn("test_fixture_numeric_times_are_inverted_without_clock_proof",
                      tests)
        self.assertGreaterEqual(len(tests), 25)

    def test_untrusted_root_custom_hook_is_not_invoked(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("custom source-root conversion invoked")
        for root in (None, str(checker.ROOT), HostileRoot()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(root), {})

    def test_source_root_and_ancestor_symlinks_block(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias),
                             ("root:trusted_path_required",))
            alias.unlink()
            alias.symlink_to(checker.ROOT.parent, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias / checker.ROOT.name),
                             ("root:trusted_path_required",))

    def test_source_parent_traversal_blocks(self):
        fake = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(checker.check_sources(fake),
                         ("root:trusted_path_required",))
        self.assertEqual(checker.test_inventory(fake), {})


if __name__ == "__main__":
    unittest.main()
