#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_quantum_gradient_jko_entropy_production_v0_47"
READY = "WORLD_QUANTUM_GRADIENT_JKO_ENTROPY_PRODUCTION_V0_47_READY"
BLOCKED = "WORLD_QUANTUM_GRADIENT_JKO_ENTROPY_PRODUCTION_V0_47_BLOCKED"

REQUIRED_COMPONENTS = {
    "discrete_gradient_flow_step",
    "entropy_production",
    "energy_dissipation_inequality",
    "jko_proximal_cost",
    "jko_optimality",
    "equilibrium_witness",
    "lyapunov_gap",
    "free_energy_decay",
    "stationarity_certificate",
    "higher_gauge_covariance",
    "analytic_gradient_flow_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_46_exact": True,
    "genuine_quantum_gradient_flow_external": True,
    "minimizing_movement_convergence_external": True,
    "jko_metric_gradient_flow_external": True,
    "physical_entropy_production_identification_external": True,
    "quantum_log_sobolev_decay_external": True,
    "continuous_energy_dissipation_external": True,
    "continuum_gradient_flow_external": True,
    "world_not_gradient_trajectory": True,
    "entropy_production_not_physical_heat": True,
    "stationary_not_truth_authority": True,
    "equilibrium_not_ontological_identity": True,
    "jko_minimizer_not_execution_authority": True,
    "gradient_flow_read_only_sidecar": True,
    "candidate_not_authority": True,
    "validation_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markovian_history_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}

FORBIDDEN_TRUE_FIELDS = (
    "gradient_flow_executed_by_runtime",
    "physical_entropy_production_computed_by_runtime",
    "jko_optimization_executed_by_runtime",
    "physical_equilibrium_declared_by_runtime",
    "truth_inferred_from_stationarity",
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
    source_v046_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_quantum_gradient_jko_entropy_production(
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

    for field in ("world_model_id", "source_v046_sha256", "formal_module_sha256"):
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
        "source_v046_sha256": str(plan.get("source_v046_sha256", "")),
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
        source_v046_sha256=state["source_v046_sha256"],
        formal_module_sha256=state["formal_module_sha256"],
        bridge_state_digest=digest(state) if not blockers else "",
        blockers=blockers,
    )
