import unittest

from runtime.kuuos_runtime_daemon_qi_runtime_output_action_router_v0_1 import route_qi_runtime_output_surface


BASE_SURFACE = {
    "daemon_status": "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY",
    "daemon_stop_reason": "MAX_TICKS_REACHED",
    "recoverability_status": "RECOVERY_UNRESOLVED",
    "recommended_recovery_action": "no_action",
    "recovery_unsafe": False,
    "daemon_health_status": "REOBSERVE_REQUIRED",
    "next_operator_action": "no_action",
    "observation_debt_status": "NO_OBSERVATION_DEBT",
    "recommended_observation_action": "no_action",
    "compaction_plan_status": "NO_COMPACTION_DEBT",
    "recommended_compaction_action": "no_action",
}


def surface(**updates):
    value = dict(BASE_SURFACE)
    value.update(updates)
    return value


class QiRuntimeOutputActionRouterTests(unittest.TestCase):
    def test_hold_has_priority_over_other_actions(self):
        route = route_qi_runtime_output_surface(surface=surface(
            recovery_unsafe=True,
            next_operator_action="invoke_manual_runner",
            recommended_observation_action="observe",
            recommended_compaction_action="compact_trace",
        ))
        self.assertEqual(route.route_decision, "ROUTE_HOLD")
        self.assertEqual(route.next_outer_action, "hold")
        self.assertEqual(route.route_priority, "critical")
        self.assertFalse(route.grants_execution_authority)

    def test_observation_routes_before_compaction_and_reentry(self):
        route = route_qi_runtime_output_surface(surface=surface(
            observation_debt_status="OBSERVATION_DEBT_OPEN",
            recommended_observation_action="observe",
            compaction_plan_status="COMPACTION_READY",
            recommended_compaction_action="compact_trace",
            recoverability_status="RECOVERABLE_BY_MANUAL_RUNNER",
            recommended_recovery_action="invoke_manual_runner",
        ))
        self.assertEqual(route.route_decision, "ROUTE_OBSERVATION")
        self.assertEqual(route.next_outer_action, "observe")
        self.assertEqual(route.route_priority, "high")

    def test_compaction_routes_before_reentry_when_no_observation_debt(self):
        route = route_qi_runtime_output_surface(surface=surface(
            compaction_plan_status="COMPACTION_READY",
            recommended_compaction_action="compact_trace",
            recoverability_status="RECOVERABLE_BY_MANUAL_RUNNER",
            recommended_recovery_action="invoke_manual_runner",
        ))
        self.assertEqual(route.route_decision, "ROUTE_COMPACTION")
        self.assertEqual(route.next_outer_action, "compact_trace")
        self.assertEqual(route.route_priority, "high")

    def test_manual_runner_routes_to_managed_reentry_chain(self):
        route = route_qi_runtime_output_surface(surface=surface(
            recoverability_status="RECOVERABLE_BY_MANUAL_RUNNER",
            recommended_recovery_action="invoke_manual_runner",
            next_operator_action="invoke_manual_runner",
        ))
        self.assertEqual(route.route_decision, "ROUTE_REENTRY")
        self.assertEqual(route.next_outer_action, "managed_reentry_chain")
        self.assertEqual(route.route_priority, "high")

    def test_no_action_when_surface_has_no_actionable_debt(self):
        route = route_qi_runtime_output_surface(surface=BASE_SURFACE)
        self.assertEqual(route.route_decision, "ROUTE_NO_ACTION")
        self.assertEqual(route.next_outer_action, "no_action")
        self.assertEqual(route.route_priority, "low")


if __name__ == "__main__":
    unittest.main()
