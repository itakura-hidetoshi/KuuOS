#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_probe_execution_candidate_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        scheduler = root / "scheduler.json"
        out = root / "candidate.json"
        dump(scheduler, {
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
        })
        completed = subprocess.run([
            sys.executable, str(CLI), "--scheduler", str(scheduler), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("candidate_output_missing")
        else:
            value = load(out)
            if value.get("candidate_status") != "QI_PROBE_EXECUTION_CANDIDATE_READY":
                errors.append("candidate_status_mismatch")
            if value.get("execution_candidate_only") is not True:
                errors.append("execution_candidate_only_not_true")
            if value.get("scheduler_due_required") is not True:
                errors.append("scheduler_due_required_not_true")
            if value.get("scheduler_due_satisfied") is not True:
                errors.append("scheduler_due_satisfied_not_true")
            if value.get("requires_operator_review") is not True:
                errors.append("requires_operator_review_not_true")
            if value.get("requires_governor_approval") is not True:
                errors.append("requires_governor_approval_not_true")
            if value.get("authority") != "none":
                errors.append("authority_not_none")
            for key in [
                "scheduler_state_mutation_performed",
                "control_packet_mutation_performed",
                "probe_execution_performed",
                "dry_run_execution_performed",
                "next_tick_execution_performed",
                "memory_write_performed",
                "world_update_performed",
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_dry_run_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_scheduler_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        dump(scheduler, {
            "adjustment_status": "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED",
            "authority": "scheduler_state",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_dry_run_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_world_update_authority": False,
            "scheduler_result": {
                "scheduler_status": "QI_SCHEDULER_STATE_UPDATED",
                "due_status": "WAIT",
                "scheduled_probe_type": "observation_debt_probe",
                "grants_execution_authority": False,
                "grants_probe_execution_authority": False,
                "grants_dry_run_execution_authority": False,
                "grants_next_tick_execution_authority": False,
                "grants_control_packet_authority": False,
                "grants_memory_overwrite_authority": False,
                "grants_world_update_authority": False,
            },
        })
        completed = subprocess.run([
            sys.executable, str(CLI), "--scheduler", str(scheduler), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("candidate_status") != "QI_PROBE_EXECUTION_CANDIDATE_BLOCKED":
                errors.append("blocked_candidate_status_mismatch")
            if "scheduler_due_status_not_due" not in value.get("candidate_blockers", []):
                errors.append("blocked_due_blocker_missing")
            if value.get("grants_probe_execution_authority") is not False:
                errors.append("blocked_probe_authority_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi probe execution candidate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
