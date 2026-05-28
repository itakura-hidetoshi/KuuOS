#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_middle_way_authority_scope_gate_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


AUTHORITY = {
    "gate_status": "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_READY",
    "authority_emergence_outcome": "AUTHORITY_GRANT_CANDIDATE",
    "authority_grant_candidate_only": True,
    "execution_requires_separate_gate": True,
    "local_limited_revocable": True,
    "authority": "none",
    "reviewed_probe_type": "observation_debt_probe",
    "conventional_authority_scope": "single_probe_execution_candidate_review",
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
    "authority_scope": "single_probe_execution_candidate_review",
    "authority_not_reified": True,
    "authority_not_denied_when_conditions_hold": True,
    "avoids_eternalism": True,
    "avoids_nihilism": True,
    "conditioned_local_authority_only": True,
    "ultimate_non_reification_preserved": True,
    "dependent_origination_trace_present": True,
    "two_truths_boundary_preserved": True,
    "local_limited_revocable": True,
    "mass_gap_barrier_preserved": True,
    "no_direct_execution_collapse": True,
    "eternalist_authority_claim": False,
    "nihilist_authority_denial": False,
    "authority_scope_unbounded": False,
    "authority_irrevocable": False,
    "direct_execution_requested": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        auth = root / "authority.json"
        ctx = root / "ctx.json"
        out = root / "scope.json"
        dump(auth, AUTHORITY)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--authority-emergence", str(auth), "--context", str(ctx), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("scope_output_missing")
        else:
            value = load(out)
            if value.get("gate_status") != "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_READY":
                errors.append("gate_status_mismatch")
            if value.get("middle_way_scope_outcome") != "MIDDLE_WAY_AUTHORITY_SCOPE_READY":
                errors.append("scope_outcome_mismatch")
            if value.get("middle_way_scope_only") is not True:
                errors.append("middle_way_scope_only_not_true")
            if value.get("authority_scope_candidate_only") is not True:
                errors.append("authority_scope_candidate_only_not_true")
            if value.get("actual_probe_execution_authority") is not False:
                errors.append("actual_probe_execution_authority_not_false")
            if value.get("execution_requires_separate_gate") is not True:
                errors.append("execution_requires_separate_gate_not_true")
            if value.get("authority") != "none":
                errors.append("authority_not_none")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "probe_execution_performed",
                "memory_write_performed",
                "world_update_performed",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["eternalist_authority_claim"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--authority-emergence", str(auth), "--context", str(ctx), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("gate_status") != "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_BLOCKED":
                errors.append("blocked_gate_status_mismatch")
            if "eternalist_authority_claim" not in value.get("scope_blockers", []):
                errors.append("eternalist_blocker_missing")
            if value.get("actual_probe_execution_authority") is not False:
                errors.append("blocked_actual_probe_execution_authority_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi middle-way authority scope gate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
