#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_quantum_log_sobolev_contractivity_mixing_v0_48"
READY = "WORLD_QUANTUM_LOG_SOBOLEV_CONTRACTIVITY_MIXING_V0_48_READY"
BLOCKED = "WORLD_QUANTUM_LOG_SOBOLEV_CONTRACTIVITY_MIXING_V0_48_BLOCKED"

REQUIRED_COMPONENTS = {
    "finite_log_sobolev_certificate",
    "contraction_factor",
    "relative_entropy_to_equilibrium",
    "iterated_gradient_flow",
    "relative_entropy_decay",
    "lyapunov_decay",
    "mixing_distance",
    "finite_exponential_mixing_bound",
    "higher_gauge_covariance",
    "analytic_mixing_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_47_exact": True,
    "genuine_quantum_log_sobolev_external": True,
    "hypercontractivity_equivalence_external": True,
    "spectral_gap_comparison_external": True,
    "primitive_quantum_markov_semigroup_external": True,
    "complete_log_sobolev_external": True,
    "continuous_time_exponential_mixing_external": True,
    "physical_pinsker_identification_external": True,
    "continuum_quantum_mixing_external": True,
    "world_not_markov_semigroup": True,
    "finite_contraction_not_physical_mixing": True,
    "equilibrium_not_world_collapse": True,
    "mixing_distance_not_ontological_distance": True,
    "log_sobolev_certificate_not_truth_authority": True,
    "mixing_read_only_sidecar": True,
    "candidate_not_authority": True,
    "validation_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markovian_history_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}

FORBIDDEN_TRUE_FIELDS = (
    "physical_log_sobolev_constant_computed_by_runtime",
    "quantum_markov_semigroup_executed_by_runtime",
    "physical_mixing_declared_by_runtime",
    "ergodicity_inferred_from_finite_certificate",
    "worlds_collapsed_at_equilibrium",
    "world_state_optimized_by_runtime",
    "world_updated",
)


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
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
    source_v047_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_quantum_log_sobolev_contractivity_mixing(
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

    for field in ("world_model_id", "source_v047_sha256", "formal_module_sha256"):
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
        "source_v047_sha256": str(plan.get("source_v047_sha256", "")),
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
        source_v047_sha256=state["source_v047_sha256"],
        formal_module_sha256=state["formal_module_sha256"],
        bridge_state_digest=digest(state) if not blockers else "",
        blockers=blockers,
    )
