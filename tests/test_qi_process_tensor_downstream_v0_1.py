import unittest

from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
from runtime.kuuos_queue_worker_v0_1 import process_next_queue_item
from runtime.kuuos_action_router_v0_1 import route_next_action
from runtime.kuuos_task_board_processor_v0_1 import process_next_task


PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "downstream-process-001",
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
    "process_history": PROCESS_HISTORY,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}

EVIDENCE = {
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


def assert_process_receipt(testcase, receipt):
    testcase.assertTrue(receipt["process_tensor_visible"])
    testcase.assertTrue(receipt["transition_continuity_visible"])
    testcase.assertTrue(receipt["memory_continuity_visible"])
    testcase.assertTrue(receipt["nonmarkov_memory_visible"])
    testcase.assertEqual(receipt["process_history_length"], 3)
    testcase.assertEqual(receipt["transition_support_count"], 3)
    testcase.assertEqual(receipt["memory_support_count"], 1)
    testcase.assertEqual(receipt["nonmarkov_support_count"], 1)
    testcase.assertEqual(receipt["process_tensor_reason"], "process_tensor_support_visible")
    testcase.assertFalse(receipt["grants_execution_authority"])
    testcase.assertFalse(receipt["grants_truth_authority"])
    testcase.assertFalse(receipt["grants_final_commitment_authority"])
    testcase.assertFalse(receipt["grants_memory_overwrite_authority"])


class QiProcessTensorDownstreamTests(unittest.TestCase):
    def test_process_tensor_receipt_flows_to_task_result(self):
        dispatch = dispatch_candidate_cycle(RAW, empty_queue_state())
        queue_entry = dispatch.updated_queue_state["queues"]["NEXT_NONFINAL_STAGE"][0]
        assert_process_receipt(self, dispatch.candidate_cycle_receipt["qi_process_tensor_receipt"])
        assert_process_receipt(self, queue_entry["qi_process_tensor_receipt"])
        assert_process_receipt(self, dispatch.updated_queue_state["dispatch_log"][0]["qi_process_tensor_receipt"])

        worker = process_next_queue_item(dispatch.updated_queue_state)
        self.assertIsNotNone(worker.action_packet)
        assert_process_receipt(self, worker.action_packet["qi_process_tensor_receipt"])
        assert_process_receipt(self, worker.updated_worker_state["worker_log"][0]["qi_process_tensor_receipt"])

        router = route_next_action(worker.updated_worker_state)
        self.assertIsNotNone(router.task_packet)
        assert_process_receipt(self, router.task_packet["qi_process_tensor_receipt"])
        assert_process_receipt(self, router.updated_task_board["router_log"][0]["qi_process_tensor_receipt"])

        processor = process_next_task(router.updated_task_board, EVIDENCE)
        self.assertIsNotNone(processor.task_result_receipt)
        self.assertEqual(processor.task_result_receipt["task_status"], "CANDIDATE_NEXT_READY_NONFINAL")
        assert_process_receipt(self, processor.task_result_receipt["qi_process_tensor_receipt"])
        assert_process_receipt(self, processor.updated_review_state["review_log"][0]["qi_process_tensor_receipt"])

    def test_boundary_blocked_process_tensor_receipt_flows_downstream(self):
        raw = dict(RAW)
        raw["noncollapse_guard"] = False
        dispatch = dispatch_candidate_cycle(raw, empty_queue_state())
        queue_entry = dispatch.updated_queue_state["queues"]["QUARANTINE_QUEUE"][0]
        process_receipt = queue_entry["qi_process_tensor_receipt"]
        self.assertFalse(process_receipt["process_tensor_visible"])
        self.assertEqual(process_receipt["process_tensor_reason"], "boundary_blocks_process_tensor_support")
        worker = process_next_queue_item(dispatch.updated_queue_state)
        self.assertFalse(worker.action_packet["qi_process_tensor_receipt"]["process_tensor_visible"])
        router = route_next_action(worker.updated_worker_state)
        self.assertFalse(router.task_packet["qi_process_tensor_receipt"]["process_tensor_visible"])
        processor = process_next_task(router.updated_task_board, EVIDENCE)
        self.assertFalse(processor.task_result_receipt["qi_process_tensor_receipt"]["process_tensor_visible"])


if __name__ == "__main__":
    unittest.main()
