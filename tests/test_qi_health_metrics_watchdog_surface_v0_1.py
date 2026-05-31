import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_health_metrics_watchdog_surface_v0_1 import build_qi_health_metrics_watchdog_surface


STATUS = {
    "resume_status": "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED",
    "heartbeat_count": 2,
    "safe_resume_performed": True,
    "no_op_resume": False,
    "idempotency_enforced": True,
    "duplicate_tick_blocked": True,
    "token_ledger_checked": True,
    "probe_execution_performed": False,
    "world_update_performed": False,
    "memory_overwrite_performed": False,
    "control_packet_mutation_performed": False,
    "wrapper_packet": {
        "tick_packets": [
            {
                "process_tensor_pressure": "high",
                "dominant_probe_type": "observation_debt_probe"
            }
        ]
    }
}
LEDGER = {
    "replay_cursor": {"stream": "memoryos/qi_process_tensor/append_only", "position": 2},
    "token_ledger": {"consumed_token_ids": ["tok-health-1", "tok-health-2"]}
}
EVENTS = [
    {"event_id": "evt-health-1", "tick_id": "health-1"},
    {"event_id": "evt-health-2", "tick_id": "health-2"}
]
CTX = {"read_only_required": True, "watchdog_enabled": True, "min_heartbeat_count": 1, "request_probe_execution": False, "request_world_update": False, "request_memory_write": False, "request_control_packet_mutation": False}


class QiHealthMetricsWatchdogSurfaceTests(unittest.TestCase):
    def test_health_metrics_watchdog_surface_reads_existing_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status = root / "daemon_status.json"
            event_log = root / "event_log.jsonl"
            ledger = root / "ledger_state.json"
            status.write_text(json.dumps(STATUS) + "\n", encoding="utf-8")
            ledger.write_text(json.dumps(LEDGER) + "\n", encoding="utf-8")
            event_log.write_text("\n".join(json.dumps(row) for row in EVENTS) + "\n", encoding="utf-8")
            result = build_qi_health_metrics_watchdog_surface(
                daemon_status_path=status,
                event_log_path=event_log,
                ledger_state_path=ledger,
                watchdog_context=CTX,
            )
            self.assertEqual(result.health_status, "QI_HEALTH_METRICS_WATCHDOG_HEALTHY")
            self.assertEqual(result.watchdog_status, "QI_WATCHDOG_OK")
            self.assertEqual(result.heartbeat_count, 2)
            self.assertEqual(result.jsonl_event_line_count, 2)
            self.assertEqual(result.replay_cursor_position, 2)
            self.assertEqual(result.token_ledger_count, 2)
            self.assertEqual(result.process_tensor_pressure, "high")
            self.assertIn("process_tensor_pressure_high", result.surface_warnings)
            self.assertIn("kuos_qi_daemon_health_ok", result.prometheus_text)
            self.assertFalse(result.probe_execution_performed)
            self.assertFalse(result.world_update_performed)
            self.assertFalse(result.memory_overwrite_performed)

    def test_low_heartbeat_marks_watchdog_attention(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status = root / "daemon_status.json"
            event_log = root / "event_log.jsonl"
            ledger = root / "ledger_state.json"
            status.write_text(json.dumps({**STATUS, "heartbeat_count": 0}) + "\n", encoding="utf-8")
            ledger.write_text(json.dumps(LEDGER) + "\n", encoding="utf-8")
            event_log.write_text("\n".join(json.dumps(row) for row in EVENTS) + "\n", encoding="utf-8")
            result = build_qi_health_metrics_watchdog_surface(
                daemon_status_path=status,
                event_log_path=event_log,
                ledger_state_path=ledger,
                watchdog_context=CTX,
            )
            self.assertEqual(result.health_status, "QI_HEALTH_METRICS_WATCHDOG_HEALTHY")
            self.assertEqual(result.watchdog_status, "QI_WATCHDOG_ATTENTION_REQUIRED")
            self.assertIn("heartbeat_count_below_threshold", result.surface_warnings)


if __name__ == "__main__":
    unittest.main()
