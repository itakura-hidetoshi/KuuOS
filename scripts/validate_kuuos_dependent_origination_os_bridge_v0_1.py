#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_dependent_origination_os_bridge_v0_1",
    "version": "v0.1",
    "status": "DEPENDENT_ORIGINATION_OS_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_two_truths_bridge": "kuuos_two_truths_os_bridge_v0_1",
    "attached_two_truths_bridge_spec": "specs/kuuos_two_truths_os_bridge_v0_1.json",
    "attached_kernel": "kuuos_os_autonomy_kernel_v0_1",
    "attached_kernel_spec": "specs/kuuos_os_autonomy_kernel_v0_1.json",
}

REQUIRED_CONDITIONS = [
    "repository_condition",
    "policy_condition",
    "module_condition",
    "audit_condition",
    "boundary_condition",
]

REQUIRED_EDGES = [
    "repository_to_boot",
    "policy_to_boot",
    "registry_to_schedule",
    "module_to_decide",
    "checkpoint_to_audit",
    "two_truths_gap_to_decide",
]

REQUIRED_STATES = ["PASS", "HOLD", "REPAIR_PENDING", "QUARANTINE"]

REQUIRED_WITNESS_FIELDS = [
    "cycle_id",
    "kernel_state",
    "supporting_conditions",
    "failed_conditions",
    "dependency_edges_used",
    "blockers",
    "non_authority_boundary",
    "allowed_projection",
]

ALLOWED_PROJECTIONS = [
    "evidence_receipt",
    "support_recheck_request",
    "dependency_gap_notice",
    "hold_notice",
    "repair_candidate_request",
    "quarantine_notice",
]

FORBIDDEN_PROJECTIONS = [
    "truth_commit",
    "execution_commit",
    "memory_overwrite_commit",
    "clinical_commit",
    "theorem_commit",
]

TRUE_BOUNDARY = [
    "validation_only",
    "candidate_only",
    "local_os_supervision_only",
    "dependent_origination_required",
    "two_truths_gap_required",
]

FALSE_BOUNDARY = [
    "grants_execution_authority",
    "grants_clinical_authority",
    "grants_diagnosis_authority",
    "grants_treatment_authority",
    "grants_theorem_authority",
    "grants_truth_authority",
    "grants_memory_overwrite_authority",
    "grants_governance_bypass_authority",
]


def main() -> int:
    errors: list[str] = []
    for path in [SPEC, TWO_TRUTHS, KERNEL]:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    two_truths = json.loads(TWO_TRUTHS.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if two_truths.get("bridge_id") != data.get("attached_two_truths_bridge"):
        errors.append("attached two-truths bridge mismatch")
    if kernel.get("kernel_id") != data.get("attached_kernel"):
        errors.append("attached kernel mismatch")

    principle = data.get("dependent_origination_principle", {})
    if "No kernel state" not in principle.get("statement", ""):
        errors.append("dependent origination principle statement is missing non-self-arising claim")
    if "state_t" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention state_t")
    if "truth authority" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must block truth authority")

    conditions = {item.get("surface_id"): item for item in data.get("condition_surfaces", []) if isinstance(item, dict)}
    for condition in REQUIRED_CONDITIONS:
        if condition not in conditions:
            errors.append(f"missing condition surface: {condition}")

    edges = {item.get("edge_id"): item for item in data.get("dependency_edges", []) if isinstance(item, dict)}
    for edge_id in REQUIRED_EDGES:
        edge = edges.get(edge_id)
        if edge is None:
            errors.append(f"missing dependency edge: {edge_id}")
            continue
        if edge.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"edge failure_effect must be HOLD or QUARANTINE: {edge_id}")

    states = {item.get("state"): item for item in data.get("dependent_state_rules", []) if isinstance(item, dict)}
    for state in REQUIRED_STATES:
        if state not in states:
            errors.append(f"missing dependent state rule: {state}")
    pass_rule = states.get("PASS", {})
    for claim in ["truth authority", "execution authority", "memory overwrite authority"]:
        if claim not in pass_rule.get("does_not_grant", []):
            errors.append(f"PASS does_not_grant missing: {claim}")

    witness = data.get("causal_explanation_surface", {})
    for field in REQUIRED_WITNESS_FIELDS:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness required field: {field}")
    for projection in ALLOWED_PROJECTIONS:
        if projection not in witness.get("allowed_projection", []):
            errors.append(f"missing allowed projection: {projection}")
    for projection in FORBIDDEN_PROJECTIONS:
        if projection not in witness.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    boundary = data.get("authority_boundary", {})
    for key in TRUE_BOUNDARY:
        if boundary.get(key) is not True:
            errors.append(f"authority_boundary.{key} must be true")
    for key in FALSE_BOUNDARY:
        if boundary.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")

    for rel in data.get("integration_points", []):
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"integration point missing: {rel}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: KuuOS dependent origination OS bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
