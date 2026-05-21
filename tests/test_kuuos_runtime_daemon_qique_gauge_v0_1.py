import unittest

from runtime.kuuos_runtime_daemon_qique_gauge_v0_1 import evaluate_daemon_qique_gauge

VISIBLE_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "transition_support_count": 3,
    "memory_support_count": 1,
    "nonmarkov_support_count": 1,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}

BLOCKED_SUMMARY = {
    "process_tensor_visible": False,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "transition_support_count": 3,
    "memory_support_count": 1,
    "nonmarkov_support_count": 1,
    "missing_process_requirements": ["boundary_fields_visible"],
    "process_tensor_reason": "boundary_blocks_process_tensor_support",
}

OVERDIFFUSED_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": False,
    "memory_continuity_visible": False,
    "nonmarkov_memory_visible": False,
    "process_history_length": 4,
    "transition_support_count": 1,
    "memory_support_count": 0,
    "nonmarkov_support_count": 0,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}

LOCALIZED_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": False,
    "process_history_length": 3,
    "transition_support_count": 3,
    "memory_support_count": 3,
    "nonmarkov_support_count": 0,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}


def status(summary=VISIBLE_SUMMARY, stop_reason="MAX_TICKS_REACHED", status_value="DAEMON_STATUS_READY", missing=None):
    return {
        "status": status_value,
        "stop_reason": stop_reason,
        "missing_files": list(missing or []),
        "latest_qi_process_tensor_summary": summary,
    }


class DaemonQiQueGaugeTests(unittest.TestCase):
    def test_nonmarkov_memory_active_regime(self):
        result = evaluate_daemon_qique_gauge(status())
        self.assertEqual(result.qique_regime, "NONMARKOV_MEMORY_ACTIVE")
        self.assertEqual(result.recommended_policy_hint, "CONTINUE_WITH_QI_MEMORY_MONITOR")
        self.assertEqual(result.qique_reason, "nonmarkov_memory_active")
        self.assertGreater(result.branch_energy, 0.0)
        self.assertGreater(result.scar_reentry_score, 0.0)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_incomplete_daemon_holds_for_repair(self):
        result = evaluate_daemon_qique_gauge(status(status_value="DAEMON_STATUS_INCOMPLETE", missing=["x"]))
        self.assertEqual(result.qique_regime, "INFRA_HOLD")
        self.assertEqual(result.recommended_policy_hint, "HOLD_FOR_DAEMON_REPAIR")
        self.assertEqual(result.recovery_budget_pressure, 1.0)

    def test_missing_summary_reobserves(self):
        result = evaluate_daemon_qique_gauge(status(summary=None))
        self.assertEqual(result.qique_regime, "OBSERVATION_GAP")
        self.assertEqual(result.recommended_policy_hint, "REOBSERVE_QI_PROCESS")

    def test_blocked_summary_reobserves(self):
        result = evaluate_daemon_qique_gauge(status(summary=BLOCKED_SUMMARY))
        self.assertEqual(result.qique_regime, "PROCESS_OBSERVATION_GAP")
        self.assertEqual(result.recommended_policy_hint, "REOBSERVE_QI_PROCESS")
        self.assertEqual(result.qique_reason, "boundary_blocks_process_tensor_support")

    def test_waiting_requests_more_evidence(self):
        result = evaluate_daemon_qique_gauge(status(stop_reason="WAITING_FOR_MORE_EVIDENCE"))
        self.assertEqual(result.qique_regime, "EVIDENCE_WAITING")
        self.assertEqual(result.recommended_policy_hint, "REQUEST_MORE_EVIDENCE")
        self.assertGreaterEqual(result.recovery_budget_pressure, 0.5)

    def test_quarantine_requests_review(self):
        result = evaluate_daemon_qique_gauge(status(stop_reason="QUARANTINE_RETAINED"))
        self.assertEqual(result.qique_regime, "BOUNDARY_QUARANTINE")
        self.assertEqual(result.recommended_policy_hint, "QUARANTINE_REVIEW")

    def test_overdiffusion_regime(self):
        result = evaluate_daemon_qique_gauge(status(summary=OVERDIFFUSED_SUMMARY))
        self.assertEqual(result.qique_regime, "OVERDIFFUSION")
        self.assertEqual(result.recommended_policy_hint, "FOCUS_OR_REOBSERVE")
        self.assertGreaterEqual(result.overdiffusion_score, 0.5)

    def test_localized_memory_regime(self):
        result = evaluate_daemon_qique_gauge(status(summary=LOCALIZED_SUMMARY))
        self.assertEqual(result.qique_regime, "LOCALIZED_MEMORY_CHANNEL")
        self.assertEqual(result.recommended_policy_hint, "BRANCH_EXPLORE_OR_MONITOR")
        self.assertGreaterEqual(result.localization_score, 0.67)


if __name__ == "__main__":
    unittest.main()
