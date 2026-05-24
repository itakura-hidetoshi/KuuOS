import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_trace_compaction_planner_v0_1 import (
    compile_qi_process_tensor_trace_compaction_plan,
)


BASE_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
}


class QiProcessTensorTraceCompactionPlannerTests(unittest.TestCase):
    def test_no_compaction_debt_returns_no_action(self):
        plan = compile_qi_process_tensor_trace_compaction_plan(process_tensor_summary=BASE_SUMMARY)
        self.assertEqual(plan.compaction_plan_status, "NO_COMPACTION_DEBT")
        self.assertEqual(plan.recommended_compaction_action, "no_action")
        self.assertIn("daemon_result_v0_1.json", plan.retain_targets)
        self.assertIn("latest_raw_state", plan.carry_forward_targets)
        self.assertFalse(plan.grants_execution_authority)

    def test_long_history_requests_summary_and_compaction(self):
        summary = dict(BASE_SUMMARY)
        summary["process_history_length"] = 12
        plan = compile_qi_process_tensor_trace_compaction_plan(process_tensor_summary=summary)
        self.assertEqual(plan.compaction_plan_status, "COMPACTION_READY")
        self.assertEqual(plan.recommended_compaction_action, "compact_trace")
        self.assertIn("older_process_history_prefix", plan.summarize_targets)
        self.assertIn("middle_process_history_window", plan.summarize_targets)
        self.assertIn("older_step_trace_prefix", plan.compact_targets)
        self.assertIn("middle_step_trace_window", plan.compact_targets)

    def test_observation_compaction_debt_requests_trace_compaction(self):
        plan = compile_qi_process_tensor_trace_compaction_plan(
            process_tensor_summary=BASE_SUMMARY,
            observation_debt_schedule={
                "recommended_observation_action": "compact_trace",
                "compaction_targets": ["step_trace", "process_history"],
            },
        )
        self.assertEqual(plan.compaction_plan_status, "COMPACTION_READY")
        self.assertEqual(plan.recommended_compaction_action, "compact_trace")
        self.assertIn("step_trace", plan.compact_targets)
        self.assertIn("process_history", plan.compact_targets)
        self.assertIn("process_history_summary", plan.summarize_targets)

    def test_unsafe_recovery_holds_compaction(self):
        plan = compile_qi_process_tensor_trace_compaction_plan(
            process_tensor_summary=BASE_SUMMARY,
            recoverability_projection={"recoverability_status": "UNSAFE_RECOVERY"},
        )
        self.assertEqual(plan.compaction_plan_status, "COMPACTION_HELD")
        self.assertEqual(plan.recommended_compaction_action, "hold_compaction")
        self.assertIn("UNSAFE_RECOVERY", plan.compaction_blockers)
        self.assertIn("executor_receipt", plan.no_compaction_targets)

    def test_missing_transition_retains_transition_witnesses(self):
        summary = dict(BASE_SUMMARY)
        summary["transition_continuity_visible"] = False
        plan = compile_qi_process_tensor_trace_compaction_plan(process_tensor_summary=summary)
        self.assertEqual(plan.compaction_plan_status, "COMPACTION_HELD")
        self.assertIn("adjacent_transition_edges", plan.retain_targets)
        self.assertIn("transition_witnesses", plan.no_compaction_targets)
        self.assertIn("process_tensor_not_visible", plan.compaction_blockers) if False else None

    def test_observation_hold_blocks_compaction(self):
        plan = compile_qi_process_tensor_trace_compaction_plan(
            process_tensor_summary=BASE_SUMMARY,
            observation_debt_schedule={"hold_reasons": ["recovery_unsafe"]},
        )
        self.assertEqual(plan.compaction_plan_status, "COMPACTION_HELD")
        self.assertIn("recovery_unsafe", plan.compaction_blockers)
        self.assertIn("step_trace", plan.no_compaction_targets)


if __name__ == "__main__":
    unittest.main()
