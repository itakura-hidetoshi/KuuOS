import unittest

from runtime.kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1 import evaluate_daemon_yinyang_polarity

BALANCED_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": False,
    "process_history_length": 3,
    "transition_support_count": 2,
    "memory_support_count": 2,
    "nonmarkov_support_count": 0,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}

YANG_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": False,
    "nonmarkov_memory_visible": False,
    "process_history_length": 4,
    "transition_support_count": 4,
    "memory_support_count": 0,
    "nonmarkov_support_count": 0,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}

YIN_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": False,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 4,
    "transition_support_count": 0,
    "memory_support_count": 3,
    "nonmarkov_support_count": 1,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}

FALSE_YANG_SUMMARY = {
    "process_tensor_visible": False,
    "transition_continuity_visible": True,
    "memory_continuity_visible": False,
    "nonmarkov_memory_visible": False,
    "process_history_length": 3,
    "transition_support_count": 3,
    "memory_support_count": 0,
    "nonmarkov_support_count": 0,
    "missing_process_requirements": ["boundary_fields_visible"],
    "process_tensor_reason": "boundary_blocks_process_tensor_support",
}

SWITCHING_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "transition_support_count": 2,
    "memory_support_count": 1,
    "nonmarkov_support_count": 1,
    "missing_process_requirements": ["phase_switch_witness"],
    "process_tensor_reason": "process_tensor_support_visible",
}

RECOVERY_SUMMARY = {
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


def status(summary=BALANCED_SUMMARY, stop_reason="MAX_TICKS_REACHED", status_value="DAEMON_STATUS_READY", missing=None):
    return {
        "status": status_value,
        "stop_reason": stop_reason,
        "missing_files": list(missing or []),
        "latest_qi_process_tensor_summary": summary,
    }


class DaemonYinYangPolarityGaugeTests(unittest.TestCase):
    def test_balanced_flow(self):
        result = evaluate_daemon_yinyang_polarity(status())
        self.assertEqual(result.yinyang_polarity_state, "BALANCED_FLOW")
        self.assertEqual(result.recommended_policy_hint, "CONTINUE_HARMONIZED")
        self.assertGreater(result.polarity_balance, 0.7)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_yang_overdrive(self):
        result = evaluate_daemon_yinyang_polarity(status(summary=YANG_SUMMARY))
        self.assertEqual(result.yinyang_polarity_state, "YANG_OVERDRIVE")
        self.assertEqual(result.recommended_policy_hint, "SLOW_DOWN_AND_REOBSERVE")
        self.assertGreater(result.yang_drive, result.yin_load)

    def test_yin_stagnation(self):
        result = evaluate_daemon_yinyang_polarity(status(summary=YIN_SUMMARY))
        self.assertEqual(result.yinyang_polarity_state, "YIN_STAGNATION")
        self.assertEqual(result.recommended_policy_hint, "BRANCH_EXPLORE_LIGHTLY")
        self.assertGreater(result.yin_load, result.yang_drive)

    def test_false_yang_when_process_hidden(self):
        result = evaluate_daemon_yinyang_polarity(status(summary=FALSE_YANG_SUMMARY))
        self.assertEqual(result.yinyang_polarity_state, "FALSE_YANG")
        self.assertEqual(result.recommended_policy_hint, "REOBSERVE_QI_PROCESS")
        self.assertGreaterEqual(result.false_yang_risk, 0.5)

    def test_switching_unstable(self):
        result = evaluate_daemon_yinyang_polarity(status(summary=SWITCHING_SUMMARY))
        self.assertEqual(result.yinyang_polarity_state, "SWITCHING_UNSTABLE")
        self.assertEqual(result.recommended_policy_hint, "HOLD_WITH_RECOVERY")
        self.assertGreaterEqual(result.switch_risk, 0.6)

    def test_recovery_yang_present(self):
        result = evaluate_daemon_yinyang_polarity(status(summary=RECOVERY_SUMMARY))
        self.assertEqual(result.yinyang_polarity_state, "RECOVERY_YANG_PRESENT")
        self.assertEqual(result.recommended_policy_hint, "CONTINUE_WITH_QI_MEMORY_MONITOR")

    def test_boundary_yin_required_on_quarantine(self):
        result = evaluate_daemon_yinyang_polarity(status(stop_reason="QUARANTINE_RETAINED"))
        self.assertEqual(result.yinyang_polarity_state, "BOUNDARY_YIN_REQUIRED")
        self.assertEqual(result.recommended_policy_hint, "QUARANTINE_REVIEW")

    def test_infra_hold_requires_boundary_yin(self):
        result = evaluate_daemon_yinyang_polarity(status(status_value="DAEMON_STATUS_INCOMPLETE", missing=["x"]))
        self.assertEqual(result.yinyang_polarity_state, "BOUNDARY_YIN_REQUIRED")
        self.assertEqual(result.recommended_policy_hint, "HOLD_FOR_DAEMON_REPAIR")


if __name__ == "__main__":
    unittest.main()
