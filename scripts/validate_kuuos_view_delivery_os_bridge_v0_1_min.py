#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_view_delivery_os_bridge_v0_1.json"

REQUIRED_LANES = [
    "lane_user_delivery",
    "lane_audit_delivery",
    "lane_machine_delivery",
]
REQUIRED_CHECKS = [
    "DEL_lanes_present",
    "DEL_channel_scope_visible",
    "DEL_acknowledgment_nonfinal",
    "DEL_boundary_noncollapse",
    "DEL_no_delivery_reification",
]
REQUIRED_DEBTS = [
    "DD_missing_delivery_lane",
    "DD_channel_scope_gap",
    "DD_delivery_boundary_gap",
]
REQUIRED_OUTCOMES = [
    "VIEW_DELIVERY_READY",
    "VIEW_DELIVERY_HOLD",
    "VIEW_DELIVERY_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing View Delivery OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_view_delivery_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "VIEW_DELIVERY_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_view_pack_bridge") != "kuuos_view_pack_os_bridge_v0_1":
        errors.append("view pack attachment mismatch")

    principle = data.get("delivery_principle", {})
    if "communication metadata" not in principle.get("statement", ""):
        errors.append("principle missing communication metadata")
    if "view_delivery" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing view_delivery")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    lanes = {item.get("lane_id"): item for item in data.get("delivery_lanes", []) if isinstance(item, dict)}
    for lane_id in REQUIRED_LANES:
        item = lanes.get(lane_id)
        if item is None:
            errors.append(f"missing delivery lane: {lane_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid lane failure_effect: {lane_id}")

    checks = {item.get("check_id"): item for item in data.get("delivery_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing delivery check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid delivery check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("delivery_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing delivery debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid delivery debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("delivery_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing delivery outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"delivery outcome missing allowed_projection: {outcome}")

    witness = data.get("delivery_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "delivery_lanes_used",
        "delivery_checks_run",
        "delivery_debt",
        "delivery_outcome",
        "delivery_envelope",
        "channel_scope",
        "acknowledgment_marker",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "view_pack_required", "view_delivery_required"]:
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

    print("PASS: KuuOS View Delivery OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
