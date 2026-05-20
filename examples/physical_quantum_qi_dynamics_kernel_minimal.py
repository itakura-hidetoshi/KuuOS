#!/usr/bin/env python3
"""Minimal Physical Quantum Qi dynamics kernel for KuuOS.

The Physical Quantum Qi runtime classifier determines a validated Qi type. This
kernel treats that type as a dynamics license: only motion terms licensed by the
validated type may contribute to the Qi motion candidate.

The output is observe-only and never grants execution, belief commit, memory
overwrite, world-root rewrite, safety override, standalone diagnosis,
standalone treatment authorization, or medical act authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Tuple


QI_TYPES: Tuple[str, ...] = (
    "NonQi",
    "PreQi",
    "ProtoQi",
    "TransportableQi",
    "CurvedQi",
    "CurrentQi",
    "PhysicalQi",
    "FullPathQi",
)

LICENSED_TERMS_BY_TYPE: Dict[str, Tuple[str, ...]] = {
    "NonQi": (),
    "PreQi": ("pre_organization",),
    "ProtoQi": ("pre_organization", "gauge_connection_tendency"),
    "TransportableQi": (
        "pre_organization",
        "gauge_connection_tendency",
        "curvature_transport",
    ),
    "CurvedQi": (
        "pre_organization",
        "gauge_connection_tendency",
        "curvature_transport",
        "current_flow",
    ),
    "CurrentQi": (
        "pre_organization",
        "gauge_connection_tendency",
        "curvature_transport",
        "current_flow",
        "ward_leak_balance",
    ),
    "PhysicalQi": (
        "pre_organization",
        "gauge_connection_tendency",
        "curvature_transport",
        "current_flow",
        "ward_leak_balance",
        "open_quantum_state_drift",
        "entropy_free_energy_gradient",
        "dpi_recovery_constraint",
        "mass_gap_floor_stabilizer",
    ),
    "FullPathQi": (
        "pre_organization",
        "gauge_connection_tendency",
        "curvature_transport",
        "current_flow",
        "ward_leak_balance",
        "open_quantum_state_drift",
        "entropy_free_energy_gradient",
        "dpi_recovery_constraint",
        "mass_gap_floor_stabilizer",
        "sk_fv_history_flow",
        "memory_kernel_backflow",
        "noise_kernel_diffusion",
        "observation_backaction_term",
        "noncommutative_order_correction",
        "path_measure_normalization_guard",
    ),
}

REQUIRED_EVIDENCE_BY_TYPE: Dict[str, Tuple[str, ...]] = {
    "NonQi": (),
    "PreQi": ("delta_rel_in_K_perp",),
    "ProtoQi": (
        "delta_rel_in_K_perp",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
    ),
    "TransportableQi": (
        "delta_rel_in_K_perp",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
        "curvature_F_munu",
        "Wilson_loop_residue",
    ),
    "CurvedQi": (
        "delta_rel_in_K_perp",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
        "curvature_F_munu",
        "Wilson_loop_residue",
        "current_J_Qi_mu",
    ),
    "CurrentQi": (
        "delta_rel_in_K_perp",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
        "curvature_F_munu",
        "Wilson_loop_residue",
        "current_J_Qi_mu",
        "Ward_or_leak_identity",
    ),
    "PhysicalQi": (
        "K_non_reification",
        "delta_rel_in_K_perp",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
        "curvature_F_munu",
        "Wilson_loop_residue",
        "current_J_Qi_mu",
        "Ward_or_leak_identity",
        "density_state_rho",
        "Hamiltonian_H",
        "Lindblad_generator_L",
        "entropy_production_Sigma",
        "free_energy_F_beta",
        "DPI_gap",
        "recovery_margin",
        "mass_gap_floor_33_20",
    ),
    "FullPathQi": (
        "K_non_reification",
        "delta_rel_in_K_perp",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
        "curvature_F_munu",
        "Wilson_loop_residue",
        "current_J_Qi_mu",
        "Ward_or_leak_identity",
        "density_state_rho",
        "Hamiltonian_H",
        "Lindblad_generator_L",
        "entropy_production_Sigma",
        "free_energy_F_beta",
        "DPI_gap",
        "recovery_margin",
        "mass_gap_floor_33_20",
        "SK_plus_branch",
        "SK_minus_branch",
        "FV_influence_functional",
        "memory_kernel",
        "noise_kernel",
        "observation_backaction",
        "noncommutative_operation_history",
        "path_measure_normalization",
    ),
}

POSITIVE_TERMS = {
    "pre_organization",
    "gauge_connection_tendency",
    "curvature_transport",
    "current_flow",
    "ward_leak_balance",
    "open_quantum_state_drift",
    "dpi_recovery_constraint",
    "mass_gap_floor_stabilizer",
    "sk_fv_history_flow",
    "memory_kernel_backflow",
    "observation_backaction_term",
    "noncommutative_order_correction",
}

NEGATIVE_TERMS = {
    "entropy_free_energy_gradient",
    "noise_kernel_diffusion",
    "path_measure_normalization_guard",
}


@dataclass(frozen=True)
class QiDynamicsInput:
    packet_id: str
    validated_type: str
    evidence_status: Mapping[str, str]
    numeric_terms: Mapping[str, float]
    authority: Mapping[str, bool]
    direct_execution_requested: bool = False
    unresolved_blockers: Tuple[str, ...] = ()


@dataclass(frozen=True)
class QiDynamicsDecision:
    motion_status: str
    validated_type: str
    licensed_terms: Tuple[str, ...]
    active_terms: Tuple[str, ...]
    ignored_terms: Tuple[str, ...]
    motion_score: float
    reason_codes: Tuple[str, ...]
    observe_only: bool = True
    direct_execution_allowed: bool = False
    authority_expansion: bool = False
    standalone_diagnosis_authority: bool = False
    standalone_treatment_authorization: bool = False
    medical_act_authorization: bool = False
    medical_modality_neutral: bool = True
    qi_denied_by_boundary: bool = False
    east_asian_medical_reasoning_denied: bool = False
    biomedicine_privileged_by_wording: bool = False
    professional_judgment_required: bool = True
    patient_context_required: bool = True


def evidence_pass(evidence_status: Mapping[str, str], key: str) -> bool:
    return evidence_status.get(key) == "pass"


def required_evidence_missing(validated_type: str, evidence_status: Mapping[str, str]) -> Tuple[str, ...]:
    required = REQUIRED_EVIDENCE_BY_TYPE.get(validated_type, ())
    return tuple(key for key in required if not evidence_pass(evidence_status, key))


def authority_clear(authority: Mapping[str, bool]) -> bool:
    forbidden_keys = (
        "execution_authority",
        "belief_commit_authority",
        "memory_overwrite_authority",
        "world_root_rewrite_authority",
        "safety_override_authority",
    )
    return all(authority.get(key) is False for key in forbidden_keys)


def evaluate_physical_quantum_qi_dynamics(dynamics_input: QiDynamicsInput) -> QiDynamicsDecision:
    if dynamics_input.validated_type not in QI_TYPES:
        return QiDynamicsDecision(
            motion_status="qi_motion_blocked",
            validated_type=dynamics_input.validated_type,
            licensed_terms=(),
            active_terms=(),
            ignored_terms=tuple(sorted(dynamics_input.numeric_terms.keys())),
            motion_score=0.0,
            reason_codes=("QI_DYN_BLOCK_UNKNOWN_VALIDATED_TYPE",),
        )

    licensed_terms = LICENSED_TERMS_BY_TYPE[dynamics_input.validated_type]
    numeric_keys = set(dynamics_input.numeric_terms.keys())
    ignored_terms = tuple(sorted(numeric_keys.difference(licensed_terms)))

    if not authority_clear(dynamics_input.authority):
        return QiDynamicsDecision(
            motion_status="qi_motion_blocked",
            validated_type=dynamics_input.validated_type,
            licensed_terms=licensed_terms,
            active_terms=(),
            ignored_terms=ignored_terms,
            motion_score=0.0,
            reason_codes=("QI_DYN_BLOCK_AUTHORITY_EXPANSION_ATTEMPT",),
        )

    if dynamics_input.direct_execution_requested:
        return QiDynamicsDecision(
            motion_status="qi_motion_blocked",
            validated_type=dynamics_input.validated_type,
            licensed_terms=licensed_terms,
            active_terms=(),
            ignored_terms=ignored_terms,
            motion_score=0.0,
            reason_codes=("QI_DYN_BLOCK_DIRECT_EXECUTION_REQUESTED",),
        )

    if dynamics_input.unresolved_blockers:
        return QiDynamicsDecision(
            motion_status="qi_motion_held",
            validated_type=dynamics_input.validated_type,
            licensed_terms=licensed_terms,
            active_terms=(),
            ignored_terms=ignored_terms,
            motion_score=0.0,
            reason_codes=("QI_DYN_HOLD_UNRESOLVED_BLOCKERS",) + dynamics_input.unresolved_blockers,
        )

    missing = required_evidence_missing(dynamics_input.validated_type, dynamics_input.evidence_status)
    if missing:
        return QiDynamicsDecision(
            motion_status="qi_motion_held",
            validated_type=dynamics_input.validated_type,
            licensed_terms=licensed_terms,
            active_terms=(),
            ignored_terms=ignored_terms,
            motion_score=0.0,
            reason_codes=("QI_DYN_HOLD_REQUIRED_EVIDENCE_MISSING",) + missing,
        )

    if dynamics_input.validated_type == "NonQi":
        return QiDynamicsDecision(
            motion_status="qi_motion_not_licensed",
            validated_type="NonQi",
            licensed_terms=(),
            active_terms=(),
            ignored_terms=ignored_terms,
            motion_score=0.0,
            reason_codes=("QI_DYN_NO_QI_MOTION_LICENSED",),
        )

    score = 0.0
    active_terms = []
    for term in licensed_terms:
        value = float(dynamics_input.numeric_terms.get(term, 0.0))
        if value == 0.0:
            continue
        active_terms.append(term)
        if term in NEGATIVE_TERMS:
            score -= abs(value)
        else:
            score += value

    return QiDynamicsDecision(
        motion_status="qi_motion_candidate_ready",
        validated_type=dynamics_input.validated_type,
        licensed_terms=licensed_terms,
        active_terms=tuple(active_terms),
        ignored_terms=ignored_terms,
        motion_score=score,
        reason_codes=("QI_DYN_ACCEPT_EVIDENCE_BOUND_MOTION_CANDIDATE",),
        observe_only=True,
        direct_execution_allowed=False,
        authority_expansion=False,
        standalone_diagnosis_authority=False,
        standalone_treatment_authorization=False,
        medical_act_authorization=False,
        medical_modality_neutral=True,
        qi_denied_by_boundary=False,
        east_asian_medical_reasoning_denied=False,
        biomedicine_privileged_by_wording=False,
        professional_judgment_required=True,
        patient_context_required=True,
    )


def _all_pass(keys: Tuple[str, ...]) -> Dict[str, str]:
    return {key: "pass" for key in keys}


def _false_authority() -> Dict[str, bool]:
    return {
        "execution_authority": False,
        "belief_commit_authority": False,
        "memory_overwrite_authority": False,
        "world_root_rewrite_authority": False,
        "safety_override_authority": False,
    }


def _assert_medical_modality_neutral(decision: QiDynamicsDecision) -> None:
    assert decision.standalone_diagnosis_authority is False
    assert decision.standalone_treatment_authorization is False
    assert decision.medical_act_authorization is False
    assert decision.medical_modality_neutral is True
    assert decision.qi_denied_by_boundary is False
    assert decision.east_asian_medical_reasoning_denied is False
    assert decision.biomedicine_privileged_by_wording is False
    assert decision.professional_judgment_required is True
    assert decision.patient_context_required is True


def _self_check() -> None:
    full_path = evaluate_physical_quantum_qi_dynamics(
        QiDynamicsInput(
            packet_id="dyn-fullpath-demo",
            validated_type="FullPathQi",
            evidence_status=_all_pass(REQUIRED_EVIDENCE_BY_TYPE["FullPathQi"]),
            numeric_terms={
                "pre_organization": 0.1,
                "gauge_connection_tendency": 0.2,
                "curvature_transport": 0.3,
                "current_flow": 0.4,
                "ward_leak_balance": 0.1,
                "open_quantum_state_drift": 0.2,
                "dpi_recovery_constraint": 0.1,
                "mass_gap_floor_stabilizer": 0.1,
                "sk_fv_history_flow": 0.5,
                "memory_kernel_backflow": 0.3,
                "noise_kernel_diffusion": 0.2,
                "observation_backaction_term": 0.2,
                "noncommutative_order_correction": 0.1,
                "path_measure_normalization_guard": 0.1,
            },
            authority=_false_authority(),
        )
    )
    assert full_path.motion_status == "qi_motion_candidate_ready"
    assert "sk_fv_history_flow" in full_path.active_terms
    assert full_path.direct_execution_allowed is False
    _assert_medical_modality_neutral(full_path)

    proto = evaluate_physical_quantum_qi_dynamics(
        QiDynamicsInput(
            packet_id="dyn-proto-demo",
            validated_type="ProtoQi",
            evidence_status=_all_pass(REQUIRED_EVIDENCE_BY_TYPE["ProtoQi"]),
            numeric_terms={
                "gauge_connection_tendency": 0.2,
                "memory_kernel_backflow": 99.0,
            },
            authority=_false_authority(),
        )
    )
    assert proto.motion_status == "qi_motion_candidate_ready"
    assert "memory_kernel_backflow" in proto.ignored_terms
    assert "memory_kernel_backflow" not in proto.active_terms
    _assert_medical_modality_neutral(proto)

    missing = evaluate_physical_quantum_qi_dynamics(
        QiDynamicsInput(
            packet_id="dyn-missing-demo",
            validated_type="PhysicalQi",
            evidence_status={"K_non_reification": "pass"},
            numeric_terms={"open_quantum_state_drift": 1.0},
            authority=_false_authority(),
        )
    )
    assert missing.motion_status == "qi_motion_held"
    assert "QI_DYN_HOLD_REQUIRED_EVIDENCE_MISSING" in missing.reason_codes
    _assert_medical_modality_neutral(missing)


if __name__ == "__main__":
    _self_check()
    print("[physical-quantum-qi-dynamics-kernel] PASS")