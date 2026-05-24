import unittest

from runtime.kuuos_runtime_daemon_qi_recovery_feedback_bridge_v0_1 import compile_qi_recovery_feedback


class QiRecoveryFeedbackBridgeTests(unittest.TestCase):
    def test_hold_route_yields_safety_feedback(self):
        feedback = compile_qi_recovery_feedback(
            route_result={"route_decision": "ROUTE_HOLD", "next_outer_action": "hold"}
        )
        self.assertEqual(feedback.feedback_signal, "QI_FEEDBACK_HOLD_REQUIRED")
        self.assertEqual(feedback.policy_adjustment_hint, "raise_safety_barrier_and_request_review")
        self.assertEqual(feedback.feedback_priority, "critical")
        self.assertFalse(feedback.grants_execution_authority)

    def test_observation_route_yields_information_gain_feedback(self):
        feedback = compile_qi_recovery_feedback(
            route_result={"route_decision": "ROUTE_OBSERVATION", "next_outer_action": "reobserve"}
        )
        self.assertEqual(feedback.feedback_signal, "QI_FEEDBACK_OBSERVATION_REQUIRED")
        self.assertEqual(feedback.policy_adjustment_hint, "prefer_information_gain_over_reentry")
        self.assertEqual(feedback.active_inference_hint, "increase_epistemic_value_weight")
        self.assertEqual(feedback.observation_feedback, "reobserve_required")

    def test_compaction_route_yields_trace_load_feedback(self):
        feedback = compile_qi_recovery_feedback(
            route_result={"route_decision": "ROUTE_COMPACTION", "next_outer_action": "compact_trace"}
        )
        self.assertEqual(feedback.feedback_signal, "QI_FEEDBACK_COMPACTION_REQUIRED")
        self.assertEqual(feedback.policy_adjustment_hint, "reduce_trace_load_before_more_reentry")
        self.assertEqual(feedback.compaction_feedback, "compact_trace_required")

    def test_reentry_performed_yields_candidate_rollout_feedback(self):
        feedback = compile_qi_recovery_feedback(
            dispatch_result={
                "route_decision": "ROUTE_REENTRY",
                "next_outer_action": "managed_reentry_chain",
                "dispatcher_status": "QI_RUNTIME_OUTPUT_ACTION_DISPATCHED",
                "action_invoked": True,
                "invoked_action": "managed_reentry_chain",
                "reentry_cycles_run": 1,
                "reentry_ticks_invoked": 1,
                "final_raw_state_path": "/tmp/raw.json",
                "final_state_bundle_path": "/tmp/bundle.json",
                "dispatch_reason": "MAX_CYCLES_REACHED",
            }
        )
        self.assertEqual(feedback.feedback_signal, "QI_FEEDBACK_REENTRY_PERFORMED")
        self.assertEqual(feedback.policy_adjustment_hint, "incorporate_reentry_result_as_candidate_rollout_feedback")
        self.assertEqual(feedback.reentry_feedback, "bounded_reentry_invoked")
        self.assertEqual(feedback.final_raw_state_path, "/tmp/raw.json")

    def test_reentry_blocked_yields_precondition_feedback(self):
        feedback = compile_qi_recovery_feedback(
            dispatch_result={
                "route_decision": "ROUTE_REENTRY",
                "next_outer_action": "managed_reentry_chain",
                "dispatcher_status": "QI_RUNTIME_OUTPUT_ACTION_NOT_DISPATCHED",
                "action_invoked": False,
                "dispatch_reason": "managed_reentry_requires_raw_state_and_evidence",
            }
        )
        self.assertEqual(feedback.feedback_signal, "QI_FEEDBACK_REENTRY_BLOCKED")
        self.assertEqual(feedback.policy_adjustment_hint, "do_not_escalate_reentry_without_missing_inputs")
        self.assertEqual(feedback.reentry_feedback, "reentry_route_blocked")


if __name__ == "__main__":
    unittest.main()
