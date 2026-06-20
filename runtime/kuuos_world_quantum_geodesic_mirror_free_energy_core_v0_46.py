#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_quantum_geodesic_mirror_free_energy_v0_46"
READY = "WORLD_QUANTUM_GEODESIC_MIRROR_FREE_ENERGY_V0_46_READY"
BLOCKED = "WORLD_QUANTUM_GEODESIC_MIRROR_FREE_ENERGY_V0_46_BLOCKED"

REQUIRED_COMPONENTS = {
    "exponential_geodesic",
    "mixture_geodesic",
    "quantum_geodesic_action",
    "variational_complexity",
    "variational_inaccuracy",
    "variational_free_energy",
    "surprisal_shadow_bound",
    "free_energy_gradient",
    "mirror_descent_step",
    "bregman_descent_certificate",
    "projected_mirror_defect",
    "higher_gauge_covariance",
    "analytic_variational_flow_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_45_exact": True,
    "smooth_quantum_geodesic_external": True,
    "bkm_levi_civita_geodesic_external": True,
    "legendre_mirror_map_external": True,
    "mirror_descent_convergence_external": True,
    "variational_free_energy_principle_external": True,
    "evidence_bound_identification_external": True,
    "active_inference_interpretation_external": True,
    "continuum_variational_flow_external": True,
    "world_not_geodesic_path": True,
    "low_free_energy_not_truth_authority": True,
    "descent_witness_not_execution_authority": True,
    "evidence_bound_not_physical_evidence": True,
    "geodesic_action_not_world_history_identity": True,
    "variational_flow_read_only_sidecar": True,
    "candidate_not_authority": True,
    "validation_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markovian_history_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}

FORBIDDEN_TRUE_FIELDS = (
    "quantum_geodesic_constructed_by_runtime",
    "physical_free_energy_computed_by_runtime",
    "mirror_descent_executed_by_runtime",
    "truth_inferred_from_low_free_energy",
    "execution_granted_from_descent",
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
    source_v045_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_quantum_geodesic_mirror_free_energy(
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
        "source_v045_sha256",
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
        "source_v045_sha256": str(plan.get("source_v045_sha256", "")),
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
        source_v045_sha256=state["source_v045_sha256"],
        formal_module_sha256=state["formal_module_sha256"],
        bridge_state_digest=digest(state) if not blockers else "",
        blockers=blockers,
    )
