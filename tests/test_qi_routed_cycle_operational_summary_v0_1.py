import unittest

from runtime.kuuos_runtime_daemon_qi_routed_cycle_operational_summary_v0_1 import (
    compile_qi_routed_cycle_operational_summary,
)


DAEMON = {
    "daemon_status": "KUUOS_RUNTIME_DAEMON_COMPLETED",
    "stop_reason": "max_ticks_reached",
    "ticks_run": 1,
    "scheduled_compact_before_next_tick": False,
    "scheduled_reobserve_before_next_tick": False,
    "scheduled_hold_until_observation": False,
}

ROUTE = {
    "route_decision": "QI_RUNTIME_OUTPUT_ROUTE_READY",
    "next_outer_action": "NO_ACTION",
}

DISPATCH = {
    "dispatcher_status": "QI_RUNTIME_OUTPUT_ACTION_NOT_INVOKED",
    "reentry_cycles_run": 0,
}

SHADOW = {
    "shadow_decision": "QI_POLICY_FLOW_CANDIDATE_SHADOW_EVALUATED",
    "candidate_shadow_score": 0.85,
    "candidate_shadow_grade": "strong_shadow_candidate",
}

ADMISSION = {
    "shadow_admission_decision": "QI_POLICY_FLOW_SHADOW_CANDIDATE_ADMITTED",
    "admitted_shadow_candidate_action": "prefer_observation_candidate",
}


class QiRoutedCycleOperationalSummaryTests(unittest.TestCase):
    def test_shadow_ready_mode_when_candidate_admitted(self):
        result = compile_qi_routed_cycle_operational_summary(
            daemon_result=DAEMON,
            route_result=ROUTE,
            dispatch_result=DISPATCH,
            recovery_feedback={"feedback_signal": "QI_FEEDBACK_NO_ACTION"},
            shadow_evaluation=SHADOW,
            shadow_admission=ADMISSION,
        )
        self.assertEqual(result.recommended_next_runtime_mode, "SHADOW_READY_FOR_POLICY_FLOW_REVIEW")
        self.assertEqual(result.policy_shadow_score, 0.85)
        self.assertIn("shadow_candidate_admitted", result.operational_positive_signals)
        self.assertTrue(result.operational_summary_only)
        self.assertTrue(result.read_only)
        self.assertFalse(result.grants_execution_authority)

    def test_hold_mode_takes_priority_over_shadow_ready(self):
        daemon = dict(DAEMON)
        daemon["scheduled_hold_until_observation"] = True
        result = compile_qi_routed_cycle_operational_summary(
            daemon_result=daemon,
            route_result=ROUTE,
            dispatch_result=DISPATCH,
            recovery_feedback={"feedback_signal": "QI_FEEDBACK_HOLD_REQUIRED"},
            shadow_evaluation=SHADOW,
            shadow_admission=ADMISSION,
        )
        self.assertEqual(result.recommended_next_runtime_mode, "HOLD_REOBSERVE")
        self.assertIn("hold_until_observation", result.operational_blockers)
        self.assertTrue(result.hold_until_observation)

    def test_reobserve_mode_takes_priority_over_compaction(self):
        daemon = dict(DAEMON)
        daemon["scheduled_reobserve_before_next_tick"] = True
        daemon["scheduled_compact_before_next_tick"] = True
        result = compile_qi_routed_cycle_operational_summary(
            daemon_result=daemon,
            route_result=ROUTE,
            dispatch_result=DISPATCH,
            recovery_feedback={"feedback_signal": "QI_FEEDBACK_OBSERVATION_REQUIRED"},
        )
        self.assertEqual(result.recommended_next_runtime_mode, "REOBSERVE")
        self.assertTrue(result.reobserve_before_next_tick)
        self.assertTrue(result.compact_before_next_tick)
        self.assertIn("observation_debt_visible", result.operational_warnings)

    def test_compaction_mode_when_only_compaction_hint_visible(self):
        daemon = dict(DAEMON)
        daemon["scheduled_compact_before_next_tick"] = True
        result = compile_qi_routed_cycle_operational_summary(
            daemon_result=daemon,
            route_result=ROUTE,
            dispatch_result=DISPATCH,
            recovery_feedback={"feedback_signal": "QI_FEEDBACK_COMPACTION_REQUIRED"},
        )
        self.assertEqual(result.recommended_next_runtime_mode, "COMPACT_TRACE")
        self.assertTrue(result.compact_before_next_tick)
        self.assertIn("trace_compaction_visible", result.operational_warnings)

    def test_missing_daemon_blocks_summary_but_stays_read_only(self):
        result = compile_qi_routed_cycle_operational_summary(
            daemon_result={},
            route_result=ROUTE,
            dispatch_result=DISPATCH,
        )
        self.assertIn("daemon_result_missing", result.operational_blockers)
        self.assertTrue(result.read_only)
        self.assertTrue(result.candidate_only)
        self.assertFalse(result.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
