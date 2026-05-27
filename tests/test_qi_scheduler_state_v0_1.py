import unittest

from runtime.kuuos_runtime_daemon_qi_scheduler_state_v0_1 import step_qi_scheduler_state


READY_PROPOSAL = {
    "scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY",
    "recommended_schedule_mode": "near_term_revisit",
    "recommended_revisit_after_ticks": 1,
    "source_recommended_probe_type": "observation_debt_probe",
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


class QiSchedulerStateTests(unittest.TestCase):
    def test_due_when_current_tick_reaches_next_due_tick(self):
        result = step_qi_scheduler_state(
            scheduler_state={"last_scheduled_tick": 4},
            scheduler_proposal=READY_PROPOSAL,
            current_tick=5,
        )
        self.assertEqual(result.scheduler_status, "QI_SCHEDULER_STATE_UPDATED")
        self.assertEqual(result.due_status, "DUE")
        self.assertEqual(result.next_due_tick, 5)
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

    def test_wait_before_next_due_tick(self):
        result = step_qi_scheduler_state(
            scheduler_state={"last_scheduled_tick": 4},
            scheduler_proposal=READY_PROPOSAL,
            current_tick=4,
        )
        self.assertEqual(result.scheduler_status, "QI_SCHEDULER_STATE_UPDATED")
        self.assertEqual(result.due_status, "WAIT")
        self.assertEqual(result.next_due_tick, 5)

    def test_blocked_when_proposal_not_ready(self):
        proposal = dict(READY_PROPOSAL)
        proposal["scheduler_status"] = "QI_PROBE_SCHEDULER_PROPOSAL_BLOCKED"
        result = step_qi_scheduler_state(
            scheduler_state={"last_scheduled_tick": 4},
            scheduler_proposal=proposal,
            current_tick=5,
        )
        self.assertEqual(result.scheduler_status, "QI_SCHEDULER_STATE_BLOCKED")
        self.assertIn("scheduler_proposal_not_ready", result.scheduler_blockers)
        self.assertFalse(result.scheduler_state_updated)
        self.assertFalse(result.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
