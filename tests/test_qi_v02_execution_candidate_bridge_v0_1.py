import unittest

from runtime.kuuos_runtime_daemon_qi_v02_execution_candidate_bridge_v0_1 import build_qi_v02_execution_candidate_bridge


V02 = {
    "adjustment_status": "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED",
    "replay_reuse_integrated": True,
    "scheduler_state_updated": True,
    "scheduler_authority_scope": "scheduler_state_only",
    "authority": "scheduler_state",
    "grants_scheduler_authority": True,
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "base_result": {
        "adjustment_status": "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED",
        "process_tensor_aware": True,
        "authority": "scheduler_state",
        "grants_scheduler_authority": True,
        "grants_execution_authority": False,
        "grants_probe_execution_authority": False,
        "grants_dry_run_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_control_packet_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_world_update_authority": False,
        "scheduler_result": {
            "scheduler_status": "QI_SCHEDULER_STATE_UPDATED",
            "due_status": "DUE",
            "scheduled_probe_type": "observation_debt_probe",
            "scheduled_mode": "near_term_revisit",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_dry_run_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_world_update_authority": False,
        },
    },
}


class QiV02ExecutionCandidateBridgeTests(unittest.TestCase):
    def test_v02_scheduler_surface_builds_candidate_without_authority(self):
        result = build_qi_v02_execution_candidate_bridge(v02_scheduler_surface=V02)
        self.assertEqual(result.bridge_status, "QI_V02_EXECUTION_CANDIDATE_BRIDGE_READY")
        self.assertEqual(result.candidate_status, "QI_PROBE_EXECUTION_CANDIDATE_READY")
        self.assertTrue(result.bridge_candidate_only)
        self.assertTrue(result.scheduler_due_satisfied)
        self.assertEqual(result.candidate_packet["candidate_probe_type"], "observation_debt_probe")
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_v02_surface_with_probe_execution_blocks_bridge(self):
        payload = dict(V02)
        payload["probe_execution_performed"] = True
        result = build_qi_v02_execution_candidate_bridge(v02_scheduler_surface=payload)
        self.assertEqual(result.bridge_status, "QI_V02_EXECUTION_CANDIDATE_BRIDGE_BLOCKED")
        self.assertIn("v02_probe_execution_performed_not_false", result.bridge_blockers)


if __name__ == "__main__":
    unittest.main()
