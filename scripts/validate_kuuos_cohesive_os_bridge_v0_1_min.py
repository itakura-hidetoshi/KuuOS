#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_cohesive_os_bridge_v0_1.json"

REQUIRED_MODALITIES = [
    "shape_runtime_flow",
    "flat_audit_observable",
    "sharp_boundary_constraint",
]
REQUIRED_CHECKS = [
    "COH_shape_runtime_visible",
    "COH_flat_audit_lineage_visible",
    "COH_sharp_boundary_noncollapse",
    "COH_modalities_do_not_collapse",
]
REQUIRED_DEBTS = [
    "CD_shape_gap",
    "CD_flat_audit_gap",
    "CD_sharp_boundary_gap",
]
REQUIRED_OUTCOMES = [
    "COHESIVE_CANDIDATE",
    "COHESIVE_HOLD",
    "COHESIVE_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Cohesive OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_cohesive_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "COHESIVE_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_infinity_topos_bridge") != "kuuos_infinity_topos_os_bridge_v0_1":
        errors.append("infinity topos attachment mismatch")

    principle = data.get("cohesive_principle", {})
    if "continuous runtime flow" not in principle.get("statement", ""):
        errors.append("cohesive principle missing continuous runtime flow")
    if "cohesive_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing cohesive_candidate")
    if "does not create truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    modalities = {item.get("modality_id"): item for item in data.get("cohesive_modalities", []) if isinstance(item, dict)}
    for modality_id in REQUIRED_MODALITIES:
        item = modalities.get(modality_id)
        if item is None:
            errors.append(f"missing cohesive modality: {modality_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid modality failure_effect: {modality_id}")

    checks = {item.get("check_id"): item for item in data.get("cohesion_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing cohesion check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid cohesion check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("cohesive_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing cohesive debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid cohesive debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("cohesive_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing cohesive outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"cohesive outcome missing allowed_projection: {outcome}")

    witness = data.get("cohesive_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "cohesive_modalities_used",
        "cohesion_checks_run",
        "cohesive_debt",
        "cohesive_outcome",
        "sharp_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "infinity_topos_required", "cohesion_required"]:
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

    print("PASS: KuuOS Cohesive OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
