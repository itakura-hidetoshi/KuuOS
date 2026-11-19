"""v0.29 original native Belief→Decision→Plural→Wa source-binding tests.

Unlike synthetic field-only successful stubs, these tests build the
original native full-cycle receipt and read the ORIGINAL DecisionStore
commit event from the local fixture ledger without modifying source
state or other OS kernels. No external issuer/authenticity claim.

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
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    PASS, BLOCKED, NO_DATA,
)
from runtime.kuuos_lean_python_decision_native_binding_v0_29 import (
    audit_native_decision_from_belief,
)
from runtime.kuuos_lean_python_plural_native_binding_v0_29 import (
    audit_native_plural_consensus,
)
from runtime.kuuos_lean_python_wa_native_binding_v0_29 import (
    audit_native_wa_endorsement,
)
from runtime.kuuos_lean_python_belief_gerbe_native_binding_v0_29 import (
    audit_native_belief_gerbe_source,
    audit_native_gerbe_v03_theorem_conditions,
)


class NativeDecisionMediatorBindingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-v029-native-os-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.receipt = build_native_full_cycle_receipt(cls.root)
        if validate_native_full_cycle_receipt(cls.receipt):
            raise AssertionError("original_native_v13_fixture_not_valid")
        cls.states = cls.receipt["native_artifacts"]
        cls.commits = DecisionStore(cls.root / "decision")._read_ledger()
        if not cls.commits:
            raise AssertionError("original_decision_commit_ledger_empty")
        cls.last_event = cls.commits[-1]["event"]

    def binding(self):
        return audit_native_decision_from_belief(
            self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
            self.states["DecisionOS"], self.last_event)

    def test_original_native_cycle_is_valid_and_source_is_committed(self):
        self.assertEqual(validate_native_full_cycle_receipt(self.receipt), [])
        for name in ("DecisionOS", "DecisionOSPlural", "DecisionOSWa"):
            self.assertEqual(self.states[name]["current_phase"], "commit")

    def test_real_belief_gerbe_receipt_preserves_version_gap(self):
        audit = audit_native_belief_gerbe_source(
            self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
            self.states["DecisionOS"])
        self.assertEqual(audit.status, NO_DATA)
        self.assertTrue(audit.original_state_validated)
        self.assertTrue(any("BeliefGerbeV03" in issue for issue in audit.issues))
        # The original v0.3 gerbe Lean-boundary fields ARE checked locally.
        # Only the v0.3 → v0.1 typed refinement remains NO_DATA.
        self.assertTrue(audit.source_bound_python_conditions_checked)
        self.assertEqual(audit.checked_witnesses, 7)
        self.assertFalse(audit.formal_lean_python_refinement_proved)
        self.assertFalse(audit.lean_proof_term_constructed)
        self.assertFalse(audit.execution_authority_granted)

    def test_original_belief_v03_gerbe_lean_conditions_pass_locally(self):
        local = audit_native_gerbe_v03_theorem_conditions(
            self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
            self.states["DecisionOS"])
        self.assertEqual(local.status, PASS, local.issues)
        self.assertEqual(local.checked_witnesses, 7)
        self.assertTrue(local.original_state_validated)
        self.assertTrue(local.source_bound_python_conditions_checked)
        self.assertFalse(local.formal_lean_python_refinement_proved)
        self.assertIn("BeliefOSReceipt.path_search_used",
                      local.source_field_paths)

    def test_v03_gerbe_local_proof_fields_cannot_be_forged(self):
        forged = deepcopy(self.states["BeliefOSReceipt"])
        forged["path_search_used"] = True
        local = audit_native_gerbe_v03_theorem_conditions(
            self.states["BeliefOSState"], forged,
            self.states["DecisionOS"])
        self.assertEqual(local.status, BLOCKED)

    def test_real_decision_selected_gate_and_commit_event_are_checked(self):
        audit = self.binding()
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertEqual(audit.checked_witnesses, 1)
        self.assertTrue(audit.original_state_validated)
        self.assertFalse(audit.original_edge_validated)
        self.assertTrue(audit.source_bound_python_conditions_checked)
        self.assertIn("DecisionOS.commit_event.payload", audit.source_field_paths)

    def test_original_decision_commit_is_from_actual_store_ledger(self):
        self.assertEqual(self.last_event["target_phase"], "commit")
        self.assertEqual(self.last_event["decision_event_digest"],
                         self.states["DecisionOS"]["event_history"][-1]["decision_event_digest"])
        self.assertEqual(
            DecisionStore(self.root / "decision").recover(require_snapshot_match=True),
            self.states["DecisionOS"])
        self.assertEqual(self.binding().status, PASS)

    def test_real_plural_original_consensus_order_is_bound(self):
        audit = audit_native_plural_consensus(
            self.states["DecisionOS"], self.states["DecisionOSPlural"])
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertTrue(audit.original_edge_validated)
        self.assertTrue(audit.source_bound_python_conditions_checked)
        self.assertIn("DecisionOSPlural.ranked_aggregates", audit.source_field_paths)

    def test_real_wa_original_endorsement_is_bound(self):
        audit = audit_native_wa_endorsement(
            self.states["DecisionOSPlural"], self.states["DecisionOSWa"])
        self.assertEqual(audit.status, PASS, audit.issues)
        self.assertTrue(audit.original_edge_validated)
        self.assertEqual(audit.checked_witnesses, 1)
        self.assertTrue(audit.source_bound_python_conditions_checked)

    def test_all_original_native_state_and_store_bytes_are_preserved(self):
        before = _fingerprint(self.receipt)
        ledger = self.root / "decision" / "decision-ledger.jsonl"
        ledger_before = ledger.read_bytes()
        self.binding()
        audit_native_plural_consensus(
            self.states["DecisionOS"], self.states["DecisionOSPlural"])
        audit_native_wa_endorsement(
            self.states["DecisionOSPlural"], self.states["DecisionOSWa"])
        audit_native_belief_gerbe_source(
            self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
            self.states["DecisionOS"])
        self.assertEqual(before, _fingerprint(self.receipt))
        self.assertEqual(ledger_before, ledger.read_bytes())

    def test_missing_commit_event_stays_no_data(self):
        audit = audit_native_decision_from_belief(
            self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
            self.states["DecisionOS"], None)
        self.assertEqual(audit.status, NO_DATA)

    def test_decision_forged_commit_flag_is_blocked(self):
        bad = deepcopy(self.last_event)
        bad["payload"]["memory_overwrite"] = True
        audit = audit_native_decision_from_belief(
            self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
            self.states["DecisionOS"], bad)
        self.assertEqual(audit.status, BLOCKED)

    def test_decision_mismatched_belief_receipt_is_blocked(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad["route"] = "HOLD"
        audit = audit_native_decision_from_belief(
            self.states["BeliefOSState"], bad,
            self.states["DecisionOS"], self.last_event)
        self.assertEqual(audit.status, BLOCKED)

    def test_plural_tampered_selected_source_cannot_pass(self):
        bad = deepcopy(self.states["DecisionOSPlural"])
        bad["selected_option_id"] = "forged"
        result = audit_native_plural_consensus(
            self.states["DecisionOS"], bad)
        self.assertEqual(result.status, BLOCKED)

    def test_plural_false_consensus_truth_authority_is_blocked(self):
        bad = deepcopy(self.states["DecisionOSPlural"])
        bad["non_authority"]["consensus_truth_authority_granted"] = True
        self.assertEqual(audit_native_plural_consensus(
            self.states["DecisionOS"], bad).status, BLOCKED)

    def test_wa_forged_false_harmony_flag_is_blocked(self):
        bad = deepcopy(self.states["DecisionOSWa"])
        selected = bad["source_selected_option_id"]
        matches = [x for x in bad["false_harmony_records"]
                   if x["option_id"] == selected]
        self.assertEqual(len(matches), 1)
        matches[0]["confirmed_false_harmony"] = True
        self.assertEqual(audit_native_wa_endorsement(
            self.states["DecisionOSPlural"], bad).status, BLOCKED)

    def test_wa_forged_minority_field_is_blocked(self):
        bad = deepcopy(self.states["DecisionOSWa"])
        selected = bad["source_selected_option_id"]
        profile = next(x for x in bad["profiles"] if x["option_id"] == selected)
        profile["minority_preserved"] = False
        self.assertEqual(audit_native_wa_endorsement(
            self.states["DecisionOSPlural"], bad).status, BLOCKED)

    def test_missing_mediator_source_keeps_no_data(self):
        self.assertEqual(audit_native_plural_consensus(None,
            self.states["DecisionOSPlural"]).status, NO_DATA)
        self.assertEqual(audit_native_wa_endorsement(None,
            self.states["DecisionOSWa"]).status, NO_DATA)

    def test_source_bound_success_does_not_promote_refinement_or_authority(self):
        for audit in (
            self.binding(),
            audit_native_plural_consensus(
                self.states["DecisionOS"], self.states["DecisionOSPlural"]),
            audit_native_wa_endorsement(
                self.states["DecisionOSPlural"], self.states["DecisionOSWa"]),
            audit_native_belief_gerbe_source(
                self.states["BeliefOSState"], self.states["BeliefOSReceipt"],
                self.states["DecisionOS"]),
        ):
            self.assertFalse(audit.formal_lean_python_refinement_proved)
            self.assertFalse(audit.lean_proof_term_constructed)
            self.assertFalse(audit.external_issuer_authenticated)
            self.assertFalse(audit.truth_authority_granted)
            self.assertFalse(audit.execution_authority_granted)
            self.assertFalse(audit.native_state_modified)


if __name__ == "__main__":
    unittest.main()
