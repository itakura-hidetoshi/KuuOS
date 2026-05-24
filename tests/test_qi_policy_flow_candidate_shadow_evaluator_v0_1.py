import unittest

from runtime.kuuos_runtime_daemon_qi_policy_flow_candidate_shadow_evaluator_v0_1 import (
    compile_qi_policy_flow_candidate_shadow_evaluation,
)


READY_VIEW = {
    "view_decision": "QI_POLICY_FLOW_CANDIDATE_VIEW_READY",
    "view_reason": "queued_candidate_with_required_boundaries",
    "policy_flow_view_available": True,
    "candidate_action": "prefer_observation_candidate",
    "candidate_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
    "candidate_priority": "high",
    "candidate_weight_hints": {"epistemic_value": 0.9, "action_precision": -0.3},
    "policy_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
    "active_inference_constraints": ["no_belief_update", "no_precision_commit"],
    "boundary_markers": {
        "append_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "no_policy_mutation": True,
        "no_belief_update": True,
        "no_precision_commit": True,
    },
    "final_raw_state_path": "/tmp/raw.json",
    "final_state_bundle_path": "/tmp/bundle.json",
}


class QiPolicyFlowCandidateShadowEvaluatorTests(unittest.TestCase):
    def test_ready_view_gets_shadow_score_without_authority(self):
        result = compile_qi_policy_flow_candidate_shadow_evaluation(intake_view=READY_VIEW)
        self.assertEqual(result.shadow_decision, "QI_POLICY_FLOW_CANDIDATE_SHADOW_EVALUATED")
        self.assertGreater(result.candidate_shadow_score, 0.5)
        self.assertIn(result.candidate_shadow_grade, {"moderate_shadow_candidate", "strong_shadow_candidate"})
        self.assertEqual(result.candidate_action, "prefer_observation_candidate")
        self.assertIn("policy_mutation_blocked", result.positive_terms)
        self.assertIn("belief_update_blocked", result.positive_terms)
        self.assertTrue(result.shadow_only)
        self.assertTrue(result.read_only)
        self.assertFalse(result.grants_execution_authority)

    def test_blocked_view_blocks_shadow_evaluation(self):
        result = compile_qi_policy_flow_candidate_shadow_evaluation(
            intake_view={
                "view_decision": "QI_POLICY_FLOW_CANDIDATE_VIEW_BLOCKED",
                "view_reason": "required_constraints_missing",
                "policy_flow_view_available": False,
                "policy_flow_candidate_view": {"blocked": True},
                "boundary_markers": {"candidate_only": True, "nonfinal_marker": True},
            }
        )
        self.assertEqual(result.shadow_decision, "QI_POLICY_FLOW_CANDIDATE_SHADOW_BLOCKED")
        self.assertEqual(result.candidate_shadow_score, 0.0)
        self.assertIn("intake_view_not_ready", result.blocker_terms)
        self.assertIsNone(result.candidate_action)
        self.assertFalse(result.grants_truth_authority)

    def test_missing_boundary_blocks_shadow_evaluation(self):
        bad = dict(READY_VIEW)
        bad["boundary_markers"] = dict(READY_VIEW["boundary_markers"])
        bad["boundary_markers"]["no_precision_commit"] = False
        result = compile_qi_policy_flow_candidate_shadow_evaluation(intake_view=bad)
        self.assertEqual(result.shadow_decision, "QI_POLICY_FLOW_CANDIDATE_SHADOW_BLOCKED")
        self.assertIn("required_boundary_missing", result.blocker_terms)
        self.assertIn("missing:no_precision_commit", result.warning_terms)
        self.assertEqual(result.candidate_shadow_grade, "blocked_shadow_candidate")


if __name__ == "__main__":
    unittest.main()
