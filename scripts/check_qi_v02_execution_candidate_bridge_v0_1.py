#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_v02_execution_candidate_bridge_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


V02 = {
    "adjustment_status": "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED",
    "replay_reuse_integrated": True,
    "scheduler_state_updated": True,
    "scheduler_authority_scope": "scheduler_state_only",
    "authority": "scheduler_state",
    "grants_scheduler_authority": True,
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "base_result": {
        "adjustment_status": "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED",
        "process_tensor_aware": True,
        "authority": "scheduler_state",
        "grants_scheduler_authority": True,
        "grants_execution_authority": False,
        "grants_probe_execution_authority": False,
        "grants_dry_run_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_control_packet_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_world_update_authority": False,
        "scheduler_result": {
            "scheduler_status": "QI_SCHEDULER_STATE_UPDATED",
            "due_status": "DUE",
            "scheduled_probe_type": "observation_debt_probe",
            "scheduled_mode": "near_term_revisit",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_dry_run_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_world_update_authority": False,
        },
    },
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        v02 = root / "v02.json"
        out = root / "bridge.json"
        cand = root / "candidate.json"
        dump(v02, V02)
        completed = subprocess.run([
            sys.executable, str(CLI), "--v02-scheduler", str(v02), "--write", str(out), "--write-candidate", str(cand), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file() or not cand.is_file():
            errors.append("bridge_output_missing")
        else:
            value = load(out)
            candidate = load(cand)
            if value.get("bridge_status") != "QI_V02_EXECUTION_CANDIDATE_BRIDGE_READY":
                errors.append("bridge_status_mismatch")
            if value.get("bridge_candidate_only") is not True:
                errors.append("bridge_candidate_only_not_true")
            if candidate.get("candidate_status") != "QI_PROBE_EXECUTION_CANDIDATE_READY":
                errors.append("candidate_status_mismatch")
            if candidate.get("candidate_probe_type") != "observation_debt_probe":
                errors.append("candidate_probe_type_mismatch")
            if value.get("probe_execution_performed") is not False:
                errors.append("probe_execution_performed_not_false")
            if value.get("memory_write_performed") is not False:
                errors.append("memory_write_performed_not_false")
            if value.get("world_update_performed") is not False:
                errors.append("world_update_performed_not_false")
            if value.get("grants_probe_execution_authority") is not False:
                errors.append("grants_probe_execution_authority_not_false")

        blocked = root / "blocked.json"
        bad = json.loads(json.dumps(V02))
        bad["probe_execution_performed"] = True
        dump(v02, bad)
        completed = subprocess.run([
            sys.executable, str(CLI), "--v02-scheduler", str(v02), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("bridge_status") != "QI_V02_EXECUTION_CANDIDATE_BRIDGE_BLOCKED":
                errors.append("blocked_bridge_status_mismatch")
            if "v02_probe_execution_performed_not_false" not in value.get("bridge_blockers", []):
                errors.append("probe_execution_blocker_missing")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi v0.2 execution candidate bridge check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
