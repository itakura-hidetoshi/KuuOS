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
    for module in [
        "SK_FV_path_integral",
        "SK_FV_Qi_action_v0_2A",
        "Ward_leak_identity",
        "Ward_leak_identity_v0_2B",
        "DPI_recoverability",
        "IndraNet_gauge_transport",
        "KuString_Qi_emergence_bridge",
        "Qi_OS_handoff",
    ]:
        if module not in spec.get("deepening_modules", {}):
            errors.append(f"missing module {module}")
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
