"""v0.43 exact Lean theorem declarations, source pins, and test discovery.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_middle_way_semantic_sources_v0_43 as checker,
)


class MiddleWaySemanticSourceTests(unittest.TestCase):
    def test_prior_and_current_source_checks(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_exact_original_belief_and_five_store_runtime_source_pins(self):
        for path in (
            "runtime/kuuos_lean_python_belief_gerbe_store_origin_v0_42.py",
            "runtime/kuuos_lean_python_five_store_chain_compat_v0_38.py",
            "scripts/check_kuuos_lean_python_belief_gerbe_store_sources_v0_42.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v043_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_exact_middle_way_verify_plan_and_codeai_lean_import_pins(self):
        for path in (
            "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean",
            "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
            "formal/KUOS/CodeAI/VersionBoundRepairMemoryV0_1.lean",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v043_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_original_proven_history_theorem_sources_are_pinned(self):
        for path in (
            "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean",
            "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean",
            "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean",
            "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn(
                    "v043_original_source_changed:" + path,
                    checker.check_sources(checker.ROOT),
                )

    def test_eleven_conditional_lean_theorems_have_source_declarations(self):
        src, issue = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(issue)
        lines = tuple(line.strip() for line in src.decode("utf-8").splitlines())
        self.assertEqual(len(checker.LEAN_DECLARATIONS), 11)
        for name in checker.LEAN_DECLARATIONS:
            with self.subTest(name=name):
                self.assertTrue(
                    any(line == name or line.startswith(name + " ")
                        or line.startswith(name + ":") for line in lines),
                    name,
                )
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_lean_imports_are_original_exact_scope(self):
        src, issue = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(issue)
        lines = src.decode("utf-8").splitlines()
        for item in checker.LEAN_IMPORTS:
            self.assertIn(item, lines)
        self.assertIn("import Mathlib", lines)

    def test_new_file_absence_is_not_success(self):
        path = "formal/KUOS/Architecture/AbsentMiddleWay.lean"
        with patch.object(checker, "NEW", checker.NEW + (path,)):
            self.assertIn(
                "v043_new_file_missing:" + path,
                checker.check_sources(checker.ROOT),
            )

    def test_new_fixtures_and_decision_support_tests_are_discoverable(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.TEST_CLASSES))
        tests = inventory[checker.NEW[3]]
        self.assertIn(
            "test_original_nine_stores_are_locally_checked_under_one_plan_seam",
            tests,
        )
        self.assertIn(
            "test_codeai_memory_decision_plan_consume_advice_not_authority",
            tests,
        )
        self.assertIn(
            "test_seam_fingerprint_mismatch_blocks_despite_both_subaudits_success",
            tests,
        )
        self.assertGreaterEqual(len(tests), 20)

    def test_no_fake_lean_proof_or_derived_external_authority(self):
        from runtime.kuuos_lean_python_middle_way_semantic_bridge_v0_43 import (
            MiddleWaySemanticAudit, SCOPED_COMPATIBLE,
        )
        r = MiddleWaySemanticAudit(status=SCOPED_COMPATIBLE)
        for key in (
            "source_blobs_pinned_by_static_checker",
            "local_formal_simulation_witness_constructed",
            "universal_lean_python_semantic_refinement_proved",
            "global_descent_proved",
            "execution_authority_granted",
            "git_authority_granted",
        ):
            self.assertFalse(getattr(r, key), key)

    def test_root_hook_or_string_path_not_allowed_for_source_checker(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("unsafe root hook")
        for root in (None, str(checker.ROOT), HostileRoot()):
            self.assertEqual(
                checker.check_sources(root), ("root:trusted_path_required",),
            )
            self.assertEqual(checker.test_inventory(root), {})

    def test_source_symlink_and_parent_symlink_block(self):
        with TemporaryDirectory() as d:
            link = Path(d) / "alias"
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

    def test_parent_traversal_of_source_root_blocks(self):
        root = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(
            checker.check_sources(root), ("root:trusted_path_required",),
        )
        self.assertEqual(checker.test_inventory(root), {})


if __name__ == "__main__":
    unittest.main()
