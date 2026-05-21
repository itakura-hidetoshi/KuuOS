#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_seal_projection_boundary_os_bridge_v0_1.json"

REQUIRED_LANES = [
    "lane_user_projection",
    "lane_audit_projection",
    "lane_machine_projection",
]
REQUIRED_CHECKS = [
    "PROJ_lanes_present",
    "PROJ_visibility_boundary_visible",
    "PROJ_boundary_noncollapse",
    "PROJ_no_projection_reification",
]
REQUIRED_DEBTS = [
    "PD_missing_projection_lane",
    "PD_visibility_gap",
    "PD_projection_boundary_gap",
]
REQUIRED_OUTCOMES = [
    "SEAL_PROJECTION_READY",
    "SEAL_PROJECTION_HOLD",
    "SEAL_PROJECTION_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Seal Projection Boundary OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_seal_projection_boundary_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "SEAL_PROJECTION_BOUNDARY_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_review_seal_bridge") != "kuuos_review_seal_os_bridge_v0_1":
        errors.append("review seal attachment mismatch")

    principle = data.get("projection_principle", {})
    if "bounded metadata" not in principle.get("statement", ""):
        errors.append("principle missing bounded metadata")
    if "seal_projection" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing seal_projection")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    lanes = {item.get("lane_id"): item for item in data.get("projection_lanes", []) if isinstance(item, dict)}
    for lane_id in REQUIRED_LANES:
        item = lanes.get(lane_id)
        if item is None:
            errors.append(f"missing projection lane: {lane_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid lane failure_effect: {lane_id}")

    checks = {item.get("check_id"): item for item in data.get("projection_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing projection check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid projection check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("projection_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing projection debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid projection debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("projection_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing projection outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"projection outcome missing allowed_projection: {outcome}")

    witness = data.get("projection_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "projection_lanes_used",
        "projection_checks_run",
        "projection_debt",
        "projection_outcome",
        "seal_status",
        "renewal_window",
        "visibility_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "review_seal_required", "seal_projection_boundary_required"]:
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

    print("PASS: KuuOS Seal Projection Boundary OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
