import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_health_projection_v0_1 import (
    compile_qi_process_tensor_health_projection,
)


BASE_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "missing_process_requirements": [],
}


class QiProcessTensorHealthProjectionTests(unittest.TestCase):
    def test_incomplete_process_tensor_requests_observation(self):
        projection = compile_qi_process_tensor_health_projection(
            process_tensor_summary={
                "process_tensor_visible": False,
                "transition_continuity_visible": False,
                "memory_continuity_visible": False,
                "nonmarkov_memory_visible": False,
                "process_history_length": 0,
                "missing_process_requirements": ["process_history_min_length_or_explicit_process_tensor"],
            }
        )
        self.assertEqual(projection.qi_process_tensor_phase, "QI_PROCESS_TENSOR_FORMATION_INCOMPLETE")
        self.assertEqual(projection.daemon_health_status, "WAITING_FOR_PROCESS_TENSOR_SUPPORT")
        self.assertEqual(projection.next_operator_action, "observe")
        self.assertFalse(projection.grants_execution_authority)

    def test_reentry_compact_first_requests_compaction(self):
        projection = compile_qi_process_tensor_health_projection(
            process_tensor_summary=BASE_SUMMARY,
            reentry_plan={
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST",
                "next_invocation_mode": "COMPACT_THEN_BOUNDED_REENTRY",
            },
        )
        self.assertEqual(projection.qi_process_tensor_phase, "QI_REENTRY_COMPACT_FIRST")
        self.assertEqual(projection.daemon_health_status, "NEEDS_COMPACTION")
        self.assertEqual(projection.next_operator_action, "compact_trace")

    def test_reentry_reobserve_first_requests_reobserve(self):
        projection = compile_qi_process_tensor_health_projection(
            process_tensor_summary=BASE_SUMMARY,
            reentry_plan={
                "plan_status": "QI_PROCESS_TENSOR_REENTRY_REOBSERVE_FIRST",
                "next_invocation_mode": "REOBSERVE_THEN_BOUNDED_REENTRY",
            },
        )
        self.assertEqual(projection.qi_process_tensor_phase, "QI_REENTRY_REOBSERVE_FIRST")
        self.assertEqual(projection.daemon_health_status, "REOBSERVE_REQUIRED")
        self.assertEqual(projection.next_operator_action, "reobserve")

    def test_single_tick_token_ready_requests_manual_runner(self):
        projection = compile_qi_process_tensor_health_projection(
            process_tensor_summary=BASE_SUMMARY,
            reentry_plan={"plan_status": "QI_PROCESS_TENSOR_REENTRY_READY"},
            license_gate={"license_decision": "BOUNDED_TICK_LICENSE_GRANTED"},
            invocation_boundary={
                "invocation_decision": "SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
                "single_tick_invocation_token": True,
            },
        )
        self.assertEqual(projection.qi_process_tensor_phase, "QI_SINGLE_TICK_TOKEN_READY")
        self.assertEqual(projection.daemon_health_status, "HEALTHY_REENTRY_READY")
        self.assertEqual(projection.next_operator_action, "invoke_manual_runner")
        self.assertEqual(projection.recommended_next_receipt, "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json")
        self.assertFalse(projection.grants_execution_authority)

    def test_executor_invoked_requests_no_action(self):
        projection = compile_qi_process_tensor_health_projection(
            process_tensor_summary=BASE_SUMMARY,
            executor_receipt={
                "executor_status": "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED",
                "tick_invoked": True,
            },
        )
        self.assertEqual(projection.qi_process_tensor_phase, "QI_BOUNDED_TICK_COMPLETED")
        self.assertEqual(projection.daemon_health_status, "EXECUTOR_INVOKED")
        self.assertEqual(projection.next_operator_action, "no_action")

    def test_license_denied_requests_hold(self):
        projection = compile_qi_process_tensor_health_projection(
            process_tensor_summary=BASE_SUMMARY,
            license_gate={
                "license_decision": "NO_BOUNDED_TICK_LICENSE",
                "denied_reason": "reentry_plan_is_held",
            },
        )
        self.assertEqual(projection.qi_process_tensor_phase, "QI_REENTRY_LICENSE_DENIED")
        self.assertEqual(projection.daemon_health_status, "EXECUTOR_DENIED")
        self.assertEqual(projection.next_operator_action, "hold")
        self.assertEqual(projection.health_reason, "reentry_plan_is_held")


if __name__ == "__main__":
    unittest.main()
