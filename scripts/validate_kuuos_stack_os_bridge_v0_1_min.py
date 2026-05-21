#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_stack_os_bridge_v0_1.json"

REQUIRED_FIBERS = [
    "F_core_runtime_candidates",
    "F_evidence_lineage_candidates",
    "F_policy_boundary_candidates",
]
REQUIRED_EQUIVALENCES = [
    "EQ_core_refinement_equivalence",
    "EQ_lineage_receipt_equivalence",
    "EQ_boundary_noncollapse_equivalence",
]
REQUIRED_CHECKS = [
    "SC_fibers_present",
    "SC_equivalence_witnesses_present",
    "SC_equivalence_not_identity",
    "SC_boundary_preserved_across_fibers",
]
REQUIRED_OUTCOMES = [
    "STACK_CANDIDATE",
    "STACK_HOLD",
    "STACK_QUARANTINE",
]


def has_any(values: list[str], needles: list[str]) -> bool:
    joined = " ".join(str(value) for value in values)
    return any(needle in joined for needle in needles)


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Stack OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))

    if data.get("bridge_id") != "kuuos_stack_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "STACK_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_hyperdescent_bridge") != "kuuos_hyperdescent_os_bridge_v0_1":
        errors.append("hyperdescent attachment mismatch")

    principle = data.get("stack_principle", {})
    if "stack-like family" not in principle.get("statement", ""):
        errors.append("stack principle missing stack-like family")
    if "stack_candidate" not in principle.get("runtime_formula", ""):
        errors.append("stack formula missing stack_candidate")
    if "not identity" not in principle.get("non_reification_rule", ""):
        errors.append("stack non-reification rule must block identity")

    fibers = {item.get("fiber_id"): item for item in data.get("runtime_fibers", []) if isinstance(item, dict)}
    for fiber_id in REQUIRED_FIBERS:
        item = fibers.get(fiber_id)
        if item is None:
            errors.append(f"missing fiber: {fiber_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid fiber failure_effect: {fiber_id}")

    equivalences = {item.get("witness_id"): item for item in data.get("equivalence_witnesses", []) if isinstance(item, dict)}
    required_negative_markers = {
        "EQ_core_refinement_equivalence": ["identity", "truth", "execution authority"],
        "EQ_lineage_receipt_equivalence": ["external audit acceptance", "memory overwrite"],
        "EQ_boundary_noncollapse_equivalence": ["truth authority", "world identity"],
    }
    for witness_id in REQUIRED_EQUIVALENCES:
        item = equivalences.get(witness_id)
        if item is None:
            errors.append(f"missing equivalence witness: {witness_id}")
            continue
        markers = required_negative_markers[witness_id]
        if not has_any(item.get("does_not_mean", []), markers):
            errors.append(f"equivalence witness missing required negative boundary: {witness_id}")
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid equivalence failure_effect: {witness_id}")

    checks = {item.get("check_id"): item for item in data.get("stack_coherence_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing stack coherence check: {check_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid stack check failure_effect: {check_id}")

    outcomes = {item.get("outcome"): item for item in data.get("stack_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing stack outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"stack outcome missing allowed_projection: {outcome}")

    witness = data.get("stack_witness_surface", {})
    for field in [
        "cycle_id",
        "kernel_state",
        "runtime_fibers_used",
        "equivalence_witnesses_used",
        "stack_outcome",
        "non_identity_boundary",
        "allowed_projection",
    ]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing stack witness field: {field}")
    for projection in ["truth_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "hyperdescent_required", "stack_required"]:
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

    print("PASS: KuuOS Stack OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
