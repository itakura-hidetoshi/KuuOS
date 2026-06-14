#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_indra_qi_approved_action_core_v0_9 import (
    APPROVAL_BOUNDARY,
    APPROVAL_VERSION,
    EVIDENCE_BOUNDARY,
    EVIDENCE_VERSION,
    REQUIRED_BOUNDARY as EXECUTION_BOUNDARY,
    approval_digest,
    evidence_digest,
    execution_plan_digest,
)
from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import (
    ACTION_COLLECTION,
    clamp,
    items,
    mapping,
    number,
    sha,
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


def build_action_plan(
    plan: Mapping[str, Any],
    world: Mapping[str, Any],
    reentry: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "version": "indra_qi_recoverability_action_envelope_plan_v0_8",
        "action_envelope_id": str(plan.get("action_envelope_id", "")),
        "source_reentry_id": str(reentry.get("reentry_id", "")),
        "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
        "source_world_state_digest": str(world.get("indra_qi_world_state_digest", "")),
        "source_dynamic_world_state_digest": str(
            world.get("process_tensor_dynamic_world_state_digest", "")
        ),
        "source_v14_world_model_digest": str(reentry.get("v14_world_model_digest", "")),
        "action_mode": "recoverability_gated_candidate_envelope",
        "gate_policy": dict(mapping(plan.get("gate_policy"))),
        "boundary": dict(ACTION_BOUNDARY),
    }
    value["action_plan_digest"] = action_plan_digest(value)
    return value


def select_candidate(
    envelope: Mapping[str, Any],
    action_kind: str,
    blockers: list[str],
) -> dict[str, Any]:
    field = ACTION_COLLECTION.get(action_kind, "")
    values = [dict(mapping(value)) for value in items(envelope.get(field))]
    values = [value for value in values if value]
    if not values:
        blockers.append(f"bounded_cycle_selected_{action_kind}_candidate_missing")
        return {}
    values.sort(
        key=lambda value: (
            -number(value.get("candidate_priority")),
            str(value.get("candidate_id", "")),
        )
    )
    return values[0]


def build_execution_plan(
    *,
    plan: Mapping[str, Any],
    world: Mapping[str, Any],
    reentry: Mapping[str, Any],
    causal: Mapping[str, Any],
    envelope: Mapping[str, Any],
    activation: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    action_kind = str(plan.get("selected_action_kind", ""))
    variable_name = str(candidate.get("source_causal_variable", ""))
    current = mapping(mapping(causal.get("variables")).get(variable_name))
    current_value = number(current.get("value"))
    if action_kind == "observation_request":
        approved_value = current_value
    elif action_kind == "counterfactual_candidate":
        interval = items(
            mapping(candidate.get("candidate_payload")).get("candidate_value_interval")
        )
        approved_value = (
            clamp((number(interval[0]) + number(interval[1])) / 2.0)
            if len(interval) == 2
            else current_value
        )
        if approved_value == current_value and len(interval) == 2:
            approved_value = clamp(number(interval[1]))
    else:
        delta = number(mapping(candidate.get("candidate_payload")).get("maximum_delta"))
        approved_value = clamp(current_value + delta / 2.0)

    evidence = {
        "version": EVIDENCE_VERSION,
        "evidence_id": str(plan.get("evidence_id", "")),
        "variable_name": variable_name,
        "observed_value": current_value,
        "observed_uncertainty": number(current.get("uncertainty")),
        "source_v14_world_model_digest": str(causal.get("world_model_digest", "")),
        "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
        "instrument_trace_digest": sha(
            {
                "runner_id": str(plan.get("runner_id", "")),
                "generation": plan.get("generation_index"),
                "variable": variable_name,
                "causal_digest": str(causal.get("world_model_digest", "")),
            }
        ),
        "boundary": dict(EVIDENCE_BOUNDARY),
    }
    evidence["evidence_digest"] = evidence_digest(evidence)
    approval = {
        "version": APPROVAL_VERSION,
        "approval_id": str(plan.get("approval_id", "")),
        "approved_candidate_id": str(candidate.get("candidate_id", "")),
        "approved_candidate_digest": str(candidate.get("action_candidate_digest", "")),
        "approved_action_kind": action_kind,
        "approved_transaction_id": str(plan.get("action_transaction_id", "")),
        "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
        "source_evidence_digest": evidence["evidence_digest"],
        "approval_scope": "single_candidate_single_transaction",
        "boundary": dict(APPROVAL_BOUNDARY),
    }
    approval["approval_digest"] = approval_digest(approval)
    value = {
        "version": "indra_qi_approved_recovery_action_plan_v0_9",
        "execution_id": str(plan.get("execution_id", "")),
        "source_action_envelope_id": str(envelope.get("action_envelope_id", "")),
        "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
        "source_action_activation_record_digest": str(
            activation.get("activation_record_digest", "")
        ),
        "source_reentry_id": str(reentry.get("reentry_id", "")),
        "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
        "source_world_state_digest": str(world.get("indra_qi_world_state_digest", "")),
        "source_dynamic_world_state_digest": str(
            world.get("process_tensor_dynamic_world_state_digest", "")
        ),
        "source_v14_world_model_digest": str(causal.get("world_model_digest", "")),
        "selected_candidate_id": str(candidate.get("candidate_id", "")),
        "selected_candidate_digest": str(candidate.get("action_candidate_digest", "")),
        "selected_action_kind": action_kind,
        "action_transaction_id": str(plan.get("action_transaction_id", "")),
        "undo_transaction_id": str(plan.get("undo_transaction_id", "")),
        "feedback_id": str(plan.get("feedback_id", "")),
        "approved_value": approved_value,
        "approved_uncertainty": number(current.get("uncertainty")),
        "fresh_observation_evidence": evidence,
        "approval": approval,
        "feedback_policy": dict(mapping(plan.get("feedback_policy"))),
        "boundary": dict(EXECUTION_BOUNDARY),
    }
    value["execution_plan_digest"] = execution_plan_digest(value)
    return value


def approved_feedback_candidate_ids(
    feedback: Mapping[str, Any],
    blockers: list[str],
) -> list[str]:
    candidates = [mapping(value) for value in items(feedback.get("feedback_candidates"))]
    local = [
        str(value.get("candidate_id", ""))
        for value in candidates
        if value.get("feedback_kind") == "local_patch_observation_candidate"
    ]
    flow = [
        str(value.get("candidate_id", ""))
        for value in candidates
        if value.get("feedback_kind") == "qi_flow_observable_candidate"
    ]
    if not local:
        blockers.append("bounded_cycle_feedback_local_patch_candidate_missing")
    if not flow:
        blockers.append("bounded_cycle_feedback_qi_flow_candidate_missing")
    return ([local[0]] if local else []) + ([flow[0]] if flow else [])


def build_bridge_plan(
    *,
    plan: Mapping[str, Any],
    world: Mapping[str, Any],
    reentry: Mapping[str, Any],
    execution: Mapping[str, Any],
    execution_ledger: Mapping[str, Any],
    feedback: Mapping[str, Any],
    feedback_handoff: Mapping[str, Any],
    previous_cycle_digest: str,
    approved_ids: list[str],
) -> dict[str, Any]:
    value = {
        "version": "indra_qi_child_feedback_parent_cycle_plan_v0_10",
        "bridge_id": str(plan.get("parent_bridge_id", "")),
        "source_execution_id": str(execution.get("execution_id", "")),
        "source_execution_record_digest": str(execution.get("execution_record_digest", "")),
        "source_execution_ledger_record_digest": str(execution_ledger.get("record_digest", "")),
        "source_reentry_id": str(reentry.get("reentry_id", "")),
        "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
        "source_parent_world_state_digest": str(world.get("indra_qi_world_state_digest", "")),
        "source_child_feedback_id": str(feedback.get("feedback_id", "")),
        "source_child_feedback_packet_digest": str(feedback.get("feedback_packet_digest", "")),
        "source_child_feedback_handoff_digest": str(
            feedback_handoff.get("approval_handoff_digest", "")
        ),
        "activation_id": str(plan.get("activation_id", "")),
        "cycle_id": str(plan.get("process_tensor_cycle_id", "")),
        "expected_previous_cycle_state_digest": previous_cycle_digest,
        "approved_candidate_ids": list(approved_ids),
        "handoff_mode": "child_feedback_to_parent_process_tensor_cycle",
        "process_tensor_policy": dict(mapping(plan.get("process_tensor_policy"))),
        "evolution_policy": dict(mapping(plan.get("evolution_policy"))),
        "boundary": dict(BRIDGE_BOUNDARY),
    }
    value["bridge_plan_digest"] = bridge_plan_digest(value)
    return value


def build_loop_plan(
    *,
    plan: Mapping[str, Any],
    world: Mapping[str, Any],
    handoff: Mapping[str, Any],
    bridge_record: Mapping[str, Any],
    bridge_ledger: Mapping[str, Any],
    cycle: Mapping[str, Any],
    seed: Mapping[str, Any],
) -> dict[str, Any]:
    previous_dynamic = str(world.get("process_tensor_dynamic_world_state_digest", "")) or "GENESIS"
    value = {
        "version": "indra_qi_parent_cycle_assimilation_reentry_plan_v0_11",
        "loop_id": str(plan.get("generation_run_id", "")),
        "source_v0_10_bridge_id": str(handoff.get("bridge_id", "")),
        "source_v0_10_handoff_packet_digest": str(handoff.get("handoff_packet_digest", "")),
        "source_v0_10_bridge_record_digest": str(bridge_record.get("bridge_record_digest", "")),
        "source_v0_10_ledger_record_digest": str(bridge_ledger.get("record_digest", "")),
        "source_parent_world_state_digest": str(world.get("indra_qi_world_state_digest", "")),
        "source_cycle_id": str(cycle.get("cycle_id", "")),
        "source_cycle_state_digest": str(cycle.get("process_tensor_cycle_state_digest", "")),
        "source_cycle_seed_packet_digest": str(seed.get("next_cycle_seed_packet_digest", "")),
        "assimilation_id": str(plan.get("assimilation_id", "")),
        "expected_previous_dynamic_world_state_digest": previous_dynamic,
        "reentry_id": str(plan.get("reentry_id", "")),
        "projection_id": str(plan.get("projection_id", "")),
        "causal_world_id": str(plan.get("causal_world_id", "")),
        "transaction_id": str(plan.get("causal_transaction_id", "")),
        "derived_response_patch_id": str(plan.get("derived_response_patch_id", "")),
        "derived_response_observable_id": str(
            plan.get("derived_response_observable_id", "")
        ),
        "loop_mode": "parent_cycle_assimilation_then_causal_reentry",
        "assimilation_policy": dict(mapping(plan.get("assimilation_policy"))),
        "projection_policy": dict(mapping(plan.get("projection_policy"))),
        "boundary": dict(LOOP_BOUNDARY),
    }
    value["loop_plan_digest"] = loop_plan_digest(value)
    return value


def dynamic_metrics(world: Mapping[str, Any]) -> dict[str, Any]:
    states = [mapping(value) for value in items(world.get("local_patch_dynamic_states"))]
    states += [mapping(value) for value in items(world.get("qi_flow_effective_states"))]
    states = [value for value in states if value]
    if not states:
        return {
            "state_count": 0,
            "maximum_observation_debt": 1.0,
            "minimum_recoverability_reserve": 0.0,
            "maximum_intervention_residue": 1.0,
        }
    return {
        "state_count": len(states),
        "maximum_observation_debt": round(
            max(number(value.get("observation_debt")) for value in states), 8
        ),
        "minimum_recoverability_reserve": round(
            min(number(value.get("recoverability_reserve")) for value in states), 8
        ),
        "maximum_intervention_residue": round(
            max(number(value.get("intervention_residue")) for value in states), 8
        ),
    }


def convergence_reached(
    metrics: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    return (
        int(metrics.get("state_count", 0) or 0) > 0
        and number(metrics.get("maximum_observation_debt"), 1.0)
        <= number(policy.get("maximum_observation_debt"), 0.0)
        and number(metrics.get("minimum_recoverability_reserve"), 0.0)
        >= number(policy.get("minimum_recoverability_reserve"), 1.0)
        and number(metrics.get("maximum_intervention_residue"), 1.0)
        <= number(policy.get("maximum_intervention_residue"), 0.0)
    )
