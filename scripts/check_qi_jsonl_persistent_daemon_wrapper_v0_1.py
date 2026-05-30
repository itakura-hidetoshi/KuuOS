#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_jsonl_persistent_daemon_wrapper_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: pathlib.Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


MEMORY = {"entries": [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]}
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["jsonl_wrapper"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}
CTX = {"allow_repeated_bounded_ticks": True, "jsonl_backend_required": True, "max_tick_count": 3, "tick_id_prefix": "wrap", "request_probe_execution": False, "request_memory_write": False, "request_world_update": False, "request_control_packet_mutation": False}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        memory = root / "memory.json"
        state = root / "state.json"
        proposal = root / "proposal.json"
        metrics = root / "metrics.json"
        ctx = root / "ctx.json"
        event_log = root / "event_log.jsonl"
        ledger_state = root / "ledger_state.json"
        out = root / "wrapper.json"
        dump(memory, MEMORY)
        dump(state, STATE)
        dump(proposal, PROPOSAL)
        dump(metrics, METRICS)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(ctx), "--start-tick", "1", "--tick-count", "2", "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not out.is_file() or not event_log.is_file() or not ledger_state.is_file():
            errors.append("wrapper_outputs_missing")
        else:
            value = load(out)
            events = read_jsonl(event_log)
            state_value = load(ledger_state)
            if value.get("wrapper_status") != "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED":
                errors.append("wrapper_status_mismatch")
            if value.get("completed_tick_count") != 2:
                errors.append("completed_tick_count_mismatch")
            if value.get("heartbeat_count") != 2:
                errors.append("heartbeat_count_mismatch")
            if value.get("jsonl_event_lines_appended") != 2:
                errors.append("jsonl_event_lines_appended_mismatch")
            if len(events) != 2:
                errors.append("event_log_lines_mismatch")
            if state_value.get("replay_cursor", {}).get("position") != 2:
                errors.append("ledger_cursor_mismatch")
            consumed = state_value.get("token_ledger", {}).get("consumed_token_ids", [])
            if "tok-wrap-1" not in consumed or "tok-wrap-2" not in consumed:
                errors.append("consumed_tokens_missing")
            for key in ["memory_write_performed", "memory_append_performed", "memory_overwrite_performed", "world_update_performed", "control_packet_mutation_performed", "probe_execution_performed", "grants_probe_execution_authority"]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(ctx), "--start-tick", "1", "--tick-count", "1", "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("duplicate_tick_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("wrapper_status") != "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_BLOCKED":
                errors.append("duplicate_tick_status_mismatch")
            if value.get("completed_tick_count") != 0:
                errors.append("duplicate_completed_count_not_zero")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi JSONL persistent daemon wrapper check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
