#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import command_digest

PLAN_VERSION = "indra_qi_approved_recovery_action_plan_v0_9"
EVIDENCE_VERSION = "indra_qi_fresh_observation_evidence_v0_9"
APPROVAL_VERSION = "indra_qi_single_candidate_approval_v0_9"
SELECTABLE_ACTION_KINDS = {
    "observation_request",
    "counterfactual_candidate",
    "bounded_intervention_candidate",
}
ACTION_TO_COMMAND = {
    "observation_request": "observe",
    "counterfactual_candidate": "counterfactual",
    "bounded_intervention_candidate": "intervene",
}
REQUIRED_BOUNDARY = {
    "exact_candidate_digest_required": True,
    "single_candidate_single_transaction": True,
    "fresh_observation_evidence_required": True,
    "approved_action_executes_in_child_v14": True,
    "bounded_intervention_requires_snapshot": True,
    "bounded_intervention_requires_undo_readiness": True,
    "counterfactual_persistent_state_not_mutated": True,
    "observation_updates_child_model_only": True,
    "intervention_updates_child_model_only": True,
    "parent_world_state_not_mutated": True,
    "external_world_not_actuated": True,
    "feedback_return_candidate_only": True,
    "v0_3_feedback_not_direct_mutation": True,
    "base_gauge_connection_not_mutated": True,
    "operator_algebra_unchanged": True,
    "causal_edge_not_gauge_connection": True,
    "qi_not_substance": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_external_world_actuation_authority": True,
    "not_parent_world_update_authority": True,
    "not_operator_algebra_mutation_authority": True,
    "fresh_v14_action_license_required": True,
    "fail_closed_on_boundary_loss": True,
}
EVIDENCE_BOUNDARY = {
    "fresh_observation_not_truth": True,
    "observation_not_free": True,
    "bound_to_selected_candidate": True,
    "bound_to_current_v14_digest": True,
    "instrument_trace_required": True,
    "not_external_actuation": True,
}
APPROVAL_BOUNDARY = {
    "approval_exact_candidate_digest_bound": True,
    "approval_single_transaction_only": True,
    "fresh_observation_reviewed": True,
    "approval_not_truth": True,
    "approval_not_external_actuation_authority": True,
    "approval_not_parent_world_update_authority": True,
    "approval_requires_fresh_execution_license": True,
}
FEEDBACK_BOUNDARY = {
    "feedback_is_candidate_not_direct_mutation": True,
    "source_indra_state_not_mutated": True,
    "causal_result_not_truth": True,
    "causal_edge_not_gauge_connection": True,
    "qi_feedback_not_qi_substance": True,
    "operator_algebra_unchanged": True,
    "gauge_connection_unchanged": True,
    "holonomy_preserved": True,
    "transport_residue_visible": True,
    "noncommutative_order_preserved": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
    "not_world_update_authority": True,
    "approval_required_before_world_mutation": True,
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


def execution_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "execution_plan_digest"))


def evidence_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "evidence_digest"))


def approval_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "approval_digest"))


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def validate_execution_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("approved_action_plan_version_invalid")
    if str(plan.get("execution_plan_digest", "")) != execution_plan_digest(plan):
        blockers.append("approved_action_plan_digest_invalid")
    for field in (
        "execution_id",
        "source_action_envelope_id",
        "source_action_envelope_digest",
        "source_action_activation_record_digest",
        "source_reentry_id",
        "source_reentry_record_digest",
        "source_world_state_digest",
        "source_dynamic_world_state_digest",
        "source_v14_world_model_digest",
        "selected_candidate_id",
        "selected_candidate_digest",
        "selected_action_kind",
        "action_transaction_id",
        "feedback_id",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"approved_action_plan_{field}_missing")
    selected_kind = str(plan.get("selected_action_kind", ""))
    if selected_kind not in SELECTABLE_ACTION_KINDS:
        blockers.append("approved_action_selected_kind_invalid")
    if selected_kind == "bounded_intervention_candidate" and not str(
        plan.get("undo_transaction_id", "")
    ).strip():
        blockers.append("approved_action_undo_transaction_id_missing")
    approved_value = plan.get("approved_value")
    approved_uncertainty = plan.get("approved_uncertainty")
    if isinstance(approved_value, bool) or not isinstance(approved_value, (int, float)):
        blockers.append("approved_action_value_invalid")
    if (
        isinstance(approved_uncertainty, bool)
        or not isinstance(approved_uncertainty, (int, float))
        or float(approved_uncertainty) < 0
    ):
        blockers.append("approved_action_uncertainty_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"approved_action_boundary_{field}_mismatch")
    policy = mapping(plan.get("feedback_policy"))
    kinds = mapping(policy.get("event_kind_base_weight"))
    if set(kinds) != {"observe", "intervene", "counterfactual", "undo"}:
        blockers.append("approved_action_feedback_event_weight_set_invalid")
    for field in (
        "uncertainty_penalty",
        "minimum_candidate_weight",
        "maximum_candidate_weight",
    ):
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or float(raw) < 0:
            blockers.append(f"approved_action_feedback_policy_{field}_invalid")
    if number(policy.get("minimum_candidate_weight")) > number(
        policy.get("maximum_candidate_weight"), 1.0
    ):
        blockers.append("approved_action_feedback_weight_range_invalid")


def validate_evidence(
    *,
    evidence: Mapping[str, Any],
    plan: Mapping[str, Any],
    candidate: Mapping[str, Any],
    current_variable: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if evidence.get("version") != EVIDENCE_VERSION:
        blockers.append("approved_action_evidence_version_invalid")
    if not valid_digest(evidence, "evidence_digest"):
        blockers.append("approved_action_evidence_digest_invalid")
    for field in ("evidence_id", "variable_name", "instrument_trace_digest"):
        if not str(evidence.get(field, "")).strip():
            blockers.append(f"approved_action_evidence_{field}_missing")
    if str(evidence.get("variable_name", "")) != str(
        candidate.get("source_causal_variable", "")
    ):
        blockers.append("approved_action_evidence_variable_mismatch")
    if str(evidence.get("source_v14_world_model_digest", "")) != str(
        plan.get("source_v14_world_model_digest", "")
    ):
        blockers.append("approved_action_evidence_v14_digest_mismatch")
    if str(evidence.get("source_action_envelope_digest", "")) != str(
        plan.get("source_action_envelope_digest", "")
    ):
        blockers.append("approved_action_evidence_envelope_digest_mismatch")
    observed_value = evidence.get("observed_value")
    observed_uncertainty = evidence.get("observed_uncertainty")
    if isinstance(observed_value, bool) or not isinstance(observed_value, (int, float)):
        blockers.append("approved_action_evidence_observed_value_invalid")
    if (
        isinstance(observed_uncertainty, bool)
        or not isinstance(observed_uncertainty, (int, float))
        or float(observed_uncertainty) < 0
    ):
        blockers.append("approved_action_evidence_uncertainty_invalid")
    if observed_value != current_variable.get("value"):
        blockers.append("approved_action_evidence_not_current_variable_value")
    boundary = mapping(evidence.get("boundary"))
    for field, expected in EVIDENCE_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"approved_action_evidence_boundary_{field}_mismatch")


def validate_approval(
    *, approval: Mapping[str, Any], plan: Mapping[str, Any], evidence: Mapping[str, Any], blockers: list[str]
) -> None:
    if approval.get("version") != APPROVAL_VERSION:
        blockers.append("approved_action_approval_version_invalid")
    if not valid_digest(approval, "approval_digest"):
        blockers.append("approved_action_approval_digest_invalid")
    expected = {
        "approved_candidate_id": str(plan.get("selected_candidate_id", "")),
        "approved_candidate_digest": str(plan.get("selected_candidate_digest", "")),
        "approved_action_kind": str(plan.get("selected_action_kind", "")),
        "approved_transaction_id": str(plan.get("action_transaction_id", "")),
        "source_action_envelope_digest": str(plan.get("source_action_envelope_digest", "")),
        "source_evidence_digest": str(evidence.get("evidence_digest", "")),
    }
    for field, expected_value in expected.items():
        if str(approval.get(field, "")) != expected_value:
            blockers.append(f"approved_action_approval_{field}_mismatch")
    if approval.get("approval_scope") != "single_candidate_single_transaction":
        blockers.append("approved_action_approval_scope_invalid")
    if not str(approval.get("approval_id", "")).strip():
        blockers.append("approved_action_approval_id_missing")
    boundary = mapping(approval.get("boundary"))
    for field, expected_value in APPROVAL_BOUNDARY.items():
        if boundary.get(field) is not expected_value:
            blockers.append(f"approved_action_approval_boundary_{field}_mismatch")


def find_selected_candidate(
    envelope: Mapping[str, Any], candidate_id: str, blockers: list[str]
) -> tuple[dict[str, Any], str]:
    matches: list[tuple[dict[str, Any], str]] = []
    collections = {
        "observation_requests": "observation_request",
        "counterfactual_candidates": "counterfactual_candidate",
        "bounded_intervention_candidates": "bounded_intervention_candidate",
    }
    for collection, expected_kind in collections.items():
        for raw in items(envelope.get(collection)):
            candidate = dict(mapping(raw))
            if str(candidate.get("candidate_id", "")) == candidate_id:
                matches.append((candidate, expected_kind))
    if len(matches) != 1:
        blockers.append("approved_action_selected_candidate_not_unique")
        return {}, ""
    candidate, collection_kind = matches[0]
    if str(candidate.get("action_kind", "")) != collection_kind:
        blockers.append("approved_action_selected_candidate_collection_kind_mismatch")
    if not valid_digest(candidate, "action_candidate_digest"):
        blockers.append("approved_action_selected_candidate_digest_invalid")
    boundary = mapping(candidate.get("boundary"))
    for field in (
        "candidate_only",
        "not_truth",
        "not_direct_execution",
        "not_external_actuation",
        "not_world_mutation",
        "not_operator_algebra_mutation",
        "not_gauge_connection_mutation",
        "fresh_license_required",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"approved_action_selected_candidate_boundary_{field}_not_true")
    return candidate, collection_kind


def validate_selected_value(
    *, plan: Mapping[str, Any], candidate: Mapping[str, Any], envelope: Mapping[str, Any], blockers: list[str]
) -> dict[str, Any]:
    selected_kind = str(plan.get("selected_action_kind", ""))
    if str(candidate.get("action_kind", "")) != selected_kind:
        blockers.append("approved_action_selected_kind_candidate_mismatch")
    if str(candidate.get("action_candidate_digest", "")) != str(
        plan.get("selected_candidate_digest", "")
    ):
        blockers.append("approved_action_selected_candidate_digest_mismatch")
    payload = dict(mapping(candidate.get("candidate_payload")))
    approved_value = number(plan.get("approved_value"))
    current_value = number(payload.get("current_value"))
    if selected_kind == "observation_request":
        evidence = mapping(plan.get("fresh_observation_evidence"))
        if plan.get("approved_value") != evidence.get("observed_value"):
            blockers.append("approved_action_observation_value_not_fresh_evidence")
    elif selected_kind == "counterfactual_candidate":
        interval = items(payload.get("candidate_value_interval"))
        if len(interval) != 2 or any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in interval):
            blockers.append("approved_action_counterfactual_interval_invalid")
        elif not float(interval[0]) <= approved_value <= float(interval[1]):
            blockers.append("approved_action_counterfactual_value_outside_interval")
        if payload.get("persistent_world_model_mutation_allowed") is not False:
            blockers.append("approved_action_counterfactual_mutation_boundary_invalid")
    elif selected_kind == "bounded_intervention_candidate":
        maximum_delta = number(payload.get("maximum_delta"), -1.0)
        if maximum_delta < 0:
            blockers.append("approved_action_intervention_maximum_delta_invalid")
        elif abs(approved_value - current_value) > maximum_delta + 1e-12:
            blockers.append("approved_action_intervention_value_exceeds_maximum_delta")
        if payload.get("snapshot_required") is not True:
            blockers.append("approved_action_intervention_snapshot_not_required")
        if payload.get("fresh_intervention_license_required") is not True:
            blockers.append("approved_action_intervention_fresh_license_not_required")
        variable_name = str(candidate.get("source_causal_variable", ""))
        reserves = [
            mapping(value)
            for value in items(envelope.get("undo_reserves"))
            if str(mapping(value).get("source_causal_variable", "")) == variable_name
        ]
        if len(reserves) != 1:
            blockers.append("approved_action_matching_undo_reserve_missing_or_ambiguous")
            return {}
        reserve = dict(reserves[0])
        if not valid_digest(reserve, "action_candidate_digest"):
            blockers.append("approved_action_undo_reserve_digest_invalid")
        if reserve.get("action_kind") != "undo_reserve":
            blockers.append("approved_action_undo_reserve_kind_invalid")
        return reserve
    return {}


def build_v14_action_command(
    *, plan: Mapping[str, Any], candidate: Mapping[str, Any], causal_world_id: str,
    process_tensor_context: Mapping[str, Any]
) -> dict[str, Any]:
    kind = ACTION_TO_COMMAND[str(plan.get("selected_action_kind", ""))]
    variable_name = str(candidate.get("source_causal_variable", ""))
    value = plan.get("approved_value")
    uncertainty = plan.get("approved_uncertainty")
    if kind == "observe":
        payload = {
            "values": {variable_name: value},
            "uncertainties": {variable_name: uncertainty},
            "release_interventions": [],
        }
    elif kind == "counterfactual":
        payload = {
            "do": {variable_name: value},
            "uncertainties": {variable_name: uncertainty},
            "release": [],
        }
    else:
        payload = {
            "set": {variable_name: value},
            "uncertainties": {variable_name: uncertainty},
            "release": [],
        }
    command = {
        "version": "kuuos_causal_world_model_command_v14_0",
        "kind": kind,
        "transaction_id": str(plan.get("action_transaction_id", "")),
        "world_id": causal_world_id,
        "payload": payload,
        "process_tensor_context": dict(process_tensor_context),
    }
    command["command_digest"] = command_digest(command)
    return command


def build_undo_command(
    *, plan: Mapping[str, Any], causal_world_id: str, process_tensor_context: Mapping[str, Any]
) -> dict[str, Any]:
    command = {
        "version": "kuuos_causal_world_model_command_v14_0",
        "kind": "undo",
        "transaction_id": str(plan.get("undo_transaction_id", "")),
        "world_id": causal_world_id,
        "payload": {"target_transaction_id": str(plan.get("action_transaction_id", ""))},
        "process_tensor_context": dict(process_tensor_context),
    }
    command["command_digest"] = command_digest(command)
    return command


def build_feedback_plan(
    *, plan: Mapping[str, Any], projection_packet: Mapping[str, Any], action_event: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "version": "indra_qi_causal_feedback_plan_v0_3",
        "feedback_id": str(plan.get("feedback_id", "")),
        "source_projection_id": str(projection_packet.get("projection_id", "")),
        "source_world_model_id": str(projection_packet.get("source_world_model_id", "")),
        "source_indra_qi_world_state_digest": str(
            projection_packet.get("source_indra_qi_world_state_digest", "")
        ),
        "causal_world_id": str(projection_packet.get("causal_world_id", "")),
        "source_transaction_id": str(action_event.get("transaction_id", "")),
        "source_causal_event_digest": str(action_event.get("record_digest", "")),
        "source_causal_world_model_digest": str(
            action_event.get("after_world_model_digest", "")
        ),
        "feedback_policy": dict(mapping(plan.get("feedback_policy"))),
        "infer_gauge_connection_update_from_causal_edges": False,
        "apply_feedback_directly": False,
        "boundary": dict(FEEDBACK_BOUNDARY),
    }
