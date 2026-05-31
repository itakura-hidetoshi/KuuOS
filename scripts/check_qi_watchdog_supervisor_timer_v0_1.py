#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "scripts" / "qi_jsonl_daemon_entrypoint_v0_1.py"
SUPERVISOR = ROOT / "scripts" / "run_qi_watchdog_supervisor_timer_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


MEMORY = {"entries": [{"writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED", "source_probe_type": "observation_debt_probe", "append_only": True, "memory_append_performed": True, "process_tensor_trace_preserved": True, "nonmarkov_trace_preserved": True, "observation_debt_trace_preserved": True, "recoverability_trace_preserved": True, "safe_reentry_trace_preserved": True, "lineage_preserved": True}]}
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["watchdog-supervisor"]}
PROPOSAL = {"scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY", "recommended_schedule_mode": "routine_revisit", "recommended_revisit_after_ticks": 5, "recommended_revisit_reason": "base routine", "source_recommended_probe_type": "continue_process_tensor_supervision_probe", "schedule_proposal_only": True, "authority": "none", "grants_execution_authority": False, "grants_probe_execution_authority": False, "grants_dry_run_execution_authority": False, "grants_next_tick_execution_authority": False, "grants_control_packet_authority": False, "grants_memory_overwrite_authority": False, "grants_world_update_authority": False}
METRICS = {"process_tensor_advantage_level": "moderate", "observation_debt_resolution_priority": 0.9, "safe_reentry_window_score": 0.5, "nonmarkov_link_density": 0.6, "memory_kernel_preservation_score": 0.8, "history_depth": 7}
SUPERVISOR_CTX = {"read_only_required": True, "timer_only": True, "max_allowed_iterations": 3, "min_heartbeat_count": 1, "request_daemon_restart": False, "request_daemon_stop": False, "request_daemon_resume": False, "request_probe_execution": False, "request_world_update": False, "request_memory_write": False, "request_control_packet_mutation": False}


def main() -> int:
    errors: list[str] = []
    if not ENTRYPOINT.is_file() or not SUPERVISOR.is_file():
        errors.append("required_entrypoint_or_supervisor_missing")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        state_dir = root / ".state" / "qi-jsonl"
        input_dir = root / ".state" / "qi-input"
        config = root / "daemon_config.json"
        dump(input_dir / "memory.json", MEMORY)
        dump(input_dir / "scheduler_state.json", STATE)
        dump(input_dir / "scheduler_proposal.json", PROPOSAL)
        dump(input_dir / "process_tensor_metrics.json", METRICS)
        dump(config, {"base_dir": str(root), "state_dir": ".state/qi-jsonl", "input_dir": ".state/qi-input", "desired_start_tick": 1, "desired_tick_count": 2, "max_tick_count": 2, "tick_id_prefix": "watchdog"})
        completed = subprocess.run([sys.executable, str(ENTRYPOINT), "--config", str(config), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("entrypoint_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())

        context = root / "supervisor_context.json"
        report = root / "watchdog_report.json"
        prom = root / "watchdog_metrics.prom"
        dump(context, SUPERVISOR_CTX)
        completed = subprocess.run([
            sys.executable,
            str(SUPERVISOR),
            "--daemon-status", str(state_dir / "daemon_status.json"),
            "--event-log", str(state_dir / "event_log.jsonl"),
            "--ledger-state", str(state_dir / "ledger_state.json"),
            "--context", str(context),
            "--max-iterations", "2",
            "--write", str(report),
            "--write-prometheus", str(prom),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("supervisor_unexpected_nonzero")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not report.is_file() or not prom.is_file():
            errors.append("supervisor_outputs_missing")
        else:
            value = load(report)
            prom_text = prom.read_text(encoding="utf-8")
            if value.get("supervisor_status") != "QI_WATCHDOG_SUPERVISOR_OK":
                errors.append("supervisor_status_mismatch")
            if value.get("timer_status") != "QI_WATCHDOG_TIMER_COMPLETED":
                errors.append("timer_status_mismatch")
            if value.get("iteration_count") != 2:
                errors.append("iteration_count_mismatch")
            if value.get("watchdog_exit_code") != 0:
                errors.append("exit_code_mismatch")
            if value.get("daemon_restart_performed") is not False:
                errors.append("daemon_restart_not_false")
            if value.get("daemon_control_performed") is not False:
                errors.append("daemon_control_not_false")
            if value.get("memory_write_performed") is not False:
                errors.append("memory_write_not_false")
            if len(value.get("health_packets", [])) != 2:
                errors.append("health_packet_count_mismatch")
            if "kuos_qi_watchdog_supervisor_iterations" not in prom_text:
                errors.append("prom_supervisor_iterations_missing")

        blocked_context = root / "blocked_supervisor_context.json"
        blocked_report = root / "blocked_watchdog_report.json"
        dump(blocked_context, {**SUPERVISOR_CTX, "request_daemon_restart": True})
        blocked = subprocess.run([
            sys.executable,
            str(SUPERVISOR),
            "--daemon-status", str(state_dir / "daemon_status.json"),
            "--event-log", str(state_dir / "event_log.jsonl"),
            "--ledger-state", str(state_dir / "ledger_state.json"),
            "--context", str(blocked_context),
            "--write", str(blocked_report),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if blocked.returncode != 2:
            errors.append("blocked_supervisor_exit_code_mismatch")
        if blocked_report.is_file():
            value = load(blocked_report)
            if value.get("daemon_restart_performed") is not False:
                errors.append("blocked_daemon_restart_not_false")
            if "request_daemon_restart" not in value.get("supervisor_blockers", []):
                errors.append("blocked_restart_blocker_missing")
        else:
            errors.append("blocked_report_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi watchdog supervisor timer check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
