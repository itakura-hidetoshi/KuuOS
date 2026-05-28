import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_2 import step_qi_process_tensor_aware_scheduler_state_v0_2


STATE = {"current_tick": 4, "last_revisit_tick": 2, "scheduler_status": "QI_SCHEDULER_STATE_UPDATED"}
PROPOSAL = {"recommended_revisit_after_ticks": 5, "source_recommended_probe_type": "continue_process_tensor_supervision_probe"}
METRICS = {
    "process_tensor_advantage_level": "moderate",
    "observation_debt_resolution_priority": 0.8,
    "safe_reentry_window_score": 0.5,
    "nonmarkov_link_density": 0.4,
    "memory_kernel_preservation_score": 0.7,
    "history_depth": 5,
}
REUSE = {
    "reuse_status": "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY",
    "proposal_reuse_only": True,
    "schedule_proposal_only": True,
    "reused_probe_family": "observation_debt_probe",
    "reused_scheduler_hint": "reuse_nonmarkov_history_for_observation_debt_probe",
    "reused_probe_planner_hint": "prioritize_probe_family_observation_debt_probe",
    "proposed_schedule_mode": "near_term_revisit",
    "proposed_revisit_after_ticks": 1,
    "proposed_revisit_reason": "MemoryOS replay suggests observation debt remains scheduler-relevant",
    "scheduler_state_mutation_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "grants_probe_execution_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_write_authority": False,
}


class QiProcessTensorAwareSchedulerStateV02Tests(unittest.TestCase):
    def test_reuse_proposal_integrates_into_process_tensor_scheduler(self):
        result = step_qi_process_tensor_aware_scheduler_state_v0_2(
            scheduler_state=STATE,
            scheduler_proposal=PROPOSAL,
            process_tensor_metrics=METRICS,
            current_tick=4,
            proposal_reuse=REUSE,
        )
        self.assertEqual(result.adjustment_status, "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED")
        self.assertTrue(result.replay_reuse_integrated)
        self.assertEqual(result.reused_probe_family, "observation_debt_probe")
        self.assertTrue(result.scheduler_state_mutation_performed)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_reuse_attempting_probe_execution_blocks_v02(self):
        reuse = dict(REUSE)
        reuse["probe_execution_performed"] = True
        result = step_qi_process_tensor_aware_scheduler_state_v0_2(
            scheduler_state=STATE,
            scheduler_proposal=PROPOSAL,
            process_tensor_metrics=METRICS,
            current_tick=4,
            proposal_reuse=reuse,
        )
        self.assertEqual(result.adjustment_status, "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_BLOCKED")
        self.assertIn("reuse_probe_execution_performed_not_false", result.v02_blockers)


if __name__ == "__main__":
    unittest.main()
