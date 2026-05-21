#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_gauge_os_transport_bridge_v0_1.json"
INDRANET = ROOT / "specs" / "kuuos_indranet_os_dependency_bridge_v0_1.json"
DO = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_gauge_os_transport_bridge_v0_1",
    "version": "v0.1",
    "status": "GAUGE_OS_TRANSPORT_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_indranet_bridge": "kuuos_indranet_os_dependency_bridge_v0_1",
    "attached_indranet_spec": "specs/kuuos_indranet_os_dependency_bridge_v0_1.json",
    "attached_dependent_origination_bridge": "kuuos_dependent_origination_os_bridge_v0_1",
    "attached_dependent_origination_spec": "specs/kuuos_dependent_origination_os_bridge_v0_1.json",
    "attached_two_truths_bridge": "kuuos_two_truths_os_bridge_v0_1",
    "attached_two_truths_bridge_spec": "specs/kuuos_two_truths_os_bridge_v0_1.json",
    "attached_kernel": "kuuos_os_autonomy_kernel_v0_1",
    "attached_kernel_spec": "specs/kuuos_os_autonomy_kernel_v0_1.json",
}

REQUIRED_CHARTS = ["repo_chart", "policy_chart", "module_chart", "lineage_chart", "boundary_chart"]
REQUIRED_TRANSPORTS = [
    "repo_to_policy_transport",
    "policy_to_module_transport",
    "module_to_lineage_transport",
    "lineage_to_boundary_transport",
    "boundary_to_repo_transport",
]
REQUIRED_HOLONOMY = [
    "cycle_transport_noncollapse",
    "lineage_transport_receipt_only",
    "policy_module_transport_bounded",
]
REQUIRED_WITNESS_FIELDS = [
    "cycle_id",
    "kernel_state",
    "charts_used",
    "transports_used",
    "holonomy_checks_passed",
    "preserved_quantities",
    "blocked_promotions",
    "non_reification_boundary",
    "allowed_projection",
]
ALLOWED_PROJECTIONS = [
    "gauge_transport_receipt",
    "local_chart_recheck_request",
    "holonomy_gap_notice",
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
    "world_identity_commit",
    "graph_ontology_commit",
]
TRUE_BOUNDARY = [
    "validation_only",
    "candidate_only",
    "local_os_supervision_only",
    "dependent_origination_required",
    "two_truths_gap_required",
    "indranet_local_net_required",
    "gauge_transport_required",
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
    for path in [SPEC, INDRANET, DO, TWO_TRUTHS, KERNEL]:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    indranet = json.loads(INDRANET.read_text(encoding="utf-8"))
    dep = json.loads(DO.read_text(encoding="utf-8"))
    two_truths = json.loads(TWO_TRUTHS.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if indranet.get("bridge_id") != data.get("attached_indranet_bridge"):
        errors.append("attached IndraNet bridge mismatch")
    if dep.get("bridge_id") != data.get("attached_dependent_origination_bridge"):
        errors.append("attached dependent-origination bridge mismatch")
    if two_truths.get("bridge_id") != data.get("attached_two_truths_bridge"):
        errors.append("attached two-truths bridge mismatch")
    if kernel.get("kernel_id") != data.get("attached_kernel"):
        errors.append("attached kernel mismatch")

    principle = data.get("gauge_principle", {})
    if "local charts" not in principle.get("statement", ""):
        errors.append("gauge principle must mention local charts")
    if "transport_ij" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention transport_ij")
    if "worlds" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must block identity of worlds")

    charts = {item.get("chart_id"): item for item in data.get("local_charts", []) if isinstance(item, dict)}
    for chart_id in REQUIRED_CHARTS:
        chart = charts.get(chart_id)
        if chart is None:
            errors.append(f"missing chart: {chart_id}")
            continue
        if not chart.get("coordinates"):
            errors.append(f"chart must have coordinates: {chart_id}")
        if not chart.get("blocked_projection"):
            errors.append(f"chart must block projections: {chart_id}")

    transports = {item.get("transport_id"): item for item in data.get("gauge_transports", []) if isinstance(item, dict)}
    for transport_id in REQUIRED_TRANSPORTS:
        transport = transports.get(transport_id)
        if transport is None:
            errors.append(f"missing transport: {transport_id}")
            continue
        if transport.get("from_chart") not in charts:
            errors.append(f"transport from_chart missing: {transport_id}")
        if transport.get("to_chart") not in charts:
            errors.append(f"transport to_chart missing: {transport_id}")
        if not transport.get("preserves"):
            errors.append(f"transport must preserve quantities: {transport_id}")
        if transport.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"transport failure_effect must be HOLD or QUARANTINE: {transport_id}")

    holonomy = {item.get("check_id"): item for item in data.get("holonomy_checks", []) if isinstance(item, dict)}
    for check_id in REQUIRED_HOLONOMY:
        check = holonomy.get(check_id)
        if check is None:
            errors.append(f"missing holonomy check: {check_id}")
            continue
        if len(check.get("cycle", [])) < 3:
            errors.append(f"holonomy cycle too short: {check_id}")
        if not check.get("must_preserve"):
            errors.append(f"holonomy check must preserve quantities: {check_id}")
        if check.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"holonomy failure_effect must be HOLD or QUARANTINE: {check_id}")

    witness = data.get("gauge_witness_surface", {})
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

    print("PASS: KuuOS Gauge OS transport bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
