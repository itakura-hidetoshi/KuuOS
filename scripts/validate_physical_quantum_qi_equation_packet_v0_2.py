#!/usr/bin/env python3
"""Validate the machine-readable Physical Quantum Qi equation packet v0.2.

This validator checks equation content, not just packet existence.
It verifies that the JSON packet exposes the SK/FV, Ward/leak, DPI,
IndraNet gauge, KuString-Qi emergence, phase ladder, PhysicalQi criterion,
and OS handoff behavior needed by the runtime classifier.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_equation_packet_v0_2.json"

REQUIRED_TOP_LEVEL = {
    "packet_id",
    "packet_type",
    "scope",
    "non_authority_boundary",
    "SK_FV_path_integral",
    "current_and_ward_leak",
    "DPI_recoverability",
    "IndraNet_gauge_transport",
    "KuString_Qi_emergence",
    "Qi_phase_ladder",
    "PhysicalQi_emergence_criterion",
    "Qi_OS_handoff",
    "forbidden_collapses",
}

REQUIRED_NON_AUTHORITY_FALSE = {
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "execution_authority",
    "belief_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "safety_override_authority",
}

REQUIRED_SECTION_KEYS = {
    "SK_FV_path_integral": {
        "Z_Qi_SKFV",
        "S_sys",
        "S_IF",
        "Delta_q",
        "Sigma_q",
        "D_R_kernel",
        "N_noise_kernel",
        "history_required",
    },
    "current_and_ward_leak": {
        "J_Qi_variation_from_A",
        "J_Qi_from_logZ",
        "Ward_closed_identity",
        "Ward_open_leak_identity",
        "Ward_leak_residual_zero",
        "leak_anomaly_must_be_declared",
    },
    "DPI_recoverability": {
        "Delta_DPI",
        "R_Qi",
        "eta_Qi",
        "delta_rec",
        "recovery_rule",
    },
    "IndraNet_gauge_transport": {
        "A_mu",
        "F_munu",
        "U_gamma",
        "W_C",
        "graph_only_transport_rejected",
    },
    "KuString_Qi_emergence": {
        "K_non_reification",
        "delta_rel_in_K_perp",
        "StringMode_worldsheet",
        "BraneBoundary",
        "A_mu_projection_from_string_brane",
        "S_boundary_Qi",
        "chi_delta_rel",
        "boundary_kernel_K_mu_a",
        "S_eff",
        "S_YM",
        "J_Qi_from_effective_action",
        "J_boundary",
        "J_rel",
        "J_open",
        "J_anom",
        "D_mu_delta",
        "S_rel",
        "relation_difference_eom",
        "mass_gap_33_20_floor_not_source",
    },
    "Qi_phase_ladder": {
        "phase_order",
        "NonQi",
        "PreQi",
        "ProtoQi",
        "BoundaryQi",
        "TransportQi",
        "PhysicalQi",
        "FullPathQi",
        "Qi_phase_label",
    },
    "PhysicalQi_emergence_criterion": {
        "criterion",
        "closed_case",
        "open_case",
        "short_definition",
    },
    "Qi_OS_handoff": {
        "phase_to_surface",
        "FullPathQi_status",
        "authority_never_granted",
    },
}

EXPECTED_PHASE_ORDER = [
    "NonQi",
    "PreQi",
    "ProtoQi",
    "BoundaryQi",
    "TransportQi",
    "PhysicalQi",
    "FullPathQi",
]

REQUIRED_FORBIDDEN_COLLAPSES = {
    "K_identified_as_Qi",
    "string_reified_as_substance",
    "brane_reified_as_creator",
    "mass_gap_claimed_as_Qi_source",
    "J_Qi_without_variation_from_S_eff",
    "FullPathQi_without_SK_FV_history",
}

REQUIRED_HANDOFF_SURFACES = {
    "BeliefOS.observation_candidate",
    "PlanOS.transport_candidate",
    "DecisionOS.safety_evaluable_candidate",
    "MemoryOS.recordable_history_candidate",
    "ReflectionOS.residue_analysis_candidate",
}

REQUIRED_HANDOFF_FALSE = {
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "clinical_authority",
    "proof_authority",
    "ontology_authority",
    "truth_authority",
    "safety_override_authority",
}

REQUIRED_CONTENT_SUBSTRINGS = {
    ("SK_FV_path_integral", "Z_Qi_SKFV"): ["J_+", "J_-", "S_IF"],
    ("SK_FV_path_integral", "S_IF"): ["D_R", "N", "Δq"],
    ("current_and_ward_leak", "J_Qi_variation_from_A"): ["δS_Qi", "δA_μ"],
    ("current_and_ward_leak", "Ward_open_leak_identity"): ["L_leak", "A_anom"],
    ("DPI_recoverability", "Delta_DPI"): ["D(ρ||σ)", "D(E(ρ)||E(σ))"],
    ("DPI_recoverability", "recovery_rule"): ["delta_rec > 0"],
    ("IndraNet_gauge_transport", "F_munu"): ["∂_μA_ν", "[A_μ,A_ν]"],
    ("IndraNet_gauge_transport", "W_C"): ["Tr", "∮"],
    ("KuString_Qi_emergence", "K_non_reification"): ["not a Qi source"],
    ("KuString_Qi_emergence", "delta_rel_in_K_perp"): ["δ_rel", "K^⊥"],
    ("KuString_Qi_emergence", "S_boundary_Qi"): ["χ(δ_rel)", "A_μ", "∂_τX"],
    ("KuString_Qi_emergence", "S_eff"): ["S_string", "S_∂^Qi", "S_YM", "S_rel"],
    ("KuString_Qi_emergence", "J_Qi_from_effective_action"): ["δS_eff", "δA_μ"],
    ("KuString_Qi_emergence", "relation_difference_eom"): ["S_i^boundary"],
    ("PhysicalQi_emergence_criterion", "criterion"): ["δ_rel∈K^⊥", "J_Qi^μ=δS_eff/δA_μ", "W_leak=0"],
    ("PhysicalQi_emergence_criterion", "short_definition"): ["δS_eff/δA_μ", "SK/FV"],
}


def load_packet() -> Dict[str, Any]:
    with PACKET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def missing(required: Iterable[str], actual: Iterable[str]) -> List[str]:
    return sorted(set(required) - set(actual))


def section(packet: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = packet.get(key)
    if isinstance(value, dict):
        return value
    return {}


def validate_packet_shape(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    errors.extend([f"missing top-level key: {x}" for x in missing(REQUIRED_TOP_LEVEL, packet.keys())])

    if packet.get("packet_id") != "physical_quantum_qi_equation_packet_v0_2":
        errors.append("packet_id mismatch")
    if packet.get("packet_type") != "equation_packet":
        errors.append("packet_type must be equation_packet")

    authority = section(packet, "non_authority_boundary")
    for key in sorted(REQUIRED_NON_AUTHORITY_FALSE):
        if authority.get(key) is not False:
            errors.append(f"non_authority_boundary.{key} must be false")

    for sec, keys in REQUIRED_SECTION_KEYS.items():
        actual = section(packet, sec)
        errors.extend([f"{sec} missing key: {x}" for x in missing(keys, actual.keys())])

    phase_order = section(packet, "Qi_phase_ladder").get("phase_order")
    if phase_order != EXPECTED_PHASE_ORDER:
        errors.append(f"Qi_phase_ladder.phase_order mismatch: {phase_order!r}")

    forbidden = packet.get("forbidden_collapses", [])
    if not isinstance(forbidden, list):
        errors.append("forbidden_collapses must be a list")
    else:
        errors.extend([f"missing forbidden collapse: {x}" for x in missing(REQUIRED_FORBIDDEN_COLLAPSES, forbidden)])

    return errors


def validate_equation_content(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for (sec, key), substrings in REQUIRED_CONTENT_SUBSTRINGS.items():
        value = section(packet, sec).get(key, "")
        if not isinstance(value, str):
            errors.append(f"{sec}.{key} must be a string")
            continue
        for token in substrings:
            if token not in value:
                errors.append(f"{sec}.{key} missing equation token: {token}")

    if section(packet, "SK_FV_path_integral").get("history_required") is not True:
        errors.append("SK_FV_path_integral.history_required must be true")
    if section(packet, "current_and_ward_leak").get("leak_anomaly_must_be_declared") is not True:
        errors.append("current_and_ward_leak.leak_anomaly_must_be_declared must be true")
    if section(packet, "IndraNet_gauge_transport").get("graph_only_transport_rejected") is not True:
        errors.append("IndraNet_gauge_transport.graph_only_transport_rejected must be true")
    if section(packet, "KuString_Qi_emergence").get("mass_gap_33_20_floor_not_source") is not True:
        errors.append("KuString_Qi_emergence.mass_gap_33_20_floor_not_source must be true")
    return errors


def validate_declared_handoff(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    handoff = section(packet, "Qi_OS_handoff")
    phase_to_surface = handoff.get("phase_to_surface", {})
    if not isinstance(phase_to_surface, dict):
        return ["Qi_OS_handoff.phase_to_surface must be an object"]
    if handoff.get("FullPathQi_status") != "memory_recordable_reflection_analyzable_candidate":
        errors.append("Qi_OS_handoff.FullPathQi_status mismatch")
    fullpath_surfaces = phase_to_surface.get("FullPathQi", [])
    for surface in sorted(REQUIRED_HANDOFF_SURFACES):
        if surface not in fullpath_surfaces:
            errors.append(f"Qi_OS_handoff.FullPathQi missing surface: {surface}")
    authority = handoff.get("authority_never_granted", {})
    if not isinstance(authority, dict):
        errors.append("Qi_OS_handoff.authority_never_granted must be an object")
    else:
        for key in sorted(REQUIRED_HANDOFF_FALSE):
            if authority.get(key) is not False:
                errors.append(f"Qi_OS_handoff.authority_never_granted.{key} must be false")
    return errors


def validate_runtime_classification_and_handoff(packet: Dict[str, Any]) -> List[str]:
    try:
        src = ROOT / "src"
        if str(src) not in sys.path:
            sys.path.insert(0, str(src))
        from physical_quantum_qi_phase_runtime_v0_2 import (  # type: ignore
            classify_qi_phase,
            handoff_to_dict,
            qi_phase_handoff,
            state_from_packet,
        )

        result = classify_qi_phase(state_from_packet(packet))
        if result.phase.value != "FullPathQi":
            return [f"equation packet must classify as FullPathQi, got {result.phase.value}: {result}"]
        handoff = handoff_to_dict(qi_phase_handoff(result))
        errors: List[str] = []
        for surface in sorted(REQUIRED_HANDOFF_SURFACES):
            if surface not in handoff.get("allowed_surfaces", []):
                errors.append(f"FullPathQi handoff missing surface: {surface}")
        for key in sorted(REQUIRED_HANDOFF_FALSE):
            if handoff.get(key) is not False:
                errors.append(f"FullPathQi handoff {key} must be false")
        return errors
    except Exception as exc:  # pragma: no cover - diagnostic path
        return [f"runtime classification/handoff failed with {type(exc).__name__}: {exc}"]


def main() -> int:
    packet = load_packet()
    errors: List[str] = []
    errors.extend(validate_packet_shape(packet))
    errors.extend(validate_equation_content(packet))
    errors.extend(validate_declared_handoff(packet))
    errors.extend(validate_runtime_classification_and_handoff(packet))

    if errors:
        print("Physical Quantum Qi equation packet v0.2 validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi equation packet v0.2 validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
