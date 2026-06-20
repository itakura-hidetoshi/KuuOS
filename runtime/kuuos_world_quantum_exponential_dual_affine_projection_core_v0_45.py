#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_quantum_exponential_dual_affine_projection_v0_45"
READY = "WORLD_QUANTUM_EXPONENTIAL_DUAL_AFFINE_PROJECTION_V0_45_READY"
BLOCKED = "WORLD_QUANTUM_EXPONENTIAL_DUAL_AFFINE_PROJECTION_V0_45_BLOCKED"

REQUIRED_COMPONENTS = {
    "natural_coordinate",
    "expectation_coordinate",
    "log_partition_shadow",
    "dual_potential_shadow",
    "fenchel_young_gap",
    "quantum_bregman_divergence",
    "exponential_projection",
    "mixture_projection",
    "dual_pythagorean_decomposition",
    "petz_recoverability_link",
    "higher_gauge_covariance",
    "analytic_dual_affine_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_44_exact": True,
    "genuine_quantum_exponential_family_external": True,
    "smooth_legendre_duality_external": True,
    "strict_convexity_external": True,
    "araki_bregman_identification_external": True,
    "dual_affine_autoparallel_theorem_external": True,
    "quantum_information_projection_theorem_external": True,
    "petz_sufficiency_projection_equivalence_external": True,
    "continuum_dual_affine_geometry_external": True,
    "world_not_quantum_exponential_family": True,
    "world_not_dual_coordinates": True,
    "world_not_information_projection": True,
    "zero_projection_defect_not_ontological_identity": True,
    "dual_affine_geometry_read_only_sidecar": True,
    "candidate_not_authority": True,
    "validation_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markovian_history_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}

FORBIDDEN_TRUE_FIELDS = (
    "quantum_exponential_family_constructed_by_runtime",
    "log_partition_computed_by_runtime",
    "legendre_transform_executed_by_runtime",
    "information_projection_executed_by_runtime",
    "world_identity_inferred_from_projection",
    "world_state_optimized_by_runtime",
    "world_updated",
)


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
    source_v044_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_quantum_exponential_dual_affine_projection(
    plan: Mapping[str, Any],
) -> Result:
    blockers: list[str] = []
    if plan.get("version") != VERSION:
        blockers.append("version_invalid")
    if plan.get("plan_digest") != plan_digest(plan):
        blockers.append("plan_digest_invalid")
    if set(plan.get("components", [])) != REQUIRED_COMPONENTS:
        blockers.append("components_invalid")

    boundary = plan.get("boundary")
    if not isinstance(boundary, Mapping):
        boundary = {}
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")

    for field in (
        "world_model_id",
        "source_v044_sha256",
        "formal_module_sha256",
    ):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")

    for field in FORBIDDEN_TRUE_FIELDS:
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")

    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v044_sha256": str(plan.get("source_v044_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        **{field: False for field in FORBIDDEN_TRUE_FIELDS},
    }
    return Result(
        version=VERSION,
        status=BLOCKED if blockers else READY,
        decision=decision,
        world_model_id=state["world_model_id"],
        source_v044_sha256=state["source_v044_sha256"],
        formal_module_sha256=state["formal_module_sha256"],
        bridge_state_digest=digest(state) if not blockers else "",
        blockers=blockers,
    )
