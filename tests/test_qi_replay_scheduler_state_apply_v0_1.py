import unittest

from runtime.kuuos_runtime_daemon_qi_replay_scheduler_state_apply_v0_1 import apply_qi_replay_scheduler_state


REPLAY = {
    "replay_status": "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY",
    "retrieval_only": True,
    "replay_surface_only": True,
    "memory_read_performed": True,
    "dominant_probe_type": "observation_debt_probe",
    "scheduler_reuse_hint": "reuse_nonmarkov_history_for_observation_debt_probe",
    "probe_planner_reuse_hint": "prioritize_probe_family_observation_debt_probe",
    "memory_write_performed": False,
    "memory_append_performed": False,
    "memory_overwrite_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "scheduler_state_mutation_performed": False,
    "grants_memory_write_authority": False,
    "grants_world_update_authority": False,
    "grants_probe_execution_authority": False,
}

STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["base"]}
CTX = {
    "allow_scheduler_state_update": True,
    "scheduler_update_scope": "replay_hint_only",
    "scheduler_lineage_preserved": True,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
}


class QiReplaySchedulerStateApplyTests(unittest.TestCase):
    def test_replay_hint_updates_scheduler_state_only(self):
        result = apply_qi_replay_scheduler_state(
            replay_packet=REPLAY,
            scheduler_state=STATE,
            apply_context=CTX,
        )
        self.assertEqual(result.apply_status, "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED")
        self.assertTrue(result.scheduler_state_mutation_performed)
        self.assertEqual(result.scheduler_update_scope, "replay_hint_only")
        self.assertEqual(result.next_scheduler_state["scheduler_update_kind"], "memoryos_process_tensor_replay_hint")
        self.assertEqual(result.next_scheduler_state["replay_dominant_probe_type"], "observation_debt_probe")
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_world_update_request_blocks_apply(self):
        ctx = dict(CTX)
        ctx["request_world_update"] = True
        result = apply_qi_replay_scheduler_state(
            replay_packet=REPLAY,
            scheduler_state=STATE,
            apply_context=ctx,
        )
        self.assertEqual(result.apply_status, "QI_REPLAY_SCHEDULER_STATE_APPLY_BLOCKED")
        self.assertIn("request_world_update", result.apply_blockers)
        self.assertFalse(result.scheduler_state_mutation_performed)
        self.assertFalse(result.world_update_performed)


if __name__ == "__main__":
    unittest.main()
