import unittest

from runtime.kuuos_runtime_daemon_qi_one_shot_probe_executor_v0_1 import run_qi_one_shot_probe_executor


GRANT = {
    "gate_status": "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY",
    "grant_outcome": "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED",
    "authorized_probe_type": "observation_debt_probe",
    "authority_scope": "single_probe_execution_candidate_review",
    "authority_token_kind": "single_use_probe_execution_authority",
    "grants_probe_execution_authority": True,
    "grants_execution_authority": True,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_scheduler_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "one_shot": True,
    "single_probe_only": True,
    "rollback_required": True,
    "reentry_window_bound": True,
    "authority_expires_after_use": True,
    "authority_revocable": True,
    "memory_write_allowed": False,
    "world_update_allowed": False,
    "control_packet_mutation_allowed": False,
    "probe_execution_performed": False,
    "dry_run_execution_performed": False,
    "next_tick_execution_performed": False,
    "scheduler_state_mutation_performed": False,
    "control_packet_mutation_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
}

PAYLOAD = {
    "probe_result_kind": "qi_probe_observation_debt_result",
    "probe_result_summary": "observation debt probe result artifact only",
    "token_already_consumed": False,
    "request_multi_probe": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_scheduler_mutation": False,
}


class QiOneShotProbeExecutorTests(unittest.TestCase):
    def test_one_shot_probe_consumes_token_and_outputs_artifact_only(self):
        result = run_qi_one_shot_probe_executor(grant_packet=GRANT, probe_payload=PAYLOAD)
        self.assertEqual(result.execution_status, "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED")
        self.assertTrue(result.probe_execution_performed)
        self.assertTrue(result.one_shot_token_consumed)
        self.assertTrue(result.probe_result_artifact_only)
        self.assertFalse(result.token_reuse_allowed)
        self.assertFalse(result.grants_probe_execution_authority)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.control_packet_mutation_performed)

    def test_consumed_token_blocks_execution(self):
        payload = dict(PAYLOAD)
        payload["token_already_consumed"] = True
        result = run_qi_one_shot_probe_executor(grant_packet=GRANT, probe_payload=payload)
        self.assertEqual(result.execution_status, "QI_ONE_SHOT_PROBE_EXECUTION_BLOCKED")
        self.assertIn("token_already_consumed", result.execution_blockers)
        self.assertFalse(result.probe_execution_performed)

    def test_memory_write_request_blocks_execution(self):
        payload = dict(PAYLOAD)
        payload["request_memory_write"] = True
        result = run_qi_one_shot_probe_executor(grant_packet=GRANT, probe_payload=payload)
        self.assertEqual(result.execution_status, "QI_ONE_SHOT_PROBE_EXECUTION_BLOCKED")
        self.assertIn("request_memory_write", result.execution_blockers)
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)


if __name__ == "__main__":
    unittest.main()
