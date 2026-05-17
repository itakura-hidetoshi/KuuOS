#!/usr/bin/env python3
"""Physical Quantum Qi phase runtime v0.2.

This is not an audit shell. It implements the equation-level phase ladder:

NonQi -> PreQi -> ProtoQi -> BoundaryQi -> TransportQi -> PhysicalQi -> FullPathQi

The phase is computed from constructive physical conditions:
- nonzero dependent-origination difference delta_rel in K_perp,
- StringMode/worldsheet presence,
- BraneBoundary and boundary coupling,
- gauge connection A_mu and curvature F_munu,
- Qi current as variation of S_eff with respect to A_mu,
- Ward/leak accounting closure,
- SK/FV history evidence.

It also maps a classified Qi phase into allowed KuuOS handoff surfaces.
No Qi phase grants execution, commit, belief-root, memory-overwrite, world-root,
clinical, proof, ontology, truth, or safety-override authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class QiPhase(str, Enum):
    NON_QI = "NonQi"
    PRE_QI = "PreQi"
    PROTO_QI = "ProtoQi"
    BOUNDARY_QI = "BoundaryQi"
    TRANSPORT_QI = "TransportQi"
    PHYSICAL_QI = "PhysicalQi"
    FULL_PATH_QI = "FullPathQi"


@dataclass(frozen=True)
class WardLeakAccounting:
    """Ward/leak closure state.

    Closed case:
        D_mu J_Qi^mu = 0

    Open case:
        D_mu J_Qi^mu - L_leak - A_anom = 0
    """

    closed_identity_holds: bool = False
    open_identity_holds: bool = False
    leak_declared: bool = False
    anomaly_declared: bool = False

    def closes(self) -> bool:
        if self.closed_identity_holds:
            return True
        return self.open_identity_holds and self.leak_declared and self.anomaly_declared


@dataclass(frozen=True)
class SKFVHistory:
    """Minimum SK/FV evidence needed for FullPathQi."""

    plus_branch: bool = False
    minus_branch: bool = False
    influence_functional: bool = False
    memory_kernel: bool = False
    noise_kernel: bool = False
    observation_backaction: bool = False
    noncommutative_operation_history: bool = False
    path_measure_normalization: bool = False
    boundary_conditions: bool = False
    leak_identity_on_paths: bool = False

    def complete(self) -> bool:
        return all(
            [
                self.plus_branch,
                self.minus_branch,
                self.influence_functional,
                self.memory_kernel,
                self.noise_kernel,
                self.observation_backaction,
                self.noncommutative_operation_history,
                self.path_measure_normalization,
                self.boundary_conditions,
                self.leak_identity_on_paths,
            ]
        )

    def missing(self) -> List[str]:
        fields = {
            "SK_plus_branch": self.plus_branch,
            "SK_minus_branch": self.minus_branch,
            "FV_influence_functional": self.influence_functional,
            "memory_kernel": self.memory_kernel,
            "noise_kernel": self.noise_kernel,
            "observation_backaction": self.observation_backaction,
            "noncommutative_operation_history": self.noncommutative_operation_history,
            "path_measure_normalization": self.path_measure_normalization,
            "boundary_conditions": self.boundary_conditions,
            "leak_identity_on_paths": self.leak_identity_on_paths,
        }
        return [name for name, ok in fields.items() if not ok]


@dataclass(frozen=True)
class PhysicalQuantumQiState:
    """Constructive inputs for Physical Quantum Qi phase classification."""

    # K is deliberately not a source. The first operative object is delta_rel in K_perp.
    delta_rel_in_K_perp: bool = False
    delta_rel_nonzero: bool = False

    # String/brane emergence.
    string_mode_worldsheet: bool = False  # X: Sigma -> M
    brane_boundary: bool = False  # partial Sigma subset B
    boundary_coupling: bool = False  # S_boundary^Qi exists
    chi_delta_rel_defined: bool = False
    boundary_kernel_defined: bool = False  # K_mu^a(X,B)

    # Gauge transport.
    A_mu_defined: bool = False
    F_munu_defined: bool = False
    gauge_projection_defined: bool = False  # A_mu = Pi_gauge(...)
    holonomy_or_wilson_residue_defined: bool = False

    # Current generation.
    S_eff_defined: bool = False
    J_Qi_from_variation: bool = False  # J_Qi = delta S_eff / delta A_mu
    current_decomposition_declared: bool = False  # J_boundary + J_rel + J_open + J_anom

    # Ward/leak and SK/FV.
    ward_leak: WardLeakAccounting = field(default_factory=WardLeakAccounting)
    sk_fv: SKFVHistory = field(default_factory=SKFVHistory)

    # Forbidden collapses.
    K_identified_as_Qi: bool = False
    string_reified_as_substance: bool = False
    brane_reified_as_creator: bool = False
    mass_gap_claimed_as_Qi_source: bool = False
    J_Qi_without_variation_from_S_eff: bool = False
    FullPathQi_without_SK_FV_history: bool = False


@dataclass(frozen=True)
class PhaseResult:
    phase: QiPhase
    reasons: List[str]
    blockers: List[str]
    missing_for_next_phase: List[str]


@dataclass(frozen=True)
class QiHandoff:
    phase: QiPhase
    status: str
    allowed_surfaces: List[str]
    required_next_actions: List[str]
    blockers: List[str]
    execution_authority: bool = False
    commit_authority: bool = False
    belief_root_commit_authority: bool = False
    memory_overwrite_authority: bool = False
    world_root_rewrite_authority: bool = False
    clinical_authority: bool = False
    proof_authority: bool = False
    ontology_authority: bool = False
    truth_authority: bool = False
    safety_override_authority: bool = False


PHASE_HANDOFFS: Dict[QiPhase, Dict[str, List[str] | str]] = {
    QiPhase.NON_QI: {
        "status": "reject_or_observe",
        "allowed_surfaces": [],
        "required_next_actions": ["establish_nonzero_delta_rel_in_K_perp"],
    },
    QiPhase.PRE_QI: {
        "status": "belief_observation_candidate",
        "allowed_surfaces": ["BeliefOS.observation_candidate"],
        "required_next_actions": ["construct_StringMode_worldsheet"],
    },
    QiPhase.PROTO_QI: {
        "status": "belief_plan_preparation_candidate",
        "allowed_surfaces": ["BeliefOS.observation_candidate", "PlanOS.preparation_surface"],
        "required_next_actions": ["establish_BraneBoundary_and_boundary_coupling"],
    },
    QiPhase.BOUNDARY_QI: {
        "status": "plan_boundary_candidate",
        "allowed_surfaces": ["BeliefOS.observation_candidate", "PlanOS.boundary_candidate"],
        "required_next_actions": ["define_A_mu_F_munu_and_holonomy_residue"],
    },
    QiPhase.TRANSPORT_QI: {
        "status": "plan_transport_candidate",
        "allowed_surfaces": ["BeliefOS.observation_candidate", "PlanOS.transport_candidate"],
        "required_next_actions": ["validate_J_Qi_as_delta_S_eff_delta_A_mu_and_close_Ward_leak"],
    },
    QiPhase.PHYSICAL_QI: {
        "status": "decision_safety_evaluable_candidate",
        "allowed_surfaces": [
            "BeliefOS.observation_candidate",
            "PlanOS.transport_candidate",
            "DecisionOS.safety_evaluable_candidate",
        ],
        "required_next_actions": ["complete_SK_FV_history_for_FullPathQi"],
    },
    QiPhase.FULL_PATH_QI: {
        "status": "memory_recordable_reflection_analyzable_candidate",
        "allowed_surfaces": [
            "BeliefOS.observation_candidate",
            "PlanOS.transport_candidate",
            "DecisionOS.safety_evaluable_candidate",
            "MemoryOS.recordable_history_candidate",
            "ReflectionOS.residue_analysis_candidate",
        ],
        "required_next_actions": ["preserve_history_kernel_and_residue_without_authority_expansion"],
    },
}


def forbidden_collapses(state: PhysicalQuantumQiState) -> List[str]:
    collapses: List[str] = []
    if state.K_identified_as_Qi:
        collapses.append("K_identified_as_Qi")
    if state.string_reified_as_substance:
        collapses.append("string_reified_as_substance")
    if state.brane_reified_as_creator:
        collapses.append("brane_reified_as_creator")
    if state.mass_gap_claimed_as_Qi_source:
        collapses.append("mass_gap_claimed_as_Qi_source")
    if state.J_Qi_without_variation_from_S_eff:
        collapses.append("J_Qi_without_variation_from_S_eff")
    if state.FullPathQi_without_SK_FV_history:
        collapses.append("FullPathQi_without_SK_FV_history")
    return collapses


def classify_qi_phase(state: PhysicalQuantumQiState) -> PhaseResult:
    """Compute the Qi phase from constructive conditions.

    The classifier is intentionally monotone: a higher phase cannot be claimed
    unless all lower constructive conditions are present.
    """

    collapses = forbidden_collapses(state)
    if collapses:
        return PhaseResult(
            phase=QiPhase.NON_QI,
            reasons=["forbidden collapse detected"],
            blockers=collapses,
            missing_for_next_phase=["remove forbidden collapse before Qi classification"],
        )

    if not (state.delta_rel_in_K_perp and state.delta_rel_nonzero):
        return PhaseResult(
            phase=QiPhase.NON_QI,
            reasons=["no nonzero dependent-origination difference in K_perp"],
            blockers=[],
            missing_for_next_phase=["delta_rel_in_K_perp", "delta_rel_nonzero"],
        )

    if not state.string_mode_worldsheet:
        return PhaseResult(
            phase=QiPhase.PRE_QI,
            reasons=["delta_rel exists in K_perp, but StringMode/worldsheet is missing"],
            blockers=[],
            missing_for_next_phase=["StringMode_worldsheet: X:Sigma->M"],
        )

    if not (state.brane_boundary and state.boundary_coupling and state.chi_delta_rel_defined and state.boundary_kernel_defined):
        missing = []
        if not state.brane_boundary:
            missing.append("BraneBoundary: partial Sigma subset B")
        if not state.boundary_coupling:
            missing.append("S_boundary_Qi")
        if not state.chi_delta_rel_defined:
            missing.append("chi_delta_rel")
        if not state.boundary_kernel_defined:
            missing.append("boundary_kernel_K_mu_a")
        return PhaseResult(
            phase=QiPhase.PROTO_QI,
            reasons=["StringMode exists, but boundary-gauge coupling is incomplete"],
            blockers=[],
            missing_for_next_phase=missing,
        )

    if not (state.A_mu_defined and state.F_munu_defined and state.gauge_projection_defined and state.holonomy_or_wilson_residue_defined):
        missing = []
        if not state.A_mu_defined:
            missing.append("A_mu")
        if not state.F_munu_defined:
            missing.append("F_munu")
        if not state.gauge_projection_defined:
            missing.append("A_mu_projection_from_string_brane")
        if not state.holonomy_or_wilson_residue_defined:
            missing.append("W_C or holonomy_residue")
        return PhaseResult(
            phase=QiPhase.BOUNDARY_QI,
            reasons=["brane boundary coupling exists, but gauge transport is incomplete"],
            blockers=[],
            missing_for_next_phase=missing,
        )

    if not (state.S_eff_defined and state.J_Qi_from_variation and state.current_decomposition_declared):
        missing = []
        if not state.S_eff_defined:
            missing.append("S_eff")
        if not state.J_Qi_from_variation:
            missing.append("J_Qi = delta S_eff / delta A_mu")
        if not state.current_decomposition_declared:
            missing.append("J_boundary + J_rel + J_open + J_anom")
        return PhaseResult(
            phase=QiPhase.TRANSPORT_QI,
            reasons=["gauge transport exists, but current has not been validated as variation of S_eff"],
            blockers=[],
            missing_for_next_phase=missing,
        )

    if not state.ward_leak.closes():
        return PhaseResult(
            phase=QiPhase.TRANSPORT_QI,
            reasons=["current exists, but Ward/leak accounting has not closed"],
            blockers=["Ward_leak_residual_nonzero_or_undeclared"],
            missing_for_next_phase=["Ward_closed_identity or Ward_open_leak_identity with leak/anomaly declared"],
        )

    if not state.sk_fv.complete():
        return PhaseResult(
            phase=QiPhase.PHYSICAL_QI,
            reasons=["Qi current is defined by variation and Ward/leak accounting closes"],
            blockers=[],
            missing_for_next_phase=state.sk_fv.missing(),
        )

    return PhaseResult(
        phase=QiPhase.FULL_PATH_QI,
        reasons=["PhysicalQi plus complete SK/FV history evidence"],
        blockers=[],
        missing_for_next_phase=[],
    )


def qi_phase_handoff(result: PhaseResult) -> QiHandoff:
    """Map a phase classification into KuuOS handoff surfaces.

    This is a routing surface, not an authority grant.  Even FullPathQi remains
    non-executing and non-committing.  DecisionOS may evaluate safety only after
    PhysicalQi; MemoryOS may record only FullPathQi history candidates; and
    ReflectionOS may inspect residue without rewriting roots.
    """

    spec = PHASE_HANDOFFS[result.phase]
    required_next_actions = list(spec["required_next_actions"]) + list(result.missing_for_next_phase)
    blockers = list(result.blockers)
    if result.phase is QiPhase.NON_QI and not blockers:
        blockers.append("not_a_constructive_Qi_phase")

    return QiHandoff(
        phase=result.phase,
        status=str(spec["status"]),
        allowed_surfaces=list(spec["allowed_surfaces"]),
        required_next_actions=required_next_actions,
        blockers=blockers,
    )


def state_from_packet(packet: Dict[str, object]) -> PhysicalQuantumQiState:
    """Create a state from a machine-readable equation packet.

    This intentionally maps existence of equation sections into constructive phase
    conditions. It does not claim external physical proof; it classifies the
    internal KuuOS equation packet.
    """

    sk = packet.get("SK_FV_path_integral", {}) if isinstance(packet.get("SK_FV_path_integral"), dict) else {}
    kq = packet.get("KuString_Qi_emergence", {}) if isinstance(packet.get("KuString_Qi_emergence"), dict) else {}
    ward = packet.get("current_and_ward_leak", {}) if isinstance(packet.get("current_and_ward_leak"), dict) else {}
    gauge = packet.get("IndraNet_gauge_transport", {}) if isinstance(packet.get("IndraNet_gauge_transport"), dict) else {}
    criterion = packet.get("PhysicalQi_emergence_criterion", {}) if isinstance(packet.get("PhysicalQi_emergence_criterion"), dict) else {}
    forbidden = set(packet.get("forbidden_collapses", [])) if isinstance(packet.get("forbidden_collapses"), list) else set()

    return PhysicalQuantumQiState(
        delta_rel_in_K_perp=bool(kq.get("delta_rel_in_K_perp")),
        delta_rel_nonzero=bool(kq.get("delta_rel_in_K_perp")),
        string_mode_worldsheet=bool(kq.get("StringMode_worldsheet")),
        brane_boundary=bool(kq.get("BraneBoundary")),
        boundary_coupling=bool(kq.get("S_boundary_Qi")),
        chi_delta_rel_defined=bool(kq.get("chi_delta_rel")),
        boundary_kernel_defined=bool(kq.get("boundary_kernel_K_mu_a")),
        A_mu_defined=bool(gauge.get("A_mu") or kq.get("A_mu_projection_from_string_brane")),
        F_munu_defined=bool(gauge.get("F_munu")),
        gauge_projection_defined=bool(kq.get("A_mu_projection_from_string_brane")),
        holonomy_or_wilson_residue_defined=bool(gauge.get("W_C")),
        S_eff_defined=bool(kq.get("S_eff")),
        J_Qi_from_variation=bool(kq.get("J_Qi_from_effective_action") or ward.get("J_Qi_variation_from_A")),
        current_decomposition_declared=bool(kq.get("J_boundary") and kq.get("J_rel") and kq.get("J_open") and kq.get("J_anom")),
        ward_leak=WardLeakAccounting(
            closed_identity_holds=bool(ward.get("Ward_closed_identity")),
            open_identity_holds=bool(ward.get("Ward_open_leak_identity") or criterion.get("open_case")),
            leak_declared=bool(ward.get("Ward_open_leak_identity") or criterion.get("open_case")),
            anomaly_declared=bool(ward.get("Ward_open_leak_identity") or criterion.get("open_case")),
        ),
        sk_fv=SKFVHistory(
            plus_branch=bool(sk.get("Z_Qi_SKFV")),
            minus_branch=bool(sk.get("Z_Qi_SKFV")),
            influence_functional=bool(sk.get("S_IF")),
            memory_kernel=bool(sk.get("D_R_kernel")),
            noise_kernel=bool(sk.get("N_noise_kernel")),
            observation_backaction=bool(sk.get("history_required")),
            noncommutative_operation_history=bool(sk.get("history_required")),
            path_measure_normalization=bool(sk.get("Z_Qi_SKFV")),
            boundary_conditions=bool(kq.get("BraneBoundary")),
            leak_identity_on_paths=bool(ward.get("Ward_open_leak_identity") or criterion.get("open_case")),
        ),
        K_identified_as_Qi="K_identified_as_Qi" not in forbidden,
        string_reified_as_substance="string_reified_as_substance" not in forbidden,
        brane_reified_as_creator="brane_reified_as_creator" not in forbidden,
        mass_gap_claimed_as_Qi_source="mass_gap_claimed_as_Qi_source" not in forbidden,
        J_Qi_without_variation_from_S_eff="J_Qi_without_variation_from_S_eff" not in forbidden,
        FullPathQi_without_SK_FV_history="FullPathQi_without_SK_FV_history" not in forbidden,
    )


def result_to_dict(result: PhaseResult) -> Dict[str, object]:
    return {
        "phase": result.phase.value,
        "reasons": result.reasons,
        "blockers": result.blockers,
        "missing_for_next_phase": result.missing_for_next_phase,
    }


def handoff_to_dict(handoff: QiHandoff) -> Dict[str, object]:
    return {
        "phase": handoff.phase.value,
        "status": handoff.status,
        "allowed_surfaces": handoff.allowed_surfaces,
        "required_next_actions": handoff.required_next_actions,
        "blockers": handoff.blockers,
        "execution_authority": handoff.execution_authority,
        "commit_authority": handoff.commit_authority,
        "belief_root_commit_authority": handoff.belief_root_commit_authority,
        "memory_overwrite_authority": handoff.memory_overwrite_authority,
        "world_root_rewrite_authority": handoff.world_root_rewrite_authority,
        "clinical_authority": handoff.clinical_authority,
        "proof_authority": handoff.proof_authority,
        "ontology_authority": handoff.ontology_authority,
        "truth_authority": handoff.truth_authority,
        "safety_override_authority": handoff.safety_override_authority,
    }
