import unittest

from runtime.kuuos_runtime_daemon_qi_actuation_license_gate_v0_1 import build_qi_actuation_license_candidate


READY_SUMMARY = {
    "summary_status": "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY",
    "qi_process_tensor_characterization": "observation_debt_limited_qi_process_tensor",
    "summary_only": True,
    "read_only": True,
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
}

READY_PHASE = {
    "packet_status": "QI_PROCESS_TENSOR_REVIEW_PHASE_BOUNDARY_READY",
    "phase_boundary_only": True,
    "current_phase_only": True,
    "mutable_by_pr": True,
    "replacement_allowed": True,
    "finality_claimed": False,
    "append_only_required": False,
    "overwrite_forbidden": False,
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
}


class QiActuationLicenseGateTests(unittest.TestCase):
    def test_dry_run_candidate_ready_without_authority(self):
        candidate = build_qi_actuation_license_candidate(
            trend_summary=READY_SUMMARY,
            phase_boundary_packet=READY_PHASE,
            requested_actuation_mode="dry_run_probe_simulation",
        )
        self.assertEqual(candidate.gate_status, "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY")
        self.assertEqual(candidate.candidate_license_kind, "dry_run_probe_simulation_candidate")
        self.assertEqual(candidate.allowed_next_surface, "dry_run_probe_executor_candidate_review")
        self.assertTrue(candidate.license_candidate_only)
        self.assertTrue(candidate.dry_run_candidate_only)
        self.assertTrue(candidate.requires_governor_approval)
        self.assertTrue(candidate.requires_operator_review)
        self.assertEqual(candidate.authority, "none")
        self.assertFalse(candidate.grants_execution_authority)
        self.assertFalse(candidate.grants_probe_execution_authority)
        self.assertFalse(candidate.grants_dry_run_execution_authority)
        self.assertFalse(candidate.grants_next_tick_execution_authority)
        self.assertFalse(candidate.grants_control_packet_authority)
        self.assertFalse(candidate.grants_memory_overwrite_authority)
        self.assertFalse(candidate.grants_world_update_authority)

    def test_non_dry_run_request_is_blocked(self):
        candidate = build_qi_actuation_license_candidate(
            trend_summary=READY_SUMMARY,
            phase_boundary_packet=READY_PHASE,
            requested_actuation_mode="probe_execution",
        )
        self.assertEqual(candidate.gate_status, "QI_ACTUATION_LICENSE_GATE_BLOCKED")
        self.assertIn("non_dry_run_actuation_not_allowed_v0_1", candidate.gate_blockers)
        self.assertIsNone(candidate.candidate_license_kind)
        self.assertFalse(candidate.grants_execution_authority)

    def test_phase_finality_claim_blocks_candidate(self):
        phase = dict(READY_PHASE)
        phase["finality_claimed"] = True
        candidate = build_qi_actuation_license_candidate(
            trend_summary=READY_SUMMARY,
            phase_boundary_packet=phase,
            requested_actuation_mode="dry_run_probe_simulation",
        )
        self.assertEqual(candidate.gate_status, "QI_ACTUATION_LICENSE_GATE_BLOCKED")
        self.assertIn("review_phase_boundary_finality_claimed_not_false", candidate.gate_blockers)
        self.assertFalse(candidate.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
