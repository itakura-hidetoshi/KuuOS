import unittest

from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_append_writeback_v0_1 import run_qi_memoryos_process_tensor_append_writeback


PROBE = {
    "execution_status": "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED",
    "probe_type": "observation_debt_probe",
    "probe_result_summary": "artifact only",
    "probe_execution_performed": True,
    "probe_result_artifact_only": True,
    "one_shot_token_consumed": True,
    "token_reuse_allowed": False,
    "grants_probe_execution_authority": False,
    "grants_execution_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "grants_control_packet_authority": False,
    "grants_scheduler_authority": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "scheduler_state_mutation_performed": False,
}

CTX = {
    "append_only_required": True,
    "lineage_preserved": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "no_memory_overwrite": True,
    "no_world_update": True,
    "no_control_packet_mutation": True,
    "request_memory_overwrite": False,
    "request_memory_delete": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_scheduler_mutation": False,
}


class QiMemoryOSAppendWritebackTests(unittest.TestCase):
    def test_append_writeback(self):
        r = run_qi_memoryos_process_tensor_append_writeback(probe_result=PROBE, writeback_context=CTX)
        self.assertEqual(r.writeback_status, "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED")
        self.assertTrue(r.memory_append_performed)
        self.assertTrue(r.memory_write_performed)
        self.assertTrue(r.nonmarkov_trace_preserved)
        self.assertFalse(r.memory_overwrite_performed)
        self.assertFalse(r.world_update_performed)

    def test_overwrite_blocks(self):
        ctx = dict(CTX)
        ctx["request_memory_overwrite"] = True
        r = run_qi_memoryos_process_tensor_append_writeback(probe_result=PROBE, writeback_context=ctx)
        self.assertEqual(r.writeback_status, "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_BLOCKED")
        self.assertIn("request_memory_overwrite", r.writeback_blockers)
        self.assertFalse(r.memory_append_performed)


if __name__ == "__main__":
    unittest.main()
