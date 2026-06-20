#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_information_geometric_higher_gauge_v0_43"
READY = "WORLD_INFORMATION_GEOMETRIC_HIGHER_GAUGE_V0_43_READY"
BLOCKED = "WORLD_INFORMATION_GEOMETRIC_HIGHER_GAUGE_V0_43_BLOCKED"

REQUIRED_COMPONENTS = {
    "finite_statistical_manifold_sidecar",
    "observation_law",
    "score_and_centered_score",
    "fisher_metric",
    "dual_connections",
    "alpha_connections",
    "cubic_tensor",
    "divergence_and_dual_divergence",
    "statistical_curvature",
    "gauge_covariant_parameter_transport",
    "gauge_covariant_tangent_transport",
    "information_gauge_two_cell",
    "product_higher_curvature",
    "nonmarkov_boundary_preservation",
}

REQUIRED_BOUNDARY = {
    "source_v0_42_exact": True,
    "smooth_statistical_manifold_external": True,
    "chentsov_uniqueness_external": True,
    "data_processing_external": True,
    "quantum_information_geometry_external": True,
    "physical_fisher_identification_external": True,
    "continuum_information_gauge_field_external": True,
    "world_not_probability_law": True,
    "world_not_statistical_manifold": True,
    "world_not_fisher_metric": True,
    "zero_divergence_not_world_identity": True,
    "information_geometry_read_only_sidecar": True,
    "multi_world_noncollapse_preserved": True,
    "nonmarkovian_history_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
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


def build_world_information_geometric_higher_gauge(
    plan: Mapping[str, Any],
) -> Result:
    blockers: list[str] = []
    if plan.get("version") != VERSION:
        blockers.append("version_invalid")
    if plan.get("plan_digest") != plan_digest(plan):
        blockers.append("plan_digest_invalid")
    if set(plan.get("components", [])) != REQUIRED_COMPONENTS:
        blockers.append("components_invalid")
    boundary = plan.get("boundary") if isinstance(
        plan.get("boundary"), Mapping) else {}
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    for field in (
        "world_model_id", "source_v042_sha256", "formal_module_sha256"
    ):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "statistical_manifold_constructed_by_runtime",
        "physical_fisher_metric_computed_by_runtime",
        "world_identity_inferred_from_divergence",
        "higher_gauge_curvature_flattened_by_runtime",
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
        "physical_fisher_metric_computed_by_runtime": False,
        "world_identity_inferred_from_divergence": False,
        "higher_gauge_curvature_flattened_by_runtime": False,
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
