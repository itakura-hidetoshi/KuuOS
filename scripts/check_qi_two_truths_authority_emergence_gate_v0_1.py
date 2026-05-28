#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_two_truths_authority_emergence_gate_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


READY_REVIEW = {
    "gate_status": "QI_PROBE_EXECUTION_REVIEW_GATE_READY",
    "review_outcome": "READY_FOR_AUTHORITY_REVIEW",
    "ready_for_authority_review": True,
    "authority_review_required": True,
    "authority": "none",
    "reviewed_probe_type": "observation_debt_probe",
    "reviewed_schedule_mode": "near_term_revisit",
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

READY_CONTEXT = {
    "conventional_authority_scope": "single_probe_execution_candidate_review",
    "ultimate_non_reification_preserved": True,
    "dependent_origination_trace_present": True,
    "two_truths_boundary_preserved": True,
    "mass_gap_barrier_preserved": True,
    "superstring_membrane_boundary_preserved": True,
    "super_relativity_record_surface_present": True,
    "causal_trace_present": True,
    "rollback_path_present": True,
    "safe_reentry_window_acceptable": True,
    "observation_debt_targeted_or_bounded": True,
    "memory_kernel_preservation_acceptable": True,
    "operator_review_record_present": True,
    "governor_review_record_present": True,
    "authority_claims_ultimate_truth": False,
    "authority_scope_unbounded": False,
    "authority_irrevocable": False,
    "mass_gap_collapsed": False,
    "direct_execution_requested": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        review = root / "review.json"
        context = root / "context.json"
        out = root / "authority.json"
        dump(review, READY_REVIEW)
        dump(context, READY_CONTEXT)
        completed = subprocess.run([
            sys.executable, str(CLI), "--review-gate", str(review), "--context", str(context), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("authority_output_missing")
        else:
            value = load(out)
            if value.get("gate_status") != "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_READY":
                errors.append("gate_status_mismatch")
            if value.get("authority_emergence_outcome") != "AUTHORITY_GRANT_CANDIDATE":
                errors.append("authority_emergence_outcome_mismatch")
            if value.get("authority_grant_candidate_only") is not True:
                errors.append("authority_grant_candidate_only_not_true")
            if value.get("actual_probe_execution_authority") is not False:
                errors.append("actual_probe_execution_authority_not_false")
            if value.get("execution_requires_separate_gate") is not True:
                errors.append("execution_requires_separate_gate_not_true")
            if value.get("local_limited_revocable") is not True:
                errors.append("local_limited_revocable_not_true")
            if value.get("authority") != "none":
                errors.append("authority_not_none")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_dry_run_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_scheduler_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
                "probe_execution_performed",
                "memory_write_performed",
                "world_update_performed",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_context = dict(READY_CONTEXT)
        bad_context["mass_gap_collapsed"] = True
        dump(context, bad_context)
        completed = subprocess.run([
            sys.executable, str(CLI), "--review-gate", str(review), "--context", str(context), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("gate_status") != "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_BLOCKED":
                errors.append("blocked_gate_status_mismatch")
            if "mass_gap_collapsed" not in value.get("authority_blockers", []):
                errors.append("mass_gap_collapsed_blocker_missing")
            if value.get("actual_probe_execution_authority") is not False:
                errors.append("blocked_actual_probe_execution_authority_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi two-truths authority emergence gate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
