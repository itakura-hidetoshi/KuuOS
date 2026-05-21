#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_descent_os_bridge_v0_1.json"
CECH = ROOT / "specs" / "kuuos_cech_obstruction_os_bridge_v0_1.json"
SHEAF = ROOT / "specs" / "kuuos_sheaf_os_gluing_bridge_v0_1.json"
GAUGE = ROOT / "specs" / "kuuos_gauge_os_transport_bridge_v0_1.json"
INDRANET = ROOT / "specs" / "kuuos_indranet_os_dependency_bridge_v0_1.json"
DO = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_descent_os_bridge_v0_1",
    "version": "v0.1",
    "status": "DESCENT_OS_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_cech_obstruction_bridge": "kuuos_cech_obstruction_os_bridge_v0_1",
    "attached_cech_obstruction_spec": "specs/kuuos_cech_obstruction_os_bridge_v0_1.json",
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

REQUIRED_DESCENT = ["D_core_runtime", "D_evidence_lineage", "D_policy_boundary"]
REQUIRED_CHECKS = [
    "ED_cover_present",
    "ED_sections_compatible",
    "ED_obstruction_visible",
    "ED_boundary_preserved",
    "ED_global_candidate_not_identity",
]
REQUIRED_OUTCOMES = [
    "EFFECTIVE_DESCENT_CANDIDATE",
    "NON_EFFECTIVE_DESCENT_HOLD",
    "NON_EFFECTIVE_DESCENT_QUARANTINE",
]
REQUIRED_WITNESS_FIELDS = [
    "cycle_id",
    "kernel_state",
    "cover_used",
    "descent_data_used",
    "effective_descent_checks_run",
    "obstruction_status",
    "descent_outcome",
    "non_reification_boundary",
    "allowed_projection",
]
ALLOWED_PROJECTIONS = [
    "descent_candidate_receipt",
    "descent_gap_notice",
    "hold_notice",
    "repair_candidate_request",
    "quarantine_notice",
]
FORBIDDEN_PROJECTIONS = [
    "truth_commit",
    "memory_overwrite_commit",
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
    "descent_required",
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
    paths = [SPEC, CECH, SHEAF, GAUGE, INDRANET, DO, TWO_TRUTHS, KERNEL]
    for path in paths:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    cech = json.loads(CECH.read_text(encoding="utf-8"))
    sheaf = json.loads(SHEAF.read_text(encoding="utf-8"))
    gauge = json.loads(GAUGE.read_text(encoding="utf-8"))
    indranet = json.loads(INDRANET.read_text(encoding="utf-8"))
    dep = json.loads(DO.read_text(encoding="utf-8"))
    two_truths = json.loads(TWO_TRUTHS.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if cech.get("bridge_id") != data.get("attached_cech_obstruction_bridge"):
        errors.append("attached Cech obstruction bridge mismatch")
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

    principle = data.get("descent_principle", {})
    if "descent data" not in principle.get("statement", ""):
        errors.append("descent principle must mention descent data")
    if "effective_descent" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention effective_descent")
    if "candidate-level witness" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must preserve candidate witness")

    descent = {item.get("descent_id"): item for item in data.get("descent_data", []) if isinstance(item, dict)}
    for descent_id in REQUIRED_DESCENT:
        item = descent.get(descent_id)
        if item is None:
            errors.append(f"missing descent data: {descent_id}")
            continue
        if not item.get("cover"):
            errors.append(f"descent data must have cover: {descent_id}")
        if not item.get("local_sections"):
            errors.append(f"descent data must have local sections: {descent_id}")
        if not item.get("candidate_projection"):
            errors.append(f"descent data must have candidate projection: {descent_id}")

    checks = {item.get("check_id"): item for item in data.get("effective_descent_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_CHECKS:
        item = checks.get(check_id)
        if item is None:
            errors.append(f"missing effective descent check: {check_id}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"effective descent failure_effect must be HOLD or QUARANTINE: {check_id}")

    outcomes = {item.get("outcome"): item for item in data.get("descent_outcomes", []) if isinstance(item, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing descent outcome: {outcome}")
            continue
        if not item.get("allowed_projection"):
            errors.append(f"descent outcome must have allowed projection: {outcome}")

    witness = data.get("descent_witness_surface", {})
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

    print("PASS: KuuOS Descent OS bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
