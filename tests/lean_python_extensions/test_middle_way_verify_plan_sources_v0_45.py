"""v0.45 original VerifyOS/PlanOS Python and Lean proof-source pins.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_middle_way_verify_plan_sources_v0_45 as checker,
)


class VerifyPlanSixRoutesSourceTests(unittest.TestCase):
    def test_all_original_lean_and_python_pins_pass(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_actual_verify_and_plan_kernels_are_pinned(self):
        for path in (
            "runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py",
            "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v045_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_verify_and_plan_lean_files_are_pinned(self):
        for path in (
            "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean",
            "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v045_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_original_fixture_bundles_cannot_silently_change(self):
        for path in (
            "scripts/check_verifyos_middle_way_conditional_continuity_verification_v0_4.py",
            "scripts/check_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v045_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_priors_lean_simulation_and_v044_checker_are_immutable(self):
        for path in (
            "formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean",
            "formal/KUOS/Architecture/LeanPythonFiniteEvidenceWitnessV0_44.lean",
            "scripts/check_kuuos_lean_python_finite_evidence_sources_v0_44.py",
        ):
            with self.subTest(path=path), patch.dict(
                checker.PINNED, {path: "0" * 40},
            ):
                self.assertIn("v045_original_source_changed:" + path,
                              checker.check_sources(checker.ROOT))

    def test_correct_original_import_and_eight_definitions_nine_theorems(self):
        raw, issue = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(issue)
        lines = tuple(x.strip() for x in raw.decode("utf-8").splitlines())
        self.assertEqual(len(checker.LEAN_DEFINITIONS), 8)
        self.assertEqual(len(checker.LEAN_THEOREMS), 9)
        for name in checker.LEAN_DEFINITIONS + checker.LEAN_THEOREMS:
            self.assertTrue(
                any(line == name or line.startswith(name + " ")
                    or line.startswith(name + ":") for line in lines),
                name,
            )
        for name in checker.LEAN_IMPORTS:
            self.assertIn(name, lines)

    def test_lean_proof_hole_scan_preserves_identifiers_and_noncode(self):
        source = '''
import Mathlib
def admittedForStatus : Bool := true
def no_admit_suffix := admittedForStatus
def proof_name_admit_example := true
def literal := "axiom sorry admit -- /-"
def escaped := "string with \"sorry\" inside"
-- axiom bogus : True
/- outer sorry /- nested admit -/ axiom -/
def «sorry» := true
def «admit» := true
'''
        self.assertFalse(checker._contains_unproved_lean(source))

    def test_lean_proof_hole_scan_detects_actual_tokens(self):
        for name, source in (
            ("axiom", "axiom unproved : True"),
            ("sorry", "theorem unproved : True := by\n  exact sorry"),
            ("admit", "theorem unproved : True := by\n  admit"),
            ("inline", "theorem unproved : True := by\n  first | assumption | sorry"),
        ):
            with self.subTest(name=name):
                self.assertTrue(checker._contains_unproved_lean(source))

    def test_lean_lexical_scan_rejects_unterminated_regions(self):
        for source in ('/- unterminated', 'def x := "unterminated',
                       'def «unfinished'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                checker._contains_unproved_lean(source)

    def test_no_missing_new_file_is_treated_as_complete_source(self):
        absent = "formal/KUOS/Architecture/FakeSixRoute.lean"
        with patch.object(checker, "NEW", checker.NEW + (absent,)):
            self.assertIn("v045_new_file_missing:" + absent,
                          checker.check_sources(checker.ROOT))

    def test_original_six_native_case_tests_are_discoverable(self):
        tests = checker.test_inventory(checker.ROOT)
        self.assertEqual(set(tests), set(checker.TEST_CLASSES))
        names = tests[checker.NEW[3]]
        self.assertIn("test_all_six_original_verify_and_plan_kernels_run", names)
        self.assertIn(
            "test_original_verify_certificate_substituted_in_plan_envelope_blocks",
            names,
        )
        self.assertIn("test_only_retain_is_admitted_without_executing_plan",
                      names)
        self.assertGreaterEqual(len(names), 20)

    def test_untrusted_source_root_is_not_fetched_or_executed(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("untrusted fspath hook")
        for root in (None, str(checker.ROOT), HostilePath()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))
            self.assertEqual(checker.test_inventory(root), {})

    def test_source_symlink_or_parent_symlink_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias),
                             ("root:trusted_path_required",))
            alias.unlink()
            alias.symlink_to(checker.ROOT.parent, target_is_directory=True)
            self.assertEqual(checker.check_sources(alias / checker.ROOT.name),
                             ("root:trusted_path_required",))

    def test_source_traversal_is_blocked(self):
        alias = checker.ROOT / ".." / checker.ROOT.name
        self.assertEqual(checker.check_sources(alias),
                         ("root:trusted_path_required",))
        self.assertEqual(checker.test_inventory(alias), {})


if __name__ == "__main__":
    unittest.main()
