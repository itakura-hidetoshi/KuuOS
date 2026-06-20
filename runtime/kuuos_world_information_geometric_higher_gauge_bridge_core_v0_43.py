#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_information_geometric_higher_gauge_bridge_v0_43"
READY = "WORLD_INFORMATION_GEOMETRIC_HIGHER_GAUGE_BRIDGE_V0_43_READY"
BLOCKED = "WORLD_INFORMATION_GEOMETRIC_HIGHER_GAUGE_BRIDGE_V0_43_BLOCKED"

REQUIRED_COMPONENTS = {
    "finite_statistical_observation_model",
    "score_covector_bundle",
    "fisher_metric",
    "dual_affine_connections",
    "amari_chentsov_cubic_tensor",
    "alpha_connection_family",
    "information_divergence",
    "entropy_dual_potential",
    "information_projection",
    "exponential_mixture_geodesics",
    "gauge_covariant_statistical_transport",
    "higher_coherence_information_holonomy",
    "primal_dual_information_curvature",
    "branch_statistical_embedding",
    "history_dependent_nonmarkov_information_geometry",
    "araki_petz_information_shadow",
    "analytic_information_geometry_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_42_exact": True,
    "smooth_statistical_manifold_external": True,
    "chentsov_uniqueness_external": True,
    "levi_civita_existence_external": True,
    "alpha_connection_smoothness_external": True,
    "geodesic_existence_uniqueness_external": True,
    "quantum_fisher_monotonicity_external": True,
    "araki_hessian_realization_external": True,
    "petz_orthogonal_projection_external": True,
    "higher_gauge_stack_information_geometry_external": True,
    "continuum_information_geometry_external": True,
    "world_not_statistical_manifold": True,
    "world_not_probability_distribution": True,
    "world_not_fisher_metric": True,
    "world_not_information_projection": True,
    "information_distance_not_ontological_distance": True,
    "gauge_equivalent_coordinates_not_world_identity": True,
    "information_geometry_read_only_analytic_sidecar": True,
    "candidate_not_authority": True,
    "validation_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "runtime_cannot_execute_policy": True,
    "fail_closed": True,
}


def digest(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def plan_digest(plan: Mapping[str, Any]) -> str:
    value = dict(plan)
    value.pop("plan_digest", None)
    return digest(value)


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    decision: str
    world_model_id: str
    source_v042_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_information_geometric_higher_gauge_bridge(
    plan: Mapping[str, Any],
) -> Result:
    blockers: list[str] = []
    if plan.get("version") != VERSION:
        blockers.append("version_invalid")
    if plan.get("plan_digest") != plan_digest(plan):
        blockers.append("plan_digest_invalid")
    if set(plan.get("components", [])) != REQUIRED_COMPONENTS:
        blockers.append("components_invalid")
    boundary = (
        plan.get("boundary")
        if isinstance(plan.get("boundary"), Mapping)
        else {}
    )
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    for field in (
        "world_model_id",
        "source_v042_sha256",
        "formal_module_sha256",
    ):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "statistical_manifold_constructed_by_runtime",
        "fisher_metric_computed_by_runtime",
        "information_projection_performed_by_runtime",
        "belief_optimized_by_runtime",
        "policy_executed_by_runtime",
        "chentsov_theorem_claimed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v042_sha256": str(plan.get("source_v042_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "statistical_manifold_constructed_by_runtime": False,
        "fisher_metric_computed_by_runtime": False,
        "information_projection_performed_by_runtime": False,
        "belief_optimized_by_runtime": False,
        "policy_executed_by_runtime": False,
        "chentsov_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v042_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
