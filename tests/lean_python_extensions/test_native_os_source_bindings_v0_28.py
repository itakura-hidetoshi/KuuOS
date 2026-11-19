"""v0.28 native source-bound per-OS regression on real KuuOS full-cycle fixture.

Tests exercise ORIGINAL Plan/Act/Observe/Verify/Learn state snapshots and
typed handoffs, never synthetic stand-ins for a successful source binding.
Test fixture writes are isolated to TemporaryDirectory, not production.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    PASS, NO_DATA, BLOCKED,
)
from runtime.kuuos_lean_python_plan_native_binding_v0_28 import (
    audit_native_plan_effect_guards,
)
from runtime.kuuos_lean_python_act_native_binding_v0_28 import (
    audit_native_act_authorization,
)
from runtime.kuuos_lean_python_observe_native_binding_v0_28 import (
    audit_native_observe_from_act,
)
from runtime.kuuos_lean_python_verify_native_binding_v0_28 import (
    audit_native_verify_from_observe,
)
from runtime.kuuos_lean_python_learn_native_binding_v0_28 import (
    audit_native_learn_from_verify,
)


class NativePerOSSourceBindingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v028-native-os-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        problems = validate_native_full_cycle_receipt(cls.native)
        if problems:
            raise AssertionError(("original_native_full_cycle_invalid", problems))
        cls.states = cls.native["native_artifacts"]

    def test_original_native_eight_os_cycle_is_the_source(self):
        self.assertEqual(len(self.states), 10)
        for name in ("PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS"):
            with self.subTest(os=name):
                self.assertEqual(self.states[name]["current_phase"], "commit")
        self.assertEqual(validate_native_full_cycle_receipt(self.native), [])

    def test_plan_effectful_steps_have_source_bound_lean_guards(self):
        audit = audit_native_plan_effect_guards(self.states["PlanOS"])
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertTrue(audit.original_state_validated)
        self.assertGreaterEqual(audit.checked_witnesses, 1)
        self.assertTrue(audit.source_bound_python_conditions_checked)
        self.assertIn("PlanOS.steps[*].depends_on", audit.source_field_paths)

    def test_act_bound_receipts_never_invent_numeric_jobs_or_host_authority(self):
        audit = audit_native_act_authorization(
            self.states["PlanOS"], self.states["ActOS"])
        self.assertEqual(audit.status, NO_DATA, audit.issues)
        self.assertTrue(audit.original_state_validated)
        self.assertFalse(audit.execution_authority_granted)
        self.assertTrue(any("actual_jobsClaimed" in v for v in audit.issues))
        self.assertTrue(any("actual_slicesRun" in v for v in audit.issues))
        self.assertIn("ActOS.step_authorization.single_use", audit.source_field_paths)

    def test_observe_native_comparison_receipt_and_debt_are_typed(self):
        audit = audit_native_observe_from_act(
            self.states["ActOS"], self.states["ObserveOS"])
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertTrue(audit.original_edge_validated)
        self.assertEqual(audit.checked_witnesses, 1)
        self.assertIn("ObserveOS.comparison_receipt.verdict", audit.source_field_paths)

    def test_verify_native_adjudication_and_debts_are_typed(self):
        audit = audit_native_verify_from_observe(
            self.states["ObserveOS"], self.states["VerifyOS"])
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertTrue(audit.original_edge_validated)
        self.assertTrue(audit.source_bound_python_conditions_checked)
        self.assertIn(
            "VerifyOS.adjudication_receipt.criterion_satisfied",
            audit.source_field_paths)

    def test_learn_native_future_only_delta_is_typed(self):
        audit = audit_native_learn_from_verify(
            self.states["VerifyOS"], self.states["LearnOS"])
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertTrue(audit.original_edge_validated)
        self.assertIn("LearnOS.learning_delta.memory_overwrite",
                      audit.source_field_paths)
        self.assertIn("LearnOS.learning_delta.expiration_condition_digest",
                      audit.source_field_paths)

    def test_original_native_artifacts_are_not_mutated_by_any_projection(self):
        before = _fingerprint(self.native)
        plan, act, observe, verify, learn = (
            self.states[n] for n in
            ("PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS")
        )
        audit_native_plan_effect_guards(plan)
        audit_native_act_authorization(plan, act)
        audit_native_observe_from_act(act, observe)
        audit_native_verify_from_observe(observe, verify)
        audit_native_learn_from_verify(verify, learn)
        self.assertEqual(_fingerprint(self.native), before)

    def test_missing_upstream_native_state_remains_no_data(self):
        self.assertEqual(
            audit_native_observe_from_act(None, self.states["ObserveOS"]).status,
            NO_DATA)
        self.assertEqual(
            audit_native_verify_from_observe(None, self.states["VerifyOS"]).status,
            NO_DATA)
        self.assertEqual(
            audit_native_learn_from_verify(None, self.states["LearnOS"]).status,
            NO_DATA)

    def test_plan_tampered_original_step_is_not_accepted(self):
        modified = deepcopy(self.states["PlanOS"])
        steps = [s for s in modified["steps"] if s["effectful"]]
        self.assertTrue(steps)
        steps[0]["stop_condition_digests"] = []
        self.assertEqual(audit_native_plan_effect_guards(modified).status, BLOCKED)

    def test_act_authorization_widening_is_blocked(self):
        modified = deepcopy(self.states["ActOS"])
        modified["step_authorization"]["single_use"] = False
        self.assertEqual(audit_native_act_authorization(
            self.states["PlanOS"], modified).status, BLOCKED)

    def test_observe_comparison_digest_tampering_is_blocked(self):
        modified = deepcopy(self.states["ObserveOS"])
        modified["comparison_receipt"]["comparison_is_verification"] = True
        self.assertEqual(
            audit_native_observe_from_act(self.states["ActOS"], modified).status,
            BLOCKED)

    def test_verify_criterion_tamper_is_blocked(self):
        modified = deepcopy(self.states["VerifyOS"])
        modified["adjudication_receipt"]["criterion_satisfied"] = False
        self.assertEqual(
            audit_native_verify_from_observe(self.states["ObserveOS"], modified).status,
            BLOCKED)

    def test_learn_future_only_tamper_is_blocked(self):
        modified = deepcopy(self.states["LearnOS"])
        modified["learning_delta"]["future_only"] = False
        self.assertEqual(
            audit_native_learn_from_verify(self.states["VerifyOS"], modified).status,
            BLOCKED)

    def test_cross_os_wrong_source_identity_is_blocked(self):
        altered = deepcopy(self.states["ObserveOS"])
        altered["source_act_state_digest"] = "wrong"
        self.assertEqual(audit_native_observe_from_act(
            self.states["ActOS"], altered).status, BLOCKED)

    def test_no_python_projection_promotes_authority_or_formal_refinement(self):
        for item in (
            audit_native_plan_effect_guards(self.states["PlanOS"]),
            audit_native_act_authorization(self.states["PlanOS"], self.states["ActOS"]),
            audit_native_observe_from_act(self.states["ActOS"], self.states["ObserveOS"]),
            audit_native_verify_from_observe(self.states["ObserveOS"], self.states["VerifyOS"]),
            audit_native_learn_from_verify(self.states["VerifyOS"], self.states["LearnOS"]),
        ):
            with self.subTest(os=item.os_name):
                self.assertFalse(item.native_state_modified)
                self.assertFalse(item.lean_proof_term_constructed)
                self.assertFalse(item.formal_lean_python_refinement_proved)
                self.assertFalse(item.execution_authority_granted)
                self.assertFalse(item.truth_authority_granted)
                self.assertFalse(item.global_host_effect_certified)
                self.assertFalse(item.external_issuer_authenticated)


if __name__ == "__main__":
    unittest.main()
