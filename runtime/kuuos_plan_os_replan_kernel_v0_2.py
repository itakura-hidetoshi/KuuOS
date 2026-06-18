from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_learn_os_types_v0_1 import (
    LEARNING_DELTA_VERSION,
    MIDDLE_WAY_REPORT_VERSION,
    learning_delta_digest,
    middle_way_report_digest,
)
from runtime.kuuos_plan_os_replan_types_v0_2 import (
    APPLY_RESULT_VERSION,
    CANDIDATE_PACKET_VERSION,
    CANDIDATE_TYPES,
    CONSTRAINT_REPORT_VERSION,
    DECISION_RECEIPT_VERSION,
    EVENT_VERSION,
    HISTORY_PACKET_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    QI_CONDITION_PACKET_VERSION,
    REPLAN_PHASE_RECEIPT_VERSION,
    REQUIRED_BOUNDARY,
    ROUTES,
    ROUTE_BY_CANDIDATE_TYPE,
    STATE_VERSION,
    SYNTHESIS_PACKET_VERSION,
    apply_result_digest,
    candidate_digest,
    constraint_report_digest,
    copy_boundary,
    copy_non_authority,
    decision_receipt_digest,
    history_packet_digest,
    next_phase,
    nonnegative_number,
    qi_condition_packet_digest,
    replan_event_digest,
    replan_phase_receipt_digest,
    replan_state_digest,
    require_bool,
    require_int,
    require_string,
    synthesis_packet_digest,
    unit_number,
    unique_strings,
)

ALLOWED_CANDIDATES_BY_LEARNING_ROUTE = {
    "LEARNING_REINFORCEMENT_CANDIDATE": {
        "continue",
        "strengthen",
        "slow_down",
        "hold",
    },
    "LEARNING_REPAIR_CANDIDATE": {
        "repair",
        "slow_down",
        "reroute",
        "hold",
    },
    "LEARNING_REOBSERVATION_CANDIDATE": {"reobserve", "hold"},
    "LEARNING_HOLD": {"hold", "reobserve"},
}
SWITCH_EXEMPT_TYPES = frozenset({"continue", "hold", "reobserve"})


def _seal(packet: dict[str, Any], field: str, supplied: Any = None) -> dict[str, Any]:
    packet[field] = ""
    expected = sha({key: value for key, value in packet.items() if key != field})
    packet[field] = expected
    if supplied not in (None, "", expected):
        raise ValueError(f"{field}_invalid")
    return packet


def _validate_learn_payloads(learn_state: Mapping[str, Any]) -> None:
    delta = learn_state.get("learning_delta")
    gate = learn_state.get("middle_way_report")
    if not isinstance(delta, Mapping) or delta.get("version") != LEARNING_DELTA_VERSION:
        raise ValueError("source_learning_delta_invalid")
    if delta.get("learning_delta_digest") != learning_delta_digest(delta):
        raise ValueError("source_learning_delta_digest_invalid")
    if delta.get("learning_delta_digest") != learn_state.get("learning_delta_digest"):
        raise ValueError("source_learning_delta_binding_mismatch")
    if delta.get("future_only") is not True:
        raise ValueError("source_learning_delta_future_only_required")
    if delta.get("active_now") is not False:
        raise ValueError("source_learning_delta_must_be_inactive")
    if delta.get("activation_requires_replan") is not True:
        raise ValueError("source_learning_delta_replan_required")
    if not isinstance(gate, Mapping) or gate.get("version") != MIDDLE_WAY_REPORT_VERSION:
        raise ValueError("source_middle_way_report_invalid")
    if gate.get("middle_way_report_digest") != middle_way_report_digest(gate):
        raise ValueError("source_middle_way_report_digest_invalid")
    if gate.get("middle_way_report_digest") != learn_state.get("middle_way_report_digest"):
        raise ValueError("source_middle_way_report_binding_mismatch")


def build_initial_replan_state(
    *,
    replan_id: str,
    current_plan_state: Mapping[str, Any],
    learn_state: Mapping[str, Any],
    current_cycle_index: int,
    plan_budget: float,
    maximum_candidate_risk: float,
    base_switch_threshold: float,
    now_ms: int,
) -> dict[str, Any]:
    plan_errors = validate_plan_state(current_plan_state)
    if plan_errors:
        raise ValueError("invalid_current_plan_state:" + ";".join(plan_errors))
    if current_plan_state.get("current_phase") != "commit":
        raise ValueError("current_plan_not_committed")
    learn_errors = validate_learn_state(learn_state)
    if learn_errors:
        raise ValueError("invalid_source_learn_state:" + ";".join(learn_errors))
    if learn_state.get("current_phase") != "commit":
        raise ValueError("source_learn_not_committed")
    if learn_state.get("learning_recorded") is not True:
        raise ValueError("source_learning_not_recorded")
    if learn_state.get("replan_required") is not True:
        raise ValueError("source_replan_debt_missing")
    _validate_learn_payloads(learn_state)
    if current_plan_state.get("mission_contract_digest") != learn_state.get(
        "mission_contract_digest"
    ):
        raise ValueError("replan_mission_contract_mismatch")

    state = {
        "version": STATE_VERSION,
        "replan_id": require_string(replan_id, "replan_id"),
        "lineage_id": require_string(current_plan_state.get("lineage_id"), "lineage_id"),
        "mission_contract_digest": require_string(
            current_plan_state.get("mission_contract_digest"), "mission_contract_digest"
        ),
        "source_plan_id": require_string(current_plan_state.get("plan_id"), "source_plan_id"),
        "source_plan_state_digest": require_string(
            current_plan_state.get("plan_state_digest"), "source_plan_state_digest"
        ),
        "source_committed_plan_digest": require_string(
            current_plan_state.get("latest_committed_plan_digest"),
            "source_committed_plan_digest",
        ),
        "source_plan_basis_digest": require_string(
            current_plan_state.get("plan_basis_digest"), "source_plan_basis_digest"
        ),
        "source_plan_route": require_string(
            current_plan_state.get("route"), "source_plan_route"
        ),
        "source_learn_id": require_string(learn_state.get("learn_id"), "source_learn_id"),
        "source_learn_state_digest": require_string(
            learn_state.get("learn_state_digest"), "source_learn_state_digest"
        ),
        "source_learning_route": require_string(
            learn_state.get("route"), "source_learning_route"
        ),
        "source_learning_delta_digest": require_string(
            learn_state.get("learning_delta_digest"), "source_learning_delta_digest"
        ),
        "source_middle_way_report_digest": require_string(
            learn_state.get("middle_way_report_digest"),
            "source_middle_way_report_digest",
        ),
        "source_verification_evidence_digest": require_string(
            learn_state.get("source_verification_evidence_digest"),
            "source_verification_evidence_digest",
        ),
        "source_learning_delta": deepcopy(dict(learn_state["learning_delta"])),
        "source_middle_way_report": deepcopy(dict(learn_state["middle_way_report"])),
        "current_cycle_index": require_int(current_cycle_index, "current_cycle_index"),
        "active_from_cycle": require_int(current_cycle_index, "current_cycle_index") + 1,
        "plan_budget": nonnegative_number(plan_budget, "plan_budget"),
        "maximum_candidate_risk": unit_number(
            maximum_candidate_risk, "maximum_candidate_risk"
        ),
        "base_switch_threshold": unit_number(
            base_switch_threshold, "base_switch_threshold"
        ),
        "current_phase": "bind",
        "route": "PENDING",
        "event_index": 0,
        "replan_version": 0,
        "committed_records": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "predecessor_replan_state_digest": "",
        "replan_state_digest": "",
        "history_packet": {},
        "history_packet_digest": "",
        "qi_condition_packet": {},
        "qi_condition_packet_digest": "",
        "candidates": [],
        "candidate_field_digest": "",
        "constraint_reports": [],
        "constraint_field_digest": "",
        "admissible_candidate_ids": [],
        "decision_receipt": {},
        "decision_receipt_digest": "",
        "selected_candidate_id": "",
        "selected_candidate_digest": "",
        "synthesis_packet": {},
        "synthesis_packet_digest": "",
        "next_plan_basis_digest": "",
        "next_plan_basis_committed": False,
        "next_plan_phase_required": False,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "memory_overwrite": False,
        "host_license_granted": False,
        "processed_event_digests": [],
        "event_history": [],
        "record_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["replan_state_digest"] = replan_state_digest(state)
    return state


def validate_replan_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("replan_state_version_invalid")
        for field in (
            "replan_id",
            "lineage_id",
            "mission_contract_digest",
            "source_plan_id",
            "source_plan_state_digest",
            "source_committed_plan_digest",
            "source_plan_basis_digest",
            "source_plan_route",
            "source_learn_id",
            "source_learn_state_digest",
            "source_learning_route",
            "source_learning_delta_digest",
            "source_middle_way_report_digest",
            "source_verification_evidence_digest",
        ):
            require_string(state.get(field), field)
        for field in (
            "current_cycle_index",
            "active_from_cycle",
            "event_index",
            "replan_version",
            "committed_records",
            "updated_at_ms",
        ):
            require_int(state.get(field), field)
        if state.get("active_from_cycle") != int(state.get("current_cycle_index", -1)) + 1:
            errors.append("replan_active_cycle_invalid")
        nonnegative_number(state.get("plan_budget"), "plan_budget")
        unit_number(state.get("maximum_candidate_risk"), "maximum_candidate_risk")
        unit_number(state.get("base_switch_threshold"), "base_switch_threshold")
        if state.get("current_phase") not in PHASES:
            errors.append("replan_state_phase_invalid")
        if state.get("route") not in ROUTES:
            errors.append("replan_state_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("replan_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("replan_state_boundary_invalid")
        if state.get("replan_state_digest") != replan_state_digest(state):
            errors.append("replan_state_digest_invalid")
        if state.get("active_now") is not False:
            errors.append("replan_present_activation_forbidden")
        if state.get("current_cycle_unchanged") is not True:
            errors.append("replan_current_cycle_mutation_forbidden")
        if state.get("past_plan_unchanged") is not True:
            errors.append("replan_past_plan_mutation_forbidden")
        if state.get("memory_overwrite") is not False:
            errors.append("replan_memory_overwrite_forbidden")
        if state.get("host_license_granted") is not False:
            errors.append("replan_host_license_forbidden")
        candidate_ids = [str(item.get("candidate_id", "")) for item in state.get("candidates", [])]
        if len(candidate_ids) != len(set(candidate_ids)):
            errors.append("replan_candidate_id_duplicate")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("replan_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(state.get("event_index", -1)):
            errors.append("replan_event_history_count_mismatch")
        if state.get("next_plan_basis_committed") is True:
            if state.get("current_phase") != "commit_next":
                errors.append("replan_committed_before_commit_next")
            if state.get("next_plan_phase_required") is not True:
                errors.append("replan_next_plan_phase_debt_missing")
            if not state.get("next_plan_basis_digest"):
                errors.append("replan_next_plan_basis_missing")
    except (TypeError, ValueError, KeyError) as exc:
        errors.append(str(exc))
    return errors


def build_replan_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "replan_id": require_string(state.get("replan_id"), "replan_id"),
        "lineage_id": require_string(state.get("lineage_id"), "lineage_id"),
        "expected_replan_state_digest": require_string(
            state.get("replan_state_digest"), "expected_replan_state_digest"
        ),
        "source_phase": require_string(state.get("current_phase"), "source_phase"),
        "target_phase": require_string(target_phase, "target_phase"),
        "event_index": require_int(state.get("event_index"), "event_index") + 1,
        "artifact_digest": require_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "replan_event_digest": "",
    }
    event["replan_event_digest"] = replan_event_digest(event)
    return event


def build_history_packet(
    *,
    state: Mapping[str, Any],
    previous_plan_change_digests: list[str],
    successful_transition_digests: list[str],
    failed_transition_digests: list[str],
    oscillation_history_digests: list[str],
    recovery_history_digests: list[str],
    stagnation_history_digests: list[str],
    action_history_digest: str,
    observation_history_digest: str,
    verification_history_digest: str,
    learning_history_digest: str,
    history_window: int,
    path_dependence_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "bind":
        raise ValueError("history_requires_bound_state")
    packet = {
        "version": HISTORY_PACKET_VERSION,
        "replan_id": state["replan_id"],
        "source_plan_state_digest": state["source_plan_state_digest"],
        "source_committed_plan_digest": state["source_committed_plan_digest"],
        "source_learning_delta_digest": state["source_learning_delta_digest"],
        "current_plan_digest": state["source_committed_plan_digest"],
        "previous_plan_change_digests": unique_strings(
            previous_plan_change_digests, "previous_plan_change_digests", allow_empty=True
        ),
        "successful_transition_digests": unique_strings(
            successful_transition_digests, "successful_transition_digests", allow_empty=True
        ),
        "failed_transition_digests": unique_strings(
            failed_transition_digests, "failed_transition_digests", allow_empty=True
        ),
        "oscillation_history_digests": unique_strings(
            oscillation_history_digests, "oscillation_history_digests", allow_empty=True
        ),
        "recovery_history_digests": unique_strings(
            recovery_history_digests, "recovery_history_digests", allow_empty=True
        ),
        "stagnation_history_digests": unique_strings(
            stagnation_history_digests, "stagnation_history_digests", allow_empty=True
        ),
        "action_history_digest": require_string(action_history_digest, "action_history_digest"),
        "observation_history_digest": require_string(
            observation_history_digest, "observation_history_digest"
        ),
        "verification_history_digest": require_string(
            verification_history_digest, "verification_history_digest"
        ),
        "learning_history_digest": require_string(
            learning_history_digest, "learning_history_digest"
        ),
        "history_window": require_int(history_window, "history_window"),
        "path_dependence_digest": require_string(
            path_dependence_digest, "path_dependence_digest"
        ),
        "non_markov_history": True,
        "source_history_mutation": False,
        "history_packet_digest": "",
    }
    if packet["history_window"] < 1:
        raise ValueError("history_window_positive_required")
    packet["history_packet_digest"] = history_packet_digest(packet)
    return packet


def build_qi_condition_packet(
    *,
    state: Mapping[str, Any],
    process_tensor_digest: str,
    process_history_digest: str,
    activation: float,
    stagnation: float,
    tension: float,
    recovery: float,
    coherence: float,
    coupling: float,
    transition_readiness: float,
    local_global_balance: float,
    observation_debt: float,
    hysteresis: float,
    memory_horizon: int,
    intervention_history_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "history":
        raise ValueError("qi_condition_requires_history_state")
    packet = {
        "version": QI_CONDITION_PACKET_VERSION,
        "replan_id": state["replan_id"],
        "source_plan_state_digest": state["source_plan_state_digest"],
        "source_learning_delta_digest": state["source_learning_delta_digest"],
        "history_packet_digest": state["history_packet_digest"],
        "process_tensor_digest": require_string(process_tensor_digest, "process_tensor_digest"),
        "process_history_digest": require_string(process_history_digest, "process_history_digest"),
        "activation": unit_number(activation, "activation"),
        "stagnation": unit_number(stagnation, "stagnation"),
        "tension": unit_number(tension, "tension"),
        "recovery": unit_number(recovery, "recovery"),
        "coherence": unit_number(coherence, "coherence"),
        "coupling": unit_number(coupling, "coupling"),
        "transition_readiness": unit_number(
            transition_readiness, "transition_readiness"
        ),
        "local_global_balance": unit_number(
            local_global_balance, "local_global_balance"
        ),
        "observation_debt": unit_number(observation_debt, "observation_debt"),
        "hysteresis": unit_number(hysteresis, "hysteresis"),
        "memory_horizon": require_int(memory_horizon, "memory_horizon"),
        "intervention_history_digest": require_string(
            intervention_history_digest, "intervention_history_digest"
        ),
        "qi_context_only": True,
        "qi_grants_truth_authority": False,
        "qi_grants_causal_authority": False,
        "qi_grants_execution_authority": False,
        "qi_grants_clinical_authority": False,
        "qi_activates_plan": False,
        "qi_condition_packet_digest": "",
    }
    if packet["memory_horizon"] < 1:
        raise ValueError("memory_horizon_positive_required")
    packet["qi_condition_packet_digest"] = qi_condition_packet_digest(packet)
    return packet


def _normalize_candidate(state: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    kind = require_string(raw.get("candidate_type"), "candidate_type")
    if kind not in CANDIDATE_TYPES:
        raise ValueError("replan_candidate_type_invalid")
    allowed = ALLOWED_CANDIDATES_BY_LEARNING_ROUTE.get(state["source_learning_route"], set())
    if kind not in allowed:
        raise ValueError("replan_candidate_incompatible_with_learning_route")
    packet = {
        "version": CANDIDATE_PACKET_VERSION,
        "candidate_id": require_string(raw.get("candidate_id"), "candidate_id"),
        "replan_id": state["replan_id"],
        "source_learning_delta_digest": state["source_learning_delta_digest"],
        "source_plan_basis_digest": state["source_plan_basis_digest"],
        "candidate_type": kind,
        "target_scope": require_string(raw.get("target_scope"), "target_scope"),
        "goal_digest": require_string(raw.get("goal_digest"), "goal_digest"),
        "step_template_digests": unique_strings(
            raw.get("step_template_digests"), "step_template_digests"
        ),
        "expected_observation_digest": require_string(
            raw.get("expected_observation_digest"), "expected_observation_digest"
        ),
        "verification_criterion_digest": require_string(
            raw.get("verification_criterion_digest"),
            "verification_criterion_digest",
        ),
        "estimated_cost": nonnegative_number(raw.get("estimated_cost"), "estimated_cost"),
        "estimated_risk": unit_number(raw.get("estimated_risk"), "estimated_risk"),
        "reversibility": unit_number(raw.get("reversibility"), "reversibility"),
        "transition_distance": unit_number(
            raw.get("transition_distance"), "transition_distance"
        ),
        "switch_benefit": unit_number(raw.get("switch_benefit"), "switch_benefit"),
        "stop_condition_digests": unique_strings(
            raw.get("stop_condition_digests"), "stop_condition_digests"
        ),
        "rollback_point_digest": require_string(
            raw.get("rollback_point_digest"), "rollback_point_digest"
        ),
        "stakeholder_scope_digests": unique_strings(
            raw.get("stakeholder_scope_digests"), "stakeholder_scope_digests"
        ),
        "future_only": True,
        "active_now": False,
        "candidate_digest": "",
    }
    packet["candidate_digest"] = candidate_digest(packet)
    supplied = raw.get("candidate_digest")
    if supplied not in (None, "", packet["candidate_digest"]):
        raise ValueError("candidate_digest_invalid")
    return packet


def build_decision_receipt(
    *,
    state: Mapping[str, Any],
    decision_os_state_digest: str,
    decision_basis_digest: str,
    wa_relational_harmony_digest: str,
    selected_candidate_id: str,
    retained_candidate_ids: list[str],
    dissent_evidence_digests: list[str],
    minority_stakeholder_digests: list[str],
    decided_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "constrain":
        raise ValueError("decision_receipt_requires_constrained_state")
    selected = require_string(selected_candidate_id, "selected_candidate_id")
    admissible = set(state["admissible_candidate_ids"])
    if selected not in admissible:
        raise ValueError("decision_selected_candidate_not_admissible")
    retained = unique_strings(
        retained_candidate_ids, "retained_candidate_ids", allow_empty=True
    )
    all_ids = {item["candidate_id"] for item in state["candidates"]}
    if not set(retained).issubset(all_ids - {selected}):
        raise ValueError("decision_retained_candidate_invalid")
    packet = {
        "version": DECISION_RECEIPT_VERSION,
        "replan_id": state["replan_id"],
        "candidate_field_digest": state["candidate_field_digest"],
        "constraint_field_digest": state["constraint_field_digest"],
        "decision_os_version": "kuuos_decision_os_wa_relational_harmony_v0_3",
        "decision_os_state_digest": require_string(
            decision_os_state_digest, "decision_os_state_digest"
        ),
        "decision_basis_digest": require_string(
            decision_basis_digest, "decision_basis_digest"
        ),
        "wa_relational_harmony_digest": require_string(
            wa_relational_harmony_digest, "wa_relational_harmony_digest"
        ),
        "selected_candidate_id": selected,
        "retained_candidate_ids": retained,
        "dissent_evidence_digests": unique_strings(
            dissent_evidence_digests, "dissent_evidence_digests", allow_empty=True
        ),
        "minority_stakeholder_digests": unique_strings(
            minority_stakeholder_digests,
            "minority_stakeholder_digests",
            allow_empty=True,
        ),
        "all_candidates_considered": True,
        "minority_preserved": True,
        "decision_not_execution": True,
        "silent_substitution_detected": False,
        "decided_at_ms": require_int(decided_at_ms, "decided_at_ms"),
        "non_authority": copy_non_authority(),
        "decision_receipt_digest": "",
    }
    packet["decision_receipt_digest"] = decision_receipt_digest(packet)
    return packet


def build_synthesis_packet(
    *,
    state: Mapping[str, Any],
    next_plan_goal_digest: str,
    next_plan_step_template_digests: list[str],
    next_observation_point_digests: list[str],
    next_verification_criterion_digests: list[str],
    next_stop_condition_digests: list[str],
    next_rollback_point_digests: list[str],
    resource_envelope_digest: str,
    authority_boundary_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "deliberate":
        raise ValueError("synthesis_requires_deliberated_state")
    packet = {
        "version": SYNTHESIS_PACKET_VERSION,
        "replan_id": state["replan_id"],
        "source_plan_state_digest": state["source_plan_state_digest"],
        "source_learning_delta_digest": state["source_learning_delta_digest"],
        "history_packet_digest": state["history_packet_digest"],
        "qi_condition_packet_digest": state["qi_condition_packet_digest"],
        "decision_receipt_digest": state["decision_receipt_digest"],
        "selected_candidate_id": state["selected_candidate_id"],
        "selected_candidate_digest": state["selected_candidate_digest"],
        "next_plan_goal_digest": require_string(
            next_plan_goal_digest, "next_plan_goal_digest"
        ),
        "next_plan_step_template_digests": unique_strings(
            next_plan_step_template_digests, "next_plan_step_template_digests"
        ),
        "next_observation_point_digests": unique_strings(
            next_observation_point_digests, "next_observation_point_digests"
        ),
        "next_verification_criterion_digests": unique_strings(
            next_verification_criterion_digests,
            "next_verification_criterion_digests",
        ),
        "next_stop_condition_digests": unique_strings(
            next_stop_condition_digests, "next_stop_condition_digests"
        ),
        "next_rollback_point_digests": unique_strings(
            next_rollback_point_digests, "next_rollback_point_digests"
        ),
        "resource_envelope_digest": require_string(
            resource_envelope_digest, "resource_envelope_digest"
        ),
        "authority_boundary_digest": require_string(
            authority_boundary_digest, "authority_boundary_digest"
        ),
        "active_from_cycle": state["active_from_cycle"],
        "future_only": True,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "plan_not_execution": True,
        "host_license_granted": False,
        "synthesis_packet_digest": "",
    }
    packet["next_plan_basis_digest"] = sha(
        {key: value for key, value in packet.items() if key != "synthesis_packet_digest"}
    )
    packet["synthesis_packet_digest"] = synthesis_packet_digest(packet)
    return packet


def build_replan_phase_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_state_digest: str,
    replan_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_replan_state(state)
    if errors:
        raise ValueError("invalid_replan_state:" + ";".join(errors))
    if state.get("current_phase") != "commit_next":
        raise ValueError("replan_phase_receipt_requires_commit_next")
    if state.get("next_plan_basis_committed") is not True:
        raise ValueError("next_plan_basis_not_committed")
    packet = {
        "version": REPLAN_PHASE_RECEIPT_VERSION,
        "replan_id": state["replan_id"],
        "replan_state_digest": state["replan_state_digest"],
        "source_plan_state_digest": state["source_plan_state_digest"],
        "source_learn_state_digest": state["source_learn_state_digest"],
        "source_learning_delta_digest": state["source_learning_delta_digest"],
        "qi_condition_packet_digest": state["qi_condition_packet_digest"],
        "decision_receipt_digest": state["decision_receipt_digest"],
        "synthesis_packet_digest": state["synthesis_packet_digest"],
        "next_plan_basis_digest": state["next_plan_basis_digest"],
        "route": state["route"],
        "mission_cycle_phase": "replan",
        "current_cycle_index": state["current_cycle_index"],
        "active_from_cycle": state["active_from_cycle"],
        "future_only": True,
        "active_now": False,
        "next_plan_phase_required": True,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "plan_not_execution": True,
        "host_license_granted": False,
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "replan_phase_event_digest": require_string(
            replan_phase_event_digest, "replan_phase_event_digest"
        ),
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "replan_phase_receipt_digest": "",
    }
    packet["replan_phase_receipt_digest"] = replan_phase_receipt_digest(packet)
    return packet


def _validate_event_base(state: Mapping[str, Any], event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("replan_event_version_invalid")
    if event.get("replan_id") != state.get("replan_id"):
        errors.append("replan_event_id_mismatch")
    if event.get("lineage_id") != state.get("lineage_id"):
        errors.append("replan_event_lineage_mismatch")
    if event.get("replan_event_digest") != replan_event_digest(event):
        errors.append("replan_event_digest_invalid")
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("replan_event_authority_escalation")
    source = str(event.get("source_phase", ""))
    if source != state.get("current_phase"):
        errors.append("replan_event_source_phase_stale")
    if event.get("target_phase") != next_phase(source):
        errors.append("replan_event_phase_order_invalid")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("replan_event_index_invalid")
    if event.get("expected_replan_state_digest") != state.get("replan_state_digest"):
        errors.append("replan_event_state_digest_stale")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("replan_event_time_regression")
    return errors


def _apply_payload(state: dict[str, Any], phase: str, payload: Mapping[str, Any]) -> None:
    if phase == "history":
        packet = payload.get("history_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("history_packet_required")
        if packet.get("version") != HISTORY_PACKET_VERSION:
            raise ValueError("history_packet_version_invalid")
        if packet.get("history_packet_digest") != history_packet_digest(packet):
            raise ValueError("history_packet_digest_invalid")
        for field, expected in {
            "replan_id": state["replan_id"],
            "source_plan_state_digest": state["source_plan_state_digest"],
            "source_committed_plan_digest": state["source_committed_plan_digest"],
            "source_learning_delta_digest": state["source_learning_delta_digest"],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"history_packet_{field}_mismatch")
        if packet.get("non_markov_history") is not True:
            raise ValueError("non_markov_history_required")
        if packet.get("source_history_mutation") is not False:
            raise ValueError("source_history_mutation_forbidden")
        state["history_packet"] = deepcopy(dict(packet))
        state["history_packet_digest"] = packet["history_packet_digest"]
        return

    if phase == "qi_condition":
        packet = payload.get("qi_condition_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("qi_condition_packet_required")
        if packet.get("version") != QI_CONDITION_PACKET_VERSION:
            raise ValueError("qi_condition_packet_version_invalid")
        if packet.get("qi_condition_packet_digest") != qi_condition_packet_digest(packet):
            raise ValueError("qi_condition_packet_digest_invalid")
        for field, expected in {
            "replan_id": state["replan_id"],
            "source_plan_state_digest": state["source_plan_state_digest"],
            "source_learning_delta_digest": state["source_learning_delta_digest"],
            "history_packet_digest": state["history_packet_digest"],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"qi_condition_packet_{field}_mismatch")
        for field, expected in {
            "qi_context_only": True,
            "qi_grants_truth_authority": False,
            "qi_grants_causal_authority": False,
            "qi_grants_execution_authority": False,
            "qi_grants_clinical_authority": False,
            "qi_activates_plan": False,
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"qi_condition_{field}_invalid")
        state["qi_condition_packet"] = deepcopy(dict(packet))
        state["qi_condition_packet_digest"] = packet["qi_condition_packet_digest"]
        return

    if phase == "generate":
        raw_candidates = payload.get("candidates")
        if not isinstance(raw_candidates, list) or not raw_candidates:
            raise ValueError("replan_candidates_nonempty_list_required")
        candidates = [
            _normalize_candidate(state, item)
            for item in raw_candidates
            if isinstance(item, Mapping)
        ]
        if len(candidates) != len(raw_candidates):
            raise ValueError("replan_candidate_object_required")
        ids = [item["candidate_id"] for item in candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("replan_candidate_id_duplicate")
        state["candidates"] = candidates
        state["candidate_field_digest"] = sha(candidates)
        return

    if phase == "constrain":
        checks = payload.get("candidate_checks")
        if not isinstance(checks, Mapping):
            raise ValueError("candidate_checks_mapping_required")
        require_string(
            payload.get("mission_invariant_receipt_digest"),
            "mission_invariant_receipt_digest",
        )
        require_string(
            payload.get("authority_boundary_receipt_digest"),
            "authority_boundary_receipt_digest",
        )
        require_string(
            payload.get("resource_envelope_digest"), "resource_envelope_digest"
        )
        require_string(
            payload.get("scope_compatibility_digest"), "scope_compatibility_digest"
        )
        reports: list[dict[str, Any]] = []
        qi = state["qi_condition_packet"]
        oscillation_count = len(state["history_packet"]["oscillation_history_digests"])
        oscillation_penalty = min(0.25, 0.05 * oscillation_count)
        for candidate in state["candidates"]:
            candidate_id = candidate["candidate_id"]
            raw = checks.get(candidate_id)
            if not isinstance(raw, Mapping):
                raise ValueError(f"candidate_check_missing:{candidate_id}")
            recovery_penalty = (
                0.10
                if float(qi["recovery"]) >= 0.70
                and candidate["candidate_type"] not in SWITCH_EXEMPT_TYPES
                else 0.0
            )
            required_margin = min(
                1.0,
                float(state["base_switch_threshold"])
                + float(qi["hysteresis"])
                + oscillation_penalty
                + recovery_penalty,
            )
            switch_exempt = candidate["candidate_type"] in SWITCH_EXEMPT_TYPES
            hysteresis_passed = switch_exempt or float(candidate["switch_benefit"]) >= required_margin
            mission_ok = require_bool(raw.get("mission_invariants_preserved"), "mission_invariants_preserved")
            authority_ok = require_bool(raw.get("authority_boundary_preserved"), "authority_boundary_preserved")
            applicability_ok = require_bool(raw.get("applicability_condition_valid"), "applicability_condition_valid")
            reversal_ok = require_bool(raw.get("reversal_condition_visible"), "reversal_condition_visible")
            expiration_ok = require_bool(raw.get("expiration_condition_valid"), "expiration_condition_valid")
            scope_ok = require_bool(raw.get("scope_compatible"), "scope_compatible")
            verification_debt_visible = require_bool(raw.get("verification_debt_visible"), "verification_debt_visible")
            within_budget = float(candidate["estimated_cost"]) <= float(state["plan_budget"]) + 1e-12
            within_risk = float(candidate["estimated_risk"]) <= float(state["maximum_candidate_risk"]) + 1e-12
            qi_ready = bool(
                candidate["candidate_type"] in {"hold", "reobserve", "slow_down"}
                or float(qi["transition_readiness"]) >= float(candidate["transition_distance"])
            )
            admissible = all(
                (
                    mission_ok,
                    authority_ok,
                    applicability_ok,
                    reversal_ok,
                    expiration_ok,
                    scope_ok,
                    verification_debt_visible,
                    within_budget,
                    within_risk,
                    qi_ready,
                    hysteresis_passed,
                )
            )
            report = {
                "version": CONSTRAINT_REPORT_VERSION,
                "replan_id": state["replan_id"],
                "candidate_id": candidate_id,
                "candidate_digest": candidate["candidate_digest"],
                "mission_invariants_preserved": mission_ok,
                "authority_boundary_preserved": authority_ok,
                "applicability_condition_valid": applicability_ok,
                "reversal_condition_visible": reversal_ok,
                "expiration_condition_valid": expiration_ok,
                "scope_compatible": scope_ok,
                "observation_debt_visible": True,
                "verification_debt_visible": verification_debt_visible,
                "within_budget": within_budget,
                "within_risk": within_risk,
                "qi_transition_ready": qi_ready,
                "switch_exempt": switch_exempt,
                "base_switch_threshold": state["base_switch_threshold"],
                "qi_hysteresis": qi["hysteresis"],
                "oscillation_penalty": oscillation_penalty,
                "recovery_protection_penalty": recovery_penalty,
                "required_switch_margin": required_margin,
                "switch_benefit": candidate["switch_benefit"],
                "hysteresis_passed": hysteresis_passed,
                "admissible": admissible,
                "constraint_report_digest": "",
            }
            report["constraint_report_digest"] = constraint_report_digest(report)
            reports.append(report)
        admissible_ids = [item["candidate_id"] for item in reports if item["admissible"]]
        if not admissible_ids:
            raise ValueError("no_admissible_replan_candidate")
        state["constraint_reports"] = reports
        state["constraint_field_digest"] = sha(reports)
        state["admissible_candidate_ids"] = admissible_ids
        return

    if phase == "deliberate":
        receipt = payload.get("decision_receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("decision_receipt_required")
        if receipt.get("version") != DECISION_RECEIPT_VERSION:
            raise ValueError("decision_receipt_version_invalid")
        if receipt.get("decision_receipt_digest") != decision_receipt_digest(receipt):
            raise ValueError("decision_receipt_digest_invalid")
        for field, expected in {
            "replan_id": state["replan_id"],
            "candidate_field_digest": state["candidate_field_digest"],
            "constraint_field_digest": state["constraint_field_digest"],
        }.items():
            if receipt.get(field) != expected:
                raise ValueError(f"decision_receipt_{field}_mismatch")
        selected = str(receipt.get("selected_candidate_id", ""))
        if selected not in set(state["admissible_candidate_ids"]):
            raise ValueError("decision_selected_candidate_not_admissible")
        if receipt.get("all_candidates_considered") is not True:
            raise ValueError("decision_all_candidates_considered_required")
        if receipt.get("minority_preserved") is not True:
            raise ValueError("decision_minority_preservation_required")
        if receipt.get("decision_not_execution") is not True:
            raise ValueError("decision_execution_boundary_required")
        if receipt.get("silent_substitution_detected") is not False:
            raise ValueError("decision_silent_substitution_forbidden")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("decision_receipt_authority_escalation")
        candidate = next(item for item in state["candidates"] if item["candidate_id"] == selected)
        state["decision_receipt"] = deepcopy(dict(receipt))
        state["decision_receipt_digest"] = receipt["decision_receipt_digest"]
        state["selected_candidate_id"] = selected
        state["selected_candidate_digest"] = candidate["candidate_digest"]
        state["route"] = ROUTE_BY_CANDIDATE_TYPE[candidate["candidate_type"]]
        return

    if phase == "synthesize":
        packet = payload.get("synthesis_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("synthesis_packet_required")
        if packet.get("version") != SYNTHESIS_PACKET_VERSION:
            raise ValueError("synthesis_packet_version_invalid")
        if packet.get("synthesis_packet_digest") != synthesis_packet_digest(packet):
            raise ValueError("synthesis_packet_digest_invalid")
        for field, expected in {
            "replan_id": state["replan_id"],
            "source_plan_state_digest": state["source_plan_state_digest"],
            "source_learning_delta_digest": state["source_learning_delta_digest"],
            "history_packet_digest": state["history_packet_digest"],
            "qi_condition_packet_digest": state["qi_condition_packet_digest"],
            "decision_receipt_digest": state["decision_receipt_digest"],
            "selected_candidate_id": state["selected_candidate_id"],
            "selected_candidate_digest": state["selected_candidate_digest"],
            "active_from_cycle": state["active_from_cycle"],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"synthesis_packet_{field}_mismatch")
        for field, expected in {
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_plan_unchanged": True,
            "plan_not_execution": True,
            "host_license_granted": False,
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"synthesis_{field}_invalid")
        expected_basis = sha(
            {
                key: value
                for key, value in packet.items()
                if key not in {"synthesis_packet_digest", "next_plan_basis_digest"}
            }
        )
        if packet.get("next_plan_basis_digest") != expected_basis:
            raise ValueError("next_plan_basis_digest_invalid")
        state["synthesis_packet"] = deepcopy(dict(packet))
        state["synthesis_packet_digest"] = packet["synthesis_packet_digest"]
        state["next_plan_basis_digest"] = packet["next_plan_basis_digest"]
        return

    if phase == "commit_next":
        required = {
            "next_plan_basis_committed": True,
            "next_plan_phase_required": True,
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_plan_unchanged": True,
            "memory_overwrite": False,
            "plan_not_execution": True,
            "decision_not_execution": True,
            "qi_context_only": True,
            "host_license_granted": False,
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"replan_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("replan_commit_authority_escalation")
        if not state["next_plan_basis_digest"] or not state["decision_receipt_digest"]:
            raise ValueError("replan_synthesis_not_complete")
        state["next_plan_basis_committed"] = True
        state["next_plan_phase_required"] = True
        return

    raise ValueError("replan_target_phase_unsupported")


def _result(
    *, status: str, state: Mapping[str, Any], event_id: str, predecessor: str, errors: list[str]
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "replan_event_digest": event_id,
        "predecessor_replan_state_digest": predecessor,
        "result_replan_state_digest": state["replan_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "replan_apply_result_digest": "",
    }
    packet["replan_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_replan_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_replan_state(state)
    if state_errors:
        raise ValueError("invalid_replan_state:" + ";".join(state_errors))
    event_id = str(event.get("replan_event_digest", ""))
    predecessor = str(state["replan_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED", state=state, event_id=event_id,
            predecessor=predecessor, errors=[]
        )
    errors = _validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED", state=state, event_id=event_id,
            predecessor=predecessor, errors=errors
        )
    next_state = deepcopy(dict(state))
    phase = str(event["target_phase"])
    try:
        _apply_payload(next_state, phase, dict(event.get("payload", {})))
    except (TypeError, ValueError, KeyError) as exc:
        return _result(
            status="REJECTED", state=state, event_id=event_id,
            predecessor=predecessor, errors=[str(exc)]
        )
    next_state["predecessor_replan_state_digest"] = predecessor
    next_state["current_phase"] = phase
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(next_state["processed_event_digests"]) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": phase,
            "artifact_digest": event["artifact_digest"],
            "replan_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if phase == "commit_next":
        next_state["replan_version"] += 1
        next_state["committed_records"] += 1
        next_state["record_summaries"] = list(next_state["record_summaries"]) + [
            {
                "replan_version": next_state["replan_version"],
                "route": next_state["route"],
                "selected_candidate_id": next_state["selected_candidate_id"],
                "selected_candidate_digest": next_state["selected_candidate_digest"],
                "next_plan_basis_digest": next_state["next_plan_basis_digest"],
                "active_from_cycle": next_state["active_from_cycle"],
                "active_now": False,
                "next_plan_phase_required": True,
            }
        ]
    next_state["replan_state_digest"] = ""
    next_state["replan_state_digest"] = replan_state_digest(next_state)
    next_errors = validate_replan_state(next_state)
    if next_errors:
        raise ValueError("next_replan_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED", state=next_state, event_id=event_id,
        predecessor=predecessor, errors=[]
    )
