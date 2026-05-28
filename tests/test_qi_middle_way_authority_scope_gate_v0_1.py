import unittest

from runtime.kuuos_runtime_daemon_qi_middle_way_authority_scope_gate_v0_1 import evaluate_qi_middle_way_authority_scope


AUTHORITY = {
    "gate_status": "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_READY",
    "authority_emergence_outcome": "AUTHORITY_GRANT_CANDIDATE",
    "authority_grant_candidate_only": True,
    "execution_requires_separate_gate": True,
    "local_limited_revocable": True,
    "authority": "none",
    "reviewed_probe_type": "observation_debt_probe",
    "conventional_authority_scope": "single_probe_execution_candidate_review",
    "actual_probe_execution_authority": False,
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
    "authority_scope": "single_probe_execution_candidate_review",
    "authority_not_reified": True,
    "authority_not_denied_when_conditions_hold": True,
    "avoids_eternalism": True,
    "avoids_nihilism": True,
    "conditioned_local_authority_only": True,
    "ultimate_non_reification_preserved": True,
    "dependent_origination_trace_present": True,
    "two_truths_boundary_preserved": True,
    "local_limited_revocable": True,
    "mass_gap_barrier_preserved": True,
    "no_direct_execution_collapse": True,
    "eternalist_authority_claim": False,
    "nihilist_authority_denial": False,
    "authority_scope_unbounded": False,
    "authority_irrevocable": False,
    "direct_execution_requested": False,
}


class QiMiddleWayAuthorityScopeGateTests(unittest.TestCase):
    def test_ready_scope_is_candidate_only(self):
        result = evaluate_qi_middle_way_authority_scope(authority_emergence_packet=AUTHORITY, scope_context=CTX)
        self.assertEqual(result.gate_status, "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_READY")
        self.assertEqual(result.middle_way_scope_outcome, "MIDDLE_WAY_AUTHORITY_SCOPE_READY")
        self.assertTrue(result.middle_way_scope_only)
        self.assertTrue(result.authority_scope_candidate_only)
        self.assertFalse(result.actual_probe_execution_authority)
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.probe_execution_performed)

    def test_eternalist_claim_blocks_scope(self):
        ctx = dict(CTX)
        ctx["eternalist_authority_claim"] = True
        result = evaluate_qi_middle_way_authority_scope(authority_emergence_packet=AUTHORITY, scope_context=ctx)
        self.assertEqual(result.gate_status, "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_BLOCKED")
        self.assertIn("eternalist_authority_claim", result.scope_blockers)
        self.assertFalse(result.actual_probe_execution_authority)

    def test_nihilist_denial_blocks_scope(self):
        ctx = dict(CTX)
        ctx["nihilist_authority_denial"] = True
        result = evaluate_qi_middle_way_authority_scope(authority_emergence_packet=AUTHORITY, scope_context=ctx)
        self.assertEqual(result.gate_status, "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_BLOCKED")
        self.assertIn("nihilist_authority_denial", result.scope_blockers)
        self.assertFalse(result.actual_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
