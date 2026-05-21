#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_qi_meridian_os_bridge_v0_1.json"

REQUIRED_CHANNELS = [
    "meridian_runtime_to_policy",
    "meridian_policy_to_boundary",
    "meridian_lineage_to_review",
    "meridian_projection_to_delivery",
]
REQUIRED_CHECKS = [
    "MER_channels_present",
    "MER_runtime_policy_continuity",
    "MER_boundary_channel_noncollapse",
    "MER_lineage_channel_visible",
    "MER_delivery_channel_nonreified",
    "MER_no_meridian_reification",
]
REQUIRED_DEBTS = [
    "MD_missing_channel",
    "MD_runtime_stagnation",
    "MD_lineage_blockage",
    "MD_boundary_blockage",
]
REQUIRED_OUTCOMES = [
    "QI_MERIDIAN_READY",
    "QI_MERIDIAN_HOLD",
    "QI_MERIDIAN_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Qi Meridian OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_qi_meridian_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "QI_MERIDIAN_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_qi_circulation_bridge") != "kuuos_qi_circulation_os_bridge_v0_1":
        errors.append("qi circulation attachment mismatch")

    principle = data.get("meridian_principle", {})
    if "candidate-only channel relations" not in principle.get("statement", ""):
        errors.append("principle missing candidate-only channel relations")
    if "qi_meridian" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing qi_meridian")
    if "not a substance" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block substance reification")

    channels = {item.get("channel_id"): item for item in data.get("meridian_channels", []) if isinstance(item, dict)}
    for channel_id in REQUIRED_CHANNELS:
        item = channels.get(channel_id)
        if item is None:
            errors.append(f"missing meridian channel: {channel_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid channel failure_effect: {channel_id}")

    checks = {item.get("check_id"): item for item in data.get("meridian_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing meridian check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid meridian check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("meridian_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing meridian debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid meridian debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("meridian_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing meridian outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"meridian outcome missing allowed_projection: {outcome}")

    witness = data.get("meridian_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "meridian_channels_used",
        "meridian_checks_run",
        "meridian_debt",
        "meridian_outcome",
        "channel_topology",
        "continuity_witness",
        "blockage_debt",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "qi_circulation_required", "qi_meridian_required"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary must be true: {key}")
    for key in ["grants_execution_authority", "grants_truth_authority", "grants_memory_overwrite_authority", "grants_governance_bypass_authority"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary must be false: {key}")

    for invariant in data.get("required_invariants", []):
        if "meridian is not reified" in invariant:
            break
    else:
        errors.append("missing meridian non-reification invariant")

    for rel in data.get("integration_points", []):
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"missing integration point: {rel}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS Qi Meridian OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
