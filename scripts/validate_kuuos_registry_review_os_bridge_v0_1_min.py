#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_registry_review_os_bridge_v0_1.json"

REQUIRED_LANES = [
    "lane_local_validation",
    "lane_lineage_consistency",
    "lane_boundary_review",
]
REQUIRED_CHECKS = [
    "REV_lanes_present",
    "REV_window_visible",
    "REV_boundary_noncollapse",
    "REV_no_review_reification",
]
REQUIRED_DEBTS = [
    "RVD_missing_review_lane",
    "RVD_stale_review_window",
    "RVD_boundary_review_gap",
]
REQUIRED_OUTCOMES = [
    "REGISTRY_REVIEW_READY",
    "REGISTRY_REVIEW_HOLD",
    "REGISTRY_REVIEW_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Registry Review OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_registry_review_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "REGISTRY_REVIEW_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_receipt_registry_bridge") != "kuuos_receipt_registry_os_bridge_v0_1":
        errors.append("receipt registry attachment mismatch")

    principle = data.get("review_principle", {})
    if "explicit lanes" not in principle.get("statement", ""):
        errors.append("principle missing explicit lanes")
    if "review_entry" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing review_entry")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    lanes = {item.get("lane_id"): item for item in data.get("review_lanes", []) if isinstance(item, dict)}
    for lane_id in REQUIRED_LANES:
        item = lanes.get(lane_id)
        if item is None:
            errors.append(f"missing review lane: {lane_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid lane failure_effect: {lane_id}")

    checks = {item.get("check_id"): item for item in data.get("review_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing review check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid review check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("review_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing review debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid review debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("review_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing review outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"review outcome missing allowed_projection: {outcome}")

    witness = data.get("review_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "review_lanes_used",
        "review_checks_run",
        "review_debt",
        "review_outcome",
        "verification_window",
        "registry_key",
        "non_authority_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "receipt_registry_required", "registry_review_required"]:
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

    print("PASS: KuuOS Registry Review OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
