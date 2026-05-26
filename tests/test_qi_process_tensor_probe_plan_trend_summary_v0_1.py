import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_plan_trend_summary_v0_1 import build_qi_process_tensor_probe_plan_trend_summary


READY_INDEX = {
    "index_status": "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY",
    "dominant_probe_type": "observation_debt_probe",
    "latest_recommended_probe_type": "observation_debt_probe",
    "latest_probe_target_time_slice": "t2",
    "repeated_probe_types": ["observation_debt_probe"],
    "index_only": True,
    "read_only": True,
    "authority": "none",
    "grants_probe_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
}


class QiProcessTensorProbePlanTrendSummaryTests(unittest.TestCase):
    def test_observation_debt_dominant_index_builds_read_only_summary(self):
        summary = build_qi_process_tensor_probe_plan_trend_summary(artifact_index=READY_INDEX)
        self.assertEqual(summary.summary_status, "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY")
        self.assertEqual(summary.dominant_probe_type, "observation_debt_probe")
        self.assertEqual(summary.latest_probe_target_time_slice, "t2")
        self.assertEqual(summary.repeated_probe_types, ["observation_debt_probe"])
        self.assertEqual(summary.qi_process_tensor_characterization, "observation_debt_limited_qi_process_tensor")
        self.assertIn("observation debt", summary.trend_interpretation)
        self.assertIn("review observation debt", summary.recommended_operator_focus)
        self.assertTrue(summary.summary_only)
        self.assertTrue(summary.read_only)
        self.assertEqual(summary.authority, "none")
        self.assertFalse(summary.grants_execution_authority)
        self.assertFalse(summary.grants_probe_execution_authority)
        self.assertFalse(summary.grants_next_tick_execution_authority)
        self.assertFalse(summary.grants_control_packet_authority)
        self.assertFalse(summary.grants_memory_overwrite_authority)

    def test_not_ready_index_blocks_summary(self):
        index = dict(READY_INDEX)
        index["index_status"] = "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_BLOCKED"
        summary = build_qi_process_tensor_probe_plan_trend_summary(artifact_index=index)
        self.assertEqual(summary.summary_status, "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_BLOCKED")
        self.assertIn("artifact_index_not_ready", summary.summary_blockers)
        self.assertEqual(summary.authority, "none")
        self.assertFalse(summary.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
