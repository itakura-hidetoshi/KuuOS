from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, isfinite
from typing import Any, Iterable, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_information_geometric_qi_objective_kernel_v0_1"
PLANOS_VERSION = "v0.91"
STATUS_READY = "PLANOS_INFORMATION_GEOMETRIC_QI_OBJECTIVE_KERNEL_READY"
CANDIDATE_FIELD = (
    "continue",
    "strengthen",
    "repair",
    "slow_down",
    "reobserve",
    "reroute",
    "hold",
    "terminate_candidate",
)

BOUNDARY = {
    "kernel_owned_by_plan_os": True,
    "future_is_path_distribution_not_fixed_point": True,
    "history_is_read_only": True,
    "qi_conditions_geometry_not_authority": True,
    "authority_forbidden_paths_have_zero_mass": True,
    "candidate_field_retained_after_selection": True,
    "hold_mass_preserved_when_admissible": True,
    "future_only_synthesis": True,
    "active_now": False,
    "plan_commit_is_not_execution": True,
}


@dataclass(frozen=True)
class PlanObjectiveGeometry:
    manifold_id: str
    parameter_schema_digest: str
    base_metric_digest: str
    qi_conditioned_metric_digest: str
    history_conditioned_metric_digest: str
    current_distribution_digest: str
    target_region_digest: str
    divergence_kind: str
    entropy_weight: float
    action_weight: float


@dataclass(frozen=True)
class PlanPathAction:
    path_id: str
    candidate_id: str
    transition_action: float
    mission_potential: float
    risk_potential: float
    resource_potential: float
    authority_potential: float
    verification_potential: float
    wa_relational_potential: float
    qi_potential: float
    history_potential: float
    total_action: float
    admissible: bool
    action_digest: str


@dataclass(frozen=True)
class PlanPathDistribution:
    source_state_digest: str
    path_action_digests: tuple[str, ...]
    partition_function: float
    qi_temperature: float
    normalized_path_weights: dict[str, float]
    candidate_mass_map: dict[str, float]
    hold_mass: float
    distribution_digest: str


@dataclass(frozen=True)
class PlanObjectiveUpdate:
    prior_distribution_digest: str
    selected_candidate_id: str
    selected_candidate_mass: float
    retained_candidate_ids: tuple[str, ...]
    dissent_evidence_digests: tuple[str, ...]
    next_distribution_digest: str
    next_plan_basis_digest: str
    future_only: bool
    active_now: bool
    execution_permission: bool
    update_digest: str


@dataclass(frozen=True)
class InformationGeometricQiKernelReceipt:
    version: str
    planos_version: str
    status: str
    geometry: dict[str, Any]
    path_actions: list[dict[str, Any]]
    path_distribution: dict[str, Any] | None
    objective_update: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _finite_nonnegative(value: Any) -> bool:
    return isinstance(value, (int, float)) and isfinite(float(value)) and float(value) >= 0.0


def _positive(value: Any) -> bool:
    return isinstance(value, (int, float)) and isfinite(float(value)) and float(value) > 0.0


def _metric_digest(metric: Mapping[str, Any]) -> str:
    return sha({str(k): metric[k] for k in sorted(metric)})


def qi_condition_metric(
    base_metric: Mapping[str, float],
    qi: Mapping[str, float],
    history: Mapping[str, float],
    *,
    reroute_evidence: bool,
) -> dict[str, float]:
    metric = {str(k): float(v) for k, v in base_metric.items()}
    recovery = max(0.0, float(qi.get("recovery", 0.0)))
    stagnation = max(0.0, float(qi.get("stagnation", 0.0)))
    hysteresis = max(0.0, float(qi.get("hysteresis", 0.0)))
    oscillation = max(0.0, float(history.get("oscillation", 0.0)))
    metric["switch"] = max(0.0, metric.get("switch", 0.0) + recovery + hysteresis + oscillation)
    reroute_delta = stagnation if reroute_evidence else 0.0
    metric["reroute"] = max(0.0, metric.get("reroute", 0.0) - reroute_delta)
    return metric


def build_path_action(path: Mapping[str, Any]) -> PlanPathAction:
    path_id = str(path.get("path_id", "")).strip()
    candidate_id = str(path.get("candidate_id", "")).strip()
    components = {
        "transition_action": float(path.get("transition_action", 0.0)),
        "mission_potential": float(path.get("mission_potential", 0.0)),
        "risk_potential": float(path.get("risk_potential", 0.0)),
        "resource_potential": float(path.get("resource_potential", 0.0)),
        "authority_potential": float(path.get("authority_potential", 0.0)),
        "verification_potential": float(path.get("verification_potential", 0.0)),
        "wa_relational_potential": float(path.get("wa_relational_potential", 0.0)),
        "qi_potential": float(path.get("qi_potential", 0.0)),
        "history_potential": float(path.get("history_potential", 0.0)),
    }
    admissible = bool(path.get("admissible", False)) and components["authority_potential"] == 0.0
    total = sum(components.values()) if admissible else float("inf")
    payload = {
        "path_id": path_id,
        "candidate_id": candidate_id,
        **components,
        "total_action": total,
        "admissible": admissible,
    }
    return PlanPathAction(**payload, action_digest=sha(payload))


def _normalize_actions(
    actions: Iterable[PlanPathAction],
    *,
    qi_temperature: float,
    hold_floor: float,
) -> PlanPathDistribution:
    action_list = list(actions)
    raw: dict[str, float] = {}
    for item in action_list:
        raw[item.path_id] = exp(-item.total_action / qi_temperature) if item.admissible else 0.0
    partition = sum(raw.values())
    if partition <= 0.0:
        raise ValueError("no_admissible_path_mass")
    weights = {path_id: weight / partition for path_id, weight in raw.items()}
    candidate_mass = {candidate: 0.0 for candidate in CANDIDATE_FIELD}
    by_id = {item.path_id: item for item in action_list}
    for path_id, weight in weights.items():
        candidate_mass[by_id[path_id].candidate_id] += weight
    hold_admissible = any(item.admissible and item.candidate_id == "hold" for item in action_list)
    if hold_admissible and candidate_mass["hold"] + 1e-12 < hold_floor:
        deficit = hold_floor - candidate_mass["hold"]
        donor_total = sum(v for k, v in candidate_mass.items() if k != "hold")
        if donor_total <= 0.0 or hold_floor >= 1.0:
            raise ValueError("hold_floor_unsatisfiable")
        for candidate in candidate_mass:
            if candidate != "hold":
                candidate_mass[candidate] *= (1.0 - hold_floor) / donor_total
        candidate_mass["hold"] = hold_floor
        hold_paths = [item.path_id for item in action_list if item.admissible and item.candidate_id == "hold"]
        non_hold_paths = [item.path_id for item in action_list if item.admissible and item.candidate_id != "hold"]
        hold_raw = sum(weights[p] for p in hold_paths)
        non_hold_raw = sum(weights[p] for p in non_hold_paths)
        for path_id in hold_paths:
            weights[path_id] = hold_floor * weights[path_id] / hold_raw
        for path_id in non_hold_paths:
            weights[path_id] = (1.0 - hold_floor) * weights[path_id] / non_hold_raw
    payload = {
        "source_state_digest": "",
        "path_action_digests": tuple(item.action_digest for item in action_list),
        "partition_function": partition,
        "qi_temperature": qi_temperature,
        "normalized_path_weights": weights,
        "candidate_mass_map": candidate_mass,
        "hold_mass": candidate_mass["hold"],
    }
    return PlanPathDistribution(**payload, distribution_digest=sha(payload))


def build_information_geometric_qi_kernel(
    source_state: Mapping[str, Any],
    paths: Iterable[Mapping[str, Any]],
    *,
    base_metric: Mapping[str, float],
    qi: Mapping[str, float],
    history: Mapping[str, float],
    target_region: Mapping[str, Any],
    selected_candidate_id: str,
    dissent_evidence_digests: Iterable[str] = (),
    qi_temperature: float = 1.0,
    hold_floor: float = 0.05,
    entropy_weight: float = 1.0,
    action_weight: float = 1.0,
    reroute_evidence: bool = False,
) -> InformationGeometricQiKernelReceipt:
    blockers: list[str] = []
    if not source_state:
        blockers.append("source_state_missing")
    if not target_region:
        blockers.append("target_region_missing")
    if not _positive(qi_temperature):
        blockers.append("qi_temperature_not_positive")
    if not _finite_nonnegative(hold_floor) or float(hold_floor) >= 1.0:
        blockers.append("hold_floor_invalid")
    if any(not _finite_nonnegative(v) for v in base_metric.values()):
        blockers.append("base_metric_not_nonnegative")

    conditioned_metric = qi_condition_metric(base_metric, qi, history, reroute_evidence=reroute_evidence)
    geometry = PlanObjectiveGeometry(
        manifold_id="planos-finite-path-statistical-manifold-v0.1",
        parameter_schema_digest=sha(("goal", "steps", "observations", "verification", "resources", "rollback", "risk", "wa")),
        base_metric_digest=_metric_digest(base_metric),
        qi_conditioned_metric_digest=_metric_digest(conditioned_metric),
        history_conditioned_metric_digest=sha(history),
        current_distribution_digest=sha(source_state.get("current_distribution", {})),
        target_region_digest=sha(target_region),
        divergence_kind="KL(p||prior)",
        entropy_weight=float(entropy_weight),
        action_weight=float(action_weight),
    )

    path_actions = [build_path_action(path) for path in paths]
    if not path_actions:
        blockers.append("path_field_empty")
    path_ids = [item.path_id for item in path_actions]
    if any(not path_id for path_id in path_ids) or len(set(path_ids)) != len(path_ids):
        blockers.append("path_identity_invalid")
    if any(item.candidate_id not in CANDIDATE_FIELD for item in path_actions):
        blockers.append("candidate_outside_field")
    if selected_candidate_id not in CANDIDATE_FIELD:
        blockers.append("selected_candidate_outside_field")
    if not any(item.admissible and item.candidate_id == selected_candidate_id for item in path_actions):
        blockers.append("selected_candidate_has_no_admissible_path")

    distribution: PlanPathDistribution | None = None
    update: PlanObjectiveUpdate | None = None
    if not blockers:
        try:
            distribution = _normalize_actions(path_actions, qi_temperature=float(qi_temperature), hold_floor=float(hold_floor))
        except ValueError as exc:
            blockers.append(str(exc))

    if distribution is not None and not blockers:
        source_digest = sha(source_state)
        dist_payload = asdict(distribution)
        dist_payload["source_state_digest"] = source_digest
        dist_payload.pop("distribution_digest")
        distribution = PlanPathDistribution(**dist_payload, distribution_digest=sha(dist_payload))
        selected_mass = distribution.candidate_mass_map[selected_candidate_id]
        retained = tuple(candidate for candidate in CANDIDATE_FIELD if candidate != selected_candidate_id)
        update_payload = {
            "prior_distribution_digest": geometry.current_distribution_digest,
            "selected_candidate_id": selected_candidate_id,
            "selected_candidate_mass": selected_mass,
            "retained_candidate_ids": retained,
            "dissent_evidence_digests": tuple(str(x) for x in dissent_evidence_digests),
            "next_distribution_digest": distribution.distribution_digest,
            "next_plan_basis_digest": sha({"selected_candidate_id": selected_candidate_id, "distribution": distribution.distribution_digest}),
            "future_only": True,
            "active_now": False,
            "execution_permission": False,
        }
        update = PlanObjectiveUpdate(**update_payload, update_digest=sha(update_payload))

    status = STATUS_READY if not blockers else "PLANOS_INFORMATION_GEOMETRIC_QI_OBJECTIVE_KERNEL_BLOCKED"
    outer = {
        "version": VERSION,
        "planos_version": PLANOS_VERSION,
        "status": status,
        "geometry": asdict(geometry),
        "path_actions": [asdict(item) for item in path_actions],
        "path_distribution": asdict(distribution) if distribution else None,
        "objective_update": asdict(update) if update else None,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return InformationGeometricQiKernelReceipt(**outer, receipt_digest=sha(outer))
