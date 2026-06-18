from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.kuuos_verify_os_types_v0_1 import (
    ADJUDICATION_RECEIPT_VERSION,
    CHALLENGE_PACKET_VERSION as VERIFY_CHALLENGE_PACKET_VERSION,
    CORROBORATION_REPORT_VERSION,
    CRITERION_PACKET_VERSION,
    adjudication_receipt_digest,
    challenge_packet_digest as verify_challenge_packet_digest,
    corroboration_report_digest,
    criterion_packet_digest,
)
from runtime.kuuos_learn_os_types_v0_1 import (
    ABSTRACTION_PACKET_VERSION,
    APPLY_RESULT_VERSION,
    CHALLENGE_PACKET_VERSION,
    EVENT_VERSION,
    LEARNING_DELTA_VERSION,
    LEARNING_KINDS,
    LEARN_PHASE_RECEIPT_VERSION,
    MIDDLE_WAY_REPORT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    STATE_VERSION,
    TARGET_SCOPES,
    abstraction_packet_digest,
    apply_result_digest,
    challenge_packet_digest,
    copy_boundary,
    copy_non_authority,
    event_digest,
    learn_phase_receipt_digest,
    learning_delta_digest,
    middle_way_report_digest,
    next_phase,
    require_bool,
    require_int,
    require_string,
    state_digest,
    unit_number,
    unique_strings,
)

ROUTE_BY_KIND = {
    "reinforcement": "LEARNING_REINFORCEMENT_CANDIDATE",
    "repair": "LEARNING_REPAIR_CANDIDATE",
    "reobservation": "LEARNING_REOBSERVATION_CANDIDATE",
    "hold": "LEARNING_HOLD",
}
ALLOWED_KIND_BY_VERIFY_ROUTE = {
    "VERIFICATION_PASSED": {"reinforcement", "hold"},
    "VERIFICATION_FAILED": {"repair", "hold"},
    "VERIFICATION_INDETERMINATE": {"reobservation", "hold"},
}


def _seal(packet: dict[str, Any], field: str, supplied: Any = None) -> dict[str, Any]:
    packet[field] = ""
    expected = sha({key: value for key, value in packet.items() if key != field})
    packet[field] = expected
    if supplied not in (None, "", expected):
        raise ValueError(f"{field}_invalid")
    return packet


def _validate_verify_nested_receipts(verify_state: Mapping[str, Any]) -> None:
    criterion = verify_state.get("criterion_packet")
    challenge = verify_state.get("challenge_packet")
    corroboration = verify_state.get("corroboration_report")
    adjudication = verify_state.get("adjudication_receipt")
    if not isinstance(criterion, Mapping) or criterion.get("version") != CRITERION_PACKET_VERSION:
        raise ValueError("source_criterion_packet_invalid")
    if criterion.get("criterion_packet_digest") != criterion_packet_digest(criterion):
        raise ValueError("source_criterion_packet_digest_invalid")
    if not isinstance(challenge, Mapping) or challenge.get("version") != VERIFY_CHALLENGE_PACKET_VERSION:
        raise ValueError("source_challenge_packet_invalid")
    if challenge.get("challenge_packet_digest") != verify_challenge_packet_digest(challenge):
        raise ValueError("source_challenge_packet_digest_invalid")
    if not isinstance(corroboration, Mapping) or corroboration.get("version") != CORROBORATION_REPORT_VERSION:
        raise ValueError("source_corroboration_report_invalid")
    if corroboration.get("corroboration_report_digest") != corroboration_report_digest(corroboration):
        raise ValueError("source_corroboration_report_digest_invalid")
    if not isinstance(adjudication, Mapping) or adjudication.get("version") != ADJUDICATION_RECEIPT_VERSION:
        raise ValueError("source_adjudication_receipt_invalid")
    if adjudication.get("adjudication_receipt_digest") != adjudication_receipt_digest(adjudication):
        raise ValueError("source_adjudication_receipt_digest_invalid")


def build_initial_learn_state(
    *, learn_id: str, verify_state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    errors = validate_verify_state(verify_state)
    if errors:
        raise ValueError("invalid_source_verify_state:" + ";".join(errors))
    if verify_state.get("current_phase") != "commit":
        raise ValueError("source_verify_not_committed")
    if verify_state.get("route") == "PENDING":
        raise ValueError("source_verify_route_pending")
    if verify_state.get("verification_recorded") is not True:
        raise ValueError("source_verification_not_recorded")
    if verify_state.get("learning_required") is not True:
        raise ValueError("source_learning_debt_missing")
    _validate_verify_nested_receipts(verify_state)

    source_counterevidence = unique_strings(
        list(verify_state["challenge_packet"].get("counterevidence_digests", [])),
        "source_counterevidence_digests",
        allow_empty=True,
    )
    state = {
        "version": STATE_VERSION,
        "learn_id": require_string(learn_id, "learn_id"),
        "lineage_id": require_string(verify_state.get("lineage_id"), "lineage_id"),
        "source_verify_id": require_string(verify_state.get("verify_id"), "source_verify_id"),
        "source_verify_state_digest": require_string(
            verify_state.get("verify_state_digest"), "source_verify_state_digest"
        ),
        "source_verify_version": require_int(
            verify_state.get("verify_version"), "source_verify_version"
        ),
        "source_verify_updated_at_ms": require_int(
            verify_state.get("updated_at_ms"), "source_verify_updated_at_ms"
        ),
        "source_verification_route": require_string(
            verify_state.get("route"), "source_verification_route"
        ),
        "source_verification_evidence_digest": require_string(
            verify_state.get("verification_evidence_digest"),
            "source_verification_evidence_digest",
        ),
        "source_observe_state_digest": require_string(
            verify_state.get("source_observe_state_digest"), "source_observe_state_digest"
        ),
        "source_act_state_digest": require_string(
            verify_state.get("source_act_state_digest"), "source_act_state_digest"
        ),
        "verification_criterion_digest": require_string(
            verify_state.get("verification_criterion_digest"),
            "verification_criterion_digest",
        ),
        "criterion_packet_digest": require_string(
            verify_state.get("criterion_packet_digest"), "criterion_packet_digest"
        ),
        "source_challenge_packet_digest": require_string(
            verify_state.get("challenge_packet_digest"), "source_challenge_packet_digest"
        ),
        "corroboration_report_digest": require_string(
            verify_state.get("corroboration_report_digest"),
            "corroboration_report_digest",
        ),
        "adjudication_receipt_digest": require_string(
            verify_state.get("adjudication_receipt_digest"),
            "adjudication_receipt_digest",
        ),
        "mission_contract_digest": require_string(
            verify_state.get("mission_contract_digest"), "mission_contract_digest"
        ),
        "source_counterevidence_digests": source_counterevidence,
        "source_counterevidence_digest": sha(source_counterevidence),
        "source_unresolved_conflict": bool(
            verify_state["corroboration_report"].get("unresolved_conflict", False)
        ),
        "source_reobservation_required": require_bool(
            verify_state.get("reobservation_required"), "source_reobservation_required"
        ),
        "source_corrective_action_required": require_bool(
            verify_state.get("corrective_action_required"),
            "source_corrective_action_required",
        ),
        "current_phase": "bind",
        "route": "PENDING",
        "event_index": 0,
        "learn_version": 0,
        "committed_records": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "predecessor_learn_state_digest": "",
        "learn_state_digest": "",
        "abstraction_packet": {},
        "abstraction_packet_digest": "",
        "learning_challenge_packet": {},
        "learning_challenge_packet_digest": "",
        "learning_delta": {},
        "learning_delta_digest": "",
        "middle_way_report": {},
        "middle_way_report_digest": "",
        "learning_recorded": False,
        "learning_debt_discharged": False,
        "replan_required": False,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_records_unchanged": True,
        "corrective_action_required": False,
        "reobservation_required": bool(verify_state.get("reobservation_required", False)),
        "automatic_truth_promotion": False,
        "automatic_belief_update": False,
        "automatic_plan_update": False,
        "automatic_criterion_update": False,
        "automatic_policy_activation": False,
        "automatic_rollback": False,
        "automatic_self_modification": False,
        "processed_event_digests": [],
        "event_history": [],
        "record_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["learn_state_digest"] = state_digest(state)
    return state


def validate_learn_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("learn_state_version_invalid")
        for field in (
            "learn_id",
            "lineage_id",
            "source_verify_id",
            "source_verify_state_digest",
            "source_verification_route",
            "source_verification_evidence_digest",
            "source_observe_state_digest",
            "source_act_state_digest",
            "verification_criterion_digest",
            "criterion_packet_digest",
            "source_challenge_packet_digest",
            "corroboration_report_digest",
            "adjudication_receipt_digest",
            "mission_contract_digest",
            "source_counterevidence_digest",
        ):
            require_string(state.get(field), field)
        for field in (
            "source_verify_version",
            "source_verify_updated_at_ms",
            "event_index",
            "learn_version",
            "committed_records",
            "updated_at_ms",
        ):
            require_int(state.get(field), field)
        for field in (
            "source_unresolved_conflict",
            "source_reobservation_required",
            "source_corrective_action_required",
            "learning_recorded",
            "learning_debt_discharged",
            "replan_required",
            "active_now",
            "current_cycle_unchanged",
            "past_records_unchanged",
            "corrective_action_required",
            "reobservation_required",
        ):
            require_bool(state.get(field), field)
        unique_strings(
            state.get("source_counterevidence_digests"),
            "source_counterevidence_digests",
            allow_empty=True,
        )
        if state.get("source_counterevidence_digest") != sha(
            state.get("source_counterevidence_digests", [])
        ):
            errors.append("source_counterevidence_digest_invalid")
        if state.get("current_phase") not in PHASES:
            errors.append("learn_state_phase_invalid")
        if state.get("route") not in ROUTES:
            errors.append("learn_state_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("learn_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("learn_state_boundary_invalid")
        if state.get("learn_state_digest") != state_digest(state):
            errors.append("learn_state_digest_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("learn_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(state.get("event_index", -1)):
            errors.append("learn_event_history_count_mismatch")
        for field in (
            "automatic_truth_promotion",
            "automatic_belief_update",
            "automatic_plan_update",
            "automatic_criterion_update",
            "automatic_policy_activation",
            "automatic_rollback",
            "automatic_self_modification",
        ):
            if state.get(field) is not False:
                errors.append(f"learn_{field}_forbidden")
        if state.get("active_now") is not False:
            errors.append("learn_present_activation_forbidden")
        if state.get("current_cycle_unchanged") is not True:
            errors.append("learn_current_cycle_mutation_forbidden")
        if state.get("past_records_unchanged") is not True:
            errors.append("learn_past_record_mutation_forbidden")
        if state.get("learning_recorded") is True:
            if state.get("route") == "PENDING":
                errors.append("learn_recorded_route_pending")
            if state.get("learning_debt_discharged") is not True:
                errors.append("learn_debt_not_discharged")
            if state.get("replan_required") is not True:
                errors.append("learn_replan_debt_missing")
            route = state.get("route")
            if route == "LEARNING_REPAIR_CANDIDATE":
                if state.get("corrective_action_required") is not True:
                    errors.append("learn_repair_corrective_debt_missing")
                if state.get("reobservation_required") is not False:
                    errors.append("learn_repair_reobservation_invalid")
            elif route == "LEARNING_REOBSERVATION_CANDIDATE":
                if state.get("corrective_action_required") is not False:
                    errors.append("learn_reobserve_corrective_invalid")
                if state.get("reobservation_required") is not True:
                    errors.append("learn_reobservation_debt_missing")
            elif route == "LEARNING_REINFORCEMENT_CANDIDATE":
                if state.get("corrective_action_required") is not False:
                    errors.append("learn_reinforcement_corrective_invalid")
                if state.get("reobservation_required") is not False:
                    errors.append("learn_reinforcement_reobservation_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_learn_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "learn_id": require_string(state.get("learn_id"), "learn_id"),
        "lineage_id": require_string(state.get("lineage_id"), "lineage_id"),
        "expected_learn_state_digest": require_string(
            state.get("learn_state_digest"), "expected_learn_state_digest"
        ),
        "source_phase": require_string(state.get("current_phase"), "source_phase"),
        "target_phase": require_string(target_phase, "target_phase"),
        "event_index": require_int(state.get("event_index"), "event_index") + 1,
        "artifact_digest": require_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "learn_event_digest": "",
    }
    event["learn_event_digest"] = event_digest(event)
    return event


def build_abstraction_packet(
    *,
    state: Mapping[str, Any],
    supported_pattern_digests: list[str],
    failed_pattern_digests: list[str],
    unresolved_pattern_digests: list[str],
    counterevidence_digests: list[str],
    uncertainty_digest: str,
    residual_digest: str,
    scope_digest: str,
    qi_process_history_digest: str,
    abstraction_method_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "bind":
        raise ValueError("abstraction_requires_bound_state")
    counterevidence = unique_strings(
        counterevidence_digests, "counterevidence_digests", allow_empty=True
    )
    if counterevidence != list(state["source_counterevidence_digests"]):
        raise ValueError("abstraction_counterevidence_binding_mismatch")
    unresolved = unique_strings(
        unresolved_pattern_digests, "unresolved_pattern_digests", allow_empty=True
    )
    if state["source_unresolved_conflict"] and not unresolved:
        raise ValueError("unresolved_pattern_required")
    packet = {
        "version": ABSTRACTION_PACKET_VERSION,
        "learn_id": state["learn_id"],
        "source_verify_state_digest": state["source_verify_state_digest"],
        "source_verification_evidence_digest": state[
            "source_verification_evidence_digest"
        ],
        "supported_pattern_digests": unique_strings(
            supported_pattern_digests, "supported_pattern_digests", allow_empty=True
        ),
        "failed_pattern_digests": unique_strings(
            failed_pattern_digests, "failed_pattern_digests", allow_empty=True
        ),
        "unresolved_pattern_digests": unresolved,
        "counterevidence_digests": counterevidence,
        "uncertainty_digest": require_string(uncertainty_digest, "uncertainty_digest"),
        "residual_digest": require_string(residual_digest, "residual_digest"),
        "scope_digest": require_string(scope_digest, "scope_digest"),
        "qi_process_history_digest": require_string(
            qi_process_history_digest, "qi_process_history_digest"
        ),
        "abstraction_method_digest": require_string(
            abstraction_method_digest, "abstraction_method_digest"
        ),
        "summary_replaces_source_evidence": False,
        "counterevidence_preserved": True,
        "qi_context_only": True,
        "abstraction_packet_digest": "",
    }
    packet["abstraction_packet_digest"] = abstraction_packet_digest(packet)
    return packet


def build_learning_challenge_packet(
    *,
    state: Mapping[str, Any],
    alternative_explanation_digests: list[str],
    anti_overgeneralization_test_digests: list[str],
    distribution_shift_risk_digest: str,
    observer_bias_risk_digest: str,
    negative_transfer_risk_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "abstract":
        raise ValueError("challenge_requires_abstract_state")
    packet = {
        "version": CHALLENGE_PACKET_VERSION,
        "learn_id": state["learn_id"],
        "source_verify_state_digest": state["source_verify_state_digest"],
        "abstraction_packet_digest": state["abstraction_packet_digest"],
        "source_counterevidence_digest": state["source_counterevidence_digest"],
        "alternative_explanation_digests": unique_strings(
            alternative_explanation_digests,
            "alternative_explanation_digests",
            allow_empty=True,
        ),
        "anti_overgeneralization_test_digests": unique_strings(
            anti_overgeneralization_test_digests,
            "anti_overgeneralization_test_digests",
        ),
        "distribution_shift_risk_digest": require_string(
            distribution_shift_risk_digest, "distribution_shift_risk_digest"
        ),
        "observer_bias_risk_digest": require_string(
            observer_bias_risk_digest, "observer_bias_risk_digest"
        ),
        "negative_transfer_risk_digest": require_string(
            negative_transfer_risk_digest, "negative_transfer_risk_digest"
        ),
        "counterevidence_preserved": True,
        "challenge_complete": True,
        "challenge_packet_digest": "",
    }
    packet["challenge_packet_digest"] = challenge_packet_digest(packet)
    return packet


def build_learning_delta(
    *,
    state: Mapping[str, Any],
    learning_delta_id: str,
    learning_kind: str,
    target_scope: str,
    before_digest: str,
    after_candidate_digest: str,
    change_rationale_digest: str,
    applicability_condition_digest: str,
    reversal_condition_digest: str,
    expiration_condition_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "challenge":
        raise ValueError("delta_requires_challenged_state")
    kind = require_string(learning_kind, "learning_kind")
    if kind not in LEARNING_KINDS:
        raise ValueError("learning_kind_invalid")
    allowed = ALLOWED_KIND_BY_VERIFY_ROUTE.get(state["source_verification_route"], set())
    if kind not in allowed:
        raise ValueError("learning_kind_incompatible_with_verification_route")
    scope = require_string(target_scope, "target_scope")
    if scope not in TARGET_SCOPES:
        raise ValueError("target_scope_invalid")
    if kind == "hold" and scope != "no_change":
        raise ValueError("hold_requires_no_change_scope")
    if kind != "hold" and scope == "no_change":
        raise ValueError("candidate_requires_change_scope")
    before = require_string(before_digest, "before_digest")
    after = require_string(after_candidate_digest, "after_candidate_digest")
    if kind == "hold" and before != after:
        raise ValueError("hold_candidate_must_not_change_digest")
    packet = {
        "version": LEARNING_DELTA_VERSION,
        "learning_delta_id": require_string(learning_delta_id, "learning_delta_id"),
        "learn_id": state["learn_id"],
        "source_verify_state_digest": state["source_verify_state_digest"],
        "source_verification_evidence_digest": state[
            "source_verification_evidence_digest"
        ],
        "abstraction_packet_digest": state["abstraction_packet_digest"],
        "learning_challenge_packet_digest": state[
            "learning_challenge_packet_digest"
        ],
        "source_scope_digest": state["abstraction_packet"]["scope_digest"],
        "source_uncertainty_digest": state["abstraction_packet"]["uncertainty_digest"],
        "source_counterevidence_digest": state["source_counterevidence_digest"],
        "qi_process_history_digest": state["abstraction_packet"][
            "qi_process_history_digest"
        ],
        "learning_kind": kind,
        "target_scope": scope,
        "before_digest": before,
        "after_candidate_digest": after,
        "change_rationale_digest": require_string(
            change_rationale_digest, "change_rationale_digest"
        ),
        "applicability_condition_digest": require_string(
            applicability_condition_digest, "applicability_condition_digest"
        ),
        "reversal_condition_digest": require_string(
            reversal_condition_digest, "reversal_condition_digest"
        ),
        "expiration_condition_digest": require_string(
            expiration_condition_digest, "expiration_condition_digest"
        ),
        "future_only": True,
        "memory_overwrite": False,
        "active_now": False,
        "activation_requires_replan": True,
        "scope_widening": False,
        "invariant_removal": False,
        "current_cycle_mutation": False,
        "past_record_mutation": False,
        "learning_delta_digest": "",
    }
    packet["learning_delta_digest"] = learning_delta_digest(packet)
    return packet


def build_middle_way_report(
    *,
    state: Mapping[str, Any],
    reification_risk: float,
    nihilistic_erasure_risk: float,
    overgeneralization_risk: float,
    negative_transfer_risk: float,
    premature_activation_risk: float,
    scope_drift_risk: float,
    gate_method_digest: str,
) -> dict[str, Any]:
    if state.get("current_phase") != "delta":
        raise ValueError("middle_way_gate_requires_delta_state")
    packet = {
        "version": MIDDLE_WAY_REPORT_VERSION,
        "learn_id": state["learn_id"],
        "source_verify_state_digest": state["source_verify_state_digest"],
        "learning_delta_digest": state["learning_delta_digest"],
        "reification_risk": unit_number(reification_risk, "reification_risk"),
        "nihilistic_erasure_risk": unit_number(
            nihilistic_erasure_risk, "nihilistic_erasure_risk"
        ),
        "overgeneralization_risk": unit_number(
            overgeneralization_risk, "overgeneralization_risk"
        ),
        "negative_transfer_risk": unit_number(
            negative_transfer_risk, "negative_transfer_risk"
        ),
        "premature_activation_risk": unit_number(
            premature_activation_risk, "premature_activation_risk"
        ),
        "scope_drift_risk": unit_number(scope_drift_risk, "scope_drift_risk"),
        "counterevidence_preserved": True,
        "samvrti_candidate_usable_for_replan": True,
        "paramartha_non_reification_preserved": True,
        "qi_grants_authority": False,
        "gate_method_digest": require_string(gate_method_digest, "gate_method_digest"),
        "middle_way_report_digest": "",
    }
    packet["candidate_admissible"] = bool(
        max(
            packet["reification_risk"],
            packet["nihilistic_erasure_risk"],
            packet["overgeneralization_risk"],
            packet["negative_transfer_risk"],
            packet["premature_activation_risk"],
            packet["scope_drift_risk"],
        )
        <= 0.65
    )
    packet["middle_way_report_digest"] = middle_way_report_digest(packet)
    return packet


def build_learn_phase_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_state_digest: str,
    learn_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_learn_state(state)
    if errors:
        raise ValueError("invalid_learn_state:" + ";".join(errors))
    if state.get("current_phase") != "commit" or state.get("route") == "PENDING":
        raise ValueError("learn_phase_receipt_requires_committed_learning")
    packet = {
        "version": LEARN_PHASE_RECEIPT_VERSION,
        "learn_id": state["learn_id"],
        "learn_state_digest": state["learn_state_digest"],
        "source_verify_state_digest": state["source_verify_state_digest"],
        "source_verification_evidence_digest": state[
            "source_verification_evidence_digest"
        ],
        "learning_delta_digest": state["learning_delta_digest"],
        "middle_way_report_digest": state["middle_way_report_digest"],
        "learning_route": state["route"],
        "mission_cycle_phase": "learn",
        "future_only": True,
        "memory_overwrite": False,
        "active_now": False,
        "replan_required": True,
        "next_plan_basis_candidate_digest": sha(
            {
                "learning_delta_digest": state["learning_delta_digest"],
                "middle_way_report_digest": state["middle_way_report_digest"],
                "route": state["route"],
            }
        ),
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "learn_phase_event_digest": require_string(
            learn_phase_event_digest, "learn_phase_event_digest"
        ),
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "learn_phase_receipt_digest": "",
    }
    packet["learn_phase_receipt_digest"] = learn_phase_receipt_digest(packet)
    return packet


def _validate_event_base(state: Mapping[str, Any], event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("learn_event_version_invalid")
    if event.get("learn_id") != state.get("learn_id"):
        errors.append("learn_event_id_mismatch")
    if event.get("lineage_id") != state.get("lineage_id"):
        errors.append("learn_event_lineage_mismatch")
    if event.get("learn_event_digest") != event_digest(event):
        errors.append("learn_event_digest_invalid")
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("learn_event_authority_escalation")
    source = str(event.get("source_phase", ""))
    if source != state.get("current_phase"):
        errors.append("learn_event_source_phase_stale")
    if event.get("target_phase") != next_phase(source):
        errors.append("learn_event_phase_order_invalid")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("learn_event_index_invalid")
    if event.get("expected_learn_state_digest") != state.get("learn_state_digest"):
        errors.append("learn_event_state_digest_stale")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("learn_event_time_regression")
    return errors


def _apply_payload(state: dict[str, Any], phase: str, payload: Mapping[str, Any]) -> None:
    if phase == "abstract":
        packet = payload.get("abstraction_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("abstraction_packet_required")
        if packet.get("version") != ABSTRACTION_PACKET_VERSION:
            raise ValueError("abstraction_packet_version_invalid")
        if packet.get("abstraction_packet_digest") != abstraction_packet_digest(packet):
            raise ValueError("abstraction_packet_digest_invalid")
        for field, expected in {
            "learn_id": state["learn_id"],
            "source_verify_state_digest": state["source_verify_state_digest"],
            "source_verification_evidence_digest": state[
                "source_verification_evidence_digest"
            ],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"abstraction_packet_{field}_mismatch")
        counterevidence = unique_strings(
            packet.get("counterevidence_digests"),
            "counterevidence_digests",
            allow_empty=True,
        )
        if counterevidence != list(state["source_counterevidence_digests"]):
            raise ValueError("abstraction_counterevidence_binding_mismatch")
        if state["source_unresolved_conflict"] and not list(
            packet.get("unresolved_pattern_digests", [])
        ):
            raise ValueError("unresolved_pattern_required")
        if packet.get("summary_replaces_source_evidence") is not False:
            raise ValueError("source_evidence_replacement_forbidden")
        if packet.get("counterevidence_preserved") is not True:
            raise ValueError("counterevidence_preservation_required")
        if packet.get("qi_context_only") is not True:
            raise ValueError("qi_context_boundary_required")
        state["abstraction_packet"] = deepcopy(dict(packet))
        state["abstraction_packet_digest"] = packet["abstraction_packet_digest"]
        return

    if phase == "challenge":
        packet = payload.get("learning_challenge_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("learning_challenge_packet_required")
        if packet.get("version") != CHALLENGE_PACKET_VERSION:
            raise ValueError("learning_challenge_packet_version_invalid")
        if packet.get("challenge_packet_digest") != challenge_packet_digest(packet):
            raise ValueError("learning_challenge_packet_digest_invalid")
        for field, expected in {
            "learn_id": state["learn_id"],
            "source_verify_state_digest": state["source_verify_state_digest"],
            "abstraction_packet_digest": state["abstraction_packet_digest"],
            "source_counterevidence_digest": state["source_counterevidence_digest"],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"learning_challenge_packet_{field}_mismatch")
        unique_strings(
            packet.get("anti_overgeneralization_test_digests"),
            "anti_overgeneralization_test_digests",
        )
        if packet.get("counterevidence_preserved") is not True:
            raise ValueError("counterevidence_preservation_required")
        if packet.get("challenge_complete") is not True:
            raise ValueError("learning_challenge_complete_required")
        state["learning_challenge_packet"] = deepcopy(dict(packet))
        state["learning_challenge_packet_digest"] = packet["challenge_packet_digest"]
        return

    if phase == "delta":
        packet = payload.get("learning_delta")
        if not isinstance(packet, Mapping):
            raise ValueError("learning_delta_required")
        if packet.get("version") != LEARNING_DELTA_VERSION:
            raise ValueError("learning_delta_version_invalid")
        if packet.get("learning_delta_digest") != learning_delta_digest(packet):
            raise ValueError("learning_delta_digest_invalid")
        for field, expected in {
            "learn_id": state["learn_id"],
            "source_verify_state_digest": state["source_verify_state_digest"],
            "source_verification_evidence_digest": state[
                "source_verification_evidence_digest"
            ],
            "abstraction_packet_digest": state["abstraction_packet_digest"],
            "learning_challenge_packet_digest": state[
                "learning_challenge_packet_digest"
            ],
            "source_counterevidence_digest": state["source_counterevidence_digest"],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"learning_delta_{field}_mismatch")
        kind = str(packet.get("learning_kind", ""))
        if kind not in LEARNING_KINDS:
            raise ValueError("learning_kind_invalid")
        if kind not in ALLOWED_KIND_BY_VERIFY_ROUTE.get(
            state["source_verification_route"], set()
        ):
            raise ValueError("learning_kind_incompatible_with_verification_route")
        scope = str(packet.get("target_scope", ""))
        if scope not in TARGET_SCOPES:
            raise ValueError("target_scope_invalid")
        if kind == "hold" and scope != "no_change":
            raise ValueError("hold_requires_no_change_scope")
        if kind != "hold" and scope == "no_change":
            raise ValueError("candidate_requires_change_scope")
        required_flags = {
            "future_only": True,
            "memory_overwrite": False,
            "active_now": False,
            "activation_requires_replan": True,
            "scope_widening": False,
            "invariant_removal": False,
            "current_cycle_mutation": False,
            "past_record_mutation": False,
        }
        for field, expected in required_flags.items():
            if packet.get(field) != expected:
                raise ValueError(f"learning_delta_{field}_invalid")
        state["learning_delta"] = deepcopy(dict(packet))
        state["learning_delta_digest"] = packet["learning_delta_digest"]
        return

    if phase == "middle_way_gate":
        packet = payload.get("middle_way_report")
        if not isinstance(packet, Mapping):
            raise ValueError("middle_way_report_required")
        if packet.get("version") != MIDDLE_WAY_REPORT_VERSION:
            raise ValueError("middle_way_report_version_invalid")
        if packet.get("middle_way_report_digest") != middle_way_report_digest(packet):
            raise ValueError("middle_way_report_digest_invalid")
        for field, expected in {
            "learn_id": state["learn_id"],
            "source_verify_state_digest": state["source_verify_state_digest"],
            "learning_delta_digest": state["learning_delta_digest"],
        }.items():
            if packet.get(field) != expected:
                raise ValueError(f"middle_way_report_{field}_mismatch")
        risks = [
            unit_number(packet.get(field), field)
            for field in (
                "reification_risk",
                "nihilistic_erasure_risk",
                "overgeneralization_risk",
                "negative_transfer_risk",
                "premature_activation_risk",
                "scope_drift_risk",
            )
        ]
        computed = max(risks) <= 0.65
        if packet.get("candidate_admissible") is not computed:
            raise ValueError("middle_way_candidate_admissibility_invalid")
        required = {
            "counterevidence_preserved": True,
            "samvrti_candidate_usable_for_replan": True,
            "paramartha_non_reification_preserved": True,
            "qi_grants_authority": False,
        }
        for field, expected in required.items():
            if packet.get(field) != expected:
                raise ValueError(f"middle_way_{field}_invalid")
        state["middle_way_report"] = deepcopy(dict(packet))
        state["middle_way_report_digest"] = packet["middle_way_report_digest"]
        kind = state["learning_delta"]["learning_kind"]
        state["route"] = (
            ROUTE_BY_KIND[kind]
            if kind == "hold" or computed
            else "LEARNING_HOLD"
        )
        if state["route"] == "LEARNING_REPAIR_CANDIDATE":
            state["corrective_action_required"] = True
            state["reobservation_required"] = False
        elif state["route"] == "LEARNING_REOBSERVATION_CANDIDATE":
            state["corrective_action_required"] = False
            state["reobservation_required"] = True
        elif state["route"] == "LEARNING_REINFORCEMENT_CANDIDATE":
            state["corrective_action_required"] = False
            state["reobservation_required"] = False
        else:
            state["corrective_action_required"] = False
            state["reobservation_required"] = bool(
                state["source_reobservation_required"]
            )
        return

    if phase == "commit":
        required = {
            "future_only": True,
            "memory_overwrite": False,
            "active_now": False,
            "activation_requires_replan": True,
            "current_cycle_unchanged": True,
            "past_records_unchanged": True,
            "counterevidence_preserved": True,
            "verification_not_truth": True,
            "qi_context_only": True,
            "automatic_truth_promotion": False,
            "automatic_belief_update": False,
            "automatic_plan_update": False,
            "automatic_criterion_update": False,
            "automatic_policy_activation": False,
            "automatic_rollback": False,
            "automatic_self_modification": False,
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"learn_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("learn_commit_authority_escalation")
        if state["route"] == "PENDING" or not state["middle_way_report_digest"]:
            raise ValueError("learn_middle_way_gate_not_recorded")
        state["learning_recorded"] = True
        state["learning_debt_discharged"] = True
        state["replan_required"] = True
        return

    raise ValueError("learn_target_phase_unsupported")


def _result(
    *, status: str, state: Mapping[str, Any], event_id: str, predecessor: str, errors: list[str]
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "learn_event_digest": event_id,
        "predecessor_learn_state_digest": predecessor,
        "result_learn_state_digest": state["learn_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "learn_apply_result_digest": "",
    }
    packet["learn_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_learn_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_learn_state(state)
    if state_errors:
        raise ValueError("invalid_learn_state:" + ";".join(state_errors))
    event_id = str(event.get("learn_event_digest", ""))
    predecessor = str(state["learn_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = _validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    next_state = deepcopy(dict(state))
    phase = str(event["target_phase"])
    try:
        _apply_payload(next_state, phase, dict(event.get("payload", {})))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_learn_state_digest"] = predecessor
    next_state["current_phase"] = phase
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": phase,
            "artifact_digest": event["artifact_digest"],
            "learn_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if phase == "commit":
        next_state["learn_version"] += 1
        next_state["committed_records"] += 1
        next_state["record_summaries"] = list(next_state["record_summaries"]) + [
            {
                "learn_version": next_state["learn_version"],
                "route": next_state["route"],
                "source_verify_state_digest": next_state[
                    "source_verify_state_digest"
                ],
                "source_verification_evidence_digest": next_state[
                    "source_verification_evidence_digest"
                ],
                "learning_delta_digest": next_state["learning_delta_digest"],
                "middle_way_report_digest": next_state[
                    "middle_way_report_digest"
                ],
                "future_only": True,
                "active_now": False,
                "replan_required": True,
            }
        ]
    next_state["learn_state_digest"] = ""
    next_state["learn_state_digest"] = state_digest(next_state)
    next_errors = validate_learn_state(next_state)
    if next_errors:
        raise ValueError("next_learn_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )
