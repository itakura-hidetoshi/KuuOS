import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_jsonl_ledger_backend_adapter_v0_1 import apply_qi_jsonl_ledger_backend_adapter


TICK = {
    "daemon_status": "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY",
    "tick_id": "tick-001",
    "heartbeat_emitted": True,
    "closed_loop_tick_performed": True,
    "memory_entry_count": 1,
    "process_tensor_pressure": "high",
    "dominant_probe_type": "observation_debt_probe",
    "scheduler_update_scope": "replay_hint_only",
    "memory_read_performed": True,
    "memory_write_performed": False,
    "memory_append_performed": False,
    "memory_overwrite_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "grants_probe_execution_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_overwrite_authority": False,
}
CTX = {
    "event_id": "evt-001",
    "idempotency_key": "idem-001",
    "append_only_required": True,
    "idempotency_required": True,
    "replay_cursor_required": True,
    "token_ledger_required": True,
    "replay_cursor_stream": "memoryos/qi_process_tensor/append_only",
    "replay_cursor_advance_by": 1,
    "request_memory_overwrite": False,
    "request_world_update": False,
    "request_probe_execution": False,
}
TOKEN = {"token_event_kind": "one_shot_token_consumed", "token_id": "tok-001"}


class QiJsonlLedgerBackendAdapterTests(unittest.TestCase):
    def test_jsonl_backend_appends_event_and_writes_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "event_log.jsonl"
            state = root / "ledger_state.json"
            result = apply_qi_jsonl_ledger_backend_adapter(
                tick_packet=TICK,
                event_log_path=event_log,
                ledger_state_path=state,
                ledger_context=CTX,
                token_event=TOKEN,
            )
            self.assertEqual(result.backend_status, "QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED")
            self.assertTrue(result.event_line_appended)
            self.assertTrue(result.ledger_state_written)
            self.assertTrue(event_log.is_file())
            self.assertTrue(state.is_file())
            lines = event_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0])["event_id"], "evt-001")
            sidecar = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(sidecar["replay_cursor"]["position"], 1)
            self.assertIn("tok-001", sidecar["token_ledger"]["consumed_token_ids"])
            self.assertFalse(result.probe_execution_performed)
            self.assertFalse(result.world_update_performed)
            self.assertFalse(result.memory_overwrite_performed)

    def test_duplicate_idempotency_or_token_blocks_second_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "event_log.jsonl"
            state = root / "ledger_state.json"
            first = apply_qi_jsonl_ledger_backend_adapter(
                tick_packet=TICK,
                event_log_path=event_log,
                ledger_state_path=state,
                ledger_context=CTX,
                token_event=TOKEN,
            )
            self.assertEqual(first.backend_status, "QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED")
            second = apply_qi_jsonl_ledger_backend_adapter(
                tick_packet=TICK,
                event_log_path=event_log,
                ledger_state_path=state,
                ledger_context=CTX,
                token_event=TOKEN,
            )
            self.assertEqual(second.backend_status, "QI_JSONL_LEDGER_BACKEND_ADAPTER_BLOCKED")
            blockers = second.ledger_update_packet["ledger_blockers"]
            self.assertTrue("idempotency_key_already_seen" in blockers or "token_already_consumed" in blockers)
            self.assertEqual(len(event_log.read_text(encoding="utf-8").splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
