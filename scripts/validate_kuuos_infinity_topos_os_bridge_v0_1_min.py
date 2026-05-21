#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_infinity_topos_os_bridge_v0_1.json"

REQUIRED_WORLDS = ["W_runtime", "W_evidence", "W_boundary"]
REQUIRED_GATES = ["M_possible_candidate", "M_necessary_boundary", "M_reobserve"]
REQUIRED_PULLBACKS = ["PB_stack_to_runtime_world", "PB_lineage_to_evidence_world", "PB_boundary_to_boundary_world"]
REQUIRED_OUTCOMES = ["MODAL_TOPOS_CANDIDATE", "MODAL_TOPOS_HOLD", "MODAL_TOPOS_QUARANTINE"]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print("ERROR: missing Infinity Topos OS bridge spec")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    if data.get("bridge_id") != "kuuos_infinity_topos_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "INFINITY_TOPOS_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    if data.get("attached_stack_bridge") != "kuuos_stack_os_bridge_v0_1":
        errors.append("stack attachment mismatch")

    principle = data.get("topos_principle", {})
    if "modal local worlds" not in principle.get("statement", ""):
        errors.append("topos principle missing modal local worlds")
    if "modal_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing modal_candidate")
    if "not truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must block truth authority")

    worlds = {item.get("world_id"): item for item in data.get("modal_worlds", []) if isinstance(item, dict)}
    for world_id in REQUIRED_WORLDS:
        item = worlds.get(world_id)
        if item is None:
            errors.append(f"missing modal world: {world_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid world failure_effect: {world_id}")

    gates = {item.get("gate_id"): item for item in data.get("modality_gates", []) if isinstance(item, dict)}
    for gate_id in REQUIRED_GATES:
        item = gates.get(gate_id)
        if item is None:
            errors.append(f"missing modality gate: {gate_id}")
        elif item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid gate failure_effect: {gate_id}")

    pullbacks = {item.get("check_id"): item for item in data.get("pullback_stability_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_PULLBACKS:
        item = pullbacks.get(check_id)
        if item is None:
            errors.append(f"missing pullback check: {check_id}")
            continue
        if not item.get("must_preserve"):
            errors.append(f"pullback check must preserve quantities: {check_id}")
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"invalid pullback failure_effect: {check_id}")

    outcomes = {item.get("outcome"): item for item in data.get("topos_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing topos outcome: {outcome}")
        elif not item.get("allowed_projection"):
            errors.append(f"topos outcome missing allowed_projection: {outcome}")

    witness = data.get("topos_witness_surface", {})
    for field in ["cycle_id", "kernel_state", "modal_worlds_used", "modality_gates_used", "pullback_checks_run", "topos_outcome", "non_truth_boundary", "allowed_projection"]:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
    for projection in ["truth_commit", "execution_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "two_truths_gap_required", "stack_required", "infinity_topos_required"]:
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
    print("PASS: KuuOS Infinity Topos OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
