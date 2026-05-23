import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1 import (
    compile_qi_process_tensor_recoverability_projection,
)


BASE_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "missing_process_requirements": [],
}


class QiProcessTensorRecoverabilityProjectionTests(unittest.TestCase):
    def test_missing_process_tensor_is_recoverable_by_observation(self):
        projection = compile_qi_process_tensor_recoverability_projection(
            process_tensor_summary={
                "process_tensor_visible": False,
                "transition_continuity_visible": False,
                "memory_continuity_visible": False,
                "nonmarkov_memory_visible": False,
                "process_history_length": 0,
                "missing_process_requirements": ["process_history_min_length_or_explicit_process_tensor"],
            }
        )
        self.assertEqual(projection.recoverability_status, "RECOVERABLE_BY_OBSERVATION")
        self.assertEqual(projection.dominant_recovery_path, "observation")
        self.assertEqual(projection.recommended_recovery_action, "observe")
        self.assertTrue(projection.local_recovery_allowed)
        self.assertIn("observation_debt", projection.recovery_blockers)
        self.assertFalse(projection.grants_execution_authority)

    def test_transition_gap_is_recoverable_by_reobservation(self):
        summary = dict(BASE_SUMMARY)
        summary["transition_continuity_visible"] = False
        projection = compile_qi_process_tensor_recoverability_projection(process_tensor_summary=summary)
        self.assertEqual(projection.recoverability_status, "RECOVERABLE_BY_REOBSERVATION")
        self.assertEqual(projection.recommended_recovery_action, "reobserve")
        self.assertIn("transition_gap", projection.recovery_blockers)

    def test_compaction_debt_is_recoverable_by_compaction(self):
        projection = compile_qi_process_tensor_recoverability_projection(
            process_tensor_summary=BASE_SUMMARY,
            reentry_plan={
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST",
                "compact_before_reentry": True,
            },
        )
        self.assertEqual(projection.recoverability_status, "RECOVERABLE_BY_COMPACTION")
        self.assertEqual(projection.dominant_recovery_path, "trace_compaction")
        self.assertEqual(projection.recommended_recovery_action, "compact_trace")
        self.assertIn("compaction_debt", projection.recovery_blockers)

    def test_single_tick_token_is_recoverable_by_manual_runner(self):
        projection = compile_qi_process_tensor_recoverability_projection(
            process_tensor_summary=BASE_SUMMARY,
            license_gate={"license_decision": "BOUNDED_TICK_LICENSE_GRANTED"},
            invocation_boundary={
                "invocation_decision": "SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
                "single_tick_invocation_token": True,
            },
        )
        self.assertEqual(projection.recoverability_status, "RECOVERABLE_BY_MANUAL_RUNNER")
        self.assertEqual(projection.dominant_recovery_path, "manual_runner")
        self.assertEqual(projection.recommended_recovery_action, "invoke_manual_runner")
        self.assertEqual(projection.recommended_next_receipt, "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json")
        self.assertTrue(projection.local_recovery_allowed)
        self.assertFalse(projection.grants_execution_authority)

    def test_completed_manual_runner_marks_recovered(self):
        projection = compile_qi_process_tensor_recoverability_projection(
            process_tensor_summary=BASE_SUMMARY,
            executor_receipt={
                "executor_status": "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED",
                "tick_invoked": True,
            },
        )
        self.assertEqual(projection.recoverability_status, "RECOVERED_BY_MANUAL_RUNNER")
        self.assertEqual(projection.recommended_recovery_action, "no_action")
        self.assertFalse(projection.local_recovery_allowed)

    def test_license_denied_blocks_local_recovery(self):
        projection = compile_qi_process_tensor_recoverability_projection(
            process_tensor_summary=BASE_SUMMARY,
            license_gate={"license_decision": "NO_BOUNDED_TICK_LICENSE"},
        )
        self.assertEqual(projection.recoverability_status, "LOCAL_RECOVERY_BLOCKED")
        self.assertEqual(projection.recommended_recovery_action, "hold")
        self.assertFalse(projection.local_recovery_allowed)

    def test_inconsistent_token_and_denied_license_is_unsafe(self):
        projection = compile_qi_process_tensor_recoverability_projection(
            process_tensor_summary=BASE_SUMMARY,
            license_gate={"license_decision": "NO_BOUNDED_TICK_LICENSE"},
            invocation_boundary={"single_tick_invocation_token": True},
        )
        self.assertEqual(projection.recoverability_status, "UNSAFE_RECOVERY")
        self.assertTrue(projection.recovery_unsafe)
        self.assertFalse(projection.local_recovery_allowed)
        self.assertEqual(projection.recommended_recovery_action, "hold")


if __name__ == "__main__":
    unittest.main()
