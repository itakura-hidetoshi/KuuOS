import unittest

from runtime.kuuos_runtime_daemon_qi_probe_execution_review_gate_v0_1 import review_qi_probe_execution_candidate


BASE = {
    "candidate_status": "QI_PROBE_EXECUTION_CANDIDATE_READY",
    "candidate_probe_type": "observation_debt_probe",
    "candidate_schedule_mode": "near_term_revisit",
    "execution_candidate_only": True,
    "scheduler_due_required": True,
    "scheduler_due_satisfied": True,
    "requires_operator_review": True,
    "requires_governor_approval": True,
    "authority": "none",
    "scheduler_state_mutation_performed": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "dry_run_execution_performed": False,
    "next_tick_execution_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_scheduler_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
}


class QiProbeExecutionReviewGateTests(unittest.TestCase):
    def test_ready_candidate_passes_as_review_only(self):
        result = review_qi_probe_execution_candidate(candidate_packet=BASE)
        self.assertEqual(result.gate_status, "QI_PROBE_EXECUTION_REVIEW_GATE_READY")
        self.assertEqual(result.review_outcome, "READY_FOR_AUTHORITY_REVIEW")
        self.assertTrue(result.ready_for_authority_review)
        self.assertEqual(result.authority, "none")
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.probe_execution_performed)

    def test_blocked_candidate_holds(self):
        payload = dict(BASE)
        payload["candidate_status"] = "QI_PROBE_EXECUTION_CANDIDATE_BLOCKED"
        result = review_qi_probe_execution_candidate(candidate_packet=payload)
        self.assertEqual(result.gate_status, "QI_PROBE_EXECUTION_REVIEW_GATE_BLOCKED")
        self.assertEqual(result.review_outcome, "HOLD")
        self.assertFalse(result.ready_for_authority_review)


if __name__ == "__main__":
    unittest.main()
