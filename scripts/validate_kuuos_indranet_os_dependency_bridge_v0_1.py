#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_indranet_os_dependency_bridge_v0_1.json"
DO = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_indranet_os_dependency_bridge_v0_1",
    "version": "v0.1",
    "status": "INDRANET_OS_DEPENDENCY_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_dependent_origination_bridge": "kuuos_dependent_origination_os_bridge_v0_1",
    "attached_dependent_origination_spec": "specs/kuuos_dependent_origination_os_bridge_v0_1.json",
    "attached_two_truths_bridge": "kuuos_two_truths_os_bridge_v0_1",
    "attached_two_truths_bridge_spec": "specs/kuuos_two_truths_os_bridge_v0_1.json",
    "attached_kernel": "kuuos_os_autonomy_kernel_v0_1",
    "attached_kernel_spec": "specs/kuuos_os_autonomy_kernel_v0_1.json",
}

REQUIRED_NODES = [
    "repo_node",
    "policy_node",
    "module_node",
    "lineage_node",
    "boundary_node",
]

REQUIRED_OVERLAPS = [
    "repo_policy_overlap",
    "policy_module_overlap",
    "module_lineage_overlap",
    "lineage_boundary_overlap",
    "boundary_repo_overlap",
]

REQUIRED_GLUING_CHECKS = [
    "all_required_nodes_present",
    "overlap_coverage_nonempty",
    "no_authority_collapse_on_overlap",
    "hold_is_globalizable",
]

REQUIRED_BLOCKERS = [
    "missing_repository_support",
    "policy_boundary_mismatch",
    "module_evidence_failure",
    "lineage_break",
    "two_truths_gap_collapse",
]

REQUIRED_WITNESS_FIELDS = [
    "cycle_id",
    "kernel_state",
    "local_nodes_used",
    "overlaps_used",
    "gluing_checks_passed",
    "blocker_propagation_trace",
    "non_collapse_boundary",
    "allowed_projection",
]

ALLOWED_PROJECTIONS = [
    "evidence_receipt",
    "dependency_gap_notice",
    "local_overlap_recheck_request",
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
    "graph_ontology_commit",
]

TRUE_BOUNDARY = [
    "validation_only",
    "candidate_only",
    "local_os_supervision_only",
    "dependent_origination_required",
    "two_truths_gap_required",
    "indranet_local_net_required",
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
    for path in [SPEC, DO, TWO_TRUTHS, KERNEL]:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    dep = json.loads(DO.read_text(encoding="utf-8"))
    two_truths = json.loads(TWO_TRUTHS.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if dep.get("bridge_id") != data.get("attached_dependent_origination_bridge"):
        errors.append("attached dependent-origination bridge mismatch")
    if two_truths.get("bridge_id") != data.get("attached_two_truths_bridge"):
        errors.append("attached two-truths bridge mismatch")
    if kernel.get("kernel_id") != data.get("attached_kernel"):
        errors.append("attached kernel mismatch")

    principle = data.get("indranet_principle", {})
    if "local dependency overlaps" not in principle.get("statement", ""):
        errors.append("IndraNet principle must mention local dependency overlaps")
    if "local_state_i" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention local_state_i")
    if "graph ontology" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must block graph ontology")

    nodes = {item.get("node_id"): item for item in data.get("local_dependency_nodes", []) if isinstance(item, dict)}
    for node_id in REQUIRED_NODES:
        node = nodes.get(node_id)
        if node is None:
            errors.append(f"missing local dependency node: {node_id}")
            continue
        if not node.get("observables"):
            errors.append(f"node must have observables: {node_id}")

    overlaps = {item.get("overlap_id"): item for item in data.get("overlap_relations", []) if isinstance(item, dict)}
    for overlap_id in REQUIRED_OVERLAPS:
        overlap = overlaps.get(overlap_id)
        if overlap is None:
            errors.append(f"missing overlap: {overlap_id}")
            continue
        if len(overlap.get("nodes", [])) < 2:
            errors.append(f"overlap must involve at least two nodes: {overlap_id}")
        if overlap.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"overlap failure_effect must be HOLD or QUARANTINE: {overlap_id}")

    checks = {item.get("check_id"): item for item in data.get("gluing_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_GLUING_CHECKS:
        check = checks.get(check_id)
        if check is None:
            errors.append(f"missing gluing check: {check_id}")
            continue
        if check.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"gluing check failure_effect must be HOLD or QUARANTINE: {check_id}")

    blockers = data.get("blocker_propagation", {})
    for blocker in REQUIRED_BLOCKERS:
        if blocker not in blockers.get("blocker_classes", []):
            errors.append(f"missing blocker class: {blocker}")
    propagation_rules = blockers.get("propagation_rules", [])
    if len(propagation_rules) < len(REQUIRED_BLOCKERS):
        errors.append("not enough blocker propagation rules")
    for rule in propagation_rules:
        if rule.get("result") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"bad blocker propagation result: {rule.get('when')}")

    witness = data.get("indranet_witness_surface", {})
    for field in REQUIRED_WITNESS_FIELDS:
        if field not in witness.get("required_fields", []):
            errors.append(f"missing witness field: {field}")
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

    print("PASS: KuuOS IndraNet OS dependency bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
