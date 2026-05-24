import unittest

from runtime.kuuos_runtime_daemon_qi_policy_flow_candidate_inbox_v0_1 import (
    compile_qi_policy_flow_candidate_inbox,
)


READY_RECEIVER = {
    "intake_decision": "QI_POLICY_FLOW_CANDIDATE_INTAKE_READY",
    "intake_reason": "handoff_ready_candidate_only_nonfinal",
    "policy_flow_candidate_available": True,
    "policy_flow_candidate_action": "prefer_observation_candidate",
    "candidate_adjustment_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
    "candidate_priority": "high",
    "candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
    "policy_candidate_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
    "active_inference_constraints": ["no_belief_update", "no_precision_commit"],
    "normalized_policy_flow_intake": {
        "policy_flow_candidate_available": True,
        "candidate_action": "prefer_observation_candidate",
        "candidate_adjustment_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
        "candidate_priority": "high",
        "candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
        "candidate_only": True,
        "nonfinal_marker": True,
    },
    "candidate_only": True,
    "nonfinal_marker": True,
    "final_raw_state_path": "/tmp/raw.json",
    "final_state_bundle_path": "/tmp/bundle.json",
}


class QiPolicyFlowCandidateInboxTests(unittest.TestCase):
    def test_ready_receiver_queues_candidate_only_packet(self):
        result = compile_qi_policy_flow_candidate_inbox(receiver_result=READY_RECEIVER)
        self.assertEqual(result.inbox_decision, "QI_POLICY_FLOW_CANDIDATE_QUEUED")
        self.assertTrue(result.queued_candidate_available)
        self.assertEqual(result.queued_candidate_action, "prefer_observation_candidate")
        self.assertEqual(result.queued_candidate_class, "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN")
        self.assertGreater(result.queued_candidate_weight_hints["epistemic_value"], 0)
        self.assertTrue(result.inbox_packet["candidate_only"])
        self.assertTrue(result.inbox_packet["append_only"])
        self.assertFalse(result.grants_execution_authority)

    def test_blocked_receiver_does_not_queue_candidate(self):
        result = compile_qi_policy_flow_candidate_inbox(
            receiver_result={
                "intake_decision": "QI_POLICY_FLOW_CANDIDATE_INTAKE_BLOCKED",
                "intake_reason": "required_constraints_missing",
                "policy_flow_candidate_available": False,
                "candidate_only": True,
                "nonfinal_marker": True,
            }
        )
        self.assertEqual(result.inbox_decision, "QI_POLICY_FLOW_CANDIDATE_NOT_QUEUED")
        self.assertFalse(result.queued_candidate_available)
        self.assertIsNone(result.queued_candidate_action)
        self.assertTrue(result.inbox_packet["blocked"])
        self.assertEqual(result.inbox_packet["block_reason"], "required_constraints_missing")

    def test_missing_receiver_does_not_queue_candidate(self):
        result = compile_qi_policy_flow_candidate_inbox(receiver_result={})
        self.assertEqual(result.inbox_decision, "QI_POLICY_FLOW_CANDIDATE_NOT_QUEUED")
        self.assertEqual(result.inbox_packet["queue_status"], "blocked_candidate_only")
        self.assertTrue(result.candidate_only)
        self.assertTrue(result.nonfinal_marker)
        self.assertFalse(result.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
