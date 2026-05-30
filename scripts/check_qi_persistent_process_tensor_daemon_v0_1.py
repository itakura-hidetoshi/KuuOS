#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_persistent_process_tensor_daemon_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


MEMORY = {
    "entries": [{
        "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
        "source_probe_type": "observation_debt_probe",
        "append_only": True,
        "memory_append_performed": True,
        "process_tensor_trace_preserved": True,
        "nonmarkov_trace_preserved": True,
        "observation_debt_trace_preserved": True,
        "recoverability_trace_preserved": True,
        "safe_reentry_trace_preserved": True,
        "lineage_preserved": True
    }]
}

STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["persistent_runtime"]}
PROPOSAL = {
    "scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY",
    "recommended_schedule_mode": "routine_revisit",
    "recommended_revisit_after_ticks": 5,
    "recommended_revisit_reason": "base routine",
    "source_recommended_probe_type": "continue_process_tensor_supervision_probe",
    "schedule_proposal_only": True,
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False
}
METRICS = {
    "process_tensor_advantage_level": "moderate",
    "observation_debt_resolution_priority": 0.9,
    "safe_reentry_window_score": 0.5,
    "nonmarkov_link_density": 0.6,
    "memory_kernel_preservation_score": 0.8,
    "history_depth": 7
}
CTX = {
    "tick_id": "tick-001",
    "allow_persistent_tick": True,
    "bounded_tick": True,
    "heartbeat_required": True,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False
}


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
        out = root / "tick.json"
        dump(memory, MEMORY)
        dump(state, STATE)
        dump(proposal, PROPOSAL)
        dump(metrics, METRICS)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--context", str(ctx), "--current-tick", "9", "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not out.is_file():
            errors.append("tick_output_missing")
        else:
            value = load(out)
            if value.get("daemon_status") != "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY":
                errors.append("daemon_status_mismatch")
            if value.get("heartbeat_emitted") is not True:
                errors.append("heartbeat_not_true")
            if value.get("closed_loop_tick_performed") is not True:
                errors.append("closed_loop_tick_not_true")
            if value.get("dominant_probe_type") != "observation_debt_probe":
                errors.append("dominant_probe_type_mismatch")
            if value.get("scheduler_state_mutation_performed") is not True:
                errors.append("scheduler_state_mutation_not_true")
            if value.get("scheduler_update_scope") != "replay_hint_only":
                errors.append("scheduler_update_scope_mismatch")
            if value.get("process_tensor_pressure") != "high":
                errors.append("process_tensor_pressure_mismatch")
            for key in [
                "memory_write_performed",
                "memory_append_performed",
                "memory_overwrite_performed",
                "world_update_performed",
                "control_packet_mutation_performed",
                "probe_execution_performed",
                "grants_probe_execution_authority",
                "grants_world_update_authority",
                "grants_memory_overwrite_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["request_probe_execution"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--context", str(ctx), "--current-tick", "9", "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("daemon_status") != "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_BLOCKED":
                errors.append("blocked_status_mismatch")
            if "request_probe_execution" not in value.get("daemon_blockers", []):
                errors.append("probe_execution_blocker_missing")
            if value.get("probe_execution_performed") is not False:
                errors.append("blocked_probe_execution_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent process tensor daemon check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
