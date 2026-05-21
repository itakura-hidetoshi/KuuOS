import unittest

from runtime.kuuos_runtime_daemon_emptiness_gate_v0_1 import evaluate_daemon_emptiness_gate

BASE_QIQUE = {
    "qique_regime": "BALANCED_BOUNDED_FLOW",
    "recovery_budget_pressure": 0.0,
}

BASE_POLICY = {
    "recommended_tick_mode": "CONTINUE_BOUNDED",
    "daemon_qique_gauge": BASE_QIQUE,
}


class DaemonEmptinessGateTests(unittest.TestCase):
    def test_passes_bounded_non_reifying_continue(self):
        result = evaluate_daemon_emptiness_gate(BASE_POLICY, tick_density=1)
        self.assertEqual(result.recommended_emptiness_action, "CONTINUE_ADVISORY_ONLY")
        self.assertEqual(result.gate_status, "EMPTINESS_GATE_PASS")
        self.assertTrue(result.non_reification_assertions["policy_hint_is_not_command"])
        self.assertTrue(result.non_reification_assertions["qique_regime_is_not_essence"])
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_high_tick_density_compacts_before_continue(self):
        result = evaluate_daemon_emptiness_gate(BASE_POLICY, tick_density=10)
        self.assertEqual(result.recommended_emptiness_action, "COMPACT_TRACE_BEFORE_CONTINUE")
        self.assertEqual(result.gate_reason, "tick_density_high")
        self.assertEqual(result.tick_density, 10)

    def test_reobserve_policy_reobserves_with_non_reification(self):
        policy = dict(BASE_POLICY)
        policy["recommended_tick_mode"] = "REOBSERVE_QI_PROCESS"
        result = evaluate_daemon_emptiness_gate(policy, tick_density=2)
        self.assertEqual(result.recommended_emptiness_action, "REOBSERVE_WITH_NON_REIFICATION")
        self.assertEqual(result.gate_status, "EMPTINESS_GATE_REOBSERVE")

    def test_quarantine_policy_holds_nonfinal(self):
        policy = dict(BASE_POLICY)
        policy["recommended_tick_mode"] = "QUARANTINE_REVIEW"
        result = evaluate_daemon_emptiness_gate(policy, tick_density=2)
        self.assertEqual(result.recommended_emptiness_action, "HOLD_OR_QUARANTINE_NONFINAL")
        self.assertEqual(result.gate_status, "EMPTINESS_GATE_BLOCKING_REIFICATION")

    def test_high_recovery_pressure_holds_and_compacts(self):
        policy = {
            "recommended_tick_mode": "CONTINUE_BOUNDED",
            "daemon_qique_gauge": {
                "qique_regime": "RECOVERY_PRESSURE_HIGH",
                "recovery_budget_pressure": 0.85,
            },
        }
        result = evaluate_daemon_emptiness_gate(policy, tick_density=2)
        self.assertEqual(result.recommended_emptiness_action, "HOLD_AND_COMPACT_TRACE")
        self.assertEqual(result.gate_status, "EMPTINESS_GATE_PRESSURE_HOLD")
        self.assertEqual(result.qique_recovery_budget_pressure, 0.85)

    def test_active_memory_with_density_uses_compact_monitor(self):
        policy = {
            "recommended_tick_mode": "CONTINUE_WITH_QI_MEMORY_MONITOR",
            "daemon_qique_gauge": {
                "qique_regime": "NONMARKOV_MEMORY_ACTIVE",
                "recovery_budget_pressure": 0.0,
            },
        }
        result = evaluate_daemon_emptiness_gate(policy, tick_density=3)
        self.assertEqual(result.recommended_emptiness_action, "CONTINUE_WITH_COMPACT_MONITOR")
        self.assertEqual(result.gate_reason, "memory_active_requires_compact_monitor")


if __name__ == "__main__":
    unittest.main()
