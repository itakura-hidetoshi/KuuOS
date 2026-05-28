#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_limited_one_shot_execution_authority_grant_gate_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


SCOPE = {
    "gate_status": "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_READY",
    "middle_way_scope_outcome": "MIDDLE_WAY_AUTHORITY_SCOPE_READY",
    "middle_way_scope_only": True,
    "authority_scope_candidate_only": True,
    "execution_requires_separate_gate": True,
    "authority": "none",
    "reviewed_probe_type": "observation_debt_probe",
    "authority_scope": "single_probe_execution_candidate_review",
    "actual_probe_execution_authority": False,
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

CTX = {
    "operator_approved_one_shot": True,
    "governor_approved_one_shot": True,
    "single_probe_only": True,
    "rollback_path_verified": True,
    "safe_reentry_window_bound": True,
    "memory_write_forbidden": True,
    "world_update_forbidden": True,
    "control_packet_mutation_forbidden": True,
    "authority_expires_after_use": True,
    "authority_revocable": True,
    "request_multi_probe": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_persistent_authority": False,
    "rollback_unavailable": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        scope = root / "scope.json"
        ctx = root / "ctx.json"
        out = root / "grant.json"
        dump(scope, SCOPE)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--middle-way-scope", str(scope), "--context", str(ctx), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("grant_output_missing")
        else:
            value = load(out)
            if value.get("gate_status") != "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY":
                errors.append("gate_status_mismatch")
            if value.get("grant_outcome") != "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED":
                errors.append("grant_outcome_mismatch")
            if value.get("grants_probe_execution_authority") is not True:
                errors.append("probe_authority_not_true")
            if value.get("grants_execution_authority") is not True:
                errors.append("execution_authority_not_true")
            for key in [
                "one_shot",
                "single_probe_only",
                "rollback_required",
                "reentry_window_bound",
                "authority_expires_after_use",
                "authority_revocable",
            ]:
                if value.get(key) is not True:
                    errors.append(f"{key}_not_true")
            for key in [
                "memory_write_allowed",
                "world_update_allowed",
                "control_packet_mutation_allowed",
                "probe_execution_performed",
                "dry_run_execution_performed",
                "next_tick_execution_performed",
                "memory_write_performed",
                "world_update_performed",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["request_memory_write"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--middle-way-scope", str(scope), "--context", str(ctx), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("gate_status") != "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_BLOCKED":
                errors.append("blocked_gate_status_mismatch")
            if "request_memory_write" not in value.get("grant_blockers", []):
                errors.append("memory_write_blocker_missing")
            if value.get("grants_probe_execution_authority") is not False:
                errors.append("blocked_probe_authority_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi limited one-shot execution-authority grant gate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
