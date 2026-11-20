"""v0.46 source pin/inventory tests, separate from formal Lean elaboration.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_decision_verify_plan_sources_v0_46 as checker,
)


class NativeDecisionVerifyPlanSourceTests(unittest.TestCase):
    def test_original_pins_and_new_source_inventory_pass(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_exact_original_decisionos_lean_and_python_pins(self):
        for path in (
            "formal/KUOS/DecisionOS/BoundedPlanSynthesisRequestHandoffV0_8.lean",
            "runtime/kuuos_decisionos_bounded_plan_synthesis_request_handoff_v0_8.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v046_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_verify_plan_lean_kernels_remain_unmodified(self):
        for path in (
            "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean",
            "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v046_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_verify_plan_python_kernels_remain_unmodified(self):
        for path in (
            "runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py",
            "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v046_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_test_fixture_source_is_not_rewritten(self):
        for path in (
            "scripts/check_decisionos_bounded_plan_synthesis_request_handoff_v0_8.py",
            "scripts/check_verifyos_middle_way_conditional_continuity_verification_v0_4.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v046_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_all_v045_changed_files_are_retained_as_exact_source(self):
        for path in (
            "formal/KUOS/Architecture/LeanPythonVerifyPlanSixRoutesV0_45.lean",
            "runtime/kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45.py",
            "scripts/check_kuuos_lean_python_middle_way_verify_plan_sources_v0_45.py",
            "tests/lean_python_extensions/test_middle_way_verify_plan_six_routes_v0_45.py",
            "tests/lean_python_extensions/test_middle_way_verify_plan_sources_v0_45.py",
            "docs/KUUOS_LEAN_PYTHON_MIDDLE_WAY_VERIFY_PLAN_SIX_ROUTES_v0_45.md",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v046_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_expected_original_imports_and_six_lean_declarations_exist(self):
        raw, problem = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(problem)
        source = raw.decode("utf-8")
        lines = tuple(x.strip() for x in source.splitlines())
        self.assertEqual(len(checker.LEAN_IMPORTS), 3)
        self.assertEqual(len(checker.LEAN_DECLARATIONS), 6)
        for name in checker.LEAN_IMPORTS:
            self.assertIn(name, lines)
        for name in checker.LEAN_DECLARATIONS:
            self.assertTrue(any(
                line == name or line.startswith(name + " ")
                or line.startswith(name + ":") for line in lines
            ), name)

    def test_new_test_class_and_original_kernel_tests_are_discoverable(self):
        inventory = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(inventory), set(checker.TEST_CLASSES))
        native = inventory[checker.NEW[3]]
        self.assertIn("test_original_three_kernel_builders_execute_all_six_routes",
                      native)
        self.assertIn("test_original_decision_to_verify_full_packet_substitution_is_blocked",
                      native)
        self.assertIn("test_only_retain_has_bounded_intake_not_plan_synthesis",
                      native)
        self.assertGreaterEqual(len(native), 20)

    def test_noncode_lean_tokens_do_not_trigger_false_unproved_claim(self):
        self.assertFalse(checker.prior._contains_unproved_lean(
            'def admittedForStatus := true\n/- sorry admit axiom -/\n'
            'def literal := "sorry"\n'
        ))

    def test_actual_lean_proof_holes_are_distinguished(self):
        for term in ("sorry", "admit", "axiom"):
            with self.subTest(term=term):
                self.assertTrue(checker.prior._contains_unproved_lean(
                    "theorem unavailable : True := by " + term
                ))

    def test_missing_new_file_cannot_be_silently_skipped(self):
        fake = "formal/KUOS/Architecture/UnseenV046.lean"
        with patch.object(checker, "NEW", checker.NEW + (fake,)):
            self.assertIn("v046_new_file_missing:" + fake,
                          checker.check_sources(checker.ROOT))

    def test_wrong_original_source_pin_cannot_hide_provenance_drift(self):
        with patch.dict(
            checker.PINNED,
            {"runtime/kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45.py":
             "f" * 40},
        ):
            self.assertNotEqual(checker.check_sources(checker.ROOT), ())

    def test_no_untrusted_path_coercion_or_nonpath_root_is_executed(self):
        class Hostile:
            def __fspath__(self):
                raise AssertionError("side-effectful path hook")
        for root in (None, str(checker.ROOT), Hostile()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(root), {})

    def test_source_parent_symlinks_are_rejected(self):
        with TemporaryDirectory() as temp:
            alias = Path(temp) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias),
                             ("root:trusted_path_required",))

    def test_traversed_source_root_is_rejected(self):
        alias = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(checker.check_sources(alias),
                         ("root:trusted_path_required",))

    def test_source_lexical_check_remains_read_only(self):
        before = checker.check_sources(checker.ROOT)
        after = checker.check_sources(checker.ROOT)
        self.assertEqual(before, ())
        self.assertEqual(after, ())


if __name__ == "__main__":
    unittest.main()
