import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_plan_artifact_index_v0_1 import build_qi_process_tensor_probe_plan_artifact_index


def sample_artifact(probe_type, target, risk, gain, debt):
    return {
        "artifact_status": "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY",
        "recommended_probe_type": probe_type,
        "probe_target_time_slice": target,
        "probe_risk_level": risk,
        "probe_expected_recoverability_gain": gain,
        "probe_expected_observation_debt_reduction": debt,
        "proposal_artifact_only": True,
        "read_only": True,
        "authority": "none",
        "grants_probe_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_control_packet_authority": False,
        "grants_memory_overwrite_authority": False,
    }


class QiProcessTensorProbePlanArtifactIndexTests(unittest.TestCase):
    def test_index_counts_repeated_probe_types_and_means(self):
        index = build_qi_process_tensor_probe_plan_artifact_index(artifacts=[
            sample_artifact("observation_debt_probe", "t0", "medium", 0.1, 0.6),
            sample_artifact("recoverability_branch_probe", "t1", "low", 0.5, 0.2),
            sample_artifact("observation_debt_probe", "t2", "medium", 0.2, 0.7),
        ])
        self.assertEqual(index.index_status, "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY")
        self.assertEqual(index.artifact_count, 3)
        self.assertEqual(index.ready_artifact_count, 3)
        self.assertEqual(index.probe_type_counts["observation_debt_probe"], 2)
        self.assertEqual(index.dominant_probe_type, "observation_debt_probe")
        self.assertEqual(index.latest_recommended_probe_type, "observation_debt_probe")
        self.assertEqual(index.latest_probe_target_time_slice, "t2")
        self.assertEqual(index.repeated_probe_types, ["observation_debt_probe"])
        self.assertAlmostEqual(index.mean_expected_recoverability_gain, 0.266667)
        self.assertAlmostEqual(index.mean_expected_observation_debt_reduction, 0.5)
        self.assertTrue(index.index_only)
        self.assertTrue(index.read_only)
        self.assertEqual(index.authority, "none")
        self.assertFalse(index.grants_probe_execution_authority)
        self.assertFalse(index.grants_next_tick_execution_authority)

    def test_missing_artifacts_blocks_index(self):
        index = build_qi_process_tensor_probe_plan_artifact_index(artifacts=[])
        self.assertEqual(index.index_status, "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_BLOCKED")
        self.assertIn("probe_plan_artifacts_missing", index.index_blockers)
        self.assertEqual(index.authority, "none")
        self.assertFalse(index.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
