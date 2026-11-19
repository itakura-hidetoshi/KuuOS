"""v0.33 original Plural->Wa->PlanOS native source compatibility regressions.

Only the ORIGINAL full-cycle fixture is used for native states and original
validators. Its replan receipt was not retained in native_artifacts; we
reconstruct it with the ORIGINAL v0.3 receipt constructor and EXACT original
fixture parameters, not an authenticated externally issued receipt.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import (
    audit_decision_plan_edge,
)
from runtime.kuuos_lean_python_wa_plan_local_compat_v0_33 import (
    audit_native_wa_plan_local_compatibility,
    SCOPED_COMPATIBLE, BLOCKED, NO_DATA,
)


class NativeWaPlanLocalCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v033-wa-plan-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.state = cls.native["native_artifacts"]
        cls.replan = build_replan_wa_activation_receipt(
            state=cls.state["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )

    def audit(self, plural=None, wa=None, plan=None, receipt=None):
        return audit_native_wa_plan_local_compatibility(
            self.state["DecisionOSPlural"] if plural is None else plural,
            self.state["DecisionOSWa"] if wa is None else wa,
            self.state["PlanOS"] if plan is None else plan,
            self.replan if receipt is None else receipt,
        )

    def test_native_fixture_is_valid(self):
        self.assertEqual(validate_native_full_cycle_receipt(self.native), [])
        self.assertEqual(self.state["DecisionOSWa"]["current_phase"], "commit")
        self.assertEqual(self.state["PlanOS"]["current_phase"], "commit")

    def test_original_native_wa_plan_compatibility_checks_each_layer(self):
        a = self.audit()
        self.assertEqual(a.status, SCOPED_COMPATIBLE, a.issues)
        self.assertTrue(a.original_wa_conditions_checked)
        self.assertTrue(a.original_plan_guards_checked)
        self.assertTrue(a.original_replan_edge_checked)
        self.assertTrue(a.selected_lean_data_conditions_checked)
        self.assertEqual(a.observed_wa_digest, _fingerprint(self.state["DecisionOSWa"]))
        self.assertEqual(a.observed_plan_digest, _fingerprint(self.state["PlanOS"]))
        self.assertEqual(a.observed_replan_receipt_digest,
                         self.replan["wa_activation_receipt_digest"])
        self.assertGreater(len(a.checked_field_paths), 20)

    def test_missing_replan_receipt_is_not_a_pass(self):
        self.assertEqual(audit_native_wa_plan_local_compatibility(
            self.state["DecisionOSPlural"], self.state["DecisionOSWa"],
            self.state["PlanOS"], None).status, NO_DATA)

    def test_missing_plural_source_stays_no_data(self):
        self.assertEqual(audit_native_wa_plan_local_compatibility(
            None, self.state["DecisionOSWa"], self.state["PlanOS"],
            self.replan).status, NO_DATA)

    def test_wrong_source_type_is_blocked(self):
        self.assertEqual(audit_native_wa_plan_local_compatibility(
            [], self.state["DecisionOSWa"], self.state["PlanOS"],
            self.replan).status, BLOCKED)

    def test_forged_replan_future_only_cannot_cross_edge(self):
        bad = deepcopy(self.replan)
        bad["future_only"] = False
        self.assertEqual(self.audit(receipt=bad).status, BLOCKED)

    def test_forged_replan_digest_is_blocked(self):
        bad = deepcopy(self.replan)
        bad["wa_activation_receipt_digest"] = "forged"
        self.assertEqual(self.audit(receipt=bad).status, BLOCKED)

    def test_source_wa_digest_change_is_blocked(self):
        bad = deepcopy(self.state["PlanOS"])
        bad["source_wa_state_digest"] = "forged"
        self.assertEqual(self.audit(plan=bad).status, BLOCKED)

    def test_plan_guard_mutation_is_blocked(self):
        bad = deepcopy(self.state["PlanOS"])
        bad["guard_summary"]["all_effects_guarded"] = False
        self.assertEqual(self.audit(plan=bad).status, BLOCKED)

    def test_wa_record_mutation_is_not_a_pass(self):
        bad = deepcopy(self.state["DecisionOSWa"])
        bad["wa_state_digest"] = "forged"
        self.assertEqual(self.audit(wa=bad).status, BLOCKED)

    def test_original_source_and_store_files_are_unmodified(self):
        before = _fingerprint(self.native)
        bytes_before = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)
        after = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(before, _fingerprint(self.native))
        self.assertEqual(bytes_before, after)

    def test_no_authority_or_formal_descent_from_local_pass(self):
        a = self.audit()
        self.assertEqual(a.status, SCOPED_COMPATIBLE)
        for key in (
            "formal_descent_certified", "global_gluing_proved",
            "complete_lean_python_refinement_proved", "lean_proof_term_constructed",
            "external_issuer_authenticated",
            "external_replan_receipt_authenticated", "host_license_granted",
            "execution_authority_granted", "truth_authority_granted",
            "git_authority_granted", "original_state_mutated",
        ):
            self.assertIs(getattr(a, key), False, key)

    def test_direct_decision_to_plan_shortcut_is_not_registered(self):
        x = audit_decision_plan_edge(
            "DecisionOS", "PlanOS",
            self.state["DecisionOS"], self.state["PlanOS"],
            replan_activation_receipt=self.replan)
        self.assertEqual(x.status, NO_DATA)


if __name__ == "__main__":
    unittest.main()
