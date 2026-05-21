import unittest

from runtime.kuuos_action_router_v0_1 import route_next_action
from runtime.kuuos_feedback_merger_v0_1 import merge_task_result_into_next_state
from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
from runtime.kuuos_queue_worker_v0_1 import process_next_queue_item
from runtime.kuuos_task_board_processor_v0_1 import process_next_task


BASE_RAW = {
    "cycle_id": "feedback-001",
    "next_cycle_id": "feedback-002",
    "generated_at_utc": "2026-05-21T00:00:00+00:00",
    "dispatched_at_utc": "2026-05-21T00:00:01+00:00",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "physical_process_visible": True,
    "thermodynamic_activity_visible": True,
    "process_tensor_visible": True,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}

FULL_EVIDENCE = {
    "boundary_review_evidence": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "identity_blocker": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
    "runtime_variation_visible": True,
    "policy_candidate_receipt": True,
    "value_witness_receipt": True,
    "barrier_witness_receipt": True,
    "candidate_only": True,
    "nonfinal_marker": True,
    "hold_review_evidence": True,
}


def task_result_for(raw, evidence=FULL_EVIDENCE):
    queue_state = dispatch_candidate_cycle(raw, empty_queue_state()).updated_queue_state
    worker_state = process_next_queue_item(queue_state).updated_worker_state
    task_board = route_next_action(worker_state).updated_task_board
    return process_next_task(task_board, evidence).task_result_receipt


class KuuOSFeedbackMergerTests(unittest.TestCase):
    def test_candidate_next_ready_sets_next_state_ready_nonfinal(self):
        receipt = task_result_for(BASE_RAW)
        result = merge_task_result_into_next_state(BASE_RAW, receipt)
        self.assertEqual(result.merge_status, "MERGED_RESOLVED_APPEND_ONLY")
        self.assertEqual(result.task_status, "CANDIDATE_NEXT_READY_NONFINAL")
        self.assertEqual(result.next_raw_state["cycle_id"], "feedback-002")
        self.assertEqual(result.next_raw_state["previous_cycle_id"], "feedback-001")
        self.assertTrue(result.next_raw_state["ready_for_next_candidate_stage"])
        self.assertTrue(result.next_raw_state["candidate_only"])
        self.assertTrue(result.next_raw_state["nonfinal_marker"])
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)
        self.assertEqual(len(result.merge_receipt["receipt_hash"]), 64)

    def test_reobserve_resolved_repairs_runtime_policy_inputs_for_next_cycle(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        receipt = task_result_for(raw, FULL_EVIDENCE)
        self.assertEqual(receipt["task_status"], "REOBSERVE_RESOLVED")
        result = merge_task_result_into_next_state(raw, receipt)
        self.assertEqual(result.merge_status, "MERGED_RESOLVED_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["runtime_variation_visible"])
        self.assertTrue(result.next_raw_state["policy_candidate_receipt"])
        self.assertTrue(result.next_raw_state["value_witness_receipt"])
        self.assertTrue(result.next_raw_state["barrier_witness_receipt"])

    def test_lineage_resolved_repairs_lineage_inputs_for_next_cycle(self):
        raw = dict(BASE_RAW)
        raw["registry_key"] = False
        receipt = task_result_for(raw, FULL_EVIDENCE)
        self.assertEqual(receipt["task_status"], "LINEAGE_RECHECK_RESOLVED")
        result = merge_task_result_into_next_state(raw, receipt)
        self.assertTrue(result.next_raw_state["receipt_hash"])
        self.assertTrue(result.next_raw_state["support_refs"])
        self.assertTrue(result.next_raw_state["registry_key"])

    def test_delivery_resolved_repairs_delivery_inputs_for_next_cycle(self):
        raw = dict(BASE_RAW)
        raw["acknowledgment_marker"] = False
        receipt = task_result_for(raw, FULL_EVIDENCE)
        self.assertEqual(receipt["task_status"], "DELIVERY_RECHECK_RESOLVED")
        result = merge_task_result_into_next_state(raw, receipt)
        self.assertTrue(result.next_raw_state["view_delivery_receipt"])
        self.assertTrue(result.next_raw_state["channel_scope"])
        self.assertTrue(result.next_raw_state["acknowledgment_marker"])

    def test_waiting_result_keeps_feedback_waiting_and_missing_evidence(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        evidence = dict(FULL_EVIDENCE)
        evidence["value_witness_receipt"] = False
        receipt = task_result_for(raw, evidence)
        self.assertEqual(receipt["task_status"], "REOBSERVE_WAITING")
        result = merge_task_result_into_next_state(raw, receipt)
        self.assertEqual(result.merge_status, "MERGED_WAITING_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["feedback_waiting"])
        self.assertIn("value_witness_receipt", result.next_raw_state["feedback_missing_evidence"])

    def test_quarantine_retained_does_not_repair_boundary_fields(self):
        raw = dict(BASE_RAW)
        raw["world_identity_blocker"] = False
        receipt = task_result_for(raw, FULL_EVIDENCE)
        self.assertEqual(receipt["task_status"], "QUARANTINE_REVIEWED_RETAINED")
        result = merge_task_result_into_next_state(raw, receipt)
        self.assertEqual(result.merge_status, "MERGED_QUARANTINE_RETAINED_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["quarantine_retained"])
        self.assertFalse(result.next_raw_state["world_identity_blocker"])

    def test_unknown_task_status_is_held(self):
        receipt = dict(task_result_for(BASE_RAW))
        receipt["task_status"] = "SOMETHING_UNKNOWN"
        result = merge_task_result_into_next_state(BASE_RAW, receipt)
        self.assertEqual(result.merge_status, "MERGED_UNKNOWN_HELD_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["feedback_waiting"])
        self.assertEqual(result.next_raw_state["feedback_status"], "UNKNOWN_RESULT_HELD")


if __name__ == "__main__":
    unittest.main()
