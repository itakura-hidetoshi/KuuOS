import unittest

from runtime.kuuos_closed_loop_driver_v0_1 import run_closed_loop_driver

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": True},
]

BASE_RAW = {
    "cycle_id": "driver-001",
    "next_cycle_id": "driver-002",
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
    testcase.assertEqual(summary["process_tensor_reason"], "process_tensor_support_visible")
    testcase.assertFalse(summary["grants_execution_authority"])
    testcase.assertFalse(summary["grants_truth_authority"])


class KuuOSClosedLoopDriverTests(unittest.TestCase):
    def test_driver_runs_bounded_steps_until_max_steps(self):
        result = run_closed_loop_driver(BASE_RAW, FULL_EVIDENCE, max_steps=2)
        self.assertEqual(result.driver_status, "DRIVER_MAX_STEPS_REACHED_APPEND_ONLY")
        self.assertEqual(result.stop_reason, "MAX_STEPS_REACHED")
        self.assertEqual(result.steps_run, 2)
        self.assertEqual(len(result.step_trace), 2)
        self.assertEqual(len(result.final_state_bundle["loop_log"]), 2)
        assert_process_summary(self, result.step_trace[0]["qi_process_tensor_summary"])
        assert_process_summary(self, result.final_state_bundle["loop_log"][0]["qi_process_tensor_summary"])
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)

    def test_driver_stops_on_waiting_for_more_evidence(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        raw["process_history"] = []
        evidence = dict(FULL_EVIDENCE)
        evidence["value_witness_receipt"] = False
        result = run_closed_loop_driver(raw, evidence, max_steps=5)
        self.assertEqual(result.driver_status, "DRIVER_WAITING_APPEND_ONLY")
        self.assertEqual(result.stop_reason, "WAITING_FOR_MORE_EVIDENCE")
        self.assertEqual(result.steps_run, 1)
        self.assertTrue(result.final_raw_state["feedback_waiting"])
        self.assertIn("value_witness_receipt", result.final_raw_state["feedback_missing_evidence"])
        summary = result.step_trace[0]["qi_process_tensor_summary"]
        self.assertFalse(summary["process_tensor_visible"])
        self.assertIn("process_history_min_length_or_explicit_process_tensor", summary["missing_process_requirements"])

    def test_driver_stops_on_quarantine_retained(self):
        raw = dict(BASE_RAW)
        raw["world_identity_blocker"] = False
        result = run_closed_loop_driver(raw, FULL_EVIDENCE, max_steps=5)
        self.assertEqual(result.driver_status, "DRIVER_QUARANTINE_RETAINED_APPEND_ONLY")
        self.assertEqual(result.stop_reason, "QUARANTINE_RETAINED")
        self.assertEqual(result.steps_run, 1)
        self.assertTrue(result.final_raw_state["quarantine_retained"])
        self.assertFalse(result.final_raw_state["world_identity_blocker"])
        summary = result.step_trace[0]["qi_process_tensor_summary"]
        self.assertFalse(summary["process_tensor_visible"])
        self.assertEqual(summary["process_tensor_reason"], "boundary_blocks_process_tensor_support")

    def test_driver_uses_evidence_sequence_per_step(self):
        evidence_sequence = [FULL_EVIDENCE, FULL_EVIDENCE]
        result = run_closed_loop_driver(BASE_RAW, evidence_sequence, max_steps=2)
        self.assertEqual(result.steps_run, 2)
        self.assertEqual(result.step_trace[0]["task_status"], "CANDIDATE_NEXT_READY_NONFINAL")
        self.assertEqual(result.step_trace[1]["task_status"], "CANDIDATE_NEXT_READY_NONFINAL")
        assert_process_summary(self, result.step_trace[0]["qi_process_tensor_summary"])

    def test_driver_hard_caps_large_max_steps(self):
        result = run_closed_loop_driver(BASE_RAW, FULL_EVIDENCE, max_steps=100)
        self.assertEqual(result.stop_reason, "MAX_STEPS_REACHED")
        self.assertEqual(result.steps_run, 25)
        assert_process_summary(self, result.step_trace[0]["qi_process_tensor_summary"])

    def test_driver_minimum_one_step_for_zero_max_steps(self):
        result = run_closed_loop_driver(BASE_RAW, FULL_EVIDENCE, max_steps=0)
        self.assertEqual(result.steps_run, 1)
        assert_process_summary(self, result.step_trace[0]["qi_process_tensor_summary"])

    def test_driver_accepts_existing_state_bundle_append_only(self):
        first = run_closed_loop_driver(BASE_RAW, FULL_EVIDENCE, max_steps=1)
        raw2 = dict(first.final_raw_state)
        raw2["next_cycle_id"] = "driver-003"
        raw2["generated_at_utc"] = "2026-05-21T00:01:00+00:00"
        raw2["dispatched_at_utc"] = "2026-05-21T00:01:01+00:00"
        second = run_closed_loop_driver(raw2, FULL_EVIDENCE, max_steps=1, state_bundle=first.final_state_bundle)
        self.assertEqual(len(second.final_state_bundle["loop_log"]), 2)
        self.assertEqual(len(second.final_state_bundle["queue_state"]["dispatch_log"]), 2)
        self.assertEqual(len(second.final_state_bundle["worker_state"]["worker_log"]), 2)
        self.assertEqual(len(second.final_state_bundle["review_state"]["task_result_receipts"]), 2)
        assert_process_summary(self, second.step_trace[0]["qi_process_tensor_summary"])


if __name__ == "__main__":
    unittest.main()
