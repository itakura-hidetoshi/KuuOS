import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_planner_v0_1 import plan_qi_process_tensor_probe


BASE_METRICS = {
    "metrics_status": "QI_PROCESS_TENSOR_ADVANTAGE_READY",
    "history_depth": 4,
    "transition_visibility_ratio": 0.9,
    "memory_link_density": 0.9,
    "nonmarkov_link_density": 0.8,
    "multi_time_correlation_visibility": 0.85,
    "recoverability_branching_capacity": 0.82,
    "observation_debt_resolution_priority": 0.1,
    "memory_kernel_preservation_score": 0.86,
    "safe_reentry_window_score": 0.84,
    "process_tensor_advantage_level": "high",
    "recommended_next_process_focus": "continue_process_tensor_supervision",
}

RAW_STATE = {
    "process_history": [
        {"step_id": "p0", "time_slice": "t0"},
        {"step_id": "p1", "time_slice": "t1"},
    ]
}


class QiProcessTensorProbePlannerTests(unittest.TestCase):
    def test_ready_metrics_produce_read_only_supervision_probe(self):
        plan = plan_qi_process_tensor_probe(
            latest_process_tensor_advantage_metrics=BASE_METRICS,
            raw_state=RAW_STATE,
            projection_summary={"projection_statuses": {"recoverability": "ready", "observation_debt": "low"}},
        )
        self.assertEqual(plan.probe_plan_status, "QI_PROCESS_TENSOR_PROBE_PLAN_READY")
        self.assertEqual(plan.recommended_probe_type, "continue_process_tensor_supervision_probe")
        self.assertEqual(plan.probe_target_time_slice, "t1")
        self.assertEqual(plan.probe_risk_level, "low")
        self.assertTrue(plan.probe_plan_only)
        self.assertTrue(plan.read_only)
        self.assertTrue(plan.metrics_only)
        self.assertEqual(plan.authority, "none")
        self.assertFalse(plan.grants_execution_authority)
        self.assertFalse(plan.grants_probe_execution_authority)
        self.assertFalse(plan.grants_next_tick_execution_authority)
        self.assertFalse(plan.grants_control_packet_authority)
        self.assertFalse(plan.grants_memory_overwrite_authority)

    def test_observation_debt_focus_selects_observation_debt_probe(self):
        metrics = dict(BASE_METRICS)
        metrics["recommended_next_process_focus"] = "resolve_observation_debt"
        metrics["observation_debt_resolution_priority"] = 0.8
        plan = plan_qi_process_tensor_probe(
            latest_process_tensor_advantage_metrics=metrics,
            raw_state=RAW_STATE,
            observation_debt={"priority": 0.9, "highest_priority_time_slice": "t_debt"},
        )
        self.assertEqual(plan.probe_plan_status, "QI_PROCESS_TENSOR_PROBE_PLAN_READY_WITH_WARNINGS")
        self.assertEqual(plan.recommended_probe_type, "observation_debt_probe")
        self.assertEqual(plan.probe_target_time_slice, "t_debt")
        self.assertGreater(plan.probe_expected_observation_debt_reduction, 0.5)
        self.assertIn("observation_debt_priority_high", plan.probe_warnings)

    def test_low_recoverability_selects_recoverability_branch_probe(self):
        metrics = dict(BASE_METRICS)
        metrics["recoverability_branching_capacity"] = 0.2
        metrics["recommended_next_process_focus"] = "open_recoverability_branch"
        plan = plan_qi_process_tensor_probe(
            latest_process_tensor_advantage_metrics=metrics,
            raw_state=RAW_STATE,
            recoverability_status={"status": "hold"},
        )
        self.assertEqual(plan.recommended_probe_type, "recoverability_branch_probe")
        self.assertGreater(plan.probe_expected_recoverability_gain, 0.4)
        self.assertIn(plan.probe_risk_level, {"medium", "low"})

    def test_low_memory_kernel_selects_memory_probe_without_authority(self):
        metrics = dict(BASE_METRICS)
        metrics["memory_kernel_preservation_score"] = 0.2
        metrics["recommended_next_process_focus"] = "preserve_memory_kernel"
        plan = plan_qi_process_tensor_probe(latest_process_tensor_advantage_metrics=metrics, raw_state=RAW_STATE)
        self.assertEqual(plan.recommended_probe_type, "memory_kernel_probe")
        self.assertIn("memory_kernel_preservation_low", plan.probe_warnings)
        self.assertFalse(plan.grants_memory_overwrite_authority)
        self.assertFalse(plan.grants_probe_execution_authority)

    def test_missing_metrics_blocks_probe_plan(self):
        plan = plan_qi_process_tensor_probe(latest_process_tensor_advantage_metrics={}, raw_state={})
        self.assertEqual(plan.probe_plan_status, "QI_PROCESS_TENSOR_PROBE_PLAN_BLOCKED")
        self.assertEqual(plan.recommended_probe_type, "repair_process_tensor_inputs")
        self.assertEqual(plan.probe_risk_level, "blocked")
        self.assertIn("process_tensor_advantage_metrics_missing", plan.probe_blockers)
        self.assertIn("process_history_missing", plan.probe_blockers)
        self.assertFalse(plan.grants_execution_authority)
        self.assertFalse(plan.grants_next_tick_execution_authority)


if __name__ == "__main__":
    unittest.main()
