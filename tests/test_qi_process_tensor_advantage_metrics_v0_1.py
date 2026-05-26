import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_advantage_metrics_v0_1 import compute_qi_process_tensor_advantage_metrics


RICH_RAW = {
    "physical_process_visible": True,
    "thermodynamic_activity_visible": True,
    "process_history": [
        {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
        {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
        {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
        {"step_id": "p3", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    ],
}

WEAK_RAW = {
    "physical_process_visible": True,
    "thermodynamic_activity_visible": False,
    "process_history": [
        {"step_id": "p0", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
        {"step_id": "p1", "transition_visible": False, "memory_link_visible": False, "nonmarkov_link_visible": False},
    ],
}

SUMMARY_GOOD = {
    "projection_statuses": {
        "recoverability": "ready",
        "health": "ok",
        "observation_debt": "low",
        "trace_compaction": "ready",
    }
}

SUMMARY_DEBT = {
    "projection_statuses": {
        "recoverability": "hold",
        "health": "watch",
        "observation_debt": "high_debt",
        "trace_compaction": "partial",
    }
}


class QiProcessTensorAdvantageMetricsTests(unittest.TestCase):
    def test_rich_history_has_high_process_tensor_advantage(self):
        metrics = compute_qi_process_tensor_advantage_metrics(raw_state=RICH_RAW, projection_summary=SUMMARY_GOOD)
        self.assertEqual(metrics.metrics_status, "QI_PROCESS_TENSOR_ADVANTAGE_READY")
        self.assertEqual(metrics.history_depth, 4)
        self.assertGreaterEqual(metrics.transition_visibility_ratio, 0.9)
        self.assertGreaterEqual(metrics.memory_link_density, 0.9)
        self.assertGreaterEqual(metrics.nonmarkov_link_density, 0.7)
        self.assertGreaterEqual(metrics.multi_time_correlation_visibility, 0.8)
        self.assertGreaterEqual(metrics.recoverability_branching_capacity, 0.8)
        self.assertGreaterEqual(metrics.memory_kernel_preservation_score, 0.8)
        self.assertGreaterEqual(metrics.safe_reentry_window_score, 0.8)
        self.assertIn(metrics.process_tensor_advantage_level, {"high", "medium"})
        self.assertEqual(metrics.recommended_next_process_focus, "continue_process_tensor_supervision")
        self.assertTrue(metrics.metrics_only)
        self.assertTrue(metrics.read_only)
        self.assertFalse(metrics.grants_execution_authority)
        self.assertFalse(metrics.grants_next_tick_execution_authority)

    def test_weak_history_prioritizes_observation_debt_or_recovery(self):
        metrics = compute_qi_process_tensor_advantage_metrics(raw_state=WEAK_RAW, projection_summary=SUMMARY_DEBT)
        self.assertEqual(metrics.metrics_status, "QI_PROCESS_TENSOR_ADVANTAGE_READY")
        self.assertEqual(metrics.history_depth, 2)
        self.assertLess(metrics.memory_link_density, 0.5)
        self.assertLess(metrics.nonmarkov_link_density, 0.5)
        self.assertGreater(metrics.observation_debt_resolution_priority, 0.5)
        self.assertIn(metrics.recommended_next_process_focus, {
            "resolve_observation_debt",
            "open_recoverability_branch",
            "preserve_memory_kernel",
            "widen_safe_reentry_window",
        })
        self.assertIn("thermodynamic_activity_visibility_missing", metrics.warnings)

    def test_missing_process_history_blocks_advantage_claim(self):
        metrics = compute_qi_process_tensor_advantage_metrics(raw_state={}, projection_summary={})
        self.assertEqual(metrics.metrics_status, "QI_PROCESS_TENSOR_ADVANTAGE_BLOCKED")
        self.assertEqual(metrics.process_tensor_advantage_level, "blocked")
        self.assertIn("process_history_missing", metrics.blockers)
        self.assertEqual(metrics.recommended_next_process_focus, "repair_process_tensor_inputs")
        self.assertFalse(metrics.grants_truth_authority)
        self.assertFalse(metrics.grants_memory_overwrite_authority)


if __name__ == "__main__":
    unittest.main()
