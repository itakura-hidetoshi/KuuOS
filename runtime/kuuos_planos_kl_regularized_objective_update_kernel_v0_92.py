from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, isfinite
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_kl_regularized_objective_update_kernel_v0_92"
SOURCE_VERSION = "kuuos_planos_information_geometric_qi_objective_kernel_v0_91"
STATUS_READY = "PLANOS_KL_REGULARIZED_OBJECTIVE_UPDATE_KERNEL_READY"
CANDIDATE_FIELD = (
    "continue", "strengthen", "repair", "slow_down",
    "reobserve", "reroute", "hold", "terminate_candidate",
)

BOUNDARY = {
    "prior_distribution_preserved": True,
    "admissible_support_preserved": True,
    "positive_prior_support_preserved": True,
    "hold_mass_preserved": True,
    "authority_invariance_preserved": True,
    "history_read_only": True,
    "future_only": True,
    "active_now": False,
    "execution_permission": False,
}


@dataclass(frozen=True)
class KLRegularizedObjectiveUpdate:
    version: str
    source_version: str
    status: str
    prior_distribution_digest: str
    expected_action_digest: str
    admissible_candidate_ids: list[str]
    beta: float
    entropy_weight: float
    effective_temperature: float
    next_distribution: dict[str, float] | None
    selected_candidate_id: str
    selected_candidate_mass: float
    retained_candidate_ids: list[str]
    next_distribution_digest: str
    next_plan_basis_digest: str
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalise(values: Mapping[str, float]) -> dict[str, float]:
    total = sum(values.values())
    if not isfinite(total) or total <= 0.0:
        return {}
    return {key: value / total for key, value in values.items()}


def _preserve_hold_floor(distribution: dict[str, float], hold_floor: float) -> dict[str, float]:
    if "hold" not in distribution or distribution["hold"] >= hold_floor:
        return distribution
    other_total = sum(value for key, value in distribution.items() if key != "hold")
    if other_total <= 0.0:
        return {key: (1.0 if key == "hold" else 0.0) for key in distribution}
    scale = (1.0 - hold_floor) / other_total
    return {
        key: (hold_floor if key == "hold" else value * scale)
        for key, value in distribution.items()
    }


def build_kl_regularized_objective_update(
    source_kernel: Mapping[str, Any],
    *,
    prior_distribution: Mapping[str, float],
    expected_action: Mapping[str, float],
    admissible_candidate_ids: list[str],
    beta: float = 1.0,
    entropy_weight: float = 0.25,
    hold_floor: float = 0.05,
    selected_candidate_id: str | None = None,
) -> KLRegularizedObjectiveUpdate:
    blockers: list[str] = []
    if source_kernel.get("version") != SOURCE_VERSION:
        blockers.append("source_kernel_version_invalid")
    if source_kernel.get("status") != "PLANOS_INFORMATION_GEOMETRIC_QI_OBJECTIVE_KERNEL_READY":
        blockers.append("source_kernel_not_ready")
    if not source_kernel.get("receipt_digest"):
        blockers.append("source_kernel_receipt_digest_missing")

    if beta < 0.0 or not isfinite(beta):
        blockers.append("beta_invalid")
    if entropy_weight < 0.0 or not isfinite(entropy_weight):
        blockers.append("entropy_weight_invalid")
    if hold_floor < 0.0 or hold_floor >= 1.0 or not isfinite(hold_floor):
        blockers.append("hold_floor_invalid")

    admissible = list(dict.fromkeys(admissible_candidate_ids))
    if not admissible or len(admissible) != len(admissible_candidate_ids):
        blockers.append("admissible_candidate_ids_invalid")
    if any(candidate not in CANDIDATE_FIELD for candidate in admissible):
        blockers.append("unknown_admissible_candidate")

    prior = {candidate: float(prior_distribution.get(candidate, 0.0)) for candidate in admissible}
    actions = {candidate: float(expected_action.get(candidate, float("nan"))) for candidate in admissible}
    for candidate in admissible:
        if prior[candidate] <= 0.0 or not isfinite(prior[candidate]):
            blockers.append(f"prior_support_invalid:{candidate}")
        if actions[candidate] < 0.0 or not isfinite(actions[candidate]):
            blockers.append(f"expected_action_invalid:{candidate}")

    prior_normalized = _normalise(prior)
    if not prior_normalized:
        blockers.append("prior_distribution_not_normalizable")

    selected = selected_candidate_id or (
        min(admissible, key=lambda candidate: actions[candidate]) if admissible and not blockers else ""
    )
    if selected and selected not in admissible:
        blockers.append("selected_candidate_outside_admissible_field")

    next_distribution: dict[str, float] | None = None
    selected_mass = 0.0
    retained: list[str] = []
    next_distribution_digest = ""
    next_plan_basis_digest = ""
    status = "PLANOS_KL_REGULARIZED_OBJECTIVE_UPDATE_KERNEL_BLOCKED"
    effective_temperature = 1.0 + entropy_weight

    if not blockers:
        raw = {
            candidate: (prior_normalized[candidate] ** (1.0 / effective_temperature))
            * exp(-beta * actions[candidate] / effective_temperature)
            for candidate in admissible
        }
        next_distribution = _normalise(raw)
        if not next_distribution:
            blockers.append("next_distribution_not_normalizable")
        else:
            if "hold" in admissible:
                next_distribution = _preserve_hold_floor(next_distribution, hold_floor)
            next_distribution = _normalise(next_distribution)
            if not next_distribution or abs(sum(next_distribution.values()) - 1.0) > 1e-9:
                blockers.append("next_distribution_not_normalized")
            elif any(value <= 0.0 for value in next_distribution.values()):
                blockers.append("positive_support_not_preserved")

    if not blockers and next_distribution is not None:
        selected_mass = next_distribution[selected]
        retained = [candidate for candidate in admissible if candidate != selected]
        next_distribution_digest = sha(next_distribution)
        next_plan_basis = {
            "selected_candidate_id": selected,
            "selected_candidate_mass": selected_mass,
            "retained_candidate_ids": retained,
            "prior_distribution_digest": sha(prior_normalized),
            "next_distribution_digest": next_distribution_digest,
            "future_only": True,
            "active_now": False,
            "execution_permission": False,
        }
        next_plan_basis_digest = sha(next_plan_basis)
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "prior_distribution_digest": sha(prior_normalized) if prior_normalized else "",
        "expected_action_digest": sha(actions) if actions else "",
        "admissible_candidate_ids": admissible,
        "beta": beta,
        "entropy_weight": entropy_weight,
        "effective_temperature": effective_temperature,
        "next_distribution": next_distribution,
        "selected_candidate_id": selected,
        "selected_candidate_mass": selected_mass,
        "retained_candidate_ids": retained,
        "next_distribution_digest": next_distribution_digest,
        "next_plan_basis_digest": next_plan_basis_digest,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return KLRegularizedObjectiveUpdate(**outer, receipt_digest=sha(outer))
