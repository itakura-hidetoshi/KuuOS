import unittest

from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1 import build_qi_memoryos_process_tensor_retrieval_replay


ENTRY = {
    "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
    "source_probe_type": "observation_debt_probe",
    "append_only": True,
    "memory_append_performed": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "lineage_preserved": True,
}

CTX = {
    "request_memory_write": False,
    "request_memory_overwrite": False,
    "request_world_update": False,
    "request_scheduler_mutation": False,
    "request_probe_execution": False,
}


class QiMemoryOSProcessTensorRetrievalReplayTests(unittest.TestCase):
    def test_replay_surface_is_read_only_and_reuses_nonmarkov_history(self):
        result = build_qi_memoryos_process_tensor_retrieval_replay(
            memory_entries=[ENTRY],
            replay_context=CTX,
        )
        self.assertEqual(result.replay_status, "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY")
        self.assertEqual(result.dominant_probe_type, "observation_debt_probe")
        self.assertTrue(result.retrieval_only)
        self.assertTrue(result.replay_surface_only)
        self.assertTrue(result.memory_read_performed)
        self.assertTrue(result.nonmarkov_trace_available)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)
        self.assertFalse(result.scheduler_state_mutation_performed)
        self.assertFalse(result.grants_probe_execution_authority)

    def test_world_update_request_blocks_replay_surface(self):
        ctx = dict(CTX)
        ctx["request_world_update"] = True
        result = build_qi_memoryos_process_tensor_retrieval_replay(
            memory_entries=[ENTRY],
            replay_context=ctx,
        )
        self.assertEqual(result.replay_status, "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_BLOCKED")
        self.assertIn("request_world_update", result.replay_blockers)
        self.assertFalse(result.world_update_performed)


if __name__ == "__main__":
    unittest.main()
