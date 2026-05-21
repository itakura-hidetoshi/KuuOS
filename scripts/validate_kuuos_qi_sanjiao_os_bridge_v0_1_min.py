#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_qi_sanjiao_os_bridge_v0_1.json"

REQUIRED_MEMBRANES = [
    "lower_lineage_membrane",
    "middle_policy_membrane",
    "upper_delivery_membrane",
    "boundary_permeability_membrane",
]
REQUIRED_CHECKS = [
    "SJ_membranes_present",
    "SJ_lower_lineage_continuity",
    "SJ_middle_policy_transformation_visible",
    "SJ_upper_delivery_diffusion_nonfinal",
    "SJ_boundary_permeability_noncollapse",
    "SJ_no_sanjiao_reification",
]
REQUIRED_DEBTS = [
    "SJD_missing_membrane",
    "SJD_lower_lineage_stasis",
    "SJD_middle_policy_turbulence",
    "SJD_upper_delivery_gap",
    "SJD_boundary_membrane_block",
]
REQUIRED_OUTCOMES = [
    "QI_SANJIAO_READY",
    "QI_SANJIAO_HOLD",
    "QI_SANJIAO_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Qi Sanjiao OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_qi_sanjiao_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "QI_SANJIAO_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_qi_meridian_bridge") != "kuuos_qi_meridian_os_bridge_v0_1":
        errors.append("qi meridian attachment mismatch")

    principle = data.get("sanjiao_principle", {})
    if "candidate-only membrane regulation" not in principle.get("statement", ""):
        errors.append("principle missing candidate-only membrane regulation")
    if "qi_sanjiao" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing qi_sanjiao")
    if "not a substance" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block substance reification")

    membranes = {item.get("membrane_id"): item for item in data.get("sanjiao_membranes", []) if isinstance(item, dict)}
    for membrane_id in REQUIRED_MEMBRANES:
        item = membranes.get(membrane_id)
        if item is None:
            errors.append(f"missing sanjiao membrane: {membrane_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid membrane failure_effect: {membrane_id}")

    checks = {item.get("check_id"): item for item in data.get("sanjiao_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing sanjiao check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid sanjiao check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("sanjiao_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing sanjiao debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid sanjiao debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("sanjiao_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing sanjiao outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"sanjiao outcome missing allowed_projection: {outcome}")

    witness = data.get("sanjiao_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "sanjiao_membranes_used",
        "sanjiao_checks_run",
        "sanjiao_debt",
        "sanjiao_outcome",
        "lower_lineage_membrane",
        "middle_policy_membrane",
        "upper_delivery_membrane",
        "boundary_permeability_membrane",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "qi_meridian_required", "qi_sanjiao_required"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary must be true: {key}")
    for key in ["grants_execution_authority", "grants_truth_authority", "grants_memory_overwrite_authority", "grants_governance_bypass_authority"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary must be false: {key}")

    for invariant in data.get("required_invariants", []):
        if "sanjiao is not reified" in invariant:
            break
    else:
        errors.append("missing sanjiao non-reification invariant")

    for rel in data.get("integration_points", []):
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"missing integration point: {rel}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS Qi Sanjiao OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
