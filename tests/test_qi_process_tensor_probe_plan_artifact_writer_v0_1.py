import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_plan_artifact_writer_v0_1 import build_qi_process_tensor_probe_plan_artifact


READY_STATUS_VIEW = {
    "status_view_status": "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY",
    "out_dir": "/tmp/supervisor",
    "latest_controlled_loop_result_path": "/tmp/supervisor/controlled_loop.json",
    "recommended_probe_type": "observation_debt_probe",
    "probe_target_time_slice": "t_debt",
    "probe_risk_level": "medium",
    "grants_probe_execution_authority": False,
    "latest_process_tensor_advantage_metrics": {
        "metrics_status": "QI_PROCESS_TENSOR_ADVANTAGE_READY",
        "process_tensor_advantage_score": 0.72,
    },
    "latest_process_tensor_probe_plan": {
        "probe_plan_status": "QI_PROCESS_TENSOR_PROBE_PLAN_READY_WITH_WARNINGS",
        "recommended_probe_type": "observation_debt_probe",
        "probe_target_time_slice": "t_debt",
        "probe_expected_recoverability_gain": 0.12,
        "probe_expected_observation_debt_reduction": 0.66,
        "probe_risk_level": "medium",
        "probe_plan_only": True,
        "read_only": True,
        "authority": "none",
        "grants_probe_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_memory_overwrite_authority": False,
    },
}


class QiProcessTensorProbePlanArtifactWriterTests(unittest.TestCase):
    def test_ready_status_view_builds_proposal_artifact_without_authority(self):
        artifact = build_qi_process_tensor_probe_plan_artifact(status_view=READY_STATUS_VIEW)
        self.assertEqual(artifact.artifact_status, "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY")
        self.assertEqual(artifact.recommended_probe_type, "observation_debt_probe")
        self.assertEqual(artifact.probe_target_time_slice, "t_debt")
        self.assertEqual(artifact.probe_risk_level, "medium")
        self.assertGreater(artifact.probe_expected_observation_debt_reduction, 0.5)
        self.assertEqual(artifact.artifact_blockers, [])
        self.assertTrue(artifact.proposal_artifact_only)
        self.assertTrue(artifact.read_only)
        self.assertEqual(artifact.authority, "none")
        self.assertFalse(artifact.grants_execution_authority)
        self.assertFalse(artifact.grants_probe_execution_authority)
        self.assertFalse(artifact.grants_next_tick_execution_authority)
        self.assertFalse(artifact.grants_control_packet_authority)
        self.assertFalse(artifact.grants_memory_overwrite_authority)

    def test_missing_probe_plan_blocks_artifact(self):
        status_view = dict(READY_STATUS_VIEW)
        status_view["latest_process_tensor_probe_plan"] = {}
        artifact = build_qi_process_tensor_probe_plan_artifact(status_view=status_view)
        self.assertEqual(artifact.artifact_status, "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_BLOCKED")
        self.assertIn("latest_process_tensor_probe_plan_missing", artifact.artifact_blockers)
        self.assertEqual(artifact.authority, "none")
        self.assertFalse(artifact.grants_probe_execution_authority)

    def test_authority_claim_in_probe_plan_blocks_artifact(self):
        status_view = dict(READY_STATUS_VIEW)
        probe_plan = dict(READY_STATUS_VIEW["latest_process_tensor_probe_plan"])
        probe_plan["grants_probe_execution_authority"] = True
        status_view["latest_process_tensor_probe_plan"] = probe_plan
        artifact = build_qi_process_tensor_probe_plan_artifact(status_view=status_view)
        self.assertEqual(artifact.artifact_status, "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_BLOCKED")
        self.assertIn("probe_plan_execution_authority_not_false", artifact.artifact_blockers)
        self.assertFalse(artifact.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
