import unittest

from runtime.kuuos_runtime_daemon_qi_policy_flow_handoff_receiver_v0_1 import (
    compile_qi_policy_flow_handoff_receiver,
)


READY_HANDOFF = {
    "handoff_decision": "QI_POLICY_CANDIDATE_HANDOFF_READY",
    "handoff_reason": "admission_gate_admitted_candidate",
    "admitted_candidate_action": "prefer_observation_candidate",
    "candidate_only": True,
    "nonfinal_marker": True,
    "policy_flow_handoff_payload": {
        "candidate_adjustment_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
        "recommended_candidate_action": "prefer_observation_candidate",
        "candidate_priority": "high",
        "candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
        "policy_candidate_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
        "active_inference_constraints": ["no_belief_update", "no_precision_commit"],
        "candidate_only": True,
        "nonfinal_marker": True,
    },
    "final_raw_state_path": "/tmp/raw.json",
    "final_state_bundle_path": "/tmp/bundle.json",
}


class QiPolicyFlowHandoffReceiverTests(unittest.TestCase):
    def test_ready_handoff_becomes_policy_flow_candidate_intake(self):
        result = compile_qi_policy_flow_handoff_receiver(admitted_policy_candidate_handoff=READY_HANDOFF)
        self.assertEqual(result.intake_decision, "QI_POLICY_FLOW_CANDIDATE_INTAKE_READY")
        self.assertTrue(result.policy_flow_candidate_available)
        self.assertEqual(result.policy_flow_candidate_action, "prefer_observation_candidate")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN")
        self.assertGreater(result.candidate_weight_hints["epistemic_value"], 0)
        self.assertTrue(result.normalized_policy_flow_intake["candidate_only"])
        self.assertTrue(result.normalized_policy_flow_intake["nonfinal_marker"])
        self.assertFalse(result.grants_execution_authority)

    def test_blocked_handoff_stays_blocked_intake(self):
        result = compile_qi_policy_flow_handoff_receiver(
            admitted_policy_candidate_handoff={
                "handoff_decision": "QI_POLICY_CANDIDATE_HANDOFF_BLOCKED",
                "handoff_reason": "required_constraints_missing",
                "candidate_only": True,
                "nonfinal_marker": True,
                "policy_flow_handoff_payload": {
                    "blocked": True,
                    "block_reason": "required_constraints_missing",
                    "candidate_only": True,
                    "nonfinal_marker": True,
                },
            }
        )
        self.assertEqual(result.intake_decision, "QI_POLICY_FLOW_CANDIDATE_INTAKE_BLOCKED")
        self.assertFalse(result.policy_flow_candidate_available)
        self.assertIsNone(result.policy_flow_candidate_action)
        self.assertEqual(result.intake_reason, "required_constraints_missing")
        self.assertTrue(result.normalized_policy_flow_intake["candidate_only"])

    def test_missing_handoff_blocks_intake(self):
        result = compile_qi_policy_flow_handoff_receiver(admitted_policy_candidate_handoff={})
        self.assertEqual(result.intake_decision, "QI_POLICY_FLOW_CANDIDATE_INTAKE_BLOCKED")
        self.assertFalse(result.policy_flow_candidate_available)
        self.assertEqual(result.intake_reason, "handoff_not_ready")
        self.assertFalse(result.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
