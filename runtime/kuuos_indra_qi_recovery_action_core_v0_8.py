#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

PLAN_VERSION = "indra_qi_recoverability_action_envelope_plan_v0_8"
ALLOWED_ACTION_KINDS = {
    "observation_request",
    "counterfactual_candidate",
    "bounded_intervention_candidate",
    "undo_reserve",
}
MODE_ORDER = {
    "bounded_intervention_candidate": 0,
    "counterfactual_first": 1,
    "observe_only": 2,
}
REQUIRED_BOUNDARY = {
    "action_envelope_not_execution": True,
    "action_candidate_not_truth": True,
    "debt_gates_action_surface": True,
    "recoverability_gates_action_surface": True,
    "critical_corridor_observe_only": True,
    "qi_flow_observation_only": True,
    "counterfactual_before_intervention_when_constrained": True,
    "bounded_intervention_requires_open_corridor": True,
    "undo_reserve_required_for_intervention_candidate": True,
    "parent_world_state_not_mutated": True,
    "child_causal_world_not_mutated": True,
    "base_gauge_connection_not_mutated": True,
    "operator_algebra_unchanged": True,
    "causal_edge_not_gauge_connection": True,
    "qi_not_substance": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
    "not_external_world_actuation_authority": True,
    "not_world_update_authority": True,
    "fresh_action_license_required": True,
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


def action_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "action_plan_digest"))


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("recovery_action_plan_version_invalid")
    if str(plan.get("action_plan_digest", "")) != action_plan_digest(plan):
        blockers.append("recovery_action_plan_digest_invalid")
    for field in (
        "action_envelope_id",
        "source_reentry_id",
        "source_reentry_record_digest",
        "source_world_state_digest",
        "source_dynamic_world_state_digest",
        "source_v14_world_model_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"recovery_action_plan_{field}_missing")
    if plan.get("action_mode") != "recoverability_gated_candidate_envelope":
        blockers.append("recovery_action_plan_mode_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"recovery_action_boundary_{field}_mismatch")

    policy = mapping(plan.get("gate_policy"))
    bounded_fields = (
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
    )
    for field in bounded_fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"recovery_action_policy_{field}_invalid")
    observe = number(policy.get("observe_only_risk_threshold"), 1.0)
    counterfactual = number(policy.get("counterfactual_first_risk_threshold"), 0.0)
    if counterfactual > observe:
        blockers.append("recovery_action_policy_risk_threshold_order_invalid")
    for field in (
        "max_observation_requests",
        "max_counterfactual_candidates",
        "max_intervention_candidates",
    ):
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
            blockers.append(f"recovery_action_policy_{field}_invalid")


def dynamic_indexes(world_state: Mapping[str, Any]) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    patches: dict[str, Mapping[str, Any]] = {}
    flows: dict[str, Mapping[str, Any]] = {}
    for raw in items(world_state.get("local_patch_dynamic_states")):
        state = mapping(raw)
        patch_id = str(mapping(state.get("target")).get("patch_id", ""))
        if patch_id:
            patches[patch_id] = state
    for raw in items(world_state.get("qi_flow_effective_states")):
        state = mapping(raw)
        flow_id = str(mapping(state.get("target")).get("flow_id", ""))
        if flow_id:
            flows[flow_id] = state
    return patches, flows


def corridor_index(world_state: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for raw in items(world_state.get("recoverability_corridors")):
        value = mapping(raw)
        target = mapping(value.get("target"))
        key = str(target.get("patch_id", "")) or str(target.get("flow_id", ""))
        if key:
            result[key] = value
    return result


def risk_score(state: Mapping[str, Any], policy: Mapping[str, Any]) -> float:
    return clamp(
        number(policy.get("debt_risk_weight"), 0.35) * number(state.get("observation_debt"))
        + number(policy.get("residue_risk_weight"), 0.25) * number(state.get("intervention_residue"))
        + number(policy.get("tension_risk_weight"), 0.20) * number(state.get("relational_tension"))
        + number(policy.get("recovery_loss_risk_weight"), 0.20)
        * (1.0 - number(state.get("recoverability_reserve"), 1.0))
    )


def observation_priority(
    state: Mapping[str, Any], variable: Mapping[str, Any], policy: Mapping[str, Any]
) -> float:
    return clamp(
        number(policy.get("observation_priority_debt_weight"), 0.45)
        * number(state.get("observation_debt"))
        + number(policy.get("observation_priority_uncertainty_weight"), 0.35)
        * number(variable.get("uncertainty"))
        + number(policy.get("observation_priority_recovery_loss_weight"), 0.20)
        * (1.0 - number(state.get("recoverability_reserve"), 1.0))
    )


def classify_mode(
    *,
    state: Mapping[str, Any],
    corridor: Mapping[str, Any],
    is_flow: bool,
    policy: Mapping[str, Any],
) -> tuple[str, float, float]:
    risk = risk_score(state, policy)
    openness = number(
        corridor.get("openness"),
        number(state.get("recoverability_corridor_openness")),
    )
    status = str(
        corridor.get("status", state.get("recoverability_corridor_status", "critical"))
    )
    debt = number(state.get("observation_debt"))
    recovery = number(state.get("recoverability_reserve"))
    if is_flow:
        return "observe_only", risk, openness
    if status == "critical" or risk >= number(policy.get("observe_only_risk_threshold"), 0.72):
        return "observe_only", risk, openness
    intervention_allowed = (
        status == "open"
        and recovery >= number(policy.get("minimum_intervention_recoverability"), 0.67)
        and debt <= number(policy.get("maximum_intervention_debt"), 0.25)
        and openness >= number(policy.get("minimum_intervention_corridor_openness"), 0.67)
    )
    if (
        status == "constrained"
        or risk >= number(policy.get("counterfactual_first_risk_threshold"), 0.38)
        or not intervention_allowed
    ):
        return "counterfactual_first", risk, openness
    return "bounded_intervention_candidate", risk, openness


def action_candidate(
    *,
    candidate_id: str,
    kind: str,
    variable_name: str,
    binding: Mapping[str, Any],
    state: Mapping[str, Any],
    corridor: Mapping[str, Any],
    variable: Mapping[str, Any],
    priority: float,
    mode: str,
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "variable_name": variable_name,
        "current_value": variable.get("value"),
        "current_uncertainty": variable.get("uncertainty"),
        "binding": dict(binding),
        "observation_debt": state.get("observation_debt"),
        "recoverability_reserve": state.get("recoverability_reserve"),
        "intervention_residue": state.get("intervention_residue"),
        "relational_tension": state.get("relational_tension"),
        "corridor_status": corridor.get(
            "status", state.get("recoverability_corridor_status")
        ),
        "corridor_openness": corridor.get(
            "openness", state.get("recoverability_corridor_openness")
        ),
    }
    if kind == "observation_request":
        payload.update(
            {
                "requested_measurement": "fresh_observation_required",
                "predicted_value_not_accepted_as_observation": True,
                "release_interventions": [],
            }
        )
    elif kind == "counterfactual_candidate":
        delta = number(policy.get("maximum_intervention_delta"), 0.15)
        current = number(variable.get("value"))
        payload.update(
            {
                "candidate_value_interval": [clamp(current - delta), clamp(current + delta)],
                "persistent_world_model_mutation_allowed": False,
                "counterfactual_not_fact": True,
            }
        )
    elif kind == "bounded_intervention_candidate":
        admissibility = clamp(
            number(state.get("recoverability_reserve"))
            * (1.0 - number(state.get("observation_debt")))
            * (1.0 - number(state.get("intervention_residue")))
            * number(payload.get("corridor_openness"))
        )
        payload.update(
            {
                "maximum_delta": round(
                    number(policy.get("maximum_intervention_delta"), 0.15)
                    * admissibility,
                    8,
                ),
                "admissibility": admissibility,
                "fresh_goal_required": True,
                "fresh_intervention_license_required": True,
                "snapshot_required": True,
            }
        )
    elif kind == "undo_reserve":
        payload.update(
            {
                "target_transaction_id": "FILL_AFTER_APPROVED_INTERVENTION",
                "snapshot_required": True,
                "undo_license_required": True,
            }
        )
    candidate = {
        "candidate_id": candidate_id,
        "action_kind": kind,
        "source_causal_variable": variable_name,
        "source_variable_status": str(variable.get("status", "")),
        "gate_mode": mode,
        "candidate_priority": priority,
        "candidate_payload": payload,
        "source_dynamic_state_entry_digest": str(state.get("dynamic_state_entry_digest", "")),
        "source_corridor_digest": str(corridor.get("corridor_digest", "")),
        "boundary": {
            "candidate_only": True,
            "not_truth": True,
            "not_direct_execution": True,
            "not_external_actuation": True,
            "not_world_mutation": True,
            "not_operator_algebra_mutation": True,
            "not_gauge_connection_mutation": True,
            "fresh_license_required": True,
        },
    }
    candidate["action_candidate_digest"] = sha(candidate)
    return candidate


def build_action_envelope(
    *,
    plan: Mapping[str, Any],
    world_state: Mapping[str, Any],
    generated_projection_plan: Mapping[str, Any],
    causal_state: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    policy = mapping(plan.get("gate_policy"))
    patch_states, flow_states = dynamic_indexes(world_state)
    corridors = corridor_index(world_state)
    generated_variables = mapping(generated_projection_plan.get("variables"))
    causal_variables = mapping(causal_state.get("variables"))

    observations: list[dict[str, Any]] = []
    counterfactuals: list[dict[str, Any]] = []
    interventions: list[dict[str, Any]] = []
    undo_reserves: list[dict[str, Any]] = []
    variable_gates: list[dict[str, Any]] = []

    for name, raw in generated_variables.items():
        generated = mapping(raw)
        if generated.get("status") != "observed":
            continue
        variable = mapping(causal_variables.get(name))
        if not variable:
            blockers.append(f"recovery_action_variable_{name}_missing_from_v14_state")
            continue
        binding = mapping(generated.get("source_binding"))
        kind = str(binding.get("binding_kind", ""))
        is_flow = kind == "qi_flow_observable_projection"
        target_id = str(binding.get("flow_id", "")) if is_flow else str(binding.get("patch_id", ""))
        state = flow_states.get(target_id, {}) if is_flow else patch_states.get(target_id, {})
        corridor = corridors.get(target_id, {})
        if not state:
            blockers.append(f"recovery_action_variable_{name}_dynamic_state_missing")
            continue
        if not valid_digest(state, "dynamic_state_entry_digest"):
            blockers.append(f"recovery_action_variable_{name}_dynamic_digest_invalid")
        if corridor and not valid_digest(corridor, "corridor_digest"):
            blockers.append(f"recovery_action_variable_{name}_corridor_digest_invalid")
        conditioning = mapping(generated.get("world_conditioning"))
        if str(conditioning.get("source_dynamic_state_entry_digest", "")) != str(
            state.get("dynamic_state_entry_digest", "")
        ):
            blockers.append(f"recovery_action_variable_{name}_conditioning_digest_mismatch")

        mode, risk, openness = classify_mode(
            state=state,
            corridor=corridor,
            is_flow=is_flow,
            policy=policy,
        )
        priority = observation_priority(state, variable, policy)
        observations.append(
            action_candidate(
                candidate_id=f"observe-{name}",
                kind="observation_request",
                variable_name=name,
                binding=binding,
                state=state,
                corridor=corridor,
                variable=variable,
                priority=priority,
                mode=mode,
                policy=policy,
            )
        )
        if mode != "observe_only" and not is_flow:
            counterfactuals.append(
                action_candidate(
                    candidate_id=f"counterfactual-{name}",
                    kind="counterfactual_candidate",
                    variable_name=name,
                    binding=binding,
                    state=state,
                    corridor=corridor,
                    variable=variable,
                    priority=risk,
                    mode=mode,
                    policy=policy,
                )
            )
        if mode == "bounded_intervention_candidate" and not is_flow:
            intervention = action_candidate(
                candidate_id=f"intervention-{name}",
                kind="bounded_intervention_candidate",
                variable_name=name,
                binding=binding,
                state=state,
                corridor=corridor,
                variable=variable,
                priority=clamp(1.0 - risk),
                mode=mode,
                policy=policy,
            )
            interventions.append(intervention)
            undo_reserves.append(
                action_candidate(
                    candidate_id=f"undo-reserve-{name}",
                    kind="undo_reserve",
                    variable_name=name,
                    binding=binding,
                    state=state,
                    corridor=corridor,
                    variable=variable,
                    priority=1.0,
                    mode=mode,
                    policy=policy,
                )
            )
        variable_gates.append(
            {
                "variable_name": name,
                "binding_kind": kind,
                "target_id": target_id,
                "gate_mode": mode,
                "risk_score": risk,
                "corridor_openness": openness,
                "corridor_status": str(
                    corridor.get("status", state.get("recoverability_corridor_status", ""))
                ),
                "observation_debt": state.get("observation_debt"),
                "recoverability_reserve": state.get("recoverability_reserve"),
                "intervention_residue": state.get("intervention_residue"),
                "source_dynamic_state_entry_digest": str(state.get("dynamic_state_entry_digest", "")),
            }
        )

    observations.sort(key=lambda value: (-number(value.get("candidate_priority")), str(value.get("candidate_id"))))
    counterfactuals.sort(key=lambda value: (-number(value.get("candidate_priority")), str(value.get("candidate_id"))))
    interventions.sort(key=lambda value: (-number(value.get("candidate_priority")), str(value.get("candidate_id"))))
    observations = observations[: int(policy.get("max_observation_requests", len(observations)))]
    counterfactuals = counterfactuals[: int(policy.get("max_counterfactual_candidates", len(counterfactuals)))]
    interventions = interventions[: int(policy.get("max_intervention_candidates", len(interventions)))]
    allowed_intervention_ids = {
        str(value.get("source_causal_variable", "")) for value in interventions
    }
    undo_reserves = [
        value
        for value in undo_reserves
        if str(value.get("source_causal_variable", "")) in allowed_intervention_ids
    ]

    aggregate_mode = "bounded_intervention_candidate"
    for gate in variable_gates:
        mode = str(gate.get("gate_mode", "observe_only"))
        if MODE_ORDER.get(mode, 2) > MODE_ORDER[aggregate_mode]:
            aggregate_mode = mode

    envelope = {
        "version": "indra_qi_recoverability_action_envelope_v0_8",
        "envelope_status": "recoverability_gated_action_candidates_ready",
        "action_envelope_id": str(plan.get("action_envelope_id", "")),
        "aggregate_gate_mode": aggregate_mode,
        "variable_gates": variable_gates,
        "observation_requests": observations,
        "counterfactual_candidates": counterfactuals,
        "bounded_intervention_candidates": interventions,
        "undo_reserves": undo_reserves,
        "candidate_ordering": [
            str(value.get("candidate_id", ""))
            for value in observations + counterfactuals + interventions + undo_reserves
        ],
        "budgets": {
            "observation_request_count": len(observations),
            "counterfactual_candidate_count": len(counterfactuals),
            "bounded_intervention_candidate_count": len(interventions),
            "undo_reserve_count": len(undo_reserves),
        },
        "boundary": {
            **REQUIRED_BOUNDARY,
            "envelope_contains_candidates_only": True,
            "no_v14_command_invoked": True,
            "fresh_observation_required": True,
            "future_approval_required": True,
        },
    }
    envelope["action_envelope_digest"] = sha(envelope)
    return envelope
