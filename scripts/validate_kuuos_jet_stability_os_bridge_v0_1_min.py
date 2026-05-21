#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_jet_stability_os_bridge_v0_1.json"

REQUIRED_SURFACES = [
    "J1_runtime_flow",
    "J2_audit_lineage",
    "Jk_boundary_guard",
]
REQUIRED_CHECKS = [
    "JET_runtime_order1_visible",
    "JET_audit_order2_visible",
    "JET_boundary_orderk_noncollapse",
    "JET_truncation_visible",
    "JET_no_high_order_boundary_drift",
]
REQUIRED_DEBTS = [
    "JD_missing_jet_surface",
    "JD_truncation_gap",
    "JD_boundary_instability",
]
REQUIRED_OUTCOMES = [
    "JET_STABLE_CANDIDATE",
    "JET_STABILITY_HOLD",
    "JET_STABILITY_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Jet Stability OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_jet_stability_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "JET_STABILITY_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_differential_cohesive_bridge") != "kuuos_differential_cohesive_os_bridge_v0_1":
        errors.append("differential cohesive attachment mismatch")

    principle = data.get("jet_principle", {})
    if "finite-order local jets" not in principle.get("statement", ""):
        errors.append("jet principle missing finite-order local jets")
    if "jet_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing jet_candidate")
    if "finite-order local evidence" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must preserve finite-order local evidence")

    surfaces = {item.get("surface_id"): item for item in data.get("jet_surfaces", []) if isinstance(item, dict)}
    for surface_id in REQUIRED_SURFACES:
        item = surfaces.get(surface_id)
        if item is None:
            errors.append(f"missing jet surface: {surface_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid jet surface failure_effect: {surface_id}")

    checks = {item.get("check_id"): item for item in data.get("jet_stability_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing jet check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid jet check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("jet_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing jet debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid jet debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("jet_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing jet outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"jet outcome missing allowed_projection: {outcome}")

    witness = data.get("jet_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "jet_surfaces_used",
        "jet_orders_declared",
        "jet_stability_checks_run",
        "jet_debt",
        "jet_outcome",
        "truncation_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "differential_cohesion_required", "jet_stability_required"]:
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

    print("PASS: KuuOS Jet Stability OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
