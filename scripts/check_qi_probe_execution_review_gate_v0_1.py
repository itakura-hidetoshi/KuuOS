#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_probe_execution_review_gate_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    ready_candidate = {
        "candidate_status": "QI_PROBE_EXECUTION_CANDIDATE_READY",
        "candidate_probe_type": "observation_debt_probe",
        "candidate_schedule_mode": "near_term_revisit",
        "execution_candidate_only": True,
        "scheduler_due_required": True,
        "scheduler_due_satisfied": True,
        "requires_operator_review": True,
        "requires_governor_approval": True,
        "authority": "none",
        "scheduler_state_mutation_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "dry_run_execution_performed": False,
        "next_tick_execution_performed": False,
        "memory_write_performed": False,
        "world_update_performed": False,
        "grants_execution_authority": False,
        "grants_probe_execution_authority": False,
        "grants_dry_run_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_scheduler_authority": False,
        "grants_control_packet_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_world_update_authority": False,
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        candidate = root / "candidate.json"
        out = root / "gate.json"
        dump(candidate, ready_candidate)
        completed = subprocess.run([
            sys.executable, str(CLI), "--candidate", str(candidate), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("gate_output_missing")
        else:
            value = load(out)
            if value.get("gate_status") != "QI_PROBE_EXECUTION_REVIEW_GATE_READY":
                errors.append("gate_status_mismatch")
            if value.get("review_outcome") != "READY_FOR_AUTHORITY_REVIEW":
                errors.append("review_outcome_mismatch")
            if value.get("ready_for_authority_review") is not True:
                errors.append("ready_for_authority_review_not_true")
            if value.get("authority_review_required") is not True:
                errors.append("authority_review_required_not_true")
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
        bad = dict(ready_candidate)
        bad["grants_probe_execution_authority"] = True
        dump(candidate, bad)
        completed = subprocess.run([
            sys.executable, str(CLI), "--candidate", str(candidate), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("gate_status") != "QI_PROBE_EXECUTION_REVIEW_GATE_BLOCKED":
                errors.append("blocked_gate_status_mismatch")
            if "candidate_grants_probe_execution_authority_not_false" not in value.get("review_blockers", []):
                errors.append("blocked_authority_blocker_missing")
            if value.get("grants_probe_execution_authority") is not False:
                errors.append("blocked_gate_probe_authority_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi probe execution review gate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
