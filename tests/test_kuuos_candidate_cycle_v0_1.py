import unittest

from runtime.kuuos_candidate_cycle_v0_1 import run_candidate_cycle


PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": True},
]

BASE_RAW = {
    "cycle_id": "cycle-candidate-001",
    "generated_at_utc": "2026-05-21T00:00:00+00:00",
    "previous_receipt_hash": "prev-hash-001",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "physical_process_visible": True,
    "thermodynamic_activity_visible": True,
    "process_history": PROCESS_HISTORY,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}


class KuuOSCandidateCycleTests(unittest.TestCase):
    def test_full_qi_state_continues_to_next_nonfinal_stage(self):
        receipt = run_candidate_cycle(BASE_RAW)
        self.assertEqual(receipt.cycle_status, "CONTINUE_NONFINAL")
        self.assertEqual(receipt.qi_signal, "ALLOW_CANDIDATE")
        self.assertEqual(receipt.next_queue, "NEXT_NONFINAL_STAGE")
        self.assertFalse(receipt.terminal_for_cycle)
        self.assertEqual(len(receipt.receipt_hash), 64)
        self.assertEqual(receipt.previous_receipt_hash, "prev-hash-001")
        self.assertFalse(receipt.grants_execution_authority)
        self.assertFalse(receipt.grants_truth_authority)
        self.assertFalse(receipt.grants_final_commitment_authority)
        self.assertFalse(receipt.grants_memory_overwrite_authority)

    def test_candidate_cycle_exposes_qi_process_tensor_receipt(self):
        receipt = run_candidate_cycle(BASE_RAW)
        process_receipt = receipt.qi_process_tensor_receipt
        self.assertTrue(process_receipt["process_tensor_visible"])
        self.assertTrue(process_receipt["transition_continuity_visible"])
        self.assertTrue(process_receipt["memory_continuity_visible"])
        self.assertTrue(process_receipt["nonmarkov_memory_visible"])
        self.assertEqual(process_receipt["process_history_length"], 3)
        self.assertEqual(process_receipt["transition_support_count"], 3)
        self.assertEqual(process_receipt["memory_support_count"], 1)
        self.assertEqual(process_receipt["nonmarkov_support_count"], 1)
        self.assertEqual(process_receipt["process_tensor_reason"], "process_tensor_support_visible")
        self.assertFalse(process_receipt["grants_execution_authority"])
        self.assertFalse(process_receipt["grants_truth_authority"])
        self.assertFalse(process_receipt["grants_final_commitment_authority"])
        self.assertFalse(process_receipt["grants_memory_overwrite_authority"])

    def test_missing_physical_and_process_value_support_reobserves(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        raw["process_history"] = []
        receipt = run_candidate_cycle(raw)
        self.assertEqual(receipt.cycle_status, "REOBSERVE")
        self.assertEqual(receipt.next_queue, "REOBSERVE_QUEUE")
        self.assertTrue(receipt.terminal_for_cycle)
        self.assertIn("runtime_variation_visible", receipt.missing_inputs)
        self.assertIn("value_witness_receipt", receipt.missing_inputs)
        self.assertFalse(receipt.qi_process_tensor_receipt["process_tensor_visible"])

    def test_lineage_gap_routes_to_lineage_recheck(self):
        raw = dict(BASE_RAW)
        raw["registry_key"] = False
        receipt = run_candidate_cycle(raw)
        self.assertEqual(receipt.cycle_status, "LINEAGE_RECHECK")
        self.assertEqual(receipt.next_queue, "LINEAGE_RECHECK_QUEUE")
        self.assertTrue(receipt.terminal_for_cycle)

    def test_delivery_gap_routes_to_delivery_recheck(self):
        raw = dict(BASE_RAW)
        raw["channel_scope"] = False
        receipt = run_candidate_cycle(raw)
        self.assertEqual(receipt.cycle_status, "DELIVERY_RECHECK")
        self.assertEqual(receipt.next_queue, "DELIVERY_RECHECK_QUEUE")
        self.assertTrue(receipt.terminal_for_cycle)

    def test_boundary_failure_quarantines_and_preserves_process_tensor_receipt(self):
        raw = dict(BASE_RAW)
        raw["noncollapse_guard"] = False
        receipt = run_candidate_cycle(raw)
        self.assertEqual(receipt.cycle_status, "QUARANTINE")
        self.assertEqual(receipt.next_queue, "QUARANTINE_QUEUE")
        self.assertTrue(receipt.terminal_for_cycle)
        self.assertIn("noncollapse_guard", receipt.blocked_boundaries)
        self.assertEqual(len(receipt.receipt_hash), 64)
        self.assertFalse(receipt.qi_process_tensor_receipt["process_tensor_visible"])
        self.assertEqual(receipt.qi_process_tensor_receipt["process_tensor_reason"], "boundary_blocks_process_tensor_support")

    def test_receipt_hash_is_deterministic_for_same_timestamped_input(self):
        first = run_candidate_cycle(BASE_RAW)
        second = run_candidate_cycle(BASE_RAW)
        self.assertEqual(first.receipt_hash, second.receipt_hash)

    def test_receipt_hash_changes_when_process_history_changes(self):
        first = run_candidate_cycle(BASE_RAW)
        changed = dict(BASE_RAW)
        changed["process_history"] = PROCESS_HISTORY[:2]
        second = run_candidate_cycle(changed)
        self.assertNotEqual(first.receipt_hash, second.receipt_hash)


if __name__ == "__main__":
    unittest.main()
