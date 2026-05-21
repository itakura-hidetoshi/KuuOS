import unittest

from runtime.kuuos_action_router_v0_1 import route_next_action
from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
from runtime.kuuos_queue_worker_v0_1 import process_next_queue_item
from runtime.kuuos_task_board_processor_v0_1 import empty_review_state, process_next_task


BASE_RAW = {
    "cycle_id": "task-001",
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


def task_board_for(raw):
    queue_state = dispatch_candidate_cycle(raw, empty_queue_state()).updated_queue_state
    worker_state = process_next_queue_item(queue_state).updated_worker_state
    return route_next_action(worker_state).updated_task_board


class KuuOSTaskBoardProcessorTests(unittest.TestCase):
    def test_candidate_next_task_resolves_nonfinal(self):
        board = task_board_for(BASE_RAW)
        result = process_next_task(board, FULL_EVIDENCE)
        self.assertEqual(result.processor_status, "PROCESSED_ONE_TASK_APPEND_ONLY")
        self.assertEqual(result.selected_task_queue, "candidate_next_tasks")
        self.assertEqual(result.task_result_receipt["task_status"], "CANDIDATE_NEXT_READY_NONFINAL")
        self.assertEqual(len(result.task_result_receipt["receipt_hash"]), 64)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)

    def test_candidate_next_task_waits_when_evidence_missing(self):
        board = task_board_for(BASE_RAW)
        evidence = dict(FULL_EVIDENCE)
        evidence["noncollapse_guard"] = False
        result = process_next_task(board, evidence)
        self.assertEqual(result.task_result_receipt["task_status"], "CANDIDATE_NEXT_WAITING")
        self.assertIn("noncollapse_guard", result.task_result_receipt["missing_evidence"])

    def test_quarantine_task_has_safety_priority_and_retains_quarantine(self):
        raw_good = dict(BASE_RAW)
        raw_good["cycle_id"] = "task-good"
        raw_bad = dict(BASE_RAW)
        raw_bad["cycle_id"] = "task-bad"
        raw_bad["world_identity_blocker"] = False
        queue_state = empty_queue_state()
        queue_state = dispatch_candidate_cycle(raw_good, queue_state).updated_queue_state
        queue_state = dispatch_candidate_cycle(raw_bad, queue_state).updated_queue_state
        worker_one = process_next_queue_item(queue_state).updated_worker_state
        board = route_next_action(worker_one).updated_task_board
        result = process_next_task(board, FULL_EVIDENCE)
        self.assertEqual(result.selected_task_queue, "quarantine_tasks")
        self.assertEqual(result.task_result_receipt["task_status"], "QUARANTINE_REVIEWED_RETAINED")
        self.assertIn("quarantine_review_receipt", result.task_result_receipt["opened_notices"])

    def test_quarantine_task_waits_if_boundary_review_missing(self):
        raw = dict(BASE_RAW)
        raw["world_identity_blocker"] = False
        board = task_board_for(raw)
        evidence = dict(FULL_EVIDENCE)
        evidence["boundary_review_evidence"] = False
        result = process_next_task(board, evidence)
        self.assertEqual(result.selected_task_queue, "quarantine_tasks")
        self.assertEqual(result.task_result_receipt["task_status"], "QUARANTINE_REVIEW_WAITING")
        self.assertIn("boundary_review_evidence", result.task_result_receipt["missing_evidence"])

    def test_lineage_task_resolves_with_hash_support_registry(self):
        raw = dict(BASE_RAW)
        raw["registry_key"] = False
        board = task_board_for(raw)
        result = process_next_task(board, FULL_EVIDENCE)
        self.assertEqual(result.selected_task_queue, "lineage_recheck_tasks")
        self.assertEqual(result.task_result_receipt["task_status"], "LINEAGE_RECHECK_RESOLVED")

    def test_delivery_task_resolves_with_delivery_evidence(self):
        raw = dict(BASE_RAW)
        raw["acknowledgment_marker"] = False
        board = task_board_for(raw)
        result = process_next_task(board, FULL_EVIDENCE)
        self.assertEqual(result.selected_task_queue, "delivery_recheck_tasks")
        self.assertEqual(result.task_result_receipt["task_status"], "DELIVERY_RECHECK_RESOLVED")

    def test_reobserve_task_waits_for_policy_evidence(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        board = task_board_for(raw)
        evidence = dict(FULL_EVIDENCE)
        evidence["value_witness_receipt"] = False
        result = process_next_task(board, evidence)
        self.assertEqual(result.selected_task_queue, "reobserve_tasks")
        self.assertEqual(result.task_result_receipt["task_status"], "REOBSERVE_WAITING")
        self.assertIn("value_witness_receipt", result.task_result_receipt["missing_evidence"])

    def test_processor_skips_already_processed_task(self):
        board = task_board_for(BASE_RAW)
        first = process_next_task(board, FULL_EVIDENCE)
        second = process_next_task(board, FULL_EVIDENCE, first.updated_review_state)
        self.assertEqual(second.processor_status, "NO_UNPROCESSED_TASK_PACKET")
        self.assertIsNone(second.task_result_receipt)
        self.assertEqual(len(second.updated_review_state["task_result_receipts"]), 1)

    def test_empty_review_state_has_no_authority(self):
        state = empty_review_state()
        self.assertEqual(state["processed_task_hashes"], [])
        self.assertEqual(state["task_result_receipts"], [])
        self.assertFalse(state["grants_execution_authority"])
        self.assertFalse(state["grants_truth_authority"])
        self.assertFalse(state["grants_final_commitment_authority"])
        self.assertFalse(state["grants_memory_overwrite_authority"])


if __name__ == "__main__":
    unittest.main()
