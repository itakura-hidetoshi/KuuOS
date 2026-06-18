from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_decision_os_types_v0_1 import (
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    event_digest,
    next_phase,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    state_digest,
    validate_thresholds,
    validate_weights,
)


def build_initial_decision_state(
    *,
    decision_id: str,
    lineage_id: str,
    mission_contract_digest: str,
    mission_state_digest: str,
    source_belief_receipt_digest: str,
    decision_context_digest: str,
    decision_budget: float,
    weights: Mapping[str, Any],
    thresholds: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    normalized_weights = validate_weights(weights)
    normalized_thresholds = validate_thresholds(thresholds)
    budget = float(decision_budget)
    if budget < 0.0:
        raise ValueError("decision_budget_negative")
    state = {
        "version": STATE_VERSION,
        "decision_id": require_nonempty_string(decision_id, "decision_id"),
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "mission_contract_digest": require_nonempty_string(
            mission_contract_digest, "mission_contract_digest"
        ),
        "mission_state_digest": require_nonempty_string(
            mission_state_digest, "mission_state_digest"
        ),
        "source_belief_receipt_digest": require_nonempty_string(
            source_belief_receipt_digest, "source_belief_receipt_digest"
        ),
        "decision_context_digest": require_nonempty_string(
            decision_context_digest, "decision_context_digest"
        ),
        "decision_budget": budget,
        "weights": normalized_weights,
        "thresholds": normalized_thresholds,
        "predecessor_decision_state_digest": "",
        "decision_state_digest": "",
        "current_phase": "frame",
        "event_index": 0,
        "decision_version": 0,
        "completed_deliberations": 0,
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "frame": {
            "mission_bound": True,
            "belief_basis_conditional": True,
            "decision_not_execution": True,
        },
        "options": [],
        "admissible_option_ids": [],
        "excluded_options": [],
        "evaluation_records": [],
        "dominance_relations": [],
        "retained_alternative_ids": [],
        "challenge": {
            "counterargument_digests": [],
            "missing_evidence_digests": [],
            "stakeholder_objection_digests": [],
            "alternative_option_ids": [],
            "counterfactual_receipt_digests": [],
            "catastrophic_risk_detected": False,
            "unresolved_normative_conflict": False,
        },
        "qi_process": {
            "process_tensor_digest": "",
            "history_window_digest": "",
            "roles": [],
            "flow_phase": "unobserved",
            "authority_source": False,
        },
        "two_truths": {
            "samvrti_decision_usable": False,
            "paramartha_non_reified": True,
            "selected_option_not_absolute": True,
            "two_truths_separated": True,
        },
        "middle_way": {
            "reification_risk": 0.0,
            "nihilistic_erasure_risk": 0.0,
            "premature_closure_risk": 0.0,
            "responsibility_abandonment_risk": 0.0,
            "stakeholder_exclusion_risk": 0.0,
            "irreversibility_risk": 0.0,
            "repairability": 1.0,
            "selection_allowed": False,
            "responsible_deferral_allowed": True,
        },
        "route": "HOLD",
        "selected_option_id": "",
        "recommended_option_ids": [],
        "decision_basis_digest": "",
        "pending_replan_activation": False,
        "latest_committed_decision_digest": "",
        "advisory_receipt_digests": [],
        "processed_event_digests": [],
        "event_history": [],
        "decision_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["decision_state_digest"] = state_digest(state)
    return state


def validate_decision_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("decision_state_version_invalid")
        for field in (
            "decision_id",
            "lineage_id",
            "mission_contract_digest",
            "mission_state_digest",
            "source_belief_receipt_digest",
            "decision_context_digest",
        ):
            require_nonempty_string(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("decision_state_phase_invalid")
        for field in (
            "event_index",
            "decision_version",
            "completed_deliberations",
            "updated_at_ms",
        ):
            require_nonnegative_int(state.get(field), field)
        if float(state.get("decision_budget", -1.0)) < 0.0:
            errors.append("decision_budget_negative")
        validate_weights(require_mapping(state.get("weights"), "weights"))
        validate_thresholds(require_mapping(state.get("thresholds"), "thresholds"))
        if state.get("route") not in ROUTES:
            errors.append("decision_state_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("decision_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("decision_state_boundary_invalid")
        if state.get("decision_state_digest") != state_digest(state):
            errors.append("decision_state_digest_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("decision_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("decision_event_history_count_mismatch")
        option_ids = [str(item.get("option_id", "")) for item in state.get("options", [])]
        if len(option_ids) != len(set(option_ids)):
            errors.append("decision_option_id_duplicate")
        admissible = list(state.get("admissible_option_ids", []))
        if len(admissible) != len(set(admissible)):
            errors.append("decision_admissible_option_duplicate")
        if not set(admissible).issubset(set(option_ids)):
            errors.append("decision_admissible_option_unknown")
        selected = str(state.get("selected_option_id", ""))
        if selected and selected not in set(admissible):
            errors.append("decision_selected_option_not_admissible")
        if state.get("route") == "SELECT_CANDIDATE" and not selected:
            errors.append("decision_selected_option_missing")
        if selected and state.get("route") != "SELECT_CANDIDATE":
            errors.append("decision_selected_option_route_mismatch")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_decision_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "decision_id": require_nonempty_string(
            state.get("decision_id"), "decision_id"
        ),
        "lineage_id": require_nonempty_string(state.get("lineage_id"), "lineage_id"),
        "expected_decision_state_digest": require_nonempty_string(
            state.get("decision_state_digest"), "expected_decision_state_digest"
        ),
        "source_phase": require_nonempty_string(
            state.get("current_phase"), "source_phase"
        ),
        "target_phase": require_nonempty_string(target_phase, "target_phase"),
        "event_index": require_nonnegative_int(
            state.get("event_index"), "event_index"
        )
        + 1,
        "artifact_digest": require_nonempty_string(
            artifact_digest, "artifact_digest"
        ),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "decision_event_digest": "",
    }
    event["decision_event_digest"] = event_digest(event)
    return event


def validate_event_base(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if event.get("version") != EVENT_VERSION:
            errors.append("decision_event_version_invalid")
        if event.get("decision_id") != state.get("decision_id"):
            errors.append("decision_event_id_mismatch")
        if event.get("lineage_id") != state.get("lineage_id"):
            errors.append("decision_event_lineage_mismatch")
        if event.get("decision_event_digest") != event_digest(event):
            errors.append("decision_event_digest_invalid")
        if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("decision_event_authority_escalation")
        source = str(event.get("source_phase", ""))
        if source != state.get("current_phase"):
            errors.append("decision_event_source_phase_stale")
        if event.get("target_phase") != next_phase(source):
            errors.append("decision_event_phase_order_invalid")
        if event.get("event_index") != int(state.get("event_index", -1)) + 1:
            errors.append("decision_event_index_invalid")
        if event.get("expected_decision_state_digest") != state.get(
            "decision_state_digest"
        ):
            errors.append("decision_event_state_digest_stale")
        if int(event.get("created_at_ms", -1)) < int(
            state.get("updated_at_ms", 0)
        ):
            errors.append("decision_event_time_regression")
        require_nonempty_string(event.get("artifact_digest"), "artifact_digest")
        require_mapping(event.get("payload"), "payload")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
