import unittest

from runtime.kuuos_runtime_daemon_qi_persistent_process_tensor_daemon_v0_1 import run_qi_persistent_process_tensor_daemon_tick


MEMORY = [{
    "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
    "source_probe_type": "observation_debt_probe",
    "append_only": True,
    "memory_append_performed": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "lineage_preserved": True,
}]

STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["persistent_runtime"]}
PROPOSAL = {
    "scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY",
    "recommended_schedule_mode": "routine_revisit",
    "recommended_revisit_after_ticks": 5,
    "recommended_revisit_reason": "base routine",
    "source_recommended_probe_type": "continue_process_tensor_supervision_probe",
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
METRICS = {
    "process_tensor_advantage_level": "moderate",
    "observation_debt_resolution_priority": 0.9,
    "safe_reentry_window_score": 0.5,
    "nonmarkov_link_density": 0.6,
    "memory_kernel_preservation_score": 0.8,
    "history_depth": 7,
}
CTX = {
    "tick_id": "tick-001",
    "allow_persistent_tick": True,
    "bounded_tick": True,
    "heartbeat_required": True,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
}


class QiPersistentProcessTensorDaemonTests(unittest.TestCase):
    def test_persistent_tick_closes_loop_without_execution(self):
        result = run_qi_persistent_process_tensor_daemon_tick(
            memory_entries=MEMORY,
            scheduler_state=STATE,
            scheduler_proposal=PROPOSAL,
            process_tensor_metrics=METRICS,
            runtime_context=CTX,
            current_tick=9,
        )
        self.assertEqual(result.daemon_status, "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY")
        self.assertTrue(result.heartbeat_emitted)
        self.assertTrue(result.closed_loop_tick_performed)
        self.assertEqual(result.dominant_probe_type, "observation_debt_probe")
        self.assertEqual(result.process_tensor_pressure, "high")
        self.assertTrue(result.scheduler_state_mutation_performed)
        self.assertEqual(result.scheduler_update_scope, "replay_hint_only")
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_probe_execution_request_blocks_tick(self):
        ctx = dict(CTX)
        ctx["request_probe_execution"] = True
        result = run_qi_persistent_process_tensor_daemon_tick(
            memory_entries=MEMORY,
            scheduler_state=STATE,
            scheduler_proposal=PROPOSAL,
            process_tensor_metrics=METRICS,
            runtime_context=ctx,
            current_tick=9,
        )
        self.assertEqual(result.daemon_status, "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_BLOCKED")
        self.assertIn("request_probe_execution", result.daemon_blockers)
        self.assertFalse(result.probe_execution_performed)


if __name__ == "__main__":
    unittest.main()
