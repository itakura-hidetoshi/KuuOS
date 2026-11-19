"""v0.42 exact original Belief source pins and retained v0.41 audit coverage.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_belief_gerbe_store_sources_v0_42 as checker,
)


class NativeBeliefGerbeStoreOriginSourceTests(unittest.TestCase):
    def test_all_old_and_new_sources_match(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_original_gerbe_store_and_type_code_is_exact(self):
        for path in (
            "runtime/kuuos_belief_os_gerbe_store_v0_3.py",
            "runtime/kuuos_belief_os_gerbe_types_v0_3.py",
            "runtime/kuuos_belief_os_gerbe_coherence_v0_3.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v042_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_existing_v018_receipt_replay_cannot_be_rebound(self):
        path = "runtime/kuuos_lean_python_belief_receipt_guard_v0_18.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v042_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_original_lean_gerbe_source_is_pinned(self):
        path = "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn(
                "v042_original_source_changed:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_v041_auditor_and_source_checker_are_retained(self):
        for path in (
            "runtime/kuuos_lean_python_decision_store_origin_v0_41.py",
            "scripts/check_kuuos_lean_python_decision_store_origin_sources_v0_41.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v042_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_missing_new_file_is_never_silently_accepted(self):
        missing = "runtime/absent_v042_file.py"
        with patch.object(checker, "NEW", checker.NEW + (missing,)):
            self.assertIn(
                "v042_new_file_missing:" + missing,
                checker.check_sources(checker.ROOT),
            )

    def test_inventory_has_real_last_receipt_and_origin_tests(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.TEST_CLASSES))
        tests = inventory[checker.NEW[2]]
        self.assertIn(
            "test_v018_reconstructs_exact_last_original_receipt", tests,
        )
        self.assertIn(
            "test_alternative_origin_from_valid_final_has_empty_history_obstruction",
            tests,
        )
        self.assertGreaterEqual(len(tests), 20)

    def test_untrusted_root_cannot_run_user_path_hooks(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("unexpected path hook")
        for value in (None, str(checker.ROOT), HostileRoot()):
            self.assertEqual(
                checker.check_sources(value), ("root:trusted_path_required",),
            )
            self.assertEqual(checker.test_inventory(value), {})

    def test_symlink_or_parent_symlink_to_source_blocks(self):
        with TemporaryDirectory() as d:
            link = Path(d) / "link"
            link.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(
                checker.check_sources(link), ("root:trusted_path_required",),
            )
            link.unlink()
            link.symlink_to(checker.ROOT.parent, target_is_directory=True)
            self.assertEqual(
                checker.check_sources(link / checker.ROOT.name),
                ("root:trusted_path_required",),
            )

    def test_parent_traversal_in_source_root_blocks(self):
        root = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(
            checker.check_sources(root), ("root:trusted_path_required",),
        )
        self.assertEqual(checker.test_inventory(root), {})


if __name__ == "__main__":
    unittest.main()
