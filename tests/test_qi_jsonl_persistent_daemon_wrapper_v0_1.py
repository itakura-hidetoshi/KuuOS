import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_jsonl_persistent_daemon_wrapper_v0_1 import run_qi_jsonl_persistent_daemon_wrapper


MEMORY = [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["jsonl_wrapper"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}
CTX = {"allow_repeated_bounded_ticks": True, "jsonl_backend_required": True, "max_tick_count": 3, "tick_id_prefix": "wrap", "request_probe_execution": False, "request_memory_write": False, "request_world_update": False, "request_control_packet_mutation": False}


class QiJsonlPersistentDaemonWrapperTests(unittest.TestCase):
    def test_repeated_ticks_append_to_jsonl_and_advance_cursor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "event_log.jsonl"
            ledger_state = root / "ledger_state.json"
            result = run_qi_jsonl_persistent_daemon_wrapper(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                start_tick=1,
                tick_count=2,
                wrapper_context=CTX,
            )
            self.assertEqual(result.wrapper_status, "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED")
            self.assertEqual(result.completed_tick_count, 2)
            self.assertEqual(result.heartbeat_count, 2)
            self.assertEqual(len(event_log.read_text(encoding="utf-8").splitlines()), 2)
            state = json.loads(ledger_state.read_text(encoding="utf-8"))
            self.assertEqual(state["replay_cursor"]["position"], 2)
            self.assertIn("tok-wrap-1", state["token_ledger"]["consumed_token_ids"])
            self.assertIn("tok-wrap-2", state["token_ledger"]["consumed_token_ids"])
            self.assertFalse(result.probe_execution_performed)
            self.assertFalse(result.world_update_performed)
            self.assertFalse(result.memory_overwrite_performed)

    def test_duplicate_tick_blocks_second_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "event_log.jsonl"
            ledger_state = root / "ledger_state.json"
            first = run_qi_jsonl_persistent_daemon_wrapper(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                start_tick=1,
                tick_count=1,
                wrapper_context=CTX,
            )
            self.assertEqual(first.wrapper_status, "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED")
            second = run_qi_jsonl_persistent_daemon_wrapper(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                start_tick=1,
                tick_count=1,
                wrapper_context=CTX,
            )
            self.assertEqual(second.wrapper_status, "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_BLOCKED")
            self.assertEqual(second.completed_tick_count, 0)
            self.assertEqual(len(event_log.read_text(encoding="utf-8").splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
