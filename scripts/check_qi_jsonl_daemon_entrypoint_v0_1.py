#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "scripts" / "qi_jsonl_daemon_entrypoint_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: pathlib.Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


MEMORY = {"entries": [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]}
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["deployment"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}


def main() -> int:
    errors: list[str] = []
    if not ENTRYPOINT.is_file():
        errors.append(f"missing:{ENTRYPOINT}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        state_dir = root / ".state" / "qi-jsonl"
        input_dir = root / ".state" / "qi-input"
        config = root / "daemon_config.json"
        dump(input_dir / "memory.json", MEMORY)
        dump(input_dir / "scheduler_state.json", STATE)
        dump(input_dir / "scheduler_proposal.json", PROPOSAL)
        dump(input_dir / "process_tensor_metrics.json", METRICS)
        dump(config, {
            "base_dir": str(root),
            "state_dir": ".state/qi-jsonl",
            "input_dir": ".state/qi-input",
            "desired_start_tick": 1,
            "desired_tick_count": 2,
            "max_tick_count": 2,
            "tick_id_prefix": "deploy"
        })
        first = subprocess.run([sys.executable, str(ENTRYPOINT), "--config", str(config), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if first.returncode != 0:
            errors.append("first_entrypoint_failed")
            errors.append(first.stdout.strip() or first.stderr.strip())
        status = state_dir / "daemon_status.json"
        event_log = state_dir / "event_log.jsonl"
        ledger = state_dir / "ledger_state.json"
        if not status.is_file() or not event_log.is_file() or not ledger.is_file():
            errors.append("deployment_outputs_missing")
        else:
            value = load(status)
            if value.get("resume_status") != "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED":
                errors.append("first_status_mismatch")
            if value.get("safe_resume_performed") is not True:
                errors.append("first_safe_resume_not_true")
            if value.get("resume_tick_count") != 2:
                errors.append("first_resume_tick_count_mismatch")
            if len(read_jsonl(event_log)) != 2:
                errors.append("first_event_lines_mismatch")
            if load(ledger).get("replay_cursor", {}).get("position") != 2:
                errors.append("first_cursor_mismatch")
        second = subprocess.run([sys.executable, str(ENTRYPOINT), "--config", str(config), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if second.returncode != 0:
            errors.append("second_entrypoint_failed")
            errors.append(second.stdout.strip() or second.stderr.strip())
        if status.is_file():
            value = load(status)
            if value.get("no_op_resume") is not True:
                errors.append("second_no_op_not_true")
            if value.get("jsonl_event_lines_appended") != 0:
                errors.append("second_appended_not_zero")
        if event_log.is_file() and len(read_jsonl(event_log)) != 2:
            errors.append("second_event_lines_changed")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi JSONL daemon entrypoint check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
