"""v0.44 exhaustive Python/Lean-model evidence witness and original OS tests.

The formal Lean theorems are independently CI-checked, never inferred here.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime import kuuos_lean_python_finite_evidence_witness_v0_44 as subject


class FiniteEvidenceWitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v044-evidence-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.cycle = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.cycle) == []
        cls.states = cls.cycle["native_artifacts"]
        cls.wa_receipt = build_replan_wa_activation_receipt(
            state=cls.states["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )
        cls.plan_receipt = build_plan_phase_activation_receipt(
            state=cls.states["PlanOS"],
            mission_cycle_phase="plan",
            mission_cycle_state_digest=sha("native-full-cycle-plan-phase-state"),
            plan_phase_receipt_digest=sha("native-full-cycle-plan-phase-receipt"),
            now_ms=80_000,
        )

    def audit(self, **overrides):
        kwargs = dict(
            native_states=self.states,
            wa_replan_activation_receipt=self.wa_receipt,
            plan_phase_activation_receipt=self.plan_receipt,
            original_cycle_root=self.root,
        )
        kwargs.update(overrides)
        return subject.audit_native_finite_evidence_instance(**kwargs)

    def test_original_python_three_status_pairs_all_nine(self):
        record = subject.audit_finite_status_table()
        self.assertEqual(record.status, subject.SCOPED_TABLE_MATCH,
                         record.issues)
        self.assertEqual(record.original_python_pair_cases_checked, 9)
        self.assertTrue(record.finite_table_locally_checked)

    def test_python_model_three_status_triples_all_twenty_seven(self):
        record = subject.audit_finite_status_table()
        self.assertEqual(record.original_python_two_stage_cases_checked, 27)
        self.assertEqual(record.status, subject.SCOPED_TABLE_MATCH)

    def test_all_forty_eight_invalid_python_token_pairs_fail_closed(self):
        record = subject.audit_finite_status_table()
        self.assertEqual(record.original_python_invalid_tokens_checked, 48)
        self.assertEqual(record.status, subject.SCOPED_TABLE_MATCH)

    def test_independent_truth_table_not_reusing_original_join(self):
        cases = [
            (subject.BLOCKED, subject.LOCALLY_CHECKED, subject.BLOCKED),
            (subject.NO_DATA, subject.LOCALLY_CHECKED, subject.NO_DATA),
            (subject.LOCALLY_CHECKED, subject.LOCALLY_CHECKED,
             subject.LOCALLY_CHECKED),
            ("PASS", subject.LOCALLY_CHECKED, subject.BLOCKED),
            ("PASS", subject.NO_DATA, subject.BLOCKED),
        ]
        for left, right, expected in cases:
            self.assertEqual(
                subject._independent_string_model(left, right), expected,
            )

    def test_native_real_nine_stores_with_model_is_locally_usable(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_NATIVE_COMPATIBLE,
                         result.issues)
        self.assertEqual(result.original_native_status,
                         subject.original.SCOPED_COMPATIBLE)
        self.assertTrue(result.original_native_nine_store_audit_checked)
        self.assertTrue(result.finite_table_locally_checked)
        self.assertEqual(
            tuple(status for _, status in result.original_native_evidence_statuses),
            (subject.LOCALLY_CHECKED,) * 3,
        )

    def test_context_is_grounded_by_same_original_native_source(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_NATIVE_COMPATIBLE)
        context = dict(result.declared_context_key)
        self.assertEqual(context["worldScope"], "native-v1.3-local-source")
        self.assertEqual(context["lineageId"],
                         self.states["PlanOS"]["lineage_id"])
        self.assertEqual(context["missionContractDigest"],
                         self.states["PlanOS"]["mission_contract_digest"])
        self.assertEqual(context["sourceRoot"], str(self.root.resolve()))
        self.assertEqual(context["interpretationVersion"], subject.VERSION)
        self.assertFalse(result.external_source_authenticated)

    def test_even_concrete_finite_model_is_not_full_python_refinement(self):
        report = self.audit()
        self.assertEqual(report.status, subject.SCOPED_NATIVE_COMPATIBLE)
        for key in (
            "lean_model_proof_verified_by_this_python_process",
            "lean_to_cpython_interpreter_refinement_proved",
            "whole_os_lean_python_semantics_proved",
            "global_descent_proved",
            "external_source_authenticated",
            "common_causal_clock_proved",
            "atomic_nine_store_snapshot_proved",
            "actual_act_numeric_witnesses_proved",
            "execution_authority_granted",
            "truth_authority_granted",
            "clinical_authority_granted",
            "git_authority_granted",
            "memory_write_performed",
            "original_store_mutated",
        ):
            self.assertIs(getattr(report, key), False, key)

    def test_codeai_memory_decision_plan_advisory_not_automatic_permission(self):
        report = self.audit()
        self.assertEqual(report.status, subject.SCOPED_NATIVE_COMPATIBLE)
        self.assertEqual(
            dict(report.read_only_consumer_advice),
            dict(subject.ADVISORY_CONSUMERS),
        )
        self.assertEqual(set(dict(report.read_only_consumer_advice)),
                         {"CodeAI", "MemoryOS", "DecisionOS", "PlanOS"})

    def test_unobserved_native_source_is_no_data_not_a_true_claim(self):
        report = self.audit(native_states=None)
        self.assertEqual(report.status, subject.NO_DATA, report.issues)
        self.assertTrue(report.finite_table_locally_checked)
        self.assertFalse(report.original_native_nine_store_audit_checked)
        self.assertEqual(report.read_only_consumer_advice,
                         subject.HOLD_CONSUMERS)

    def test_missing_original_wa_receipt_remains_no_data(self):
        report = self.audit(wa_replan_activation_receipt=None)
        self.assertEqual(report.status, subject.NO_DATA, report.issues)
        self.assertTrue(report.finite_table_locally_checked)

    def test_missing_plan_activation_remains_no_data(self):
        report = self.audit(plan_phase_activation_receipt=None)
        self.assertEqual(report.status, subject.NO_DATA, report.issues)

    def test_missing_original_store_root_remains_no_data(self):
        report = self.audit(original_cycle_root=None)
        self.assertEqual(report.status, subject.NO_DATA, report.issues)

    def test_missing_original_ledger_does_not_become_a_new_model_witness(self):
        from shutil import copytree
        with TemporaryDirectory(prefix="kuuos-v044-native-missing-") as d:
            original = Path(d) / "native"
            copytree(self.root, original)
            (original / "belief" / "belief-gerbe-ledger.jsonl").unlink()
            result = self.audit(original_cycle_root=original)
        self.assertEqual(result.status, subject.NO_DATA, result.issues)

    def test_forged_upstream_receipt_blocked_even_when_finite_table_passes(self):
        states = deepcopy(self.states)
        states["BeliefOSReceipt"]["belief_gerbe_receipt_digest"] = "forged"
        report = self.audit(native_states=states)
        self.assertEqual(report.status, subject.BLOCKED, report.issues)
        self.assertTrue(report.finite_table_locally_checked)
        self.assertEqual(report.read_only_consumer_advice,
                         subject.HOLD_CONSUMERS)

    def test_forged_downstream_receipt_blocks_source_seam(self):
        receipt = deepcopy(self.plan_receipt)
        receipt["plan_activation_receipt_digest"] = "forged"
        report = self.audit(plan_phase_activation_receipt=receipt)
        self.assertEqual(report.status, subject.BLOCKED, report.issues)
        self.assertTrue(report.finite_table_locally_checked)

    def test_original_join_mutation_cannot_pass_finite_model(self):
        with patch.object(subject.original, "combine_evidence",
                          return_value=subject.LOCALLY_CHECKED):
            report = subject.audit_finite_status_table()
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("pair:incorrect:NO_DATA:NO_DATA", report.issues)
        self.assertFalse(report.finite_table_locally_checked)

    def test_propagating_bad_original_join_does_not_grant_native_permission(self):
        with patch.object(subject.original, "combine_evidence",
                          return_value=subject.LOCALLY_CHECKED):
            report = self.audit(native_states=None)
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertEqual(report.read_only_consumer_advice,
                         subject.HOLD_CONSUMERS)

    def test_original_join_exception_is_a_blocked_observation(self):
        with patch.object(subject.original, "combine_evidence",
                          side_effect=RuntimeError("deliberate test")):
            report = subject.audit_finite_status_table()
        self.assertEqual(report.status, subject.BLOCKED)
        self.assertIn("pair:runtime_exception:RuntimeError", report.issues)

    def test_unsupported_status_is_not_treated_as_a_success_label(self):
        for status in ("PASS", "", "checked", None, False, 0):
            with self.subTest(status=status):
                self.assertEqual(
                    subject._independent_string_model(
                        status, subject.LOCALLY_CHECKED,
                    ),
                    subject.BLOCKED,
                )

    def test_all_ternary_seams_agree_with_left_associative_model(self):
        for a, b, c in product(subject.STATUSES, repeat=3):
            with self.subTest(a=a, b=b, c=c):
                first = subject._independent_string_model(a, b)
                left = subject._independent_string_model(first, c)
                right = subject._independent_string_model(
                    a, subject._independent_string_model(b, c),
                )
                self.assertEqual(left, right)

    def test_original_source_files_unmodified_by_the_audit(self):
        before = {str(p.relative_to(self.root)): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        input_before = deepcopy((self.states, self.wa_receipt,
                                 self.plan_receipt))
        report = self.audit()
        self.assertEqual(report.status, subject.SCOPED_NATIVE_COMPATIBLE)
        after = {str(p.relative_to(self.root)): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(input_before, (self.states, self.wa_receipt,
                                        self.plan_receipt))

    def test_no_universal_permission_granted_by_any_model_success(self):
        report = subject.audit_finite_status_table()
        self.assertEqual(report.status, subject.SCOPED_TABLE_MATCH)
        self.assertFalse(report.execution_authority_granted)
        self.assertFalse(report.git_authority_granted)
        self.assertFalse(report.memory_write_performed)
        self.assertFalse(report.whole_os_lean_python_semantics_proved)


if __name__ == "__main__":
    unittest.main()
