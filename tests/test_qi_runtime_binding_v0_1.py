import unittest

from runtime.qi_runtime_binding_v0_1 import evaluate_qi_runtime_binding


BASE_STATE = {
    "cycle_id": "cycle-001",
    "kernel_state": "candidate",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "runtime_variation_visible": True,
    "policy_candidate_receipt": True,
    "value_witness_receipt": True,
    "barrier_witness_receipt": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}


class QiRuntimeBindingTests(unittest.TestCase):
    def test_allow_candidate_when_all_inputs_visible(self):
        receipt = evaluate_qi_runtime_binding(BASE_STATE)
        self.assertEqual(receipt.qi_signal, "ALLOW_CANDIDATE")
        self.assertFalse(receipt.grants_execution_authority)
        self.assertFalse(receipt.grants_truth_authority)
        self.assertFalse(receipt.grants_final_commitment_authority)
        self.assertFalse(receipt.grants_memory_overwrite_authority)

    def test_boundary_failure_quarantines_before_policy_checks(self):
        state = dict(BASE_STATE)
        state["two_truths_gap"] = False
        state["runtime_variation_visible"] = False
        receipt = evaluate_qi_runtime_binding(state)
        self.assertEqual(receipt.qi_signal, "QUARANTINE")
        self.assertEqual(receipt.qi_reason, "boundary_first_noncollapse_failed")
        self.assertIn("two_truths_gap", receipt.missing_inputs)
        self.assertIn("quarantine_notice", receipt.opened_notices)

    def test_forbidden_authority_projection_quarantines(self):
        state = dict(BASE_STATE)
        state["truth_commit"] = True
        receipt = evaluate_qi_runtime_binding(state)
        self.assertEqual(receipt.qi_signal, "QUARANTINE")
        self.assertEqual(receipt.qi_reason, "forbidden_authority_projection_present")
        self.assertIn("truth_commit", receipt.blocked_boundaries)

    def test_missing_candidate_marker_holds(self):
        state = dict(BASE_STATE)
        state["nonfinal_marker"] = False
        receipt = evaluate_qi_runtime_binding(state)
        self.assertEqual(receipt.qi_signal, "HOLD")
        self.assertEqual(receipt.qi_reason, "candidate_or_nonfinal_marker_missing")
        self.assertIn("nonfinal_marker", receipt.missing_inputs)

    def test_missing_policy_support_reobserve(self):
        state = dict(BASE_STATE)
        state["value_witness_receipt"] = False
        receipt = evaluate_qi_runtime_binding(state)
        self.assertEqual(receipt.qi_signal, "REOBSERVE")
        self.assertEqual(receipt.qi_reason, "runtime_policy_flow_support_missing")
        self.assertIn("value_witness_receipt", receipt.missing_inputs)

    def test_missing_lineage_support_recheck(self):
        state = dict(BASE_STATE)
        state["registry_key"] = False
        receipt = evaluate_qi_runtime_binding(state)
        self.assertEqual(receipt.qi_signal, "LINEAGE_RECHECK")
        self.assertEqual(receipt.qi_reason, "lineage_flow_support_missing")
        self.assertIn("registry_key", receipt.missing_inputs)

    def test_missing_delivery_support_recheck(self):
        state = dict(BASE_STATE)
        state["acknowledgment_marker"] = False
        receipt = evaluate_qi_runtime_binding(state)
        self.assertEqual(receipt.qi_signal, "DELIVERY_RECHECK")
        self.assertEqual(receipt.qi_reason, "projection_delivery_flow_support_missing")
        self.assertIn("acknowledgment_marker", receipt.missing_inputs)


if __name__ == "__main__":
    unittest.main()
