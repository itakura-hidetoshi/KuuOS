#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_two_truths_authority_emergence_gate_addendum_v0_1.json"


def load(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main() -> int:
    errors: list[str] = []
    m = load(MANIFEST)
    if not m:
        errors.append("manifest_missing")
    if m.get("manifest_version") != "qi_two_truths_authority_emergence_gate_addendum_v0_1":
        errors.append("manifest_version_mismatch")
    if m.get("addendum_status") != "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_ADDENDUM_READY":
        errors.append("addendum_status_mismatch")
    if m.get("extends_manifest") != "manifests/qi_probe_execution_review_gate_addendum_v0_1.json":
        errors.append("extends_manifest_mismatch")
    if m.get("authority") != "none":
        errors.append("authority_not_none")
    for key in [
        "authority_grant_candidate_only",
        "authority_review_gate_only",
        "execution_requires_separate_gate",
        "local_limited_revocable",
    ]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in [
        "actual_probe_execution_authority",
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
        if m.get(key) is not False:
            errors.append(f"{key}_not_false")
    required_conditions = {
        "ultimate_non_reification_preserved",
        "dependent_origination_trace_present",
        "two_truths_boundary_preserved",
        "mass_gap_barrier_preserved",
        "superstring_membrane_boundary_preserved",
        "super_relativity_record_surface_present",
        "causal_trace_present",
        "rollback_path_present",
        "safe_reentry_window_acceptable",
        "observation_debt_targeted_or_bounded",
        "memory_kernel_preservation_acceptable",
    }
    if not required_conditions.issubset(set(m.get("theoretical_authority_conditions", []))):
        errors.append("theoretical_authority_conditions_missing")
    forbidden = {
        "authority_claims_ultimate_truth",
        "authority_scope_unbounded",
        "authority_irrevocable",
        "mass_gap_collapsed",
        "direct_execution_requested",
    }
    if not forbidden.issubset(set(m.get("forbidden_authority_claims", []))):
        errors.append("forbidden_authority_claims_missing")
    for group in ["runtime_files", "script_files", "test_files"]:
        files = m.get(group, [])
        if not isinstance(files, list) or not files:
            errors.append(f"{group}_missing")
            continue
        for item in files:
            if not (ROOT / item).is_file():
                errors.append(f"missing_file:{item}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi two-truths authority emergence gate addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
