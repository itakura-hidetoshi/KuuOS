#!/usr/bin/env python3
"""Validate Physical Quantum Qi deepening contract v0.2."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "physical_quantum_qi_deepening_contract_v0_2.json"
EXAMPLE_PATH = ROOT / "examples" / "physical_quantum_qi_deepening_packet_v0_2.json"
CASES_PATH = ROOT / "validation_cases" / "physical_quantum_qi_deepening_validation_cases_v0_2.json"

EXPECTED_FULLPATH_STATUS = "memory_recordable_reflection_analyzable_candidate"
EXPECTED_FULLPATH_SURFACES = {
    "BeliefOS.observation_candidate",
    "PlanOS.transport_candidate",
    "DecisionOS.safety_evaluable_candidate",
    "MemoryOS.recordable_history_candidate",
    "ReflectionOS.residue_analysis_candidate",
}

REQUIRED_MODULES = [
    "SK_FV_path_integral",
    "SK_FV_Qi_action_v0_2A",
    "Qi_non_Markov_memory_v0_2E",
    "Ward_leak_identity",
    "Ward_leak_identity_v0_2B",
    "DPI_recoverability",
    "IndraNet_gauge_transport",
    "KuString_Qi_emergence_bridge",
    "Qi_OS_handoff",
]

REQUIRED_QI_NON_MARKOV_RULES = {
    "Qi_memory_is_primary_non_Markovian_semantics",
    "Markov_reduction_is_forbidden_as_Qi_semantics",
    "finite_window_projection_is_history_preserving_not_Markov_substitute",
    "discarded_history_must_leave_visible_tail_residue",
    "holonomy_history_cannot_be_erased",
    "boundary_leak_history_cannot_be_erased",
    "rollback_history_cannot_be_erased",
    "recovery_failure_cannot_be_erased",
    "current_state_only_recovery_judgment_is_forbidden",
    "current_state_only_transport_judgment_is_forbidden",
    "compression_must_preserve_source_history_or_visible_residual_debt",
    "Qi_non_Markov_memory_grants_no_authority",
}

REQUIRED_QI_NON_MARKOV_DENIES = {
    "Markov_reduction_as_Qi_semantics",
    "Markov_chart_as_semantic_substitute",
    "Markov_snapshot_claimed_as_FullPathQi",
    "current_state_only_Qi_identity",
    "current_state_only_recoverability",
    "current_state_only_transport_safety",
    "finite_window_without_tail_residue",
    "discarded_tail_residue_hidden",
    "holonomy_tail_residue_hidden",
    "boundary_leak_tail_residue_hidden",
    "recovery_tail_debt_hidden",
    "rollback_tail_debt_hidden",
    "fresh_valid_path_erasing_prior_holonomy_history",
    "repair_success_erasing_rollback_history",
    "positive_local_recovery_erasing_recovery_debt",
    "compression_as_deletion",
    "compressed_memory_replacing_source_history",
    "Qi_memory_grants_execution_authority",
    "Qi_memory_grants_truth_authority",
}

REQUIRED_QI_NON_MARKOV_INVARIANTS = {
    "Qi memory is primary non-Markovian semantics",
    "Markov reduction is forbidden as Qi semantics",
    "Finite-window Qi memory projection is history-preserving and not a Markov substitute",
    "Current-state-only Qi identity is forbidden",
    "Current-state-only recoverability is forbidden",
    "Current-state-only transport safety is forbidden",
    "Discarded Qi history must leave visible tail residue",
    "Holonomy history cannot be erased",
    "Boundary leak history cannot be erased",
    "Rollback history and recovery failure cannot be erased",
    "Compressed Qi memory cannot replace source history",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def is_pass(value: Any) -> bool:
    return value == "pass" or value is True


def authority_clear(packet: Dict[str, Any], authority_keys: List[str]) -> bool:
    authority = packet.get("authority", {})
    return all(authority.get(key) is False for key in authority_keys)


def module_errors(packet: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    modules = packet.get("modules", {})
    for module_name, module_spec in spec.get("deepening_modules", {}).items():
        if module_name not in modules:
            continue
        payload = modules.get(module_name, {})
        for key in module_spec.get("required", []):
            if not is_pass(payload.get(key)):
                errors.append(f"{module_name}.{key} is required")

        if module_name == "SK_FV_Qi_action_v0_2A":
            if not is_pass(payload.get("D_R_causal")):
                errors.append("SK_FV_Qi_action_v0_2A requires causal D_R kernel")
            if not is_pass(payload.get("N_positive_semidefinite")):
                errors.append("SK_FV_Qi_action_v0_2A requires positive semidefinite noise kernel")
            if not is_pass(payload.get("FDR_convention_declared")):
                errors.append("SK_FV_Qi_action_v0_2A requires declared FDR convention")
            if payload.get("Markov_snapshot_claimed_as_FullPathQi") is True and not is_pass(payload.get("markov_reduction_receipt_declared_if_used")):
                errors.append("SK_FV_Qi_action_v0_2A rejects Markov snapshot as FullPathQi without reduction receipt")
            if payload.get("barrier_claimed_as_qi_source") is True or not is_pass(payload.get("barrier_not_qi_source_declared")):
                errors.append("SK_FV_Qi_action_v0_2A requires barrier floor not Qi source")

        if module_name == "Qi_non_Markov_memory_v0_2E":
            if not is_pass(payload.get("qi_memory_primary")):
                errors.append("Qi_non_Markov_memory_v0_2E requires primary Qi memory")
            if not is_pass(payload.get("qi_is_non_markovian_by_definition")):
                errors.append("Qi_non_Markov_memory_v0_2E requires Qi to be non-Markovian by definition")
            if not is_pass(payload.get("markov_reduction_forbidden_as_qi_semantics")):
                errors.append("Qi_non_Markov_memory_v0_2E rejects Markov reduction as Qi semantics")
            if not is_pass(payload.get("current_state_only_identity_forbidden")):
                errors.append("Qi_non_Markov_memory_v0_2E rejects current-state-only Qi identity")
            if not is_pass(payload.get("current_state_only_recoverability_forbidden")):
                errors.append("Qi_non_Markov_memory_v0_2E rejects current-state-only recoverability")
            if not is_pass(payload.get("current_state_only_transport_safety_forbidden")):
                errors.append("Qi_non_Markov_memory_v0_2E rejects current-state-only transport safety")
            if payload.get("markov_semantic_substitute") is True:
                errors.append("Qi_non_Markov_memory_v0_2E rejects finite-window Markov semantic substitutes")
            if not is_pass(payload.get("discarded_tail_residue_declared")):
                errors.append("Qi_non_Markov_memory_v0_2E requires discarded tail residue visibility")
            if not is_pass(payload.get("holonomy_tail_residue_declared")):
                errors.append("Qi_non_Markov_memory_v0_2E requires holonomy tail residue visibility")
            if not is_pass(payload.get("boundary_leak_tail_residue_declared")):
                errors.append("Qi_non_Markov_memory_v0_2E requires boundary leak tail residue visibility")
            if payload.get("fresh_valid_path_erases_prior_holonomy_history") is True:
                errors.append("Qi_non_Markov_memory_v0_2E rejects fresh valid path erasing prior holonomy history")
            if payload.get("repair_success_erases_rollback_history") is True:
                errors.append("Qi_non_Markov_memory_v0_2E rejects repair success erasing rollback history")
            if payload.get("positive_local_recovery_erases_recovery_debt") is True:
                errors.append("Qi_non_Markov_memory_v0_2E rejects positive local recovery erasing recovery debt")
            if payload.get("compression_as_deletion") is True:
                errors.append("Qi_non_Markov_memory_v0_2E rejects compression as deletion")
            if not is_pass(payload.get("compressed_memory_cannot_replace_source_history")):
                errors.append("Qi_non_Markov_memory_v0_2E requires compressed memory not to replace source history")

        if module_name == "Ward_leak_identity_v0_2B":
            if not is_pass(payload.get("A_mu_variation_declared")):
                errors.append("Ward_leak_identity_v0_2B requires J_Qi as action variation with respect to A_mu")
            if not is_pass(payload.get("D_mu_J_declared")):
                errors.append("Ward_leak_identity_v0_2B requires covariant divergence D_mu J")
            if not is_pass(payload.get("open_or_closed_case_declared")):
                errors.append("Ward_leak_identity_v0_2B requires open/closed case declaration")
            if payload.get("open_system_trace_declared") is True and not is_pass(payload.get("L_leak_declared")):
                errors.append("Ward_leak_identity_v0_2B open system requires L_leak")
            if not is_pass(payload.get("W_leak_residual_declared")):
                errors.append("Ward_leak_identity_v0_2B requires W_leak residual")
            value = payload.get("W_leak_residual_value")
            if isinstance(value, (int, float)) and abs(value) > 0:
                errors.append("Ward_leak_identity_v0_2B nonzero W_leak residual blocks PhysicalQi/FullPathQi")
            if payload.get("closed_conservation_claimed") is True and payload.get("open_system_trace_declared") is True:
                errors.append("Ward_leak_identity_v0_2B rejects closed conservation claim with open trace")
            if payload.get("anomaly_hidden_as_leak") is True:
                errors.append("Ward_leak_identity_v0_2B rejects anomaly hidden as leak")
            if payload.get("leak_residual_hidden") is True:
                errors.append("Ward_leak_identity_v0_2B rejects hidden leak residual")

        if module_name == "DPI_recoverability":
            if payload.get("rollback_or_repair_claimed") is True:
                value = payload.get("delta_rec_value")
                if not isinstance(value, (int, float)):
                    errors.append("DPI_recoverability.delta_rec_value must be numeric when recovery is claimed")
                elif value <= 0:
                    errors.append("DPI_recoverability rollback/repair requires delta_rec_value > 0")

        if module_name == "IndraNet_gauge_transport":
            if not is_pass(payload.get("IndraNet_not_graph_only")):
                errors.append("IndraNet_gauge_transport rejects graph-only transport")
            if not is_pass(payload.get("A_mu_defined")):
                errors.append("IndraNet_gauge_transport requires A_mu gauge connection")

        if module_name == "KuString_Qi_emergence_bridge":
            if not is_pass(payload.get("K_non_reification")):
                errors.append("KuString_Qi_emergence_bridge requires K non-reification")
            if not is_pass(payload.get("mass_gap_floor_not_Qi_source")):
                errors.append("KuString_Qi_emergence_bridge requires mass gap as floor, not Qi source")

        if module_name == "Qi_OS_handoff":
            if payload.get("FullPathQi_status") != EXPECTED_FULLPATH_STATUS:
                errors.append("Qi_OS_handoff.FullPathQi_status mismatch")
            surfaces = payload.get("allowed_surfaces", [])
            if not isinstance(surfaces, list):
                errors.append("Qi_OS_handoff.allowed_surfaces must be a list")
            else:
                missing = sorted(EXPECTED_FULLPATH_SURFACES - set(surfaces))
                for surface in missing:
                    errors.append(f"Qi_OS_handoff.allowed_surfaces missing {surface}")
    return errors


def baseline_boundary_errors(packet: Dict[str, Any]) -> List[str]:
    if "baseline_established_final_declaration" not in packet:
        return []
    declaration = packet.get("baseline_established_final_declaration", {})
    if not isinstance(declaration, dict):
        return ["baseline_established_final_declaration must be an object"]
    if declaration.get("authority_boundary_complete") is not True:
        return ["baseline_established_final_declaration.authority_boundary_complete must be true"]
    return []


def validate_packet(packet: Dict[str, Any], spec: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if not authority_clear(packet, spec.get("authority_must_be_false", [])):
        errors.append("v0.2 deepening packet attempted to grant forbidden authority")
    errors.extend(module_errors(packet, spec))
    errors.extend(baseline_boundary_errors(packet))
    return (len(errors) == 0), errors


def validate_spec(spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if spec.get("schema_id") != "physical_quantum_qi_deepening_contract_v0_2":
        errors.append("schema_id mismatch")
    if spec.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if spec.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    modules = spec.get("deepening_modules", {})
    for module in REQUIRED_MODULES:
        if module not in modules:
            errors.append(f"missing module {module}")
    qi_non_markov = modules.get("Qi_non_Markov_memory_v0_2E", {})
    missing_rules = sorted(REQUIRED_QI_NON_MARKOV_RULES - set(qi_non_markov.get("rules", [])))
    for rule in missing_rules:
        errors.append(f"Qi_non_Markov_memory_v0_2E missing rule {rule}")
    missing_denies = sorted(REQUIRED_QI_NON_MARKOV_DENIES - set(qi_non_markov.get("denies", [])))
    for denied in missing_denies:
        errors.append(f"Qi_non_Markov_memory_v0_2E missing denies {denied}")
    invariants = set(spec.get("cross_module_invariants", []))
    missing_invariants = sorted(REQUIRED_QI_NON_MARKOV_INVARIANTS - invariants)
    for invariant in missing_invariants:
        errors.append(f"cross_module_invariants missing {invariant}")
    if not spec.get("cross_module_invariants"):
        errors.append("cross_module_invariants must be nonempty")
    return errors


def validate_cases(cases_doc: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for case in cases_doc.get("cases", []):
        name = case.get("name", "<unnamed>")
        if "packet_ref" in case:
            packet = load_json(ROOT / case["packet_ref"])
        else:
            packet = case.get("packet", {})
        ok, packet_errors = validate_packet(packet, spec)
        expected = case.get("expected")
        if expected == "pass" and not ok:
            errors.append(f"case {name}: expected pass, got fail: {packet_errors}")
        if expected == "fail" and ok:
            errors.append(f"case {name}: expected fail, got pass")
    return errors


def main() -> int:
    spec = load_json(SPEC_PATH)
    example = load_json(EXAMPLE_PATH)
    cases = load_json(CASES_PATH)

    errors: List[str] = []
    errors.extend(validate_spec(spec))

    ok, example_errors = validate_packet(example, spec)
    if not ok:
        errors.append("example packet failed: " + "; ".join(example_errors))

    errors.extend(validate_cases(cases, spec))

    if errors:
        print("Physical Quantum Qi deepening v0.2 validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi deepening v0.2 validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
