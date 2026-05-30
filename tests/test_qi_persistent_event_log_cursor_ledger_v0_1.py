import unittest

from runtime.kuuos_runtime_daemon_qi_persistent_event_log_cursor_ledger_v0_1 import update_qi_persistent_event_log_cursor_ledger


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
PRIOR = {"event_log": [], "replay_cursor": {"stream": "memoryos/qi_process_tensor/append_only", "position": 0}, "token_ledger": {"consumed_token_ids": []}}
CTX = {"event_id": "evt-001", "idempotency_key": "idem-001", "append_only_required": True, "idempotency_required": True, "replay_cursor_required": True, "token_ledger_required": True, "replay_cursor_advance_by": 1}
TOKEN = {"token_event_kind": "one_shot_token_consumed", "token_id": "tok-001"}


class QiPersistentEventLogCursorLedgerTests(unittest.TestCase):
    def test_ledger_appends_event_advances_cursor_and_records_token(self):
        result = update_qi_persistent_event_log_cursor_ledger(tick_packet=TICK, prior_ledger=PRIOR, ledger_context=CTX, token_event=TOKEN)
        self.assertEqual(result.ledger_status, "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_UPDATED")
        self.assertTrue(result.event_append_performed)
        self.assertEqual(result.event_log_size_after, 1)
        self.assertEqual(result.replay_cursor_after, 1)
        self.assertTrue(result.replay_cursor_monotone)
        self.assertTrue(result.token_consumption_recorded)
        self.assertIn("tok-001", result.next_ledger["token_ledger"]["consumed_token_ids"])
        self.assertFalse(result.probe_execution_performed)
        self.assertFalse(result.memory_write_performed)
        self.assertFalse(result.world_update_performed)

    def test_double_token_consumption_blocks(self):
        prior = {"event_log": [], "replay_cursor": {"position": 0}, "token_ledger": {"consumed_token_ids": ["tok-001"]}}
        result = update_qi_persistent_event_log_cursor_ledger(tick_packet=TICK, prior_ledger=prior, ledger_context=CTX, token_event=TOKEN)
        self.assertEqual(result.ledger_status, "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_BLOCKED")
        self.assertIn("token_already_consumed", result.ledger_blockers)
        self.assertTrue(result.token_double_consume_blocked)

    def test_duplicate_idempotency_key_blocks(self):
        prior = {"event_log": [{"event_id": "evt-old", "idempotency_key": "idem-001"}], "replay_cursor": {"position": 0}, "token_ledger": {"consumed_token_ids": []}}
        result = update_qi_persistent_event_log_cursor_ledger(tick_packet=TICK, prior_ledger=prior, ledger_context=CTX, token_event=None)
        self.assertEqual(result.ledger_status, "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_BLOCKED")
        self.assertIn("idempotency_key_already_seen", result.ledger_blockers)


if __name__ == "__main__":
    unittest.main()
