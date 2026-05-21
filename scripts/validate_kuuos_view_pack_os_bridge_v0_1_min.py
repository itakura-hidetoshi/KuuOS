#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_view_pack_os_bridge_v0_1.json"

REQUIRED_LANES = [
    "lane_user_view_pack",
    "lane_audit_view_pack",
    "lane_machine_view_pack",
]
REQUIRED_CHECKS = [
    "VP_lanes_present",
    "VP_scope_visible",
    "VP_redaction_boundary_noncollapse",
    "VP_no_pack_reification",
]
REQUIRED_DEBTS = [
    "VPD_missing_view_lane",
    "VPD_scope_gap",
    "VPD_boundary_gap",
]
REQUIRED_OUTCOMES = [
    "VIEW_PACK_READY",
    "VIEW_PACK_HOLD",
    "VIEW_PACK_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing View Pack OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_view_pack_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "VIEW_PACK_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_seal_projection_boundary_bridge") != "kuuos_seal_projection_boundary_os_bridge_v0_1":
        errors.append("seal projection attachment mismatch")

    principle = data.get("view_pack_principle", {})
    if "communication metadata" not in principle.get("statement", ""):
        errors.append("principle missing communication metadata")
    if "view_pack" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing view_pack")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    lanes = {item.get("lane_id"): item for item in data.get("view_pack_lanes", []) if isinstance(item, dict)}
    for lane_id in REQUIRED_LANES:
        item = lanes.get(lane_id)
        if item is None:
            errors.append(f"missing view pack lane: {lane_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid lane failure_effect: {lane_id}")

    checks = {item.get("check_id"): item for item in data.get("view_pack_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing view pack check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid view pack check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("view_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing view debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid view debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("view_pack_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing view pack outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"view pack outcome missing allowed_projection: {outcome}")

    witness = data.get("view_pack_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "view_pack_lanes_used",
        "view_pack_checks_run",
        "view_debt",
        "view_pack_outcome",
        "audience_scope",
        "redaction_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "seal_projection_boundary_required", "view_pack_required"]:
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

    print("PASS: KuuOS View Pack OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
