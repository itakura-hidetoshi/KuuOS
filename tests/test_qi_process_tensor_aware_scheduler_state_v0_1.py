import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_1 import step_qi_process_tensor_aware_scheduler_state


READY_PROPOSAL = {
    "scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY",
    "recommended_schedule_mode": "medium_horizon_revisit",
    "recommended_revisit_after_ticks": 3,
    "source_recommended_probe_type": "nonmarkov_memory_link_probe",
    "schedule_proposal_only": True,
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
}

HIGH_PRESSURE_METRICS = {
    "process_tensor_advantage_level": "QI_PROCESS_TENSOR_ADVANTAGE_READY",
    "history_depth": 5,
    "observation_debt_resolution_priority": 0.82,
    "safe_reentry_window_score": 0.28,
    "nonmarkov_link_density": 0.20,
    "memory_kernel_preservation_score": 0.40,
}

LOW_PRESSURE_METRICS = {
    "process_tensor_advantage_level": "QI_PROCESS_TENSOR_ADVANTAGE_READY",
    "history_depth": 5,
    "observation_debt_resolution_priority": 0.10,
    "safe_reentry_window_score": 0.80,
    "nonmarkov_link_density": 0.80,
    "memory_kernel_preservation_score": 0.85,
}


class QiProcessTensorAwareSchedulerStateTests(unittest.TestCase):
    def test_high_process_tensor_pressure_accelerates_revisit(self):
        result = step_qi_process_tensor_aware_scheduler_state(
            scheduler_state={"last_scheduled_tick": 4},
            scheduler_proposal=READY_PROPOSAL,
            process_tensor_metrics=HIGH_PRESSURE_METRICS,
            current_tick=5,
        )
        self.assertEqual(result.adjustment_status, "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED")
        self.assertEqual(result.base_revisit_after_ticks, 3)
        self.assertEqual(result.adjusted_revisit_after_ticks, 1)
        self.assertEqual(result.process_tensor_pressure_level, "high_process_tensor_pressure")
        self.assertTrue(result.process_tensor_aware)
        self.assertTrue(result.scheduler_state_updated)
        self.assertEqual(result.authority, "scheduler_state")
        self.assertTrue(result.grants_scheduler_authority)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.grants_dry_run_execution_authority)
        self.assertFalse(result.grants_next_tick_execution_authority)
        self.assertFalse(result.grants_control_packet_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)
        self.assertFalse(result.grants_world_update_authority)
        self.assertFalse(result.control_packet_mutation_performed)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)

    def test_low_process_tensor_pressure_keeps_base_tick(self):
        result = step_qi_process_tensor_aware_scheduler_state(
            scheduler_state={"last_scheduled_tick": 4},
            scheduler_proposal=READY_PROPOSAL,
            process_tensor_metrics=LOW_PRESSURE_METRICS,
            current_tick=5,
        )
        self.assertEqual(result.adjustment_status, "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED")
        self.assertEqual(result.base_revisit_after_ticks, 3)
        self.assertEqual(result.adjusted_revisit_after_ticks, 3)
        self.assertEqual(result.process_tensor_pressure_level, "low_process_tensor_pressure")

    def test_blocks_when_base_ticks_missing(self):
        proposal = dict(READY_PROPOSAL)
        proposal.pop("recommended_revisit_after_ticks")
        result = step_qi_process_tensor_aware_scheduler_state(
            scheduler_state={"last_scheduled_tick": 4},
            scheduler_proposal=proposal,
            process_tensor_metrics=HIGH_PRESSURE_METRICS,
            current_tick=5,
        )
        self.assertEqual(result.adjustment_status, "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_BLOCKED")
        self.assertIn("adjusted_revisit_after_ticks_missing", result.adjustment_blockers)
        self.assertFalse(result.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
