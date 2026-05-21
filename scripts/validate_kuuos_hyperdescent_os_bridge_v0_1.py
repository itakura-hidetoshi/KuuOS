#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_hyperdescent_os_bridge_v0_1.json"
DESCENT = ROOT / "specs" / "kuuos_descent_os_bridge_v0_1.json"
CECH = ROOT / "specs" / "kuuos_cech_obstruction_os_bridge_v0_1.json"
SHEAF = ROOT / "specs" / "kuuos_sheaf_os_gluing_bridge_v0_1.json"
GAUGE = ROOT / "specs" / "kuuos_gauge_os_transport_bridge_v0_1.json"
INDRANET = ROOT / "specs" / "kuuos_indranet_os_dependency_bridge_v0_1.json"
DO = ROOT / "specs" / "kuuos_dependent_origination_os_bridge_v0_1.json"
TWO_TRUTHS = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_hyperdescent_os_bridge_v0_1",
    "version": "v0.1",
    "status": "HYPERDESCENT_OS_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_descent_bridge": "kuuos_descent_os_bridge_v0_1",
    "attached_descent_spec": "specs/kuuos_descent_os_bridge_v0_1.json",
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
REQUIRED_LEVELS = ["R0_base_cover", "R1_refined_overlap_cover", "R2_higher_coherence_cover"]
REQUIRED_CHECKS = ["HC_refinement_stability", "HC_overlap_coherence_visible", "HC_holonomy_noncollapse", "HC_candidate_not_identity"]
REQUIRED_DEBTS = ["CD_refinement_gap", "CD_overlap_gap", "CD_boundary_gap"]
REQUIRED_OUTCOMES = ["HYPERDESCENT_CANDIDATE", "HYPERDESCENT_HOLD", "HYPERDESCENT_QUARANTINE"]
REQUIRED_WITNESS_FIELDS = ["cycle_id", "kernel_state", "refinement_levels_used", "higher_coherence_checks_run", "coherence_debt", "hyperdescent_outcome", "non_reification_boundary", "allowed_projection"]
ALLOWED_PROJECTIONS = ["hyperdescent_candidate_receipt", "coherence_debt_notice", "reobserve_request", "hold_notice", "repair_candidate_request", "quarantine_notice"]
FORBIDDEN_PROJECTIONS = ["truth_commit", "execution_commit", "memory_overwrite_commit", "clinical_commit", "theorem_commit", "global_truth_object_commit", "completed_os_identity_commit", "silent_pass_commit"]
TRUE_BOUNDARY = ["validation_only", "candidate_only", "local_os_supervision_only", "dependent_origination_required", "two_truths_gap_required", "indranet_local_net_required", "gauge_transport_required", "sheaf_gluing_required", "cech_obstruction_required", "descent_required", "hyperdescent_required"]
FALSE_BOUNDARY = ["grants_execution_authority", "grants_clinical_authority", "grants_diagnosis_authority", "grants_treatment_authority", "grants_theorem_authority", "grants_truth_authority", "grants_memory_overwrite_authority", "grants_governance_bypass_authority"]


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for path in [SPEC, DESCENT, CECH, SHEAF, GAUGE, INDRANET, DO, TWO_TRUTHS, KERNEL]:
        if not path.is_file():
            print(f"ERROR: missing {path.relative_to(ROOT)}")
            return 1

    data = load(SPEC)
    descent = load(DESCENT)
    cech = load(CECH)
    sheaf = load(SHEAF)
    gauge = load(GAUGE)
    indranet = load(INDRANET)
    dep = load(DO)
    two_truths = load(TWO_TRUTHS)
    kernel = load(KERNEL)

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if descent.get("bridge_id") != data.get("attached_descent_bridge"):
        errors.append("attached descent bridge mismatch")
    if cech.get("bridge_id") != data.get("attached_cech_obstruction_bridge"):
        errors.append("attached Cech bridge mismatch")
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

    principle = data.get("hyperdescent_principle", {})
    if "iterated cover refinement" not in principle.get("statement", ""):
        errors.append("principle must mention iterated cover refinement")
    if "hyperdescent_candidate" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula must mention hyperdescent_candidate")
    if "candidate-level evidence" not in principle.get("non_reification_rule", ""):
        errors.append("non_reification_rule must preserve candidate evidence")

    levels = {x.get("level_id"): x for x in data.get("refinement_levels", []) if isinstance(x, dict)}
    for level in REQUIRED_LEVELS:
        item = levels.get(level)
        if item is None:
            errors.append(f"missing refinement level: {level}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"bad refinement failure_effect: {level}")

    checks = {x.get("check_id"): x for x in data.get("higher_coherence_checks", []) if isinstance(x, dict)}
    for check in REQUIRED_CHECKS:
        item = checks.get(check)
        if item is None:
            errors.append(f"missing higher coherence check: {check}")
            continue
        if item.get("failure_effect") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"bad higher coherence failure_effect: {check}")

    debts = {x.get("debt_id"): x for x in data.get("coherence_debt_classes", []) if isinstance(x, dict)}
    for debt in REQUIRED_DEBTS:
        item = debts.get(debt)
        if item is None:
            errors.append(f"missing coherence debt: {debt}")
            continue
        if item.get("result_state") not in {"HOLD", "QUARANTINE"}:
            errors.append(f"bad coherence debt result_state: {debt}")

    outcomes = {x.get("outcome"): x for x in data.get("hyperdescent_outcomes", []) if isinstance(x, dict)}
    for outcome in REQUIRED_OUTCOMES:
        item = outcomes.get(outcome)
        if item is None:
            errors.append(f"missing outcome: {outcome}")
            continue
        if not item.get("allowed_projection"):
            errors.append(f"outcome missing allowed projection: {outcome}")

    witness = data.get("hyperdescent_witness_surface", {})
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
    print("PASS: KuuOS Hyperdescent OS bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
