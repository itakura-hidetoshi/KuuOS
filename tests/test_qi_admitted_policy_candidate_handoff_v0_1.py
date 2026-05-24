import unittest

from runtime.kuuos_runtime_daemon_qi_admitted_policy_candidate_handoff_v0_1 import (
    compile_qi_admitted_policy_candidate_handoff,
)


ADAPTER = {
    "candidate_adjustment_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
    "recommended_candidate_action": "prefer_observation_candidate",
    "candidate_priority": "high",
    "candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
    "policy_candidate_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
    "active_inference_constraints": ["no_belief_update", "no_precision_commit"],
    "candidate_only": True,
    "nonfinal_marker": True,
    "final_raw_state_path": "/tmp/raw.json",
    "final_state_bundle_path": "/tmp/bundle.json",
}

ADMISSION = {
    "admission_decision": "QI_POLICY_CANDIDATE_ADMITTED",
    "admission_reason": "candidate_only_nonfinal_constraints_satisfied",
    "admitted_candidate_action": "prefer_observation_candidate",
}


class QiAdmittedPolicyCandidateHandoffTests(unittest.TestCase):
    def test_admitted_candidate_builds_policy_flow_handoff_payload(self):
        result = compile_qi_admitted_policy_candidate_handoff(
            candidate_adapter=ADAPTER,
            admission_gate=ADMISSION,
        )
        self.assertEqual(result.handoff_decision, "QI_POLICY_CANDIDATE_HANDOFF_READY")
        self.assertEqual(result.admitted_candidate_action, "prefer_observation_candidate")
        self.assertEqual(result.policy_flow_handoff_payload["candidate_adjustment_class"], "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN")
        self.assertEqual(result.policy_flow_handoff_payload["recommended_candidate_action"], "prefer_observation_candidate")
        self.assertTrue(result.policy_flow_handoff_payload["candidate_only"])
        self.assertTrue(result.policy_flow_handoff_payload["nonfinal_marker"])
        self.assertIn("candidate_weight_hints", result.policy_flow_handoff_payload)
        self.assertEqual(result.final_raw_state_path, "/tmp/raw.json")
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_blocked_candidate_builds_blocked_payload(self):
        result = compile_qi_admitted_policy_candidate_handoff(
            candidate_adapter=ADAPTER,
            admission_gate={
                "admission_decision": "QI_POLICY_CANDIDATE_NOT_ADMITTED",
                "admission_reason": "required_constraints_missing",
            },
        )
        self.assertEqual(result.handoff_decision, "QI_POLICY_CANDIDATE_HANDOFF_BLOCKED")
        self.assertEqual(result.handoff_reason, "required_constraints_missing")
        self.assertIsNone(result.admitted_candidate_action)
        self.assertTrue(result.policy_flow_handoff_payload["blocked"])
        self.assertEqual(result.policy_flow_handoff_payload["block_reason"], "required_constraints_missing")
        self.assertTrue(result.candidate_only)
        self.assertTrue(result.nonfinal_marker)

    def test_missing_admission_blocks_handoff(self):
        result = compile_qi_admitted_policy_candidate_handoff(
            candidate_adapter=ADAPTER,
            admission_gate={},
        )
        self.assertEqual(result.handoff_decision, "QI_POLICY_CANDIDATE_HANDOFF_BLOCKED")
        self.assertEqual(result.handoff_reason, "candidate_not_admitted_or_missing")


if __name__ == "__main__":
    unittest.main()
