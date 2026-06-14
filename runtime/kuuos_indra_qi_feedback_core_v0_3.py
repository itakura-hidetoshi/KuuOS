#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    REQUIRED_BOUNDARIES,
    compute_indra_qi_world_state_digest,
)

PLAN_VERSION = "indra_qi_causal_feedback_plan_v0_3"
ALLOWED_EVENT_KINDS = {"observe", "intervene", "counterfactual", "undo"}
ALLOWED_FEEDBACK_KINDS = {
    "local_patch_observation_candidate",
    "qi_flow_observable_candidate",
}
REQUIRED_BOUNDARY = {
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


def latest_matching(records: list[dict[str, Any]], transaction_id: str) -> dict[str, Any]:
    for record in reversed(records):
        if str(record.get("transaction_id", "")) == transaction_id:
            return record
    return {}


def projection_lineage(
    projection_packet: Mapping[str, Any],
    activation: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, str, str, str]:
    if not valid_digest(projection_packet, "projection_packet_digest"):
        blockers.append("source_projection_packet_digest_invalid")
    if not valid_digest(activation, "activation_record_digest"):
        blockers.append("source_projection_activation_digest_invalid")
    if activation.get("activation_status") != "causal_projection_initialized":
        blockers.append("source_projection_activation_not_initialized")
    if str(activation.get("source_projection_packet_digest", "")) != str(
        projection_packet.get("projection_packet_digest", "")
    ):
        blockers.append("source_projection_packet_activation_digest_mismatch")
    projection_id = str(projection_packet.get("projection_id", ""))
    source_world_model_id = str(projection_packet.get("source_world_model_id", ""))
    causal_world_id = str(projection_packet.get("causal_world_id", ""))
    source_digest = str(projection_packet.get("source_indra_qi_world_state_digest", ""))
    pairs = {
        "projection_id": (projection_id, str(activation.get("projection_id", ""))),
        "source_world_model_id": (
            source_world_model_id,
            str(activation.get("source_world_model_id", "")),
        ),
        "causal_world_id": (causal_world_id, str(activation.get("causal_world_id", ""))),
        "source_indra_digest": (
            source_digest,
            str(activation.get("source_indra_qi_world_state_digest", "")),
        ),
    }
    for field, (left, right) in pairs.items():
        if left != right:
            blockers.append(f"source_projection_{field}_mismatch")
    return projection_id, source_world_model_id, causal_world_id, source_digest


def validate_indra_state(
    state: Mapping[str, Any], source_world_model_id: str, source_digest: str, blockers: list[str]
) -> None:
    if not state:
        blockers.append("source_indra_qi_world_state_missing_or_invalid")
        return
    if str(state.get("world_model_id", "")) != source_world_model_id:
        blockers.append("source_indra_qi_world_model_id_mismatch")
    if str(state.get("indra_qi_world_state_digest", "")) != source_digest:
        blockers.append("source_indra_qi_world_state_digest_mismatch")
    if compute_indra_qi_world_state_digest(state) != source_digest:
        blockers.append("source_indra_qi_world_state_digest_invalid")
    governance = mapping(state.get("governance_boundary"))
    for field, expected in REQUIRED_BOUNDARIES.items():
        if governance.get(field) is not expected:
            blockers.append(f"source_indra_qi_boundary_{field}_mismatch")
    if governance.get("direct_world_update_authority") is not False:
        blockers.append("source_indra_qi_direct_world_update_authority_not_false")
    if governance.get("operator_algebra_update_authority") is not False:
        blockers.append("source_indra_qi_operator_algebra_update_authority_not_false")


def source_event(
    *,
    transaction_id: str,
    causal_world_id: str,
    event_records: list[dict[str, Any]],
    result: Mapping[str, Any],
    causal_state: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    event = latest_matching(event_records, transaction_id)
    if not event:
        blockers.append("source_causal_event_missing")
        return {}
    if not valid_digest(event, "record_digest"):
        blockers.append("source_causal_event_digest_invalid")
    if str(event.get("world_id", "")) != causal_world_id:
        blockers.append("source_causal_event_world_id_mismatch")
    kind = str(event.get("command_kind", ""))
    if kind not in ALLOWED_EVENT_KINDS:
        blockers.append("source_causal_event_kind_not_feedback_eligible")
    if str(result.get("transaction_id", "")) != transaction_id:
        blockers.append("source_causal_result_transaction_id_mismatch")
    if str(result.get("world_id", "")) != causal_world_id:
        blockers.append("source_causal_result_world_id_mismatch")
    if str(result.get("status", "")) != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY":
        blockers.append("source_causal_result_not_ready")
    if str(result.get("event_record_digest", "")) != str(event.get("record_digest", "")):
        blockers.append("source_causal_result_event_digest_mismatch")
    if kind == "counterfactual":
        boundary = mapping(mapping(result.get("operation_result")).get("boundary"))
        if boundary.get("counterfactual_not_fact") is not True:
            blockers.append("source_counterfactual_not_fact_boundary_missing")
        if boundary.get("persistent_world_model_not_mutated") is not True:
            blockers.append("source_counterfactual_persistent_state_boundary_missing")
    else:
        if not valid_v14_digest(causal_state, "world_model_digest"):
            blockers.append("source_causal_world_state_digest_invalid")
        if str(causal_state.get("world_id", "")) != causal_world_id:
            blockers.append("source_causal_world_state_world_id_mismatch")
        if str(event.get("after_world_model_digest", "")) != str(
            causal_state.get("world_model_digest", "")
        ):
            blockers.append("source_causal_event_state_digest_mismatch")
    return event


def variable_values(
    event: Mapping[str, Any], result: Mapping[str, Any], causal_state: Mapping[str, Any]
) -> Mapping[str, Any]:
    if str(event.get("command_kind", "")) == "counterfactual":
        return mapping(mapping(result.get("operation_result")).get("projected_variables"))
    return mapping(causal_state.get("variables"))


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("feedback_plan_version_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"feedback_boundary_{field}_mismatch")
    policy = mapping(plan.get("feedback_policy"))
    kinds = mapping(policy.get("event_kind_base_weight"))
    if set(kinds) != ALLOWED_EVENT_KINDS:
        blockers.append("feedback_policy_event_kind_weight_set_invalid")
    for kind, raw in kinds.items():
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"feedback_policy_event_kind_weight_{kind}_invalid")
    minimum = policy.get("minimum_candidate_weight")
    maximum = policy.get("maximum_candidate_weight")
    for field, raw in (("minimum_candidate_weight", minimum), ("maximum_candidate_weight", maximum)):
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"feedback_policy_{field}_invalid")
    if isinstance(minimum, (int, float)) and isinstance(maximum, (int, float)) and float(minimum) > float(maximum):
        blockers.append("feedback_policy_weight_range_invalid")
    penalty = policy.get("uncertainty_penalty")
    if isinstance(penalty, bool) or not isinstance(penalty, (int, float)) or float(penalty) < 0:
        blockers.append("feedback_policy_uncertainty_penalty_invalid")
    if plan.get("infer_gauge_connection_update_from_causal_edges") is not False:
        blockers.append("feedback_plan_gauge_connection_inference_not_false")
    if plan.get("apply_feedback_directly") is not False:
        blockers.append("feedback_plan_direct_apply_not_false")


def candidate_weight(event_kind: str, uncertainty: float, policy: Mapping[str, Any]) -> float:
    base = mapping(policy.get("event_kind_base_weight")).get(event_kind, 0.0)
    penalty = policy.get("uncertainty_penalty", 1.0)
    minimum = policy.get("minimum_candidate_weight", 0.0)
    maximum = policy.get("maximum_candidate_weight", 1.0)
    values = [base, penalty, minimum, maximum]
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        return 0.0
    return round(max(float(minimum), min(float(maximum), float(base) - float(penalty) * uncertainty)), 8)


def build_candidates(
    *,
    values: Mapping[str, Any],
    bindings: Mapping[str, Any],
    event: Mapping[str, Any],
    policy: Mapping[str, Any],
    blockers: list[str],
) -> tuple[list[dict[str, Any]], int, int]:
    candidates: list[dict[str, Any]] = []
    local_count = 0
    flow_count = 0
    for variable_name, raw_binding in bindings.items():
        binding = mapping(raw_binding)
        variable = mapping(values.get(variable_name))
        if not variable:
            blockers.append(f"feedback_variable_{variable_name}_missing_from_causal_result")
            continue
        uncertainty_raw = variable.get("uncertainty", 0.0)
        if isinstance(uncertainty_raw, bool) or not isinstance(uncertainty_raw, (int, float)):
            blockers.append(f"feedback_variable_{variable_name}_uncertainty_invalid")
            continue
        uncertainty = max(float(uncertainty_raw), 0.0)
        binding_kind = str(binding.get("binding_kind", ""))
        if binding_kind == "local_patch_observable":
            feedback_kind = "local_patch_observation_candidate"
            target = {
                "patch_id": str(binding.get("patch_id", "")),
                "observable_id": str(binding.get("observable_id", "")),
                "source_digest": str(binding.get("source_digest", "")),
            }
            local_count += 1
        elif binding_kind == "qi_flow_observable_projection":
            feedback_kind = "qi_flow_observable_candidate"
            if binding.get("qi_itself") is not False:
                blockers.append(f"feedback_variable_{variable_name}_qi_itself_not_false")
            if binding.get("projection_not_flow_identity") is not True:
                blockers.append(f"feedback_variable_{variable_name}_projection_identity_boundary_missing")
            target = {
                "flow_id": str(binding.get("flow_id", "")),
                "observable_id": str(binding.get("observable_id", "")),
                "source_digest": str(binding.get("source_digest", "")),
                "qi_itself": False,
                "projection_not_flow_identity": True,
            }
            flow_count += 1
        else:
            blockers.append(f"feedback_variable_{variable_name}_binding_kind_invalid")
            continue
        candidate = {
            "candidate_id": f"feedback-{variable_name}-{event.get('transaction_id', '')}",
            "feedback_kind": feedback_kind,
            "source_causal_variable": str(variable_name),
            "source_causal_value": variable.get("value"),
            "source_causal_uncertainty": uncertainty,
            "source_causal_status": str(variable.get("status", "")),
            "target": target,
            "candidate_weight": candidate_weight(str(event.get("command_kind", "")), uncertainty, policy),
            "candidate_payload": {
                "proposed_observable_value": variable.get("value"),
                "proposed_uncertainty": uncertainty,
                "feedback_evidence_digest": sha(
                    {
                        "event_record_digest": event.get("record_digest", ""),
                        "variable_name": variable_name,
                        "variable": dict(variable),
                        "binding": dict(binding),
                    }
                ),
            },
            "boundary": {
                "candidate_only": True,
                "not_truth": True,
                "not_direct_world_mutation": True,
                "not_operator_algebra_mutation": True,
                "not_gauge_connection_mutation": True,
                "not_holonomy_replacement": True,
                "approval_required": True,
            },
        }
        candidates.append(candidate)
    return candidates, local_count, flow_count
