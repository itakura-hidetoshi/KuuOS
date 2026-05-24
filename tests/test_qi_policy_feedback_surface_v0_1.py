import unittest

from runtime.kuuos_runtime_daemon_qi_policy_feedback_surface_v0_1 import compile_qi_policy_feedback_surface


def surface(signal):
    return compile_qi_policy_feedback_surface(
        recovery_feedback={
            "feedback_signal": signal,
            "feedback_priority": "high",
            "policy_adjustment_hint": "hint",
            "active_inference_hint": "active_hint",
            "final_raw_state_path": "/tmp/raw.json",
            "final_state_bundle_path": "/tmp/bundle.json",
        }
    )


class QiPolicyFeedbackSurfaceTests(unittest.TestCase):
    def test_hold_feedback_maps_to_safety_hold_policy(self):
        result = surface("QI_FEEDBACK_HOLD_REQUIRED")
        self.assertEqual(result.policy_feedback_class, "POLICY_FEEDBACK_SAFETY_HOLD")
        self.assertEqual(result.policy_flow_candidate_signal, "prefer_safe_hold_policy_candidate")
        self.assertEqual(result.safety_barrier_hint, "raise_safety_barrier")
        self.assertTrue(result.candidate_only)
        self.assertFalse(result.grants_execution_authority)

    def test_observation_feedback_maps_to_information_gain_policy(self):
        result = surface("QI_FEEDBACK_OBSERVATION_REQUIRED")
        self.assertEqual(result.policy_feedback_class, "POLICY_FEEDBACK_INFORMATION_GAIN")
        self.assertEqual(result.policy_flow_candidate_signal, "prefer_observation_policy_candidate")
        self.assertEqual(result.efe_weight_hint, "increase_epistemic_value")
        self.assertEqual(result.observation_value_hint, "observation_required")

    def test_compaction_feedback_maps_to_trace_load_policy(self):
        result = surface("QI_FEEDBACK_COMPACTION_REQUIRED")
        self.assertEqual(result.policy_feedback_class, "POLICY_FEEDBACK_TRACE_LOAD")
        self.assertEqual(result.policy_flow_candidate_signal, "prefer_trace_load_reduction_candidate")
        self.assertEqual(result.compaction_load_hint, "compaction_required")

    def test_reentry_performed_maps_to_candidate_rollout_policy(self):
        result = surface("QI_FEEDBACK_REENTRY_PERFORMED")
        self.assertEqual(result.policy_feedback_class, "POLICY_FEEDBACK_REENTRY_ROLLOUT")
        self.assertEqual(result.policy_flow_candidate_signal, "incorporate_candidate_reentry_rollout")
        self.assertEqual(result.reentry_rollout_hint, "bounded_reentry_feedback_available")
        self.assertEqual(result.final_raw_state_path, "/tmp/raw.json")

    def test_reentry_blocked_maps_to_precondition_repair_policy(self):
        result = surface("QI_FEEDBACK_REENTRY_BLOCKED")
        self.assertEqual(result.policy_feedback_class, "POLICY_FEEDBACK_REENTRY_PRECONDITION_GAP")
        self.assertEqual(result.policy_flow_candidate_signal, "prefer_precondition_repair_over_reentry")
        self.assertEqual(result.reentry_rollout_hint, "reentry_blocked")

    def test_unknown_feedback_stays_no_action(self):
        result = surface("QI_FEEDBACK_NO_ACTION")
        self.assertEqual(result.policy_feedback_class, "POLICY_FEEDBACK_NO_ACTION")
        self.assertEqual(result.policy_flow_candidate_signal, "keep_current_policy_candidate")
        self.assertTrue(result.nonfinal_marker)


if __name__ == "__main__":
    unittest.main()
