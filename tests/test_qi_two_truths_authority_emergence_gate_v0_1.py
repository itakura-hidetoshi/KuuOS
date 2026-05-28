import unittest

from runtime.kuuos_runtime_daemon_qi_two_truths_authority_emergence_gate_v0_1 import evaluate_qi_two_truths_authority_emergence


REVIEW = {
    "gate_status": "QI_PROBE_EXECUTION_REVIEW_GATE_READY",
    "review_outcome": "READY_FOR_AUTHORITY_REVIEW",
    "ready_for_authority_review": True,
    "authority_review_required": True,
    "authority": "none",
    "reviewed_probe_type": "observation_debt_probe",
    "reviewed_schedule_mode": "near_term_revisit",
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

CTX = {
    "conventional_authority_scope": "single_probe_execution_candidate_review",
    "ultimate_non_reification_preserved": True,
    "dependent_origination_trace_present": True,
    "two_truths_boundary_preserved": True,
    "mass_gap_barrier_preserved": True,
    "superstring_membrane_boundary_preserved": True,
    "super_relativity_record_surface_present": True,
    "causal_trace_present": True,
    "rollback_path_present": True,
    "safe_reentry_window_acceptable": True,
    "observation_debt_targeted_or_bounded": True,
    "memory_kernel_preservation_acceptable": True,
    "authority_claims_ultimate_truth": False,
    "authority_scope_unbounded": False,
    "authority_irrevocable": False,
    "mass_gap_collapsed": False,
    "direct_execution_requested": False,
}


class QiTwoTruthsAuthorityEmergenceGateTests(unittest.TestCase):
    def test_ready_context_yields_grant_candidate_only(self):
        result = evaluate_qi_two_truths_authority_emergence(review_gate_packet=REVIEW, authority_context=CTX)
        self.assertEqual(result.gate_status, "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_READY")
        self.assertEqual(result.authority_emergence_outcome, "AUTHORITY_GRANT_CANDIDATE")
        self.assertTrue(result.authority_grant_candidate_only)
        self.assertFalse(result.actual_probe_execution_authority)
        self.assertTrue(result.execution_requires_separate_gate)
        self.assertEqual(result.authority, "none")
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.probe_execution_performed)

    def test_mass_gap_collapse_blocks_authority_emergence(self):
        ctx = dict(CTX)
        ctx["mass_gap_collapsed"] = True
        result = evaluate_qi_two_truths_authority_emergence(review_gate_packet=REVIEW, authority_context=ctx)
        self.assertEqual(result.gate_status, "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_BLOCKED")
        self.assertEqual(result.authority_emergence_outcome, "AUTHORITY_HOLD")
        self.assertIn("mass_gap_collapsed", result.authority_blockers)
        self.assertFalse(result.actual_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
