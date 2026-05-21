#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_selector_boundary_os_bridge_v0_1.json"

REQUIRED_SURFACES = [
    "ranking_witness_surface",
    "abstention_gate_surface",
    "handover_boundary_surface",
]
REQUIRED_CHECKS = [
    "SEL_ranking_visible",
    "SEL_abstention_available",
    "SEL_handover_boundary_noncollapse",
    "SEL_no_final_commitment",
]
REQUIRED_DEBTS = [
    "SD_ranking_gap",
    "SD_abstention_required",
    "SD_boundary_handover",
]
REQUIRED_OUTCOMES = [
    "SELECTOR_CANDIDATE",
    "SELECTOR_HOLD",
    "SELECTOR_QUARANTINE",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Selector Boundary OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_selector_boundary_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "SELECTOR_BOUNDARY_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_policy_barrier_bridge") != "kuuos_policy_barrier_os_bridge_v0_1":
        errors.append("policy barrier attachment mismatch")

    principle = data.get("selector_principle", {})
    if "candidate-only" not in principle.get("statement", ""):
        errors.append("principle missing candidate-only")
    if "selector_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing selector_candidate")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    surfaces = {item.get("surface_id"): item for item in data.get("selector_surfaces", []) if isinstance(item, dict)}
    for surface_id in REQUIRED_SURFACES:
        item = surfaces.get(surface_id)
        if item is None:
            errors.append(f"missing selector surface: {surface_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid surface failure_effect: {surface_id}")

    checks = {item.get("check_id"): item for item in data.get("selector_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing selector check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid selector check failure_effect: {check_id}")

    debts = {item.get("debt_id"): item for item in data.get("selector_debt_classes", []) if isinstance(item, dict)}
    for debt_id in REQUIRED_DEBTS:
        item = debts.get(debt_id)
        if item is None:
            errors.append(f"missing selector debt: {debt_id}")
        elif item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid selector debt result_state: {debt_id}")

    outcomes = {item.get("outcome"): item for item in data.get("selector_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing selector outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"selector outcome missing allowed_projection: {outcome}")

    witness = data.get("selector_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "selector_surfaces_used",
        "selector_checks_run",
        "selector_debt",
        "selector_outcome",
        "abstention_gate",
        "handover_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "policy_barrier_required", "selector_boundary_required"]:
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

    print("PASS: KuuOS Selector Boundary OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
