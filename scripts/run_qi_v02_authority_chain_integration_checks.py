#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=str(ROOT), text=True, capture_output=True, check=False)


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

AUTHORITY_CONTEXT = {
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

MIDDLE_CONTEXT = {
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

GRANT_CONTEXT = {
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
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        v02 = root / "v02.json"
        bridge = root / "bridge.json"
        candidate = root / "candidate.json"
        review = root / "review.json"
        authority_ctx = root / "authority_ctx.json"
        authority = root / "authority.json"
        middle_ctx = root / "middle_ctx.json"
        middle = root / "middle.json"
        grant_ctx = root / "grant_ctx.json"
        grant = root / "grant.json"

        dump(v02, V02)
        dump(authority_ctx, AUTHORITY_CONTEXT)
        dump(middle_ctx, MIDDLE_CONTEXT)
        dump(grant_ctx, GRANT_CONTEXT)

        steps = [
            ["scripts/write_qi_v02_execution_candidate_bridge_v0_1.py", "--v02-scheduler", str(v02), "--write", str(bridge), "--write-candidate", str(candidate), "--quiet"],
            ["scripts/write_qi_probe_execution_review_gate_v0_1.py", "--candidate", str(candidate), "--write", str(review), "--quiet"],
            ["scripts/write_qi_two_truths_authority_emergence_gate_v0_1.py", "--review-gate", str(review), "--context", str(authority_ctx), "--write", str(authority), "--quiet"],
            ["scripts/write_qi_middle_way_authority_scope_gate_v0_1.py", "--authority-emergence", str(authority), "--context", str(middle_ctx), "--write", str(middle), "--quiet"],
            ["scripts/write_qi_limited_one_shot_execution_authority_grant_gate_v0_1.py", "--middle-way-scope", str(middle), "--context", str(grant_ctx), "--write", str(grant), "--quiet"],
        ]
        for step in steps:
            completed = run(step)
            if completed.returncode != 0:
                errors.append(f"step_failed:{step[0]}:{completed.returncode}")
                errors.append(completed.stdout.strip() or completed.stderr.strip())
                break

        if grant.is_file():
            value = load(grant)
            if value.get("gate_status") != "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY":
                errors.append("grant_gate_not_ready")
            if value.get("grants_probe_execution_authority") is not True:
                errors.append("grant_probe_execution_authority_not_true")
            for key in ["probe_execution_performed", "memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "grants_memory_overwrite_authority", "grants_world_update_authority"]:
                if value.get(key) is not False:
                    errors.append(f"grant_{key}_not_false")
        else:
            errors.append("grant_output_missing")

        if bridge.is_file():
            bridge_value = load(bridge)
            if bridge_value.get("bridge_status") != "QI_V02_EXECUTION_CANDIDATE_BRIDGE_READY":
                errors.append("bridge_not_ready")
        if review.is_file():
            review_value = load(review)
            if review_value.get("review_outcome") != "READY_FOR_AUTHORITY_REVIEW":
                errors.append("review_not_ready_for_authority")
        if authority.is_file():
            authority_value = load(authority)
            if authority_value.get("authority_emergence_outcome") != "AUTHORITY_GRANT_CANDIDATE":
                errors.append("authority_not_grant_candidate")
        if middle.is_file():
            middle_value = load(middle)
            if middle_value.get("middle_way_scope_outcome") != "MIDDLE_WAY_AUTHORITY_SCOPE_READY":
                errors.append("middle_way_scope_not_ready")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi v0.2 authority chain integration checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
