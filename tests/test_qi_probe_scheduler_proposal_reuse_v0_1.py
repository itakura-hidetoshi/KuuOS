import unittest

from runtime.kuuos_runtime_daemon_qi_probe_scheduler_proposal_reuse_v0_1 import build_qi_probe_scheduler_proposal_reuse


APPLY = {
    "apply_status": "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED",
    "next_scheduler_state": {
        "scheduler_update_kind": "memoryos_process_tensor_replay_hint",
        "replay_dominant_probe_type": "observation_debt_probe",
        "replay_scheduler_reuse_hint": "reuse_nonmarkov_history_for_observation_debt_probe",
        "replay_probe_planner_reuse_hint": "prioritize_probe_family_observation_debt_probe",
        "lineage_preserved": True,
    },
}

CTX = {
    "reuse_scope": "proposal_only",
    "request_scheduler_state_mutation": False,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
}


class QiProbeSchedulerProposalReuseTests(unittest.TestCase):
    def test_replay_updated_scheduler_state_creates_proposal_only_reuse(self):
        result = build_qi_probe_scheduler_proposal_reuse(
            replay_applied_scheduler_state=APPLY,
            reuse_context=CTX,
        )
        self.assertEqual(result.reuse_status, "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY")
        self.assertTrue(result.proposal_reuse_only)
        self.assertTrue(result.schedule_proposal_only)
        self.assertEqual(result.reused_probe_family, "observation_debt_probe")
        self.assertEqual(result.proposed_revisit_after_ticks, 1)
        self.assertFalse(result.scheduler_state_mutation_performed)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_probe_execution_request_blocks_reuse(self):
        ctx = dict(CTX)
        ctx["request_probe_execution"] = True
        result = build_qi_probe_scheduler_proposal_reuse(
            replay_applied_scheduler_state=APPLY,
            reuse_context=ctx,
        )
        self.assertEqual(result.reuse_status, "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_BLOCKED")
        self.assertIn("request_probe_execution", result.reuse_blockers)
        self.assertFalse(result.probe_execution_performed)


if __name__ == "__main__":
    unittest.main()
