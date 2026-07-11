#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-10
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


@dataclass
class WorldConditionedObjectiveDistributionUpdateResult:
    status: str
    blockers: list[str]
    update: dict | None


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def finite(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=TOL)


def compute_world_conditioned_action_bundle_digest(
    *,
    candidate_world_projection_digests: dict[str, str],
    plan_transition_action_map: dict[str, float],
    world_transition_action_map: dict[str, float],
    combined_transition_action_map: dict[str, float],
) -> str:
    return canonical_digest(
        {
            "candidate_world_projection_digests": candidate_world_projection_digests,
            "plan_transition_action_map": plan_transition_action_map,
            "world_transition_action_map": world_transition_action_map,
            "combined_transition_action_map": combined_transition_action_map,
        }
    )


def compute_prior_distribution_digest(prior_distribution: dict[str, float]) -> str:
    return canonical_digest(prior_distribution)


def _preserve_hold_floor(
    distribution: dict[str, float], hold_floor: float
) -> dict[str, float]:
    if "hold" not in distribution or distribution["hold"] >= hold_floor - TOL:
        return distribution
    other_total = sum(value for key, value in distribution.items() if key != "hold")
    if other_total <= 0.0:
        return {key: (1.0 if key == "hold" else 0.0) for key in distribution}
    scale = (1.0 - hold_floor) / other_total
    return {
        key: (hold_floor if key == "hold" else value * scale)
        for key, value in distribution.items()
    }


def build_world_conditioned_objective_distribution_update(
    *,
    source_world_conditioned_metric_certificate_digest: str,
    source_world_binding_digest: str,
    source_world_model_state_digest: str,
    source_world_model_revision: int,
    source_world_lineage_digest: str,
    world_conditioned_action_bundle_digest: str,
    candidate_world_projection_digests: dict[str, str],
    plan_transition_action_map: dict[str, float],
    world_transition_action_map: dict[str, float],
    combined_transition_action_map: dict[str, float],
    prior_distribution_digest: str,
    prior_distribution: dict[str, float],
    admissible_candidate_ids: list[str],
    beta: float,
    entropy_weight: float,
    hold_floor: float,
) -> WorldConditionedObjectiveDistributionUpdateResult:
    blockers: list[str] = []
    text_fields = {
        "source_world_conditioned_metric_certificate_digest": source_world_conditioned_metric_certificate_digest,
        "source_world_binding_digest": source_world_binding_digest,
        "source_world_model_state_digest": source_world_model_state_digest,
        "source_world_lineage_digest": source_world_lineage_digest,
        "world_conditioned_action_bundle_digest": world_conditioned_action_bundle_digest,
        "prior_distribution_digest": prior_distribution_digest,
    }
    blockers.extend(
        f"missing_{name}"
        for name, value in text_fields.items()
        if not isinstance(value, str) or not value
    )
    if (
        not isinstance(source_world_model_revision, int)
        or isinstance(source_world_model_revision, bool)
        or source_world_model_revision < 0
    ):
        blockers.append("invalid_source_world_model_revision")
    if not finite(beta) or float(beta) < 0.0:
        blockers.append("invalid_beta")
    if not finite(entropy_weight) or float(entropy_weight) < 0.0:
        blockers.append("invalid_entropy_weight")
    if not finite(hold_floor) or not 0.0 <= float(hold_floor) < 1.0:
        blockers.append("invalid_hold_floor")

    maps = {
        "candidate_world_projection_digests": candidate_world_projection_digests,
        "plan_transition_action_map": plan_transition_action_map,
        "world_transition_action_map": world_transition_action_map,
        "combined_transition_action_map": combined_transition_action_map,
        "prior_distribution": prior_distribution,
    }
    for name, value in maps.items():
        if not isinstance(value, dict) or not value:
            blockers.append(f"invalid_{name}")

    candidate_ids: set[str] = set()
    if isinstance(candidate_world_projection_digests, dict):
        candidate_ids = set(candidate_world_projection_digests)
        if any(
            not isinstance(candidate_id, str)
            or not candidate_id
            or candidate_id not in CANDIDATE_FIELD
            for candidate_id in candidate_ids
        ):
            blockers.append("invalid_source_candidate_id")
        if any(
            not isinstance(digest, str) or not digest
            for digest in candidate_world_projection_digests.values()
        ):
            blockers.append("invalid_candidate_world_projection_digest")
        if len(set(candidate_world_projection_digests.values())) != len(
            candidate_world_projection_digests
        ):
            blockers.append("duplicate_candidate_world_projection_digest")

    for name, value in {
        "plan_transition_action_map": plan_transition_action_map,
        "world_transition_action_map": world_transition_action_map,
        "combined_transition_action_map": combined_transition_action_map,
        "prior_distribution": prior_distribution,
    }.items():
        if isinstance(value, dict) and set(value) != candidate_ids:
            blockers.append(f"{name}_candidate_set_mismatch")

    for name, action_map in {
        "plan": plan_transition_action_map,
        "world": world_transition_action_map,
        "combined": combined_transition_action_map,
    }.items():
        if isinstance(action_map, dict):
            for candidate_id, value in action_map.items():
                if not finite(value) or float(value) < 0.0:
                    blockers.append(f"invalid_{name}_action_{candidate_id}")

    if (
        isinstance(plan_transition_action_map, dict)
        and isinstance(world_transition_action_map, dict)
        and isinstance(combined_transition_action_map, dict)
    ):
        for candidate_id in candidate_ids:
            if all(
                finite(action_map.get(candidate_id))
                for action_map in (
                    plan_transition_action_map,
                    world_transition_action_map,
                    combined_transition_action_map,
                )
            ):
                plan_action = float(plan_transition_action_map[candidate_id])
                world_action = float(world_transition_action_map[candidate_id])
                combined_action = float(combined_transition_action_map[candidate_id])
                if combined_action + TOL < plan_action:
                    blockers.append(f"combined_action_below_plan_action_{candidate_id}")
                if world_action < -TOL:
                    blockers.append(f"negative_world_action_{candidate_id}")

    if not isinstance(admissible_candidate_ids, list):
        blockers.append("invalid_admissible_candidate_ids")
        admissible: list[str] = []
    else:
        admissible = list(admissible_candidate_ids)
        if not admissible or len(admissible) != len(set(admissible)):
            blockers.append("invalid_admissible_candidate_ids")
        if any(candidate_id not in candidate_ids for candidate_id in admissible):
            blockers.append("admissible_candidate_outside_source_field")

    if isinstance(prior_distribution, dict):
        total_prior = 0.0
        for candidate_id, value in prior_distribution.items():
            if not finite(value) or float(value) < 0.0:
                blockers.append(f"invalid_prior_mass_{candidate_id}")
                continue
            total_prior += float(value)
        if total_prior <= 0.0 or not math.isfinite(total_prior):
            blockers.append("prior_distribution_not_normalizable")
        for candidate_id in admissible:
            value = prior_distribution.get(candidate_id)
            if not finite(value) or float(value) <= 0.0:
                blockers.append(f"positive_prior_support_missing_{candidate_id}")

    if not blockers:
        expected_bundle_digest = compute_world_conditioned_action_bundle_digest(
            candidate_world_projection_digests=candidate_world_projection_digests,
            plan_transition_action_map=plan_transition_action_map,
            world_transition_action_map=world_transition_action_map,
            combined_transition_action_map=combined_transition_action_map,
        )
        if world_conditioned_action_bundle_digest != expected_bundle_digest:
            blockers.append("world_conditioned_action_bundle_digest_mismatch")
        if prior_distribution_digest != compute_prior_distribution_digest(
            prior_distribution
        ):
            blockers.append("prior_distribution_digest_mismatch")

    if blockers:
        return WorldConditionedObjectiveDistributionUpdateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    prior_total = sum(float(value) for value in prior_distribution.values())
    normalized_prior = {
        candidate_id: float(prior_distribution[candidate_id]) / prior_total
        for candidate_id in candidate_ids
    }
    effective_temperature = 1.0 + float(entropy_weight)
    minimum_action = min(
        float(combined_transition_action_map[candidate_id])
        for candidate_id in admissible
    )
    raw_weights = {
        candidate_id: (
            normalized_prior[candidate_id]
            ** (1.0 / effective_temperature)
            * math.exp(
                -float(beta)
                * (
                    float(combined_transition_action_map[candidate_id])
                    - minimum_action
                )
                / effective_temperature
            )
        )
        for candidate_id in admissible
    }
    partition_function = sum(raw_weights.values())
    if not math.isfinite(partition_function) or partition_function <= 0.0:
        return WorldConditionedObjectiveDistributionUpdateResult(
            STATUS_BLOCKED, ["next_distribution_not_normalizable"], None
        )

    admissible_distribution = {
        candidate_id: raw_weights[candidate_id] / partition_function
        for candidate_id in admissible
    }
    if "hold" in admissible:
        admissible_distribution = _preserve_hold_floor(
            admissible_distribution, float(hold_floor)
        )
        normalized_total = sum(admissible_distribution.values())
        admissible_distribution = {
            candidate_id: value / normalized_total
            for candidate_id, value in admissible_distribution.items()
        }

    next_distribution = {
        candidate_id: (
            admissible_distribution[candidate_id]
            if candidate_id in admissible_distribution
            else 0.0
        )
        for candidate_id in sorted(candidate_ids)
    }
    if not close(sum(next_distribution.values()), 1.0):
        return WorldConditionedObjectiveDistributionUpdateResult(
            STATUS_BLOCKED, ["next_distribution_not_normalized"], None
        )
    if any(value < -TOL for value in next_distribution.values()):
        return WorldConditionedObjectiveDistributionUpdateResult(
            STATUS_BLOCKED, ["negative_candidate_mass"], None
        )
    if any(next_distribution[candidate_id] <= 0.0 for candidate_id in admissible):
        return WorldConditionedObjectiveDistributionUpdateResult(
            STATUS_BLOCKED, ["positive_admissible_support_not_preserved"], None
        )
    if (
        "hold" in admissible
        and next_distribution["hold"] + TOL < float(hold_floor)
    ):
        return WorldConditionedObjectiveDistributionUpdateResult(
            STATUS_BLOCKED, ["hold_floor_not_preserved"], None
        )

    update = {
        "kernel": "PlanOS WORLD-Conditioned Objective Distribution Update Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.01",
        "source_world_conditioned_metric_certificate_digest": source_world_conditioned_metric_certificate_digest,
        "source_world_binding_digest": source_world_binding_digest,
        "source_world_model_state_digest": source_world_model_state_digest,
        "source_world_model_revision": source_world_model_revision,
        "source_world_lineage_digest": source_world_lineage_digest,
        "world_conditioned_action_bundle_digest": world_conditioned_action_bundle_digest,
        "candidate_world_projection_digests": dict(
            sorted(candidate_world_projection_digests.items())
        ),
        "plan_transition_action_map": dict(
            sorted((key, float(value)) for key, value in plan_transition_action_map.items())
        ),
        "world_transition_action_map": dict(
            sorted((key, float(value)) for key, value in world_transition_action_map.items())
        ),
        "combined_transition_action_map": dict(
            sorted(
                (key, float(value))
                for key, value in combined_transition_action_map.items()
            )
        ),
        "prior_distribution_digest": prior_distribution_digest,
        "normalized_prior_distribution": dict(sorted(normalized_prior.items())),
        "admissible_candidate_ids": sorted(admissible),
        "beta": float(beta),
        "entropy_weight": float(entropy_weight),
        "effective_temperature": effective_temperature,
        "minimum_combined_action": minimum_action,
        "partition_function": partition_function,
        "hold_floor": float(hold_floor),
        "next_distribution": next_distribution,
        "candidate_mass_nonnegative": True,
        "normalized_next_distribution": True,
        "admissible_support_preserved": True,
        "positive_prior_support_preserved": True,
        "hold_mass_preserved": (
            "hold" not in admissible
            or next_distribution["hold"] + TOL >= float(hold_floor)
        ),
        "candidate_field_retained": True,
        "nonadmissible_candidates_zero_mass": all(
            next_distribution[candidate_id] == 0.0
            for candidate_id in candidate_ids
            if candidate_id not in admissible
        ),
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "decision_selection_performed": False,
        "selected_candidate_id": "",
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    update["next_distribution_digest"] = canonical_digest(next_distribution)
    update["world_conditioned_distribution_update_digest"] = canonical_digest(update)
    return WorldConditionedObjectiveDistributionUpdateResult(
        STATUS_READY, [], update
    )
