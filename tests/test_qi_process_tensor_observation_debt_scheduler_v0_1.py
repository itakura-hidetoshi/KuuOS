import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_observation_debt_scheduler_v0_1 import (
    compile_qi_process_tensor_observation_debt_schedule,
)


BASE_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "missing_process_requirements": [],
}


class QiProcessTensorObservationDebtSchedulerTests(unittest.TestCase):
    def test_formation_debt_requests_observation(self):
        schedule = compile_qi_process_tensor_observation_debt_schedule(
            process_tensor_summary={
                "process_tensor_visible": False,
                "transition_continuity_visible": False,
                "memory_continuity_visible": False,
                "nonmarkov_memory_visible": False,
                "process_history_length": 0,
                "missing_process_requirements": ["process_history_min_length_or_explicit_process_tensor"],
            }
        )
        self.assertEqual(schedule.observation_debt_status, "OBSERVATION_DEBT_OPEN")
        self.assertEqual(schedule.recommended_observation_action, "observe")
        self.assertIn("process_history_min_length", schedule.observation_targets)
        self.assertIn("transition_continuity", schedule.reobserve_targets)
        self.assertFalse(schedule.grants_execution_authority)

    def test_transition_gap_requests_reobservation(self):
        summary = dict(BASE_SUMMARY)
        summary["transition_continuity_visible"] = False
        schedule = compile_qi_process_tensor_observation_debt_schedule(process_tensor_summary=summary)
        self.assertEqual(schedule.observation_debt_status, "REOBSERVATION_DEBT_OPEN")
        self.assertEqual(schedule.recommended_observation_action, "reobserve")
        self.assertIn("transition_continuity", schedule.reobserve_targets)

    def test_unsafe_recovery_holds(self):
        schedule = compile_qi_process_tensor_observation_debt_schedule(
            process_tensor_summary=BASE_SUMMARY,
            health_projection={
                "next_operator_action": "hold",
                "recoverability_status": "UNSAFE_RECOVERY",
                "recovery_unsafe": True,
                "recovery_blockers": ["boundary_blocker"],
            },
        )
        self.assertEqual(schedule.observation_debt_status, "OBSERVATION_DEBT_HELD")
        self.assertEqual(schedule.recommended_observation_action, "hold")
        self.assertIn("recovery_unsafe", schedule.hold_reasons)

    def test_compaction_debt_requests_trace_compaction(self):
        schedule = compile_qi_process_tensor_observation_debt_schedule(
            process_tensor_summary=BASE_SUMMARY,
            health_projection={"next_operator_action": "compact_trace"},
            recoverability_projection={"recovery_blockers": ["compaction_debt"]},
        )
        self.assertEqual(schedule.observation_debt_status, "TRACE_COMPACTION_DEBT")
        self.assertEqual(schedule.recommended_observation_action, "compact_trace")
        self.assertIn("step_trace", schedule.compaction_targets)

    def test_no_debt_returns_no_action(self):
        schedule = compile_qi_process_tensor_observation_debt_schedule(process_tensor_summary=BASE_SUMMARY)
        self.assertEqual(schedule.observation_debt_status, "NO_OBSERVATION_DEBT")
        self.assertEqual(schedule.recommended_observation_action, "no_action")


if __name__ == "__main__":
    unittest.main()
