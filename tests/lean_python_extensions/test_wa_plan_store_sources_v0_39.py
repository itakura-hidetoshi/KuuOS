"""v0.39 exact original constructors/stores and inherited source continuity.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import check_kuuos_lean_python_wa_plan_store_sources_v0_39 as checker


class NativeWaPlanStoreSourceTests(unittest.TestCase):
    def test_original_and_inherited_source_inventories_match(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_original_constructor_drift_blocks(self):
        for path in (
            "runtime/kuuos_decision_os_wa_state_v0_3.py",
            "runtime/kuuos_plan_os_state_v0_1.py",
        ):
            with self.subTest(path=path), patch.dict(checker.PINNED, {path: "0" * 40}):
                self.assertIn("v039_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_store_drift_blocks(self):
        for path in (
            "runtime/kuuos_decision_os_wa_store_v0_3.py",
            "runtime/kuuos_plan_os_store_v0_1.py",
        ):
            with self.subTest(path=path), patch.dict(checker.PINNED, {path: "0" * 40}):
                self.assertIn("v039_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_lean_scope_cannot_be_rebound(self):
        paths = (
            "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean",
            "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean",
            "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean",
        )
        for path in paths:
            with self.subTest(path=path), patch.dict(checker.PINNED, {path: "0" * 40}):
                self.assertIn("v039_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_retained_v038_checker_cannot_be_replaced(self):
        path = "scripts/check_kuuos_lean_python_five_store_chain_sources_v0_38.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v039_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_required_new_source_is_reported(self):
        with patch.object(checker, "NEW", checker.NEW + ("runtime/absent_v039.py",)):
            self.assertIn("v039_new_file_missing:runtime/absent_v039.py",
                          checker.check_sources(checker.ROOT))

    def test_real_origin_and_source_regressions_are_discoverable(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.CLASSES))
        origin_tests = inventory[checker.NEW[2]]
        self.assertIn("test_wa_suffix_history_cannot_replace_original_genesis", origin_tests)
        self.assertIn("test_plan_suffix_history_cannot_replace_original_genesis", origin_tests)
        self.assertGreaterEqual(len(origin_tests), 20)

    def test_untrusted_root_does_not_invoke_user_hooks(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("custom root conversion executed")
        for root in (None, str(checker.ROOT), HostilePath()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))

    def test_source_root_symlink_is_not_trusted(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(alias), {})

    def test_source_root_parent_symlink_is_not_trusted(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(checker.ROOT.parent, target_is_directory=True)
            root = alias / checker.ROOT.name
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(root), {})

    def test_inventory_rejects_custom_root_before_path_operations(self):
        class HostileRoot:
            def __truediv__(self, other):
                raise AssertionError("untrusted path operation executed")
        self.assertEqual(checker.test_inventory(HostileRoot()), {})

    def test_source_root_parent_traversal_is_not_trusted(self):
        root = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(checker.check_sources(root),
                         ("root:trusted_path_required",))
        self.assertEqual(checker.test_inventory(root), {})


if __name__ == "__main__":
    unittest.main()
