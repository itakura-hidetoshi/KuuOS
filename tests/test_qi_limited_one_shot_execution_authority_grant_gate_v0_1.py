import unittest

from runtime.kuuos_runtime_daemon_qi_limited_one_shot_execution_authority_grant_gate_v0_1 import evaluate_qi_limited_one_shot_execution_authority_grant


SCOPE = {
    "gate_status": "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_READY",
    "middle_way_scope_outcome": "MIDDLE_WAY_AUTHORITY_SCOPE_READY",
    "middle_way_scope_only": True,
    "authority_scope_candidate_only": True,
    "execution_requires_separate_gate": True,
    "authority": "none",
    "reviewed_probe_type": "observation_debt_probe",
    "authority_scope": "single_probe_execution_candidate_review",
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
    "operator_approved_one_shot": True,
    "governor_approved_one_shot": True,
    "single_probe_only": True,
    "rollback_path_verified": True,
    "safe_reentry_window_bound": True,
    "memory_write_forbidden": True,
    "world_update_forbidden": True,
    "control_packet_mutation_forbidden": True,
    "authority_expires_after_use": True,
    "authority_revocable": True,
    "request_multi_probe": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_persistent_authority": False,
    "rollback_unavailable": False,
}


class QiLimitedOneShotExecutionAuthorityGrantGateTests(unittest.TestCase):
    def test_ready_scope_grants_one_shot_authority_without_execution(self):
        result = evaluate_qi_limited_one_shot_execution_authority_grant(
            middle_way_scope_packet=SCOPE,
            grant_context=CTX,
        )
        self.assertEqual(result.gate_status, "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY")
        self.assertEqual(result.grant_outcome, "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED")
        self.assertTrue(result.grants_probe_execution_authority)
        self.assertTrue(result.grants_execution_authority)
        self.assertTrue(result.one_shot)
        self.assertTrue(result.rollback_required)
        self.assertTrue(result.authority_expires_after_use)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_allowed)
        self.assertFalse(result.world_update_allowed)
        self.assertFalse(result.grants_memory_overwrite_authority)
        self.assertFalse(result.grants_world_update_authority)

    def test_memory_write_request_blocks_grant(self):
        ctx = dict(CTX)
        ctx["request_memory_write"] = True
        result = evaluate_qi_limited_one_shot_execution_authority_grant(
            middle_way_scope_packet=SCOPE,
            grant_context=ctx,
        )
        self.assertEqual(result.gate_status, "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_BLOCKED")
        self.assertIn("request_memory_write", result.grant_blockers)
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.probe_execution_performed)

    def test_multi_probe_request_blocks_grant(self):
        ctx = dict(CTX)
        ctx["request_multi_probe"] = True
        result = evaluate_qi_limited_one_shot_execution_authority_grant(
            middle_way_scope_packet=SCOPE,
            grant_context=ctx,
        )
        self.assertEqual(result.gate_status, "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_BLOCKED")
        self.assertIn("request_multi_probe", result.grant_blockers)
        self.assertFalse(result.grants_probe_execution_authority)


if __name__ == "__main__":
    unittest.main()
