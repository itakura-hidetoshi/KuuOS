#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_jsonl_safe_resume_controller_v0_1.py"
WRAPPER = ROOT / "scripts" / "write_qi_jsonl_persistent_daemon_wrapper_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: pathlib.Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


MEMORY = {"entries": [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]}
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["safe_resume"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}
WRAP_CTX = {"allow_repeated_bounded_ticks": True, "jsonl_backend_required": True, "max_tick_count": 5, "tick_id_prefix": "wrap", "request_probe_execution": False, "request_memory_write": False, "request_world_update": False, "request_control_packet_mutation": False}
RESUME_CTX = {"allow_safe_resume": True, "jsonl_backend_required": True, "skip_processed_ticks": True, "max_tick_count": 5, "tick_id_prefix": "wrap", "request_probe_execution": False, "request_memory_write": False, "request_world_update": False, "request_control_packet_mutation": False}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file() or not WRAPPER.is_file():
        errors.append("required_cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        memory = root / "memory.json"
        state = root / "state.json"
        proposal = root / "proposal.json"
        metrics = root / "metrics.json"
        wrap_ctx = root / "wrap_ctx.json"
        resume_ctx = root / "resume_ctx.json"
        event_log = root / "event_log.jsonl"
        ledger_state = root / "ledger_state.json"
        seed = root / "seed.json"
        out = root / "resume.json"
        noop = root / "noop.json"
        dump(memory, MEMORY)
        dump(state, STATE)
        dump(proposal, PROPOSAL)
        dump(metrics, METRICS)
        dump(wrap_ctx, WRAP_CTX)
        dump(resume_ctx, RESUME_CTX)

        completed = subprocess.run([
            sys.executable, str(WRAPPER), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(wrap_ctx), "--start-tick", "1", "--tick-count", "2", "--write", str(seed), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("seed_wrapper_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())

        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(resume_ctx), "--desired-start-tick", "1", "--desired-tick-count", "4", "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("resume_cli_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if out.is_file():
            value = load(out)
            if value.get("resume_status") != "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED":
                errors.append("resume_status_mismatch")
            if value.get("skipped_processed_tick_count") != 2:
                errors.append("skipped_processed_tick_count_mismatch")
            if value.get("resume_start_tick") != 3:
                errors.append("resume_start_tick_mismatch")
            if value.get("resume_tick_count") != 2:
                errors.append("resume_tick_count_mismatch")
            if value.get("heartbeat_count") != 2:
                errors.append("heartbeat_count_mismatch")
            if value.get("jsonl_event_lines_appended") != 2:
                errors.append("jsonl_event_lines_appended_mismatch")
            if value.get("replay_cursor_after") != 4:
                errors.append("replay_cursor_after_mismatch")
            if value.get("probe_execution_performed") is not False:
                errors.append("probe_execution_not_false")
        else:
            errors.append("resume_output_missing")
        if event_log.is_file() and len(read_jsonl(event_log)) != 4:
            errors.append("event_log_line_count_not_4")

        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(resume_ctx), "--desired-start-tick", "1", "--desired-tick-count", "4", "--write", str(noop), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("noop_resume_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if noop.is_file():
            value = load(noop)
            if value.get("no_op_resume") is not True:
                errors.append("noop_not_true")
            if value.get("resume_tick_count") != 0:
                errors.append("noop_resume_tick_count_not_zero")
            if value.get("jsonl_event_lines_appended") != 0:
                errors.append("noop_appended_not_zero")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi JSONL safe resume controller check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
