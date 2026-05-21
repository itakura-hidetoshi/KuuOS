#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_review_seal_os_bridge_v0_1.json"

REQUIRED_SURFACES = [
    "seal_status_surface",
    "renewal_window_surface",
    "seal_boundary_surface",
]
REQUIRED_CHECKS = [
    "SEAL_status_visible",
    "SEAL_renewal_window_visible",
    "SEAL_boundary_noncollapse",
    "SEAL_no_seal_reification",
]
REQUIRED_DEBTS = [
    "SD_missing_seal_status",
    "SD_stale_seal_window",
    "SD_seal_boundary_gap",
]
REQUIRED_OUTCOMES = [
    "REVIEW_SEAL_READY",
    "REVIEW_SEAL_HOLD",
    "REVIEW_SEAL_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Review Seal OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_review_seal_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "REVIEW_SEAL_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_registry_review_bridge") != "kuuos_registry_review_os_bridge_v0_1":
        errors.append("registry review attachment mismatch")

    principle = data.get("seal_principle", {})
    if "candidate metadata" not in principle.get("statement", ""):
        errors.append("principle missing candidate metadata")
    if "review_seal" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing review_seal")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    surfaces = {item.get("surface_id"): item for item in data.get("seal_surfaces", []) if isinstance(item, dict)}
    for surface_id in REQUIRED_SURFACES:
        item = surfaces.get(surface_id)
        if item is None:
            errors.append(f"missing seal surface: {surface_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid surface failure_effect: {surface_id}")

    checks = {item.get("check_id"): item for item in data.get("seal_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing seal check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid seal check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("seal_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing seal debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid seal debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("seal_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing seal outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"seal outcome missing allowed_projection: {outcome}")

    witness = data.get("seal_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "seal_surfaces_used",
        "seal_checks_run",
        "seal_debt",
        "seal_outcome",
        "seal_status",
        "renewal_window",
        "non_authority_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "registry_review_required", "review_seal_required"]:
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

    print("PASS: KuuOS Review Seal OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
