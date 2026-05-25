import unittest

from runtime.kuuos_runtime_daemon_qi_projection_plan_readable_summary_v0_1 import (
    compile_qi_projection_plan_readable_summary,
)


RESULT = {
    "recommended_next_runtime_mode": "REOBSERVE",
    "recommended_next_reason": "observation_debt_or_reobserve_hint_visible",
    "next_tick_preparation": "prepare_observation",
    "required_pre_tick_actions": ["prepare_observation_packet", "collect_missing_observation"],
    "projection_statuses": {
        "recoverability": "QI_PROCESS_TENSOR_RECOVERABILITY_PROJECTED",
        "health": "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
        "observation_debt": "QI_PROCESS_TENSOR_OBSERVATION_DEBT_SCHEDULED",
        "trace_compaction": "QI_PROCESS_TENSOR_TRACE_COMPACTION_PLANNED",
    },
}


class QiProjectionPlanReadableSummaryTests(unittest.TestCase):
    def test_readable_summary_renders_core_runtime_fields(self):
        summary = compile_qi_projection_plan_readable_summary(projection_plan_result=RESULT)
        text = summary.to_text()
        self.assertEqual(summary.summary_status, "QI_PROJECTION_PLAN_READABLE_SUMMARY_COMPILED")
        self.assertIn("recommended_next_runtime_mode: REOBSERVE", text)
        self.assertIn("next_tick_preparation: prepare_observation", text)
        self.assertIn("- collect_missing_observation", text)
        self.assertIn("- health: QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY", text)
        self.assertIn("authority: none", text)
        self.assertTrue(summary.readable_summary_only)
        self.assertTrue(summary.read_only)
        self.assertFalse(summary.grants_execution_authority)
        self.assertFalse(summary.grants_next_tick_execution_authority)

    def test_missing_fields_render_unknown_without_authority(self):
        summary = compile_qi_projection_plan_readable_summary(projection_plan_result={})
        text = summary.to_text()
        self.assertIn("recommended_next_runtime_mode: UNKNOWN", text)
        self.assertIn("required_pre_tick_actions: []", text)
        self.assertIn("projection_statuses: {}", text)
        self.assertFalse(summary.grants_truth_authority)
        self.assertFalse(summary.grants_memory_overwrite_authority)


if __name__ == "__main__":
    unittest.main()
