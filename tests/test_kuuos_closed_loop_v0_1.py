import unittest

from runtime.kuuos_closed_loop_v0_1 import empty_loop_state_bundle, run_closed_loop_step

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": True},
]

BASE_RAW = {
    "cycle_id": "loop-001",
    "next_cycle_id": "loop-002",
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


def assert_process_summary(testcase, summary):
    testcase.assertTrue(summary["process_tensor_visible"])
    testcase.assertTrue(summary["transition_continuity_visible"])
    testcase.assertTrue(summary["memory_continuity_visible"])
    testcase.assertTrue(summary["nonmarkov_memory_visible"])
    testcase.assertEqual(summary["process_history_length"], 3)
    testcase.assertEqual(summary["transition_support_count"], 3)
    testcase.assertEqual(summary["memory_support_count"], 1)
    testcase.assertEqual(summary["nonmarkov_support_count"], 1)
    testcase.assertEqual(summary["process_tensor_reason"], "process_tensor_support_visible")
    testcase.assertFalse(summary["grants_execution_authority"])
    testcase.assertFalse(summary["grants_truth_authority"])


class KuuOSClosedLoopRunnerTests(unittest.TestCase):
    def test_closed_loop_completes_candidate_next_step(self):
        result = run_closed_loop_step(BASE_RAW, FULL_EVIDENCE)
        self.assertEqual(result.loop_status, "LOOP_STEP_COMPLETED_APPEND_ONLY")
        self.assertEqual(result.raw_cycle_id, "loop-001")
        self.assertEqual(result.next_cycle_id, "loop-002")
        self.assertEqual(result.queue_dispatch["target_queue"], "NEXT_NONFINAL_STAGE")
        self.assertEqual(result.queue_worker["selected_queue"], "NEXT_NONFINAL_STAGE")
        self.assertEqual(result.action_router["target_task_queue"], "candidate_next_tasks")
        self.assertEqual(result.task_processor["task_result_receipt"]["task_status"], "CANDIDATE_NEXT_READY_NONFINAL")
        self.assertEqual(result.feedback_merge["merge_status"], "MERGED_RESOLVED_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["ready_for_next_candidate_stage"])
        self.assertEqual(len(result.updated_state_bundle["loop_log"]), 1)
        assert_process_summary(self, result.updated_state_bundle["loop_log"][0]["qi_process_tensor_summary"])
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)

    def test_closed_loop_reobserve_waiting_preserved_in_next_state(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        raw["process_history"] = []
        evidence = dict(FULL_EVIDENCE)
        evidence["value_witness_receipt"] = False
        result = run_closed_loop_step(raw, evidence)
        self.assertEqual(result.queue_dispatch["target_queue"], "REOBSERVE_QUEUE")
        self.assertEqual(result.action_router["target_task_queue"], "reobserve_tasks")
        self.assertEqual(result.task_processor["task_result_receipt"]["task_status"], "REOBSERVE_WAITING")
        self.assertEqual(result.feedback_merge["merge_status"], "MERGED_WAITING_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["feedback_waiting"])
        self.assertIn("value_witness_receipt", result.next_raw_state["feedback_missing_evidence"])
        summary = result.updated_state_bundle["loop_log"][0]["qi_process_tensor_summary"]
        self.assertFalse(summary["process_tensor_visible"])
        self.assertIn("process_history_min_length_or_explicit_process_tensor", summary["missing_process_requirements"])

    def test_closed_loop_quarantine_retained_does_not_repair_boundary(self):
        raw = dict(BASE_RAW)
        raw["world_identity_blocker"] = False
        result = run_closed_loop_step(raw, FULL_EVIDENCE)
        self.assertEqual(result.queue_dispatch["target_queue"], "QUARANTINE_QUEUE")
        self.assertEqual(result.action_router["target_task_queue"], "quarantine_tasks")
        self.assertEqual(result.task_processor["task_result_receipt"]["task_status"], "QUARANTINE_REVIEWED_RETAINED")
        self.assertEqual(result.feedback_merge["merge_status"], "MERGED_QUARANTINE_RETAINED_APPEND_ONLY")
        self.assertTrue(result.next_raw_state["quarantine_retained"])
        self.assertFalse(result.next_raw_state["world_identity_blocker"])
        summary = result.updated_state_bundle["loop_log"][0]["qi_process_tensor_summary"]
        self.assertFalse(summary["process_tensor_visible"])
        self.assertEqual(summary["process_tensor_reason"], "boundary_blocks_process_tensor_support")

    def test_closed_loop_appends_to_existing_bundle(self):
        first = run_closed_loop_step(BASE_RAW, FULL_EVIDENCE)
        raw2 = dict(first.next_raw_state)
        raw2["next_cycle_id"] = "loop-003"
        raw2["generated_at_utc"] = "2026-05-21T00:01:00+00:00"
        raw2["dispatched_at_utc"] = "2026-05-21T00:01:01+00:00"
        second = run_closed_loop_step(raw2, FULL_EVIDENCE, first.updated_state_bundle)
        self.assertEqual(len(second.updated_state_bundle["loop_log"]), 2)
        self.assertEqual(second.next_cycle_id, "loop-003")
        self.assertEqual(len(second.updated_state_bundle["queue_state"]["dispatch_log"]), 2)
        self.assertEqual(len(second.updated_state_bundle["worker_state"]["worker_log"]), 2)
        self.assertEqual(len(second.updated_state_bundle["review_state"]["task_result_receipts"]), 2)
        assert_process_summary(self, second.updated_state_bundle["loop_log"][0]["qi_process_tensor_summary"])

    def test_empty_loop_state_bundle_has_no_authority(self):
        bundle = empty_loop_state_bundle()
        self.assertIn("queue_state", bundle)
        self.assertIn("worker_state", bundle)
        self.assertIn("review_state", bundle)
        self.assertFalse(bundle["grants_execution_authority"])
        self.assertFalse(bundle["grants_truth_authority"])
        self.assertFalse(bundle["grants_final_commitment_authority"])
        self.assertFalse(bundle["grants_memory_overwrite_authority"])


if __name__ == "__main__":
    unittest.main()
