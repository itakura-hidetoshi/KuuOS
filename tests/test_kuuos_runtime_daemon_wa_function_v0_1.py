import unittest

from runtime.kuuos_runtime_daemon_wa_function_v0_1 import evaluate_daemon_wa_function


def gate(action="CONTINUE_ADVISORY_ONLY", policy="CONTINUE_BOUNDED", regime="BALANCED_BOUNDED_FLOW", pressure=0.0, ticks=1):
    return {
        "recommended_emptiness_action": action,
        "policy_mode": policy,
        "qique_regime": regime,
        "qique_recovery_budget_pressure": pressure,
        "tick_density": ticks,
    }


class DaemonWaFunctionTests(unittest.TestCase):
    def test_balanced_continue_becomes_harmonized_continue(self):
        result = evaluate_daemon_wa_function(gate())
        self.assertEqual(result.recommended_runtime_posture, "CONTINUE_HARMONIZED")
        self.assertEqual(result.wa_status, "WA_HARMONIZED_CONTINUE")
        self.assertGreater(result.wa_score, 0.5)
        self.assertLess(result.nihilism_risk_score, 0.2)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_reobserve_keeps_qi_without_reification(self):
        result = evaluate_daemon_wa_function(gate(
            action="REOBSERVE_WITH_NON_REIFICATION",
            policy="REOBSERVE_QI_PROCESS",
            regime="PROCESS_OBSERVATION_GAP",
            ticks=2,
        ))
        self.assertEqual(result.recommended_runtime_posture, "SLOW_DOWN_AND_REOBSERVE")
        self.assertEqual(result.wa_status, "WA_REOBSERVE")
        self.assertGreater(result.qi_scope_score, 0.0)
        self.assertGreater(result.emptiness_score, 0.0)

    def test_hold_pressure_becomes_recovery_not_nihilism(self):
        result = evaluate_daemon_wa_function(gate(
            action="HOLD_AND_COMPACT_TRACE",
            policy="CONTINUE_BOUNDED",
            regime="RECOVERY_PRESSURE_HIGH",
            pressure=0.85,
            ticks=3,
        ))
        self.assertEqual(result.recommended_runtime_posture, "HOLD_WITH_RECOVERY")
        self.assertEqual(result.wa_status, "WA_HOLD_RECOVERY")
        self.assertGreater(result.nihilism_risk_score, 0.0)
        self.assertGreater(result.wa_score, 0.0)

    def test_quarantine_keeps_return_path(self):
        result = evaluate_daemon_wa_function(gate(
            action="HOLD_OR_QUARANTINE_NONFINAL",
            policy="QUARANTINE_REVIEW",
            regime="BOUNDARY_QUARANTINE",
            pressure=0.5,
            ticks=1,
        ))
        self.assertEqual(result.recommended_runtime_posture, "QUARANTINE_WITH_RETURN_PATH")
        self.assertEqual(result.wa_reason, "emptiness_blocks_reification_with_return_path")
        self.assertFalse(result.grants_final_commitment_authority)

    def test_high_density_compacts_before_continue(self):
        result = evaluate_daemon_wa_function(gate(
            action="COMPACT_TRACE_BEFORE_CONTINUE",
            policy="CONTINUE_WITH_QI_MEMORY_MONITOR",
            regime="NONMARKOV_MEMORY_ACTIVE",
            ticks=12,
        ))
        self.assertEqual(result.recommended_runtime_posture, "CONTINUE_AFTER_COMPACT")
        self.assertEqual(result.wa_status, "WA_COMPACT_CONTINUE")
        self.assertGreater(result.over_density_penalty, 0.0)

    def test_active_memory_uses_compact_monitor(self):
        result = evaluate_daemon_wa_function(gate(
            action="CONTINUE_WITH_COMPACT_MONITOR",
            policy="CONTINUE_WITH_QI_MEMORY_MONITOR",
            regime="NONMARKOV_MEMORY_ACTIVE",
            ticks=3,
        ))
        self.assertEqual(result.recommended_runtime_posture, "CONTINUE_WITH_COMPACT_MONITOR")
        self.assertEqual(result.wa_reason, "memory_activity_needs_compact_middle_way")

    def test_localized_memory_light_branching(self):
        result = evaluate_daemon_wa_function(gate(
            action="CONTINUE_ADVISORY_ONLY",
            policy="CONTINUE_WITH_MEMORY_MONITOR",
            regime="LOCALIZED_MEMORY_CHANNEL",
            ticks=2,
        ))
        self.assertEqual(result.recommended_runtime_posture, "BRANCH_EXPLORE_LIGHTLY")
        self.assertEqual(result.wa_status, "WA_LIGHT_BRANCH")


if __name__ == "__main__":
    unittest.main()
