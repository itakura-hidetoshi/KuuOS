#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_cech_obstruction_os_bridge_v0_1.json"
SHEAF = ROOT / "specs" / "kuuos_sheaf_os_gluing_bridge_v0_1.json"
GAUGE = ROOT / "specs" / "kuuos_gauge_os_transport_bridge_v0_1.json"
INDRANET = ROOT / "specs" / "kuuos_indranet_os_dependency_bridge_v0_1.json"
DO = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_cech_obstruction_os_bridge_v0_1",
    "version": "v0.1",
    "status": "CECH_OBSTRUCTION_OS_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_sheaf_bridge": "kuuos_sheaf_os_gluing_bridge_v0_1",
    "attached_sheaf_spec": "specs/kuuos_sheaf_os_gluing_bridge_v0_1.json",
    "attached_gauge_bridge": "kuuos_gauge_os_transport_bridge_v0_1",
    "attached_gauge_spec": "specs/kuuos_gauge_os_transport_bridge_v0_1.json",
    "attached_indranet_bridge": "kuuos_indranet_os_dependency_bridge_v0_1",
    "attached_indranet_spec": "specs/kuuos_indranet_os_dependency_bridge_v0_1.json",
    "attached_dependent_origination_bridge": "kuuos_dependent_origination_os_bridge_v0_1",
    "attached_dependent_origination_spec": "specs/kuuos_dependent_origination_os_bridge_v0_1.json",
    "attached_two_truths_bridge": "kuuos_two_truths_os_bridge_v0_1",
    "attached_two_truths_bridge_spec": "specs/kuuos_two_truths_os_bridge_v0_1.json",
    "attached_kernel": "kuuos_os_autonomy_kernel_v0_1",
    "attached_kernel_spec": "specs/kuuos_os_autonomy_kernel_v0_1.json",
}

REQUIRED_LEVELS = ["C0", "C1", "C2"]
REQUIRED_OBSTRUCTIONS = [
    "O_missing_section",
    "O_restriction_mismatch",
    "O_lineage_gap",
    "O_non_authority_gluing_failure",
    "O_global_truth_reification",
]
REQUIRED_COCYCLE_CHECKS = [
    "pairwise_overlap_compatibility",
    "lineage_boundary_cocycle",
    "global_non_reification_cocycle",
]
REQUIRED_REPAIRS = [
    "R_add_missing_section",
    "R_refine_restriction_map",
    "R_recheck_lineage_hash_chain",
    "R_strengthen_boundary_gap",
]
REQUIRED_WITNESS_FIELDS = [
    "cycle_id",
    "kernel_state",
    "cover_used",
    "cochain_level",
    "cocycle_checks_run",
    "obstruction_classes_detected",
    "candidate_repairs_opened",
    "non_reification_boundary",
    "allowed_projection",
]
ALLOWED_PROJECTIONS = [
    "obstruction_notice",
    "local_section_recheck_request",
    "restriction_gap_notice",
    "lineage_recheck_request",
    "boundary_recheck_request",
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
    "global_truth_object_commit",
    "completed_os_identity_commit",
    "silent_pass_commit",
]
TRUE_BOUNDARY = [
    "validation_only",
    "candidate_only",
    "local_os_supervision_only",
    "dependent_origination_required",
    "two_truths_gap_required",
    "indranet_local_net_required",
    "gauge_transport_required",
    "sheaf_gluing_required",
    "cech_obstruction_required",
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
    for path in [SPEC, SHEAF, GAUGE, INDRANET, DO, TWO_TRUTHS, KERNEL]:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    sheaf = json.loads(SHEAF.read_text(encoding="utf-8"))
    gauge = json.loads(GAUGE.read_text(encoding="utf-8"))
    indranet = json.loads(INDRANET.read_text(encoding="utf-8"))
    dep = json.loads(DO.read_text(encoding="utf-8"))
    two_truths = json.loads(TWO_TRUTHS.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if sheaf.get("bridge_id") != data.get("attached_sheaf_bridge"):
        errors.append("attached sheaf bridge mismatch")
    if gauge.get("bridge_id") != data.get("attached_gauge_bridge"):
        errors.append("attached gauge bridge mismatch")
    if indranet.get("bridge_id") != data.get("attached_indranet_bridge"):
        errors.append("attached IndraNet bridge mismatch")
    if dep.get("bridge_id") != data.get("attached_dependent_origination_bridge"):
        errors.append("attached dependent-origination bridge mismatch")
    if two_truths.get("bridge_id") != data.get("attached_two_truths_bridge"):
        errors.append("attached two-truths bridge mismatch")
    if kernel.get("kernel_id") != data.get("attached_kernel"):
        errors.append("attached kernel mismatch")

    principle = data.get("obstruction_principle", {})
    if "cannot be glued" not in principle.get("statement", ""):
        errors.append("obstruction principle must mention gluing failure")
    if "obstruction_class" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention obstruction_class")
    if "diagnostic witness" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must mark obstruction as diagnostic witness")

    levels = {item.get("level"): item for item in data.get("cochain_levels", []) if isinstance(item, dict)}
    for level in REQUIRED_LEVELS:
        item = levels.get(level)
        if item is None:
            errors.append(f"missing cochain level: {level}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"cochain failure_effect must be HOLD or QUARANTINE: {level}")

    obstructions = {item.get("obstruction_id"): item for item in data.get("obstruction_classes", []) if isinstance(item, dict)}
    for obstruction_id in REQUIRED_OBSTRUCTIONS:
        item = obstructions.get(obstruction_id)
        if item is None:
            errors.append(f"missing obstruction class: {obstruction_id}")
            continue
        if item.get("level") not in REQUIRED_LEVELS:
            errors.append(f"obstruction level invalid: {obstruction_id}")
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"obstruction failure_effect must be HOLD or QUARANTINE: {obstruction_id}")
        if not item.get("opens"):
            errors.append(f"obstruction must open projection: {obstruction_id}")

    cocycles = {item.get("check_id"): item for item in data.get("cocycle_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_COCYCLE_CHECKS:
        item = cocycles.get(check_id)
        if item is None:
            errors.append(f"missing cocycle check: {check_id}")
            continue
        if not item.get("detects"):
            errors.append(f"cocycle check must detect obstruction: {check_id}")
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"cocycle failure_effect must be HOLD or QUARANTINE: {check_id}")

    repairs = {item.get("repair_id"): item for item in data.get("coboundary_repair_candidates", []) if isinstance(item, dict)}
    for repair_id in REQUIRED_REPAIRS:
        item = repairs.get(repair_id)
        if item is None:
            errors.append(f"missing repair candidate: {repair_id}")
            continue
        if item.get("candidate_only") is not True:
            errors.append(f"repair candidate must be candidate_only: {repair_id}")
        if not item.get("targets"):
            errors.append(f"repair candidate must target obstruction: {repair_id}")

    witness = data.get("obstruction_witness_surface", {})
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

    print("PASS: KuuOS Cech obstruction OS bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
