import unittest

from runtime.kuuos_runtime_daemon_qi_next_runtime_mode_plan_v0_1 import (
    compile_qi_next_runtime_mode_plan,
)


def summary(mode, reason="test_reason"):
    return {
        "recommended_next_runtime_mode": mode,
        "recommended_next_reason": reason,
        "operational_blockers": ["b1"],
        "operational_warnings": ["w1"],
        "operational_positive_signals": ["p1"],
    }


class QiNextRuntimeModePlanTests(unittest.TestCase):
    def test_hold_reobserve_mode_maps_to_hold_plan(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("HOLD_REOBSERVE"))
        self.assertEqual(result.next_tick_preparation, "hold_reobserve")
        self.assertIn("hold_next_tick", result.required_pre_tick_actions)
        self.assertTrue(result.plan_only)
        self.assertFalse(result.grants_next_tick_execution_authority)

    def test_reobserve_mode_maps_to_observation_plan(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("REOBSERVE"))
        self.assertEqual(result.next_tick_preparation, "prepare_observation")
        self.assertIn("collect_missing_observation", result.required_pre_tick_actions)

    def test_compact_trace_mode_maps_to_compaction_plan(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("COMPACT_TRACE"))
        self.assertEqual(result.next_tick_preparation, "prepare_compaction")
        self.assertIn("prepare_trace_compaction", result.required_pre_tick_actions)

    def test_shadow_ready_mode_maps_to_shadow_review_plan(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("SHADOW_READY_FOR_POLICY_FLOW_REVIEW"))
        self.assertEqual(result.next_tick_preparation, "prepare_shadow_review")
        self.assertIn("prepare_policy_flow_review_packet", result.required_pre_tick_actions)
        self.assertIn("do_not_mutate_policy", result.required_pre_tick_actions)

    def test_bounded_reentry_mode_maps_to_reentry_review_plan(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("BOUNDED_REENTRY_REVIEW"))
        self.assertEqual(result.next_tick_preparation, "prepare_bounded_reentry_review")
        self.assertIn("check_reentry_cap", result.required_pre_tick_actions)

    def test_observe_mode_maps_to_observe_only(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("NO_CANDIDATE_OBSERVE"))
        self.assertEqual(result.next_tick_preparation, "observe_only")
        self.assertTrue(result.read_only)
        self.assertTrue(result.nonexecuting)

    def test_missing_summary_blocks_and_preserves_boundaries(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary={})
        self.assertEqual(result.plan_decision, "QI_NEXT_RUNTIME_MODE_PLAN_BLOCKED")
        self.assertEqual(result.next_tick_preparation, "hold_reobserve")
        self.assertIn("recover_operational_summary", result.required_pre_tick_actions)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_forbidden_actions_always_present(self):
        result = compile_qi_next_runtime_mode_plan(operational_summary=summary("REOBSERVE"))
        self.assertIn("grant_authority", result.forbidden_actions)
        self.assertIn("treat_shadow_result_as_execution_permission", result.forbidden_actions)


if __name__ == "__main__":
    unittest.main()
