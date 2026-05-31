#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "scripts" / "qi_jsonl_daemon_entrypoint_v0_1.py"
CLI = ROOT / "scripts" / "write_qi_health_metrics_watchdog_surface_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


MEMORY = {"entries": [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]}
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["health"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}
CTX = {"read_only_required": True, "watchdog_enabled": True, "min_heartbeat_count": 1, "request_probe_execution": False, "request_world_update": False, "request_memory_write": False}


def main() -> int:
    errors: list[str] = []
    if not ENTRYPOINT.is_file() or not CLI.is_file():
        errors.append("required_cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        state_dir = root / ".state" / "qi-jsonl"
        input_dir = root / ".state" / "qi-input"
        config = root / "daemon_config.json"
        dump(input_dir / "memory.json", MEMORY)
        dump(input_dir / "scheduler_state.json", STATE)
        dump(input_dir / "scheduler_proposal.json", PROPOSAL)
        dump(input_dir / "process_tensor_metrics.json", METRICS)
        dump(config, {"base_dir": str(root), "state_dir": ".state/qi-jsonl", "input_dir": ".state/qi-input", "desired_start_tick": 1, "desired_tick_count": 2, "max_tick_count": 2, "tick_id_prefix": "health"})
        completed = subprocess.run([sys.executable, str(ENTRYPOINT), "--config", str(config), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("entrypoint_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        context = root / "watchdog_context.json"
        health = root / "health.json"
        prom = root / "metrics.prom"
        dump(context, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--daemon-status", str(state_dir / "daemon_status.json"), "--event-log", str(state_dir / "event_log.jsonl"), "--ledger-state", str(state_dir / "ledger_state.json"), "--context", str(context), "--write", str(health), "--write-prometheus", str(prom), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("health_cli_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not health.is_file() or not prom.is_file():
            errors.append("health_outputs_missing")
        else:
            value = load(health)
            prom_text = prom.read_text(encoding="utf-8")
            if value.get("health_status") != "QI_HEALTH_METRICS_WATCHDOG_HEALTHY":
                errors.append("health_status_mismatch")
            if value.get("watchdog_status") != "QI_WATCHDOG_OK":
                errors.append("watchdog_status_mismatch")
            if value.get("heartbeat_count") != 2:
                errors.append("heartbeat_count_mismatch")
            if value.get("jsonl_event_line_count") != 2:
                errors.append("event_line_count_mismatch")
            if value.get("replay_cursor_position") != 2:
                errors.append("cursor_position_mismatch")
            if value.get("token_ledger_count") != 2:
                errors.append("token_count_mismatch")
            if value.get("memory_write_performed") is not False:
                errors.append("memory_write_not_false")
            if "kuos_qi_daemon_health_ok" not in prom_text:
                errors.append("prom_health_metric_missing")
            if "kuos_qi_process_tensor_pressure" not in prom_text:
                errors.append("prom_pressure_metric_missing")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi health metrics watchdog surface check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
