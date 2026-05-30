import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_jsonl_persistent_daemon_wrapper_v0_1 import run_qi_jsonl_persistent_daemon_wrapper
from runtime.kuuos_runtime_daemon_qi_jsonl_safe_resume_controller_v0_1 import run_qi_jsonl_safe_resume_controller


MEMORY = [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["safe_resume"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}
WRAP_CTX = {"allow_repeated_bounded_ticks": True, "jsonl_backend_required": True, "max_tick_count": 5, "tick_id_prefix": "wrap", "request_probe_execution": False, "request_memory_write": False, "request_world_update": False, "request_control_packet_mutation": False}
RESUME_CTX = {"allow_safe_resume": True, "jsonl_backend_required": True, "skip_processed_ticks": True, "max_tick_count": 5, "tick_id_prefix": "wrap", "request_probe_execution": False, "request_memory_write": False, "request_world_update": False, "request_control_packet_mutation": False}


class QiJsonlSafeResumeControllerTests(unittest.TestCase):
    def test_resume_skips_processed_ticks_and_runs_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "event_log.jsonl"
            ledger_state = root / "ledger_state.json"
            seed = run_qi_jsonl_persistent_daemon_wrapper(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                start_tick=1,
                tick_count=2,
                wrapper_context=WRAP_CTX,
            )
            self.assertEqual(seed.wrapper_status, "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED")
            result = run_qi_jsonl_safe_resume_controller(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                desired_start_tick=1,
                desired_tick_count=4,
                resume_context=RESUME_CTX,
            )
            self.assertEqual(result.resume_status, "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED")
            self.assertEqual(result.skipped_processed_tick_count, 2)
            self.assertEqual(result.resume_start_tick, 3)
            self.assertEqual(result.resume_tick_count, 2)
            self.assertEqual(result.heartbeat_count, 2)
            self.assertEqual(result.jsonl_event_lines_appended, 2)
            self.assertEqual(result.replay_cursor_after, 4)
            self.assertFalse(result.probe_execution_performed)
            self.assertFalse(result.world_update_performed)

    def test_noop_resume_when_all_ticks_processed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "event_log.jsonl"
            ledger_state = root / "ledger_state.json"
            seed = run_qi_jsonl_persistent_daemon_wrapper(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                start_tick=1,
                tick_count=2,
                wrapper_context=WRAP_CTX,
            )
            self.assertEqual(seed.wrapper_status, "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED")
            result = run_qi_jsonl_safe_resume_controller(
                memory_entries=MEMORY,
                scheduler_state=STATE,
                scheduler_proposal=PROPOSAL,
                process_tensor_metrics=METRICS,
                event_log_path=event_log,
                ledger_state_path=ledger_state,
                desired_start_tick=1,
                desired_tick_count=2,
                resume_context=RESUME_CTX,
            )
            self.assertEqual(result.resume_status, "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED")
            self.assertTrue(result.no_op_resume)
            self.assertEqual(result.resume_tick_count, 0)
            self.assertEqual(result.jsonl_event_lines_appended, 0)


if __name__ == "__main__":
    unittest.main()
