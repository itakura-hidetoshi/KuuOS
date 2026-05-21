#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_sheaf_os_gluing_bridge_v0_1.json"
GAUGE = ROOT / "specs" / "kuuos_gauge_os_transport_bridge_v0_1.json"
INDRANET = ROOT / "specs" / "kuuos_indranet_os_dependency_bridge_v0_1.json"
DO = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_sheaf_os_gluing_bridge_v0_1",
    "version": "v0.1",
    "status": "SHEAF_OS_GLUING_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
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

REQUIRED_SITE_OBJECTS = ["repo_chart", "policy_chart", "module_chart", "lineage_chart", "boundary_chart"]
REQUIRED_COVERS = ["core_runtime_cover", "evidence_lineage_cover", "policy_boundary_cover"]
REQUIRED_SECTIONS = ["repo_section", "policy_section", "module_section", "lineage_section", "boundary_section"]
REQUIRED_RESTRICTIONS = [
    "repo_policy_restriction",
    "policy_module_restriction",
    "module_lineage_restriction",
    "lineage_boundary_restriction",
    "boundary_repo_restriction",
]
REQUIRED_GLUING = [
    "local_sections_present",
    "overlap_restrictions_compatible",
    "non_authority_boundary_glues",
    "global_candidate_not_truth",
]
REQUIRED_OBSTRUCTIONS = [
    "missing_local_section",
    "restriction_mismatch",
    "non_authority_gluing_failure",
    "global_truth_reification",
]
REQUIRED_WITNESS_FIELDS = [
    "cycle_id",
    "kernel_state",
    "cover_used",
    "local_sections_used",
    "restriction_maps_checked",
    "gluing_conditions_passed",
    "obstructions",
    "non_reification_boundary",
    "allowed_projection",
]
ALLOWED_PROJECTIONS = [
    "sheaf_gluing_receipt",
    "local_section_recheck_request",
    "restriction_gap_notice",
    "obstruction_notice",
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
    for path in [SPEC, GAUGE, INDRANET, DO, TWO_TRUTHS, KERNEL]:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    gauge = json.loads(GAUGE.read_text(encoding="utf-8"))
    indranet = json.loads(INDRANET.read_text(encoding="utf-8"))
    dep = json.loads(DO.read_text(encoding="utf-8"))
    two_truths = json.loads(TWO_TRUTHS.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

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

    principle = data.get("sheaf_principle", {})
    if "local sections" not in principle.get("statement", ""):
        errors.append("sheaf principle must mention local sections")
    if "global_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention global_candidate")
    if "global truth object" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must block global truth object")

    site = data.get("base_site", {})
    for obj in REQUIRED_SITE_OBJECTS:
        if obj not in site.get("objects", []):
            errors.append(f"missing site object: {obj}")
    covers = {item.get("cover_id"): item for item in site.get("covering_families", []) if isinstance(item, dict)}
    for cover_id in REQUIRED_COVERS:
        cover = covers.get(cover_id)
        if cover is None:
            errors.append(f"missing cover: {cover_id}")
            continue
        if not cover.get("members"):
            errors.append(f"cover must have members: {cover_id}")

    sections = {item.get("section_id"): item for item in data.get("local_sections", []) if isinstance(item, dict)}
    for section_id in REQUIRED_SECTIONS:
        section = sections.get(section_id)
        if section is None:
            errors.append(f"missing local section: {section_id}")
            continue
        if section.get("over_chart") not in REQUIRED_SITE_OBJECTS:
            errors.append(f"section over_chart not in site: {section_id}")
        if not section.get("carries"):
            errors.append(f"section must carry data: {section_id}")
        if not section.get("forbidden_projection"):
            errors.append(f"section must block projections: {section_id}")

    restrictions = {item.get("restriction_id"): item for item in data.get("restriction_maps", []) if isinstance(item, dict)}
    for restriction_id in REQUIRED_RESTRICTIONS:
        restriction = restrictions.get(restriction_id)
        if restriction is None:
            errors.append(f"missing restriction: {restriction_id}")
            continue
        if restriction.get("from_section") not in sections:
            errors.append(f"restriction from_section missing: {restriction_id}")
        if not restriction.get("must_preserve"):
            errors.append(f"restriction must preserve quantities: {restriction_id}")
        if restriction.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"restriction failure_effect must be HOLD or QUARANTINE: {restriction_id}")

    gluing = {item.get("condition_id"): item for item in data.get("gluing_conditions", []) if isinstance(item, dict)}
    for condition_id in REQUIRED_GLUING:
        condition = gluing.get(condition_id)
        if condition is None:
            errors.append(f"missing gluing condition: {condition_id}")
            continue
        if condition.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"gluing condition failure_effect must be HOLD or QUARANTINE: {condition_id}")

    obstructions = {item.get("obstruction_id"): item for item in data.get("obstruction_classes", []) if isinstance(item, dict)}
    for obstruction_id in REQUIRED_OBSTRUCTIONS:
        obstruction = obstructions.get(obstruction_id)
        if obstruction is None:
            errors.append(f"missing obstruction: {obstruction_id}")
            continue
        if obstruction.get("effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"obstruction effect must be HOLD or QUARANTINE: {obstruction_id}")

    witness = data.get("sheaf_witness_surface", {})
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

    print("PASS: KuuOS Sheaf OS gluing bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
