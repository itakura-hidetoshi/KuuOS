"""v0.40 exact original Plural Lean/store sources and additive tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_plural_store_origin_sources_v0_40 as checker,
)


class NativePluralStoreOriginSourceTests(unittest.TestCase):
    def test_previous_and_new_source_inventory_pass(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_native_plural_constructor_and_store_are_pinned(self):
        for path in (
            "runtime/kuuos_decision_os_plural_store_v0_2.py",
            "runtime/kuuos_decision_os_plural_kernel_v0_2.py",
            "runtime/kuuos_decision_os_plural_types_v0_2.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v040_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_the_lean_plural_proof_source_is_pinned_not_inferred(self):
        path = "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("v040_original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_v039_auditor_and_checker_are_immutable_dependencies(self):
        for path in (
            "runtime/kuuos_lean_python_wa_plan_store_compat_v0_39.py",
            "scripts/check_kuuos_lean_python_wa_plan_store_sources_v0_39.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v040_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_missing_new_file_is_a_source_failure(self):
        missing = "runtime/v040_absent_original.py"
        with patch.object(checker, "NEW", checker.NEW + (missing,)):
            self.assertIn(
                "v040_new_file_missing:" + missing,
                checker.check_sources(checker.ROOT),
            )

    def test_new_regression_inventory_is_locally_discoverable(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.TEST_CLASSES))
        tests = inventory[checker.NEW[2]]
        self.assertIn(
            "test_native_suffix_can_replay_but_is_not_original_plural_genesis",
            tests,
        )
        self.assertIn("test_original_plural_wa_plan_chain_is_scoped_compatible",
                      tests)
        self.assertGreaterEqual(len(tests), 20)

    def test_untrusted_source_root_is_rejected_without_user_hook(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("untrusted __fspath__ called")
        for root in (None, str(checker.ROOT), HostileRoot()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(root), {})

    def test_symlink_source_root_or_parent_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(alias), {})
            parent = Path(d) / "parent"
            parent.symlink_to(checker.ROOT.parent, target_is_directory=True)
            self.assertEqual(
                checker.check_sources(parent / checker.ROOT.name),
                ("root:trusted_path_required",),
            )

    def test_source_parent_traversal_is_blocked(self):
        fake = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(checker.check_sources(fake),
                         ("root:trusted_path_required",))
        self.assertEqual(checker.test_inventory(fake), {})


if __name__ == "__main__":
    unittest.main()
