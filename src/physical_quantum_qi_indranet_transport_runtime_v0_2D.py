#!/usr/bin/env python3
"""Runtime adapter for Physical Quantum Qi IndraNet gauge transport v0.2D.

This module is not an audit layer.  It evaluates whether an IndraNet transport
packet is usable as a gauge-geometric transport candidate for PlanOS/phase
runtime routing.

The adapter rejects graph-only transport, missing connection/curvature/path,
hidden scope drift, hidden holonomy, and scalar-only residue collapse.  A valid
transport remains candidate-only and grants no execution, commit, belief-root,
memory-overwrite, world-root-rewrite, truth, proof, ontology, clinical, or safety
override authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class IndraNetTransportStatus(str, Enum):
    VALID_TRANSPORT_CANDIDATE = "valid_transport_candidate"
    REJECTED_GRAPH_ONLY = "rejected_graph_only"
    BLOCKED_INCOMPLETE_GEOMETRY = "blocked_incomplete_geometry"
    BLOCKED_SCOPE_DRIFT = "blocked_scope_drift"
    BLOCKED_HOLONOMY_RESIDUE = "blocked_holonomy_residue"
    BLOCKED_HIDDEN_RESIDUE = "blocked_hidden_residue"


AUTHORITY_FALSE_FIELDS = (
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "execution_authority",
    "commit_authority",
    "belief_commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "truth_authority",
    "safety_override_authority",
)


@dataclass(frozen=True)
class IndraNetTransportCandidate:
    A_mu_declared: bool = False
    F_munu_declared: bool = False
    U_gamma_declared: bool = False
    W_C_declared: bool = False
    path_gamma_declared: bool = False
    path_ordering_declared: bool = False
    source_scope_declared: bool = False
    target_scope_declared: bool = False
    scope_drift_declared: bool = False
    scope_drift_value: float = 0.0
    scope_drift_tolerance: float = 0.0
    holonomy_residue_declared: bool = False
    holonomy_residue_value: float = 0.0
    holonomy_residue_tolerance: float = 0.0
    component_residue_visibility_declared: bool = False
    transport_residue_vector_declared: bool = False
    graph_only_transport_rejected: bool = False
    scalar_residue_summary_used: bool = False
    scalar_residue_weights_declared: bool = False
    authority_boundary_false: bool = False


@dataclass(frozen=True)
class IndraNetTransportGateResult:
    status: IndraNetTransportStatus
    valid: bool
    blockers: List[str] = field(default_factory=list)
    required_next_actions: List[str] = field(default_factory=list)
    allowed_surfaces: List[str] = field(default_factory=list)
    execution_authority: bool = False
    commit_authority: bool = False
    belief_root_commit_authority: bool = False
    memory_overwrite_authority: bool = False
    world_root_rewrite_authority: bool = False
    proof_authority: bool = False
    ontology_authority: bool = False
    clinical_authority: bool = False
    truth_authority: bool = False
    safety_override_authority: bool = False


def _as_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return default


def candidate_from_packet(packet: Dict[str, Any]) -> IndraNetTransportCandidate:
    gauge = packet.get("gauge_bundle_connection", {}) if isinstance(packet.get("gauge_bundle_connection"), dict) else {}
    curv = packet.get("curvature", {}) if isinstance(packet.get("curvature"), dict) else {}
    path = packet.get("path_transport", {}) if isinstance(packet.get("path_transport"), dict) else {}
    hol = packet.get("holonomy_wilson_loop", {}) if isinstance(packet.get("holonomy_wilson_loop"), dict) else {}
    scope = packet.get("scope_drift", {}) if isinstance(packet.get("scope_drift"), dict) else {}
    residue = packet.get("transport_residue", {}) if isinstance(packet.get("transport_residue"), dict) else {}
    gate = packet.get("validity_gate", {}) if isinstance(packet.get("validity_gate"), dict) else {}
    authority = packet.get("authority_boundary", {}) if isinstance(packet.get("authority_boundary"), dict) else {}

    weights = residue.get("scalar_residue_weights_declared_if_scalar_used")
    scalar_weights_declared = isinstance(weights, dict) and all(
        isinstance(weights.get(k), (int, float)) for k in ["alpha_h", "alpha_c", "alpha_s", "alpha_p", "alpha_r", "alpha_b"]
    )

    return IndraNetTransportCandidate(
        A_mu_declared=bool(gauge.get("A_mu_declared")),
        F_munu_declared=bool(curv.get("F_munu_defined")),
        U_gamma_declared=bool(path.get("U_gamma_defined")),
        W_C_declared=bool(hol.get("W_C_defined")),
        path_gamma_declared=bool(path.get("path_gamma_declared")),
        path_ordering_declared=bool(path.get("path_ordering_declared")),
        source_scope_declared=bool(scope.get("source_scope_declared")),
        target_scope_declared=bool(scope.get("target_scope_declared")),
        scope_drift_declared="scope_drift_value_or_bound_declared" in scope,
        scope_drift_value=_as_float(scope.get("scope_drift_value_or_bound_declared")),
        scope_drift_tolerance=_as_float(scope.get("scope_drift_tolerance_declared")),
        holonomy_residue_declared="holonomy_residue_declared" in residue,
        holonomy_residue_value=_as_float(residue.get("holonomy_residue_declared")),
        holonomy_residue_tolerance=_as_float(hol.get("holonomy_tolerance_declared")),
        component_residue_visibility_declared=bool(residue.get("component_residue_visibility_declared")),
        transport_residue_vector_declared=bool(residue.get("transport_residue_vector_declared")),
        graph_only_transport_rejected=bool(gate.get("graph_only_transport_rejected")),
        scalar_residue_summary_used="scalar_residue_summary" in residue,
        scalar_residue_weights_declared=scalar_weights_declared,
        authority_boundary_false=all(authority.get(field) is False for field in AUTHORITY_FALSE_FIELDS),
    )


def evaluate_indranet_transport(candidate: IndraNetTransportCandidate) -> IndraNetTransportGateResult:
    if not candidate.graph_only_transport_rejected:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.REJECTED_GRAPH_ONLY,
            valid=False,
            blockers=["graph_only_transport_not_rejected"],
            required_next_actions=["declare_gauge_transport_not_graph_only"],
        )

    geometry_missing: List[str] = []
    if not candidate.A_mu_declared:
        geometry_missing.append("A_mu")
    if not candidate.F_munu_declared:
        geometry_missing.append("F_munu")
    if not candidate.U_gamma_declared:
        geometry_missing.append("U_gamma")
    if not candidate.W_C_declared:
        geometry_missing.append("W_C")
    if not candidate.path_gamma_declared:
        geometry_missing.append("path_gamma")
    if not candidate.path_ordering_declared:
        geometry_missing.append("path_ordering")
    if not candidate.source_scope_declared:
        geometry_missing.append("source_scope")
    if not candidate.target_scope_declared:
        geometry_missing.append("target_scope")

    if geometry_missing:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.BLOCKED_INCOMPLETE_GEOMETRY,
            valid=False,
            blockers=geometry_missing,
            required_next_actions=["complete_gauge_transport_geometry"],
        )

    if not candidate.scope_drift_declared or candidate.scope_drift_value > candidate.scope_drift_tolerance:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.BLOCKED_SCOPE_DRIFT,
            valid=False,
            blockers=["scope_drift_missing_or_above_tolerance"],
            required_next_actions=["declare_scope_drift_and_reduce_within_tolerance"],
        )

    if not candidate.holonomy_residue_declared or candidate.holonomy_residue_value > candidate.holonomy_residue_tolerance:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.BLOCKED_HOLONOMY_RESIDUE,
            valid=False,
            blockers=["holonomy_residue_missing_or_above_tolerance"],
            required_next_actions=["declare_holonomy_residue_and_reduce_within_tolerance"],
        )

    if not candidate.transport_residue_vector_declared or not candidate.component_residue_visibility_declared:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.BLOCKED_HIDDEN_RESIDUE,
            valid=False,
            blockers=["component_residue_visibility_missing"],
            required_next_actions=["expose_component_residue_vector"],
        )

    if candidate.scalar_residue_summary_used and not candidate.scalar_residue_weights_declared:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.BLOCKED_HIDDEN_RESIDUE,
            valid=False,
            blockers=["scalar_residue_weights_missing"],
            required_next_actions=["declare_scalar_residue_weights_or_remove_scalar_summary"],
        )

    if not candidate.authority_boundary_false:
        return IndraNetTransportGateResult(
            status=IndraNetTransportStatus.BLOCKED_INCOMPLETE_GEOMETRY,
            valid=False,
            blockers=["authority_boundary_not_false"],
            required_next_actions=["restore_non_authority_boundary"],
        )

    return IndraNetTransportGateResult(
        status=IndraNetTransportStatus.VALID_TRANSPORT_CANDIDATE,
        valid=True,
        allowed_surfaces=["PlanOS.transport_candidate", "ReflectionOS.residue_analysis_candidate"],
        required_next_actions=["preserve_scope_holonomy_and_component_residue_without_authority_expansion"],
    )


def result_to_dict(result: IndraNetTransportGateResult) -> Dict[str, Any]:
    return {
        "status": result.status.value,
        "valid": result.valid,
        "blockers": result.blockers,
        "required_next_actions": result.required_next_actions,
        "allowed_surfaces": result.allowed_surfaces,
        "execution_authority": result.execution_authority,
        "commit_authority": result.commit_authority,
        "belief_root_commit_authority": result.belief_root_commit_authority,
        "memory_overwrite_authority": result.memory_overwrite_authority,
        "world_root_rewrite_authority": result.world_root_rewrite_authority,
        "proof_authority": result.proof_authority,
        "ontology_authority": result.ontology_authority,
        "clinical_authority": result.clinical_authority,
        "truth_authority": result.truth_authority,
        "safety_override_authority": result.safety_override_authority,
    }
