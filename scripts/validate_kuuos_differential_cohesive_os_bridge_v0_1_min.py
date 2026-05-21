#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_differential_cohesive_os_bridge_v0_1.json"

REQUIRED_SURFACES = [
    "runtime_tangent_surface",
    "audit_difference_surface",
    "boundary_derivative_surface",
]
REQUIRED_CHECKS = [
    "DIFF_runtime_variation_visible",
    "DIFF_audit_difference_visible",
    "DIFF_boundary_derivative_noncollapse",
    "DIFF_no_silent_boundary_drift",
]
REQUIRED_DEBTS = [
    "VD_runtime_flow_gap",
    "VD_audit_delta_gap",
    "VD_boundary_drift_gap",
]
REQUIRED_OUTCOMES = [
    "DIFFERENTIAL_COHESIVE_CANDIDATE",
    "DIFFERENTIAL_COHESIVE_HOLD",
    "DIFFERENTIAL_COHESIVE_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Differential Cohesive OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_differential_cohesive_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "DIFFERENTIAL_COHESIVE_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_cohesive_bridge") != "kuuos_cohesive_os_bridge_v0_1":
        errors.append("cohesive attachment mismatch")

    principle = data.get("differential_principle", {})
    if "small candidate variations" not in principle.get("statement", ""):
        errors.append("principle missing small candidate variations")
    if "differential_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing differential_candidate")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    surfaces = {item.get("surface_id"): item for item in data.get("differential_surfaces", []) if isinstance(item, dict)}
    for surface_id in REQUIRED_SURFACES:
        item = surfaces.get(surface_id)
        if item is None:
            errors.append(f"missing differential surface: {surface_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid surface failure_effect: {surface_id}")

    checks = {item.get("check_id"): item for item in data.get("differential_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing differential check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid differential check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("variation_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing variation debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid variation debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("differential_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing differential outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"differential outcome missing allowed_projection: {outcome}")

    witness = data.get("differential_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "differential_surfaces_used",
        "differential_checks_run",
        "variation_debt",
        "differential_outcome",
        "boundary_derivative_guard",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "cohesion_required", "differential_cohesion_required"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary must be true: {key}")
    for key in ["grants_execution_authority", "grants_truth_authority", "grants_memory_overwrite_authority", "grants_governance_bypass_authority"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary must be false: {key}")

    for rel in data.get("integration_points", []):
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"missing integration point: {rel}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS Differential Cohesive OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
