#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_receipt_registry_os_bridge_v0_1.json"

REQUIRED_SURFACES = [
    "registry_entry_surface",
    "verification_pointer_surface",
    "registry_append_boundary_surface",
]
REQUIRED_CHECKS = [
    "REG_entry_key_visible",
    "REG_verification_pointers_visible",
    "REG_append_only_nonoverwrite",
    "REG_no_registry_reification",
]
REQUIRED_DEBTS = [
    "RD_missing_registry_key",
    "RD_missing_validation_ref",
    "RD_registry_overwrite_risk",
]
REQUIRED_OUTCOMES = [
    "RECEIPT_REGISTRY_ENTRY_READY",
    "RECEIPT_REGISTRY_HOLD",
    "RECEIPT_REGISTRY_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Receipt Registry OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_receipt_registry_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "RECEIPT_REGISTRY_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_output_receipt_lineage_bridge") != "kuuos_output_receipt_lineage_os_bridge_v0_1":
        errors.append("output receipt lineage attachment mismatch")

    principle = data.get("registry_principle", {})
    if "candidate evidence entry" not in principle.get("statement", ""):
        errors.append("principle missing candidate evidence entry")
    if "registry_entry" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing registry_entry")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    surfaces = {item.get("surface_id"): item for item in data.get("registry_surfaces", []) if isinstance(item, dict)}
    for surface_id in REQUIRED_SURFACES:
        item = surfaces.get(surface_id)
        if item is None:
            errors.append(f"missing registry surface: {surface_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid surface failure_effect: {surface_id}")

    checks = {item.get("check_id"): item for item in data.get("registry_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing registry check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid registry check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("registry_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing registry debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid registry debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("registry_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing registry outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"registry outcome missing allowed_projection: {outcome}")

    witness = data.get("registry_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "registry_surfaces_used",
        "registry_checks_run",
        "registry_debt",
        "registry_outcome",
        "registry_key",
        "receipt_hash",
        "append_only_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "output_receipt_lineage_required", "receipt_registry_required"]:
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

    print("PASS: KuuOS Receipt Registry OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
