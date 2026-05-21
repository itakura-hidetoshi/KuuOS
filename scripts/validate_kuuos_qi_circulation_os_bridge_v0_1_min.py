#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_qi_circulation_os_bridge_v0_1.json"

REQUIRED_CHANNELS = [
    "qi_runtime_flow_channel",
    "qi_lineage_flow_channel",
    "qi_boundary_guard_channel",
    "qi_projection_delivery_channel",
]
REQUIRED_CHECKS = [
    "QI_runtime_flow_visible",
    "QI_lineage_flow_visible",
    "QI_boundary_guard_noncollapse",
    "QI_delivery_nonreified",
    "QI_no_qi_reification",
]
REQUIRED_DEBTS = [
    "QID_runtime_stagnation",
    "QID_lineage_stagnation",
    "QID_boundary_block",
    "QID_projection_gap",
]
REQUIRED_OUTCOMES = [
    "QI_CIRCULATION_READY",
    "QI_CIRCULATION_HOLD",
    "QI_CIRCULATION_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Qi Circulation OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_qi_circulation_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "QI_CIRCULATION_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_view_delivery_bridge") != "kuuos_view_delivery_os_bridge_v0_1":
        errors.append("view delivery attachment mismatch")

    principle = data.get("qi_principle", {})
    if "candidate-only circulation" not in principle.get("statement", ""):
        errors.append("principle missing candidate-only circulation")
    if "qi_circulation" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing qi_circulation")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    channels = {item.get("channel_id"): item for item in data.get("qi_channels", []) if isinstance(item, dict)}
    for channel_id in REQUIRED_CHANNELS:
        item = channels.get(channel_id)
        if item is None:
            errors.append(f"missing qi channel: {channel_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid channel failure_effect: {channel_id}")

    checks = {item.get("check_id"): item for item in data.get("qi_circulation_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing qi check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid qi check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("qi_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing qi debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid qi debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("qi_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing qi outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"qi outcome missing allowed_projection: {outcome}")

    witness = data.get("qi_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "qi_channels_used",
        "qi_circulation_checks_run",
        "qi_debt",
        "qi_outcome",
        "runtime_flow",
        "lineage_flow",
        "boundary_guard",
        "projection_delivery_flow",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "view_delivery_required", "qi_circulation_required"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary must be true: {key}")
    for key in ["grants_execution_authority", "grants_truth_authority", "grants_memory_overwrite_authority", "grants_governance_bypass_authority"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary must be false: {key}")

    for invariant in data.get("required_invariants", []):
        if "qi is not reified" in invariant:
            break
    else:
        errors.append("missing qi non-reification invariant")

    for rel in data.get("integration_points", []):
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"missing integration point: {rel}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS Qi Circulation OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
