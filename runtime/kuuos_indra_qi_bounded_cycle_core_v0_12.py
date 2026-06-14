#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from runtime.kuuos_indra_qi_approved_action_core_v0_9 import (
    APPROVAL_BOUNDARY,
    APPROVAL_VERSION,
    EVIDENCE_BOUNDARY,
    EVIDENCE_VERSION,
    REQUIRED_BOUNDARY as EXECUTION_BOUNDARY,
    SELECTABLE_ACTION_KINDS,
    approval_digest,
    evidence_digest,
    execution_plan_digest,
)
from runtime.kuuos_indra_qi_child_feedback_cycle_core_v0_10 import (
    REQUIRED_BOUNDARY as BRIDGE_BOUNDARY,
    bridge_plan_digest,
)
from runtime.kuuos_indra_qi_parent_cycle_reentry_core_v0_11 import (
    REQUIRED_BOUNDARY as LOOP_BOUNDARY,
    loop_plan_digest,
)
from runtime.kuuos_indra_qi_recovery_action_core_v0_8 import (
    REQUIRED_BOUNDARY as ACTION_BOUNDARY,
    action_plan_digest,
)

PLAN_VERSION = "indra_qi_bounded_generational_cycle_plan_v0_12"
STATE_VERSION = "indra_qi_bounded_generational_cycle_state_v0_12"
ALLOWED_ACTION_KINDS = set(SELECTABLE_ACTION_KINDS)
ACTION_COLLECTION = {
    "observation_request": "observation_requests",
    "counterfactual_candidate": "counterfactual_candidates",
    "bounded_intervention_candidate": "bounded_intervention_candidates",
}
ACTION_COMMAND = {
    "observation_request": "observe",
    "counterfactual_candidate": "counterfactual",
    "bounded_intervention_candidate": "intervene",
}
REQUIRED_BOUNDARY = {
    "source_v0_11_handoff_required": True,
    "source_v0_11_digest_chain_exact": True,
    "one_generation_per_invocation": True,
    "generation_index_monotone": True,
    "maximum_generation_bound_enforced": True,
    "convergence_stop_enforced": True,
    "v0_8_action_surface_required": True,
    "v0_9_fresh_approval_required": True,
    "v0_10_process_tensor_review_required": True,
    "v0_11_assimilation_reentry_required": True,
    "v0_8_through_v0_11_transaction_compensated": True,
    "parent_runtime_restored_on_failure": True,
    "source_child_runtime_restored_on_failure": True,
    "partial_target_child_removed_on_failure": True,
    "runtime_local_external_state_only": True,
    "base_gauge_connection_not_mutated": True,
    "operator_algebra_unchanged": True,
    "causal_edge_not_gauge_connection": True,
    "qi_not_substance": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_external_world_actuation_authority": True,
    "not_unlicensed_execution_authority": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


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


def runner_state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "runner_state_digest"))


def _bounded(
    policy: Mapping[str, Any],
    fields: tuple[str, ...],
    blockers: list[str],
    prefix: str,
) -> None:
    for field in fields:
        raw = policy.get(field)
        if (
            isinstance(raw, bool)
            or not isinstance(raw, (int, float))
            or not 0 <= float(raw) <= 1
        ):
            blockers.append(f"bounded_cycle_{prefix}_{field}_invalid")


def _positive_int(
    policy: Mapping[str, Any],
    fields: tuple[str, ...],
    blockers: list[str],
    prefix: str,
) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw <= 0:
            blockers.append(f"bounded_cycle_{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("bounded_cycle_plan_version_invalid")
    if str(plan.get("cycle_plan_digest", "")) != cycle_plan_digest(plan):
        blockers.append("bounded_cycle_plan_digest_invalid")
    for field in (
        "runner_id",
        "generation_run_id",
        "source_v0_11_loop_id",
        "source_v0_11_handoff_packet_digest",
        "source_v0_11_record_digest",
        "source_v0_11_ledger_record_digest",
        "expected_previous_runner_state_digest",
        "action_envelope_id",
        "execution_id",
        "action_transaction_id",
        "undo_transaction_id",
        "feedback_id",
        "evidence_id",
        "approval_id",
        "parent_bridge_id",
        "activation_id",
        "process_tensor_cycle_id",
        "assimilation_id",
        "reentry_id",
        "projection_id",
        "causal_world_id",
        "causal_transaction_id",
        "derived_response_patch_id",
        "derived_response_observable_id",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"bounded_cycle_plan_{field}_missing")
    generation = plan.get("generation_index")
    maximum = plan.get("max_generations")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
        blockers.append("bounded_cycle_generation_index_invalid")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1 <= maximum <= 32:
        blockers.append("bounded_cycle_max_generations_invalid")
    if isinstance(generation, int) and isinstance(maximum, int) and generation >= maximum:
        blockers.append("bounded_cycle_generation_index_at_or_above_maximum")
    if str(plan.get("selected_action_kind", "")) not in ALLOWED_ACTION_KINDS:
        blockers.append("bounded_cycle_selected_action_kind_invalid")
    if plan.get("cycle_mode") != "one_compensated_generation":
        blockers.append("bounded_cycle_mode_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"bounded_cycle_boundary_{field}_mismatch")

    gate = mapping(plan.get("gate_policy"))
    _bounded(
        gate,
        (
            "debt_risk_weight",
            "residue_risk_weight",
            "tension_risk_weight",
            "recovery_loss_risk_weight",
            "observe_only_risk_threshold",
            "counterfactual_first_risk_threshold",
            "minimum_intervention_recoverability",
            "maximum_intervention_debt",
            "minimum_intervention_corridor_openness",
            "maximum_intervention_delta",
            "observation_priority_debt_weight",
            "observation_priority_uncertainty_weight",
            "observation_priority_recovery_loss_weight",
        ),
        blockers,
        "gate_policy",
    )
    _positive_int(
        gate,
        (
            "max_observation_requests",
            "max_counterfactual_candidates",
            "max_intervention_candidates",
        ),
        blockers,
        "gate_policy",
    )
    if number(gate.get("counterfactual_first_risk_threshold"), 1.0) > number(
        gate.get("observe_only_risk_threshold"), 0.0
    ):
        blockers.append("bounded_cycle_gate_policy_threshold_order_invalid")

    feedback = mapping(plan.get("feedback_policy"))
    _bounded(
        feedback,
        ("uncertainty_penalty", "minimum_candidate_weight", "maximum_candidate_weight"),
        blockers,
        "feedback_policy",
    )
    _bounded(
        mapping(feedback.get("event_kind_base_weight")),
        ("observe", "intervene", "counterfactual", "undo"),
        blockers,
        "feedback_weight",
    )
    if number(feedback.get("minimum_candidate_weight")) > number(
        feedback.get("maximum_candidate_weight")
    ):
        blockers.append("bounded_cycle_feedback_weight_range_invalid")

    process = mapping(plan.get("process_tensor_policy"))
    _bounded(
        process,
        (
            "min_transition_continuity_score",
            "min_memory_continuity_score",
            "min_nonmarkov_link_density",
            "min_recoverability_branching_capacity",
            "max_observation_debt_pressure",
            "min_candidate_weight",
        ),
        blockers,
        "process_tensor_policy",
    )
    depth = process.get("min_history_depth")
    if isinstance(depth, bool) or not isinstance(depth, int) or depth <= 0:
        blockers.append("bounded_cycle_process_tensor_policy_min_history_depth_invalid")
    for field in (
        "require_process_tensor_visible",
        "require_transition_continuity_visible",
        "require_memory_continuity_visible",
        "require_nonmarkov_memory_visible",
        "require_recoverability_witness",
    ):
        if process.get(field) is not True:
            blockers.append(f"bounded_cycle_process_tensor_policy_{field}_not_true")

    evolution = mapping(plan.get("evolution_policy"))
    _bounded(
        evolution,
        (
            "memory_retention",
            "intervention_residue_retention",
            "nonmarkov_retention",
            "recoverability_retention",
            "observation_debt_retention",
            "min_next_cycle_prior_weight",
            "max_next_cycle_observation_debt",
            "min_next_cycle_recoverability",
        ),
        blockers,
        "evolution_policy",
    )
    _positive_int(evolution, ("max_channels",), blockers, "evolution_policy")

    assimilation = mapping(plan.get("assimilation_policy"))
    _bounded(
        assimilation,
        (
            "world_memory_retention",
            "world_residue_retention",
            "world_nonmarkov_retention",
            "world_recoverability_retention",
            "world_debt_retention",
            "tension_debt_gain",
            "tension_residue_gain",
            "tension_recovery_loss_gain",
            "transport_resistance_gain",
            "holonomy_residue_gain",
            "seed_source_retention",
            "min_post_assimilation_seed_weight",
        ),
        blockers,
        "assimilation_policy",
    )
    _positive_int(
        assimilation,
        ("max_recoverability_branches",),
        blockers,
        "assimilation_policy",
    )

    projection = mapping(plan.get("projection_policy"))
    _bounded(
        projection,
        (
            "debt_uncertainty_gain",
            "residue_uncertainty_gain",
            "minimum_uncertainty",
            "maximum_uncertainty",
            "mechanism_weight_floor",
            "mechanism_weight_ceiling",
            "mechanism_noise_debt_gain",
            "mechanism_bias",
        ),
        blockers,
        "projection_policy",
    )
    _positive_int(
        projection,
        ("minimum_seed_count", "max_projection_variables"),
        blockers,
        "projection_policy",
    )
    if number(projection.get("minimum_uncertainty")) > number(
        projection.get("maximum_uncertainty")
    ):
        blockers.append("bounded_cycle_projection_uncertainty_range_invalid")
    if number(projection.get("mechanism_weight_floor")) > number(
        projection.get("mechanism_weight_ceiling")
    ):
        blockers.append("bounded_cycle_projection_weight_range_invalid")

    _bounded(
        mapping(plan.get("convergence_policy")),
        (
            "maximum_observation_debt",
            "minimum_recoverability_reserve",
            "maximum_intervention_residue",
        ),
        blockers,
        "convergence_policy",
    )
