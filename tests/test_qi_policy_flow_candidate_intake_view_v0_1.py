import unittest

from runtime.kuuos_runtime_daemon_qi_policy_flow_candidate_intake_view_v0_1 import (
    compile_qi_policy_flow_candidate_intake_view,
)


READY_INBOX = {
    "inbox_decision": "QI_POLICY_FLOW_CANDIDATE_QUEUED",
    "inbox_reason": "receiver_candidate_available_candidate_only_nonfinal",
    "queued_candidate_available": True,
    "queued_candidate_action": "prefer_observation_candidate",
    "queued_candidate_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
    "queued_candidate_priority": "high",
    "queued_candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
    "queued_policy_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
    "queued_active_inference_constraints": ["no_belief_update", "no_precision_commit"],
    "inbox_packet": {
        "queue_status": "queued_candidate_only",
        "candidate_action": "prefer_observation_candidate",
        "candidate_adjustment_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
        "candidate_priority": "high",
        "candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
        "policy_candidate_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
        "active_inference_constraints": ["no_belief_update", "no_precision_commit"],
        "candidate_only": True,
        "nonfinal_marker": True,
        "append_only": True,
    },
    "append_only": True,
    "candidate_only": True,
    "nonfinal_marker": True,
    "final_raw_state_path": "/tmp/raw.json",
    "final_state_bundle_path": "/tmp/bundle.json",
}


class QiPolicyFlowCandidateIntakeViewTests(unittest.TestCase):
    def test_queued_inbox_becomes_ready_candidate_view(self):
        result = compile_qi_policy_flow_candidate_intake_view(inbox_packet=READY_INBOX)
        self.assertEqual(result.view_decision, "QI_POLICY_FLOW_CANDIDATE_VIEW_READY")
        self.assertTrue(result.policy_flow_view_available)
        self.assertEqual(result.candidate_action, "prefer_observation_candidate")
        self.assertEqual(result.candidate_class, "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN")
        self.assertGreater(result.candidate_weight_hints["epistemic_value"], 0)
        self.assertTrue(result.boundary_markers["append_only"])
        self.assertTrue(result.boundary_markers["candidate_only"])
        self.assertTrue(result.boundary_markers["nonfinal_marker"])
        self.assertTrue(result.boundary_markers["no_policy_mutation"])
        self.assertTrue(result.boundary_markers["no_belief_update"])
        self.assertTrue(result.boundary_markers["no_precision_commit"])
        self.assertFalse(result.grants_execution_authority)

    def test_blocked_inbox_stays_blocked_view(self):
        result = compile_qi_policy_flow_candidate_intake_view(
            inbox_packet={
                "inbox_decision": "QI_POLICY_FLOW_CANDIDATE_NOT_QUEUED",
                "inbox_reason": "required_constraints_missing",
                "queued_candidate_available": False,
                "inbox_packet": {
                    "queue_status": "blocked_candidate_only",
                    "blocked": True,
                    "block_reason": "required_constraints_missing",
                    "candidate_only": True,
                    "nonfinal_marker": True,
                    "append_only": True,
                },
                "append_only": True,
                "candidate_only": True,
                "nonfinal_marker": True,
            }
        )
        self.assertEqual(result.view_decision, "QI_POLICY_FLOW_CANDIDATE_VIEW_BLOCKED")
        self.assertFalse(result.policy_flow_view_available)
        self.assertEqual(result.view_reason, "required_constraints_missing")
        self.assertTrue(result.policy_flow_candidate_view["blocked"])
        self.assertTrue(result.candidate_only)
        self.assertTrue(result.nonfinal_marker)

    def test_boundary_missing_blocks_ready_candidate(self):
        bad = dict(READY_INBOX)
        bad["queued_active_inference_constraints"] = ["no_belief_update"]
        bad["inbox_packet"] = dict(READY_INBOX["inbox_packet"])
        bad["inbox_packet"]["active_inference_constraints"] = ["no_belief_update"]
        result = compile_qi_policy_flow_candidate_intake_view(inbox_packet=bad)
        self.assertEqual(result.view_decision, "QI_POLICY_FLOW_CANDIDATE_VIEW_BLOCKED")
        self.assertFalse(result.boundary_markers["no_precision_commit"])
        self.assertFalse(result.policy_flow_view_available)
        self.assertFalse(result.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
