import unittest

from runtime.kuuos_runtime_daemon_qi_policy_v0_1 import evaluate_daemon_qi_policy

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


def status(summary=VISIBLE_SUMMARY, stop_reason="MAX_TICKS_REACHED", status_value="DAEMON_STATUS_READY"):
    return {
        "status": status_value,
        "stop_reason": stop_reason,
        "missing_files": [],
        "latest_qi_process_tensor_summary": summary,
    }


class DaemonQiPolicyTests(unittest.TestCase):
    def test_visible_nonmarkov_summary_continues_with_monitor(self):
        result = evaluate_daemon_qi_policy(status())
        self.assertEqual(result.recommended_tick_mode, "CONTINUE_WITH_QI_MEMORY_MONITOR")
        self.assertEqual(result.policy_reason, "process_tensor_and_nonmarkov_memory_visible")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "NONMARKOV_MEMORY_ACTIVE")
        self.assertEqual(result.daemon_qique_gauge["recommended_policy_hint"], "CONTINUE_WITH_QI_MEMORY_MONITOR")
        self.assertFalse(result.required_operator_attention)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_missing_summary_reobserves(self):
        result = evaluate_daemon_qi_policy(status(summary=None))
        self.assertEqual(result.recommended_tick_mode, "REOBSERVE_QI_PROCESS")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "OBSERVATION_GAP")
        self.assertTrue(result.required_operator_attention)

    def test_blocked_summary_reobserves(self):
        result = evaluate_daemon_qi_policy(status(summary=BLOCKED_SUMMARY))
        self.assertEqual(result.recommended_tick_mode, "REOBSERVE_QI_PROCESS")
        self.assertEqual(result.policy_reason, "boundary_blocks_process_tensor_support")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "PROCESS_OBSERVATION_GAP")
        self.assertTrue(result.required_operator_attention)

    def test_qique_overdiffusion_changes_policy_hint(self):
        result = evaluate_daemon_qi_policy(status(summary=OVERDIFFUSED_SUMMARY))
        self.assertEqual(result.recommended_tick_mode, "FOCUS_OR_REOBSERVE")
        self.assertEqual(result.policy_reason, "qique_overdiffusion")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "OVERDIFFUSION")
        self.assertTrue(result.required_operator_attention)

    def test_waiting_requests_evidence(self):
        result = evaluate_daemon_qi_policy(status(stop_reason="WAITING_FOR_MORE_EVIDENCE"))
        self.assertEqual(result.recommended_tick_mode, "REQUEST_MORE_EVIDENCE")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "EVIDENCE_WAITING")
        self.assertTrue(result.required_operator_attention)

    def test_quarantine_requests_review(self):
        result = evaluate_daemon_qi_policy(status(stop_reason="QUARANTINE_RETAINED"))
        self.assertEqual(result.recommended_tick_mode, "QUARANTINE_REVIEW")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "BOUNDARY_QUARANTINE")
        self.assertTrue(result.required_operator_attention)

    def test_incomplete_daemon_holds_for_repair(self):
        result = evaluate_daemon_qi_policy({
            "status": "DAEMON_STATUS_INCOMPLETE",
            "stop_reason": None,
            "missing_files": ["x"],
            "latest_qi_process_tensor_summary": VISIBLE_SUMMARY,
        })
        self.assertEqual(result.recommended_tick_mode, "HOLD_FOR_DAEMON_REPAIR")
        self.assertEqual(result.daemon_qique_gauge["qique_regime"], "INFRA_HOLD")
        self.assertTrue(result.required_operator_attention)


if __name__ == "__main__":
    unittest.main()
