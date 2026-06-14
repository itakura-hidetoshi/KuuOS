#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

PLAN_VERSION = "indra_qi_process_tensor_cycle_plan_v0_5"
EVENT_RESIDUE_FACTORS = {
    "observe": 0.20,
    "intervene": 0.85,
    "counterfactual": 0.40,
    "undo": 0.60,
}
REQUIRED_BOUNDARY = {
    "cycle_evolution_not_truth": True,
    "process_tensor_state_not_execution_authority": True,
    "source_world_state_not_mutated": True,
    "runtime_local_external_state_only": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "next_cycle_seed_not_fact": True,
    "next_cycle_seed_not_direct_execution_authority": True,
    "operator_algebra_unchanged": True,
    "gauge_connection_unchanged": True,
    "holonomy_preserved": True,
    "two_truths_gap_preserved": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def cycle_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "cycle_plan_digest"))


def cycle_state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "process_tensor_cycle_state_digest"))


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def target_key(target: Mapping[str, Any]) -> str:
    observable_id = str(target.get("observable_id", ""))
    if str(target.get("flow_id", "")):
        return f"flow:{target.get('flow_id')}:{observable_id}"
    return f"patch:{target.get('patch_id', '')}:{observable_id}"


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("process_tensor_cycle_plan_version_invalid")
    if str(plan.get("cycle_plan_digest", "")) != cycle_plan_digest(plan):
        blockers.append("process_tensor_cycle_plan_digest_invalid")
    if not str(plan.get("cycle_id", "")).strip():
        blockers.append("process_tensor_cycle_id_missing")
    if plan.get("evolution_mode") != "non_markov_overlay_assimilation":
        blockers.append("process_tensor_cycle_evolution_mode_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"process_tensor_cycle_boundary_{field}_mismatch")
    policy = mapping(plan.get("evolution_policy"))
    for field in (
        "memory_retention",
        "intervention_residue_retention",
        "nonmarkov_retention",
        "recoverability_retention",
        "observation_debt_retention",
        "min_next_cycle_prior_weight",
        "max_next_cycle_observation_debt",
        "min_next_cycle_recoverability",
    ):
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"process_tensor_cycle_policy_{field}_invalid")
    maximum = policy.get("max_channels")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
        blockers.append("process_tensor_cycle_policy_max_channels_invalid")


def validate_overlay_chain(overlays: list[Mapping[str, Any]], blockers: list[str]) -> None:
    previous = "GENESIS"
    seen: set[str] = set()
    for index, overlay in enumerate(overlays):
        if not valid_digest(overlay, "overlay_digest"):
            blockers.append(f"world_overlay_{index}_digest_invalid")
        digest = str(overlay.get("overlay_digest", ""))
        if not digest or digest in seen:
            blockers.append(f"world_overlay_{index}_digest_missing_or_duplicate")
        seen.add(digest)
        if str(overlay.get("previous_overlay_digest", "")) != previous:
            blockers.append(f"world_overlay_{index}_previous_digest_mismatch")
        boundary = mapping(overlay.get("boundary"))
        for field in (
            "runtime_observation_overlay_only",
            "operator_algebra_unchanged",
            "gauge_connection_unchanged",
            "holonomy_preserved",
            "external_world_not_actuated",
            "rollback_snapshot_available",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"world_overlay_{index}_{field}_not_true")
        previous = digest


def previous_channel_map(previous_state: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for raw in items(previous_state.get("channels")):
        channel = mapping(raw)
        key = str(channel.get("target_key", ""))
        if key:
            result[key] = channel
    return result


def _number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def evolve_channel(
    *,
    overlay: Mapping[str, Any],
    assessment: Mapping[str, Any],
    previous: Mapping[str, Any],
    event_kind: str,
    policy: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    weight = clamp(_number(overlay.get("candidate_weight")))
    uncertainty = clamp(_number(overlay.get("observed_uncertainty")))
    influence = clamp(weight * (1.0 - uncertainty))

    memory_retention = _number(policy.get("memory_retention"), 0.75)
    residue_retention = _number(policy.get("intervention_residue_retention"), 0.70)
    nonmarkov_retention = _number(policy.get("nonmarkov_retention"), 0.75)
    recovery_retention = _number(policy.get("recoverability_retention"), 0.70)
    debt_retention = _number(policy.get("observation_debt_retention"), 0.80)

    previous_memory = _number(previous.get("memory_kernel_strength"))
    previous_residue = _number(previous.get("intervention_residue"))
    previous_nonmarkov = _number(previous.get("nonmarkov_coupling"))
    previous_recovery = _number(previous.get("recoverability_reserve"))
    previous_debt = _number(previous.get("observation_debt"))

    assessment_nonmarkov = clamp(_number(assessment.get("nonmarkov_link_density")))
    assessment_recovery = clamp(_number(assessment.get("recoverability_branching_capacity")))
    assessment_debt = clamp(_number(assessment.get("observation_debt_pressure")))
    event_factor = EVENT_RESIDUE_FACTORS.get(event_kind, 0.50)

    memory = clamp(memory_retention * previous_memory + (1.0 - memory_retention) * influence)
    residue = clamp(
        residue_retention * previous_residue
        + (1.0 - residue_retention) * event_factor * weight
    )
    nonmarkov = clamp(
        nonmarkov_retention * previous_nonmarkov
        + (1.0 - nonmarkov_retention) * assessment_nonmarkov
    )
    recovery = clamp(
        recovery_retention * previous_recovery
        + (1.0 - recovery_retention) * assessment_recovery
    )
    debt_input = clamp(assessment_debt + uncertainty * (1.0 - weight))
    debt = clamp(debt_retention * previous_debt + (1.0 - debt_retention) * debt_input)
    resonance = clamp((memory + nonmarkov + recovery + (1.0 - debt)) / 4.0)
    next_prior = clamp(
        0.30 * weight
        + 0.20 * memory
        + 0.15 * nonmarkov
        + 0.15 * recovery
        + 0.20 * (1.0 - debt)
        - 0.10 * residue
    )

    target = dict(mapping(overlay.get("target")))
    channel = {
        "target_key": target_key(target),
        "target": target,
        "cycle_index": cycle_index,
        "observed_value": overlay.get("observed_value"),
        "observed_uncertainty": uncertainty,
        "candidate_weight": weight,
        "memory_kernel_strength": memory,
        "intervention_residue": residue,
        "nonmarkov_coupling": nonmarkov,
        "recoverability_reserve": recovery,
        "observation_debt": debt,
        "relational_resonance": resonance,
        "next_cycle_prior_weight": next_prior,
        "source_overlay_digest": str(overlay.get("overlay_digest", "")),
        "source_process_tensor_assessment_digest": str(
            overlay.get("process_tensor_assessment_digest", "")
        ),
        "source_process_history_digest": str(overlay.get("process_history_digest", "")),
        "previous_channel_state_digest": str(previous.get("channel_state_digest", "GENESIS"))
        if previous
        else "GENESIS",
        "boundary": {
            "process_tensor_channel_not_truth": True,
            "memory_kernel_not_substance": True,
            "intervention_residue_visible": True,
            "observation_debt_visible": True,
            "recoverability_visible": True,
            "non_markov_feedback_preserved": True,
            "not_direct_execution_authority": True,
        },
    }
    channel["channel_state_digest"] = sha(channel)
    return channel


def seed_admissible(channel: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return bool(
        _number(channel.get("next_cycle_prior_weight"))
        >= _number(policy.get("min_next_cycle_prior_weight"))
        and _number(channel.get("observation_debt"))
        <= _number(policy.get("max_next_cycle_observation_debt"), 1.0)
        and _number(channel.get("recoverability_reserve"))
        >= _number(policy.get("min_next_cycle_recoverability"))
    )


def build_seed_entry(channel: Mapping[str, Any], process_context: Mapping[str, Any]) -> dict[str, Any]:
    entry = {
        "seed_id": f"next-cycle-{channel.get('target_key', '')}",
        "target_key": str(channel.get("target_key", "")),
        "target": dict(mapping(channel.get("target"))),
        "prior_weight": channel.get("next_cycle_prior_weight"),
        "memory_kernel_strength": channel.get("memory_kernel_strength"),
        "intervention_residue": channel.get("intervention_residue"),
        "nonmarkov_coupling": channel.get("nonmarkov_coupling"),
        "recoverability_reserve": channel.get("recoverability_reserve"),
        "observation_debt": channel.get("observation_debt"),
        "source_channel_state_digest": str(channel.get("channel_state_digest", "")),
        "process_tensor_context": dict(process_context),
        "boundary": {
            "seed_not_fact": True,
            "seed_not_truth": True,
            "seed_not_direct_execution_authority": True,
            "seed_requires_new_projection_license": True,
            "candidate_weighting_not_truth": True,
        },
    }
    entry["seed_entry_digest"] = sha(entry)
    return entry
