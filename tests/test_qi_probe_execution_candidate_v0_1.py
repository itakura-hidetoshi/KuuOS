import unittest

from runtime.kuuos_runtime_daemon_qi_probe_execution_candidate_v0_1 import build_qi_probe_execution_candidate


READY_SCHEDULER_SURFACE = {
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
}


class QiProbeExecutionCandidateTests(unittest.TestCase):
    def test_due_scheduler_creates_candidate_without_execution_authority(self):
        result = build_qi_probe_execution_candidate(scheduler_surface=READY_SCHEDULER_SURFACE)
        self.assertEqual(result.candidate_status, "QI_PROBE_EXECUTION_CANDIDATE_READY")
        self.assertEqual(result.candidate_probe_type, "observation_debt_probe")
        self.assertTrue(result.execution_candidate_only)
        self.assertTrue(result.scheduler_due_required)
        self.assertTrue(result.scheduler_due_satisfied)
        self.assertTrue(result.requires_operator_review)
        self.assertTrue(result.requires_governor_approval)
        self.assertEqual(result.authority, "none")
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.grants_dry_run_execution_authority)
        self.assertFalse(result.grants_next_tick_execution_authority)
        self.assertFalse(result.grants_scheduler_authority)
        self.assertFalse(result.grants_control_packet_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)
        self.assertFalse(result.grants_world_update_authority)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.dry_run_execution_performed)
        self.assertFalse(result.next_tick_execution_performed)
        self.assertFalse(result.scheduler_state_mutation_performed)
        self.assertFalse(result.control_packet_mutation_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)

    def test_wait_scheduler_blocks_candidate(self):
        payload = dict(READY_SCHEDULER_SURFACE)
        nested = dict(payload["scheduler_result"])
        nested["due_status"] = "WAIT"
        payload["scheduler_result"] = nested
        result = build_qi_probe_execution_candidate(scheduler_surface=payload)
        self.assertEqual(result.candidate_status, "QI_PROBE_EXECUTION_CANDIDATE_BLOCKED")
        self.assertIn("scheduler_due_status_not_due", result.candidate_blockers)
        self.assertFalse(result.scheduler_due_satisfied)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_source_attempting_probe_authority_blocks_candidate(self):
        payload = dict(READY_SCHEDULER_SURFACE)
        payload["grants_probe_execution_authority"] = True
        result = build_qi_probe_execution_candidate(scheduler_surface=payload)
        self.assertEqual(result.candidate_status, "QI_PROBE_EXECUTION_CANDIDATE_BLOCKED")
        self.assertIn("source_grants_probe_execution_authority_not_false", result.candidate_blockers)
        self.assertFalse(result.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
