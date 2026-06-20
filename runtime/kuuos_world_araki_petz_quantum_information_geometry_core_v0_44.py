#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_araki_petz_quantum_information_geometry_v0_44"
READY = "WORLD_ARAKI_PETZ_QUANTUM_INFORMATION_GEOMETRY_V0_44_READY"
BLOCKED = "WORLD_ARAKI_PETZ_QUANTUM_INFORMATION_GEOMETRY_V0_44_BLOCKED"

REQUIRED_COMPONENTS = {
    "araki_hessian_shadow",
    "quantum_fisher_metric",
    "coarse_tangent_channel",
    "petz_tangent_recovery",
    "recovered_tangent_projection",
    "orthogonal_residual_decomposition",
    "quantum_fisher_pythagorean_identity",
    "information_loss",
    "data_processing_defect",
    "operator_petz_link",
    "higher_gauge_covariance",
    "analytic_quantum_information_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_43_exact": True,
    "araki_twice_differentiable_external": True,
    "araki_hessian_bkm_identification_external": True,
    "quantum_fisher_monotonicity_external": True,
    "petz_orthogonal_projection_theorem_external": True,
    "sufficiency_equivalence_external": True,
    "continuum_quantum_information_geometry_external": True,
    "world_not_araki_hessian": True,
    "world_not_quantum_fisher_metric": True,
    "world_not_petz_projection": True,
    "metric_recoverability_not_ontological_identity": True,
    "quantum_information_geometry_read_only_sidecar": True,
    "candidate_not_authority": True,
    "validation_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markovian_history_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}

FORBIDDEN_TRUE_FIELDS = (
    "araki_entropy_differentiated_by_runtime",
    "quantum_fisher_computed_by_runtime",
    "bkm_metric_constructed_by_runtime",
    "petz_projection_executed_by_runtime",
    "sufficiency_inferred_by_runtime",
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
    source_v043_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_araki_petz_quantum_information_geometry(
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
        "source_v043_sha256",
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
        "source_v043_sha256": str(plan.get("source_v043_sha256", "")),
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
        source_v043_sha256=state["source_v043_sha256"],
        formal_module_sha256=state["formal_module_sha256"],
        bridge_state_digest=digest(state) if not blockers else "",
        blockers=blockers,
    )
