#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_replay_scheduler_state_apply_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


REPLAY = {
    "replay_status": "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY",
    "retrieval_only": True,
    "replay_surface_only": True,
    "memory_read_performed": True,
    "dominant_probe_type": "observation_debt_probe",
    "scheduler_reuse_hint": "reuse_nonmarkov_history_for_observation_debt_probe",
    "probe_planner_reuse_hint": "prioritize_probe_family_observation_debt_probe",
    "memory_write_performed": False,
    "memory_append_performed": False,
    "memory_overwrite_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "scheduler_state_mutation_performed": False,
    "grants_memory_write_authority": False,
    "grants_world_update_authority": False,
    "grants_probe_execution_authority": False,
}

STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["base"]}
CTX = {
    "allow_scheduler_state_update": True,
    "scheduler_update_scope": "replay_hint_only",
    "scheduler_lineage_preserved": True,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        replay = root / "replay.json"
        state = root / "state.json"
        ctx = root / "ctx.json"
        out = root / "apply.json"
        out_state = root / "next_state.json"
        dump(replay, REPLAY)
        dump(state, STATE)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--replay", str(replay), "--scheduler-state", str(state), "--context", str(ctx), "--write", str(out), "--write-state", str(out_state), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file() or not out_state.is_file():
            errors.append("apply_output_missing")
        else:
            value = load(out)
            next_state = load(out_state)
            if value.get("apply_status") != "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED":
                errors.append("apply_status_mismatch")
            if value.get("scheduler_state_mutation_performed") is not True:
                errors.append("scheduler_state_mutation_not_true")
            if value.get("scheduler_update_scope") != "replay_hint_only":
                errors.append("scheduler_update_scope_mismatch")
            if next_state.get("scheduler_update_kind") != "memoryos_process_tensor_replay_hint":
                errors.append("next_state_update_kind_mismatch")
            if next_state.get("replay_dominant_probe_type") != "observation_debt_probe":
                errors.append("next_state_probe_type_mismatch")
            for key in [
                "memory_write_performed",
                "memory_append_performed",
                "world_update_performed",
                "control_packet_mutation_performed",
                "probe_execution_performed",
                "grants_memory_write_authority",
                "grants_world_update_authority",
                "grants_probe_execution_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["request_world_update"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--replay", str(replay), "--scheduler-state", str(state), "--context", str(ctx), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("apply_status") != "QI_REPLAY_SCHEDULER_STATE_APPLY_BLOCKED":
                errors.append("blocked_apply_status_mismatch")
            if "request_world_update" not in value.get("apply_blockers", []):
                errors.append("world_update_blocker_missing")
            if value.get("scheduler_state_mutation_performed") is not False:
                errors.append("blocked_scheduler_mutation_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi replay scheduler state apply check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
