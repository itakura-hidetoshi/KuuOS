import unittest

from runtime.kuuos_runtime_daemon_qi_policy_feedback_candidate_adapter_v0_1 import (
    compile_qi_policy_feedback_candidate_adapter,
)


def adapted(policy_class):
    return compile_qi_policy_feedback_candidate_adapter(
        policy_feedback_surface={
            "policy_feedback_class": policy_class,
            "policy_flow_candidate_signal": "signal",
            "active_inference_candidate_signal": "active",
            "final_raw_state_path": "/tmp/raw.json",
            "final_state_bundle_path": "/tmp/bundle.json",
        }
    )


class QiPolicyFeedbackCandidateAdapterTests(unittest.TestCase):
    def test_safety_hold_maps_to_barrier_and_precision_constraints(self):
        result = adapted("POLICY_FEEDBACK_SAFETY_HOLD")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_SAFETY_HOLD")
        self.assertEqual(result.recommended_candidate_action, "prefer_safe_hold_candidate")
        self.assertEqual(result.candidate_weight_hints["safety_barrier"], 1.0)
        self.assertLess(result.candidate_weight_hints["action_precision"], 0)
        self.assertIn("block_reentry_escalation", result.policy_candidate_constraints)
        self.assertTrue(result.candidate_only)
        self.assertFalse(result.grants_execution_authority)

    def test_information_gain_maps_to_epistemic_value(self):
        result = adapted("POLICY_FEEDBACK_INFORMATION_GAIN")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN")
        self.assertGreater(result.candidate_weight_hints["epistemic_value"], 0)
        self.assertIn("prefer_observation_candidate", result.policy_candidate_constraints)
        self.assertIn("increase_epistemic_value", result.active_inference_constraints)

    def test_trace_load_maps_to_compaction_constraints(self):
        result = adapted("POLICY_FEEDBACK_TRACE_LOAD")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_TRACE_LOAD_REDUCTION")
        self.assertGreater(result.candidate_weight_hints["trace_load_penalty"], 0)
        self.assertIn("do_not_extend_rollout_until_compacted", result.policy_candidate_constraints)

    def test_reentry_rollout_maps_to_candidate_only_rollout(self):
        result = adapted("POLICY_FEEDBACK_REENTRY_ROLLOUT")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_REENTRY_ROLLOUT")
        self.assertGreater(result.candidate_weight_hints["reentry_rollout_value"], 0)
        self.assertIn("do_not_commit_reentry_as_truth", result.policy_candidate_constraints)
        self.assertEqual(result.final_raw_state_path, "/tmp/raw.json")

    def test_precondition_gap_maps_to_repair_candidate(self):
        result = adapted("POLICY_FEEDBACK_REENTRY_PRECONDITION_GAP")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_PRECONDITION_REPAIR")
        self.assertGreater(result.candidate_weight_hints["precondition_repair"], 0)
        self.assertLess(result.candidate_weight_hints["reentry_rollout_value"], 0)
        self.assertIn("do_not_retry_reentry_without_inputs", result.policy_candidate_constraints)

    def test_no_action_stays_candidate_only_nonfinal(self):
        result = adapted("POLICY_FEEDBACK_NO_ACTION")
        self.assertEqual(result.candidate_adjustment_class, "CANDIDATE_ADJUSTMENT_NO_ACTION")
        self.assertEqual(result.recommended_candidate_action, "keep_current_candidate")
        self.assertTrue(result.nonfinal_marker)
        self.assertFalse(result.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
