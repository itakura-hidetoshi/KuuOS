from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_decision_os_wa_state_v0_3 import validate_wa_state
from runtime.kuuos_decision_os_wa_types_v0_3 import (
    ACTIVATION_RECEIPT_VERSION as WA_ACTIVATION_RECEIPT_VERSION,
    wa_activation_receipt_digest,
)
from runtime.kuuos_plan_os_types_v0_1 import (
    ACTIVE_ROUTES,
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    SOURCE_ROUTE_MAP,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    next_phase,
    nonnegative_number,
    plan_event_digest,
    plan_state_digest,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    unit_number,
)


def build_initial_plan_state(
    *,
    plan_id: str,
    source_wa_state: Mapping[str, Any],
    replan_activation_receipt: Mapping[str, Any],
    plan_budget: float,
    maximum_step_risk: float,
    now_ms: int,
) -> dict[str, Any]:
    source_errors = validate_wa_state(source_wa_state)
    if source_errors:
        raise ValueError("invalid_source_wa_state:" + ";".join(source_errors))
    if source_wa_state.get("current_phase") != "commit":
        raise ValueError("source_wa_not_committed")
    if replan_activation_receipt.get("version") != WA_ACTIVATION_RECEIPT_VERSION:
        raise ValueError("replan_activation_version_invalid")
    if replan_activation_receipt.get("wa_activation_receipt_digest") != wa_activation_receipt_digest(
        replan_activation_receipt
    ):
        raise ValueError("replan_activation_digest_invalid")
    if replan_activation_receipt.get("wa_state_digest") != source_wa_state.get(
        "wa_state_digest"
    ):
        raise ValueError("replan_activation_wa_state_mismatch")
    if replan_activation_receipt.get("committed_wa_digest") != source_wa_state.get(
        "latest_committed_wa_digest"
    ):
        raise ValueError("replan_activation_committed_wa_mismatch")
    if replan_activation_receipt.get("wa_basis_digest") != source_wa_state.get(
        "wa_basis_digest"
    ):
        raise ValueError("replan_activation_wa_basis_mismatch")
    if replan_activation_receipt.get("mission_cycle_phase") != "replan":
        raise ValueError("replan_activation_phase_invalid")
    if replan_activation_receipt.get("future_only") is not True:
        raise ValueError("replan_activation_future_only_required")
    if replan_activation_receipt.get("memory_overwrite") is not False:
        raise ValueError("replan_activation_memory_overwrite_forbidden")
    if replan_activation_receipt.get("host_license_granted") is not False:
        raise ValueError("replan_activation_host_license_forbidden")

    source_route = require_nonempty_string(source_wa_state.get("route"), "source_route")
    route = SOURCE_ROUTE_MAP.get(source_route)
    if route is None:
        raise ValueError("source_wa_route_unsupported")
    budget = nonnegative_number(plan_budget, "plan_budget")
    max_risk = unit_number(maximum_step_risk, "maximum_step_risk")

    state = {
        "version": STATE_VERSION,
        "plan_id": require_nonempty_string(plan_id, "plan_id"),
        "lineage_id": require_nonempty_string(source_wa_state.get("lineage_id"), "lineage_id"),
        "source_wa_id": require_nonempty_string(source_wa_state.get("wa_id"), "source_wa_id"),
        "source_wa_state_digest": require_nonempty_string(
            source_wa_state.get("wa_state_digest"), "source_wa_state_digest"
        ),
        "source_committed_wa_digest": require_nonempty_string(
            source_wa_state.get("latest_committed_wa_digest"),
            "source_committed_wa_digest",
        ),
        "source_wa_basis_digest": require_nonempty_string(
            source_wa_state.get("wa_basis_digest"), "source_wa_basis_digest"
        ),
        "source_plural_decision_basis_digest": require_nonempty_string(
            source_wa_state.get("source_plural_decision_basis_digest"),
            "source_plural_decision_basis_digest",
        ),
        "source_decision_basis_digest": require_nonempty_string(
            source_wa_state.get("source_decision_basis_digest"),
            "source_decision_basis_digest",
        ),
        "mission_contract_digest": require_nonempty_string(
            source_wa_state.get("mission_contract_digest"), "mission_contract_digest"
        ),
        "source_wa_route": source_route,
        "route": route,
        "source_endorsed_option_ids": list(source_wa_state.get("endorsed_option_ids", [])),
        "source_review_option_ids": list(source_wa_state.get("review_option_ids", [])),
        "source_selected_option_id": str(source_wa_state.get("source_selected_option_id", "")),
        "source_option_ids": list(source_wa_state.get("source_option_ids", [])),
        "source_retained_alternative_ids": list(
            source_wa_state.get("source_retained_alternative_ids", [])
        ),
        "source_stakeholder_registry_digest": require_nonempty_string(
            source_wa_state.get("source_stakeholder_registry_digest"),
            "source_stakeholder_registry_digest",
        ),
        "source_utility_records_digest": require_nonempty_string(
            source_wa_state.get("source_utility_records_digest"),
            "source_utility_records_digest",
        ),
        "source_veto_records_digest": require_nonempty_string(
            source_wa_state.get("source_veto_records_digest"),
            "source_veto_records_digest",
        ),
        "source_appeal_history_digest": require_nonempty_string(
            source_wa_state.get("source_appeal_history_digest"),
            "source_appeal_history_digest",
        ),
        "replan_activation_receipt_digest": require_nonempty_string(
            replan_activation_receipt.get("wa_activation_receipt_digest"),
            "replan_activation_receipt_digest",
        ),
        "replan_receipt_digest": require_nonempty_string(
            replan_activation_receipt.get("replan_receipt_digest"),
            "replan_receipt_digest",
        ),
        "mission_cycle_state_digest": require_nonempty_string(
            replan_activation_receipt.get("mission_cycle_state_digest"),
            "mission_cycle_state_digest",
        ),
        "next_plan_basis_digest": require_nonempty_string(
            replan_activation_receipt.get("next_plan_basis_digest"),
            "next_plan_basis_digest",
        ),
        "plan_budget": budget,
        "maximum_step_risk": max_risk,
        "predecessor_plan_state_digest": "",
        "plan_state_digest": "",
        "current_phase": "bind",
        "event_index": 0,
        "plan_version": 0,
        "completed_plans": 0,
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "steps": [],
        "topological_order": [],
        "resource_summary": {
            "total_cost": 0.0,
            "peak_step_risk": 0.0,
            "within_budget": True,
            "within_risk": True,
        },
        "guard_summary": {
            "all_effects_guarded": False,
            "source_identity_preserved": False,
            "route_class_valid": False,
        },
        "checkpoint_summary": {
            "all_effects_have_checkpoint": False,
            "observation_step_ids": [],
            "verification_step_ids": [],
        },
        "verification_summary": {
            "dependency_valid": False,
            "resource_valid": False,
            "guard_valid": False,
            "checkpoint_valid": False,
            "source_binding_valid": False,
            "plan_verified": False,
        },
        "plan_basis_digest": "",
        "pending_plan_phase_activation": False,
        "latest_committed_plan_digest": "",
        "processed_event_digests": [],
        "event_history": [],
        "plan_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["plan_state_digest"] = plan_state_digest(state)
    return state


def validate_plan_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("plan_state_version_invalid")
        for field in (
            "plan_id",
            "lineage_id",
            "source_wa_id",
            "source_wa_state_digest",
            "source_committed_wa_digest",
            "source_wa_basis_digest",
            "source_plural_decision_basis_digest",
            "source_decision_basis_digest",
            "mission_contract_digest",
            "source_wa_route",
            "source_stakeholder_registry_digest",
            "source_utility_records_digest",
            "source_veto_records_digest",
            "source_appeal_history_digest",
            "replan_activation_receipt_digest",
            "replan_receipt_digest",
            "mission_cycle_state_digest",
            "next_plan_basis_digest",
        ):
            require_nonempty_string(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("plan_state_phase_invalid")
        if state.get("route") not in ROUTES:
            errors.append("plan_state_route_invalid")
        expected_route = SOURCE_ROUTE_MAP.get(str(state.get("source_wa_route", "")))
        if expected_route != state.get("route"):
            errors.append("plan_route_source_mismatch")
        for field in (
            "event_index",
            "plan_version",
            "completed_plans",
            "updated_at_ms",
        ):
            require_nonnegative_int(state.get(field), field)
        nonnegative_number(state.get("plan_budget"), "plan_budget")
        unit_number(state.get("maximum_step_risk"), "maximum_step_risk")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("plan_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("plan_state_boundary_invalid")
        if state.get("plan_state_digest") != plan_state_digest(state):
            errors.append("plan_state_digest_invalid")
        source_ids = list(state.get("source_option_ids", []))
        if len(source_ids) != len(set(source_ids)):
            errors.append("plan_source_option_duplicate")
        endorsed = list(state.get("source_endorsed_option_ids", []))
        review = list(state.get("source_review_option_ids", []))
        if not set(endorsed).issubset(set(source_ids)):
            errors.append("plan_source_endorsed_unknown")
        if not set(review).issubset(set(source_ids)):
            errors.append("plan_source_review_unknown")
        step_ids = [str(item.get("step_id", "")) for item in state.get("steps", [])]
        if len(step_ids) != len(set(step_ids)):
            errors.append("plan_step_id_duplicate")
        order = list(state.get("topological_order", []))
        if order and set(order) != set(step_ids):
            errors.append("plan_topological_order_mismatch")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("plan_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("plan_event_history_count_mismatch")
        if state.get("route") in ACTIVE_ROUTES and state.get("current_phase") == "commit":
            if not state.get("steps"):
                errors.append("active_plan_steps_missing")
    except (TypeError, ValueError, KeyError) as exc:
        errors.append(str(exc))
    return errors


def build_plan_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "plan_id": require_nonempty_string(state.get("plan_id"), "plan_id"),
        "lineage_id": require_nonempty_string(state.get("lineage_id"), "lineage_id"),
        "expected_plan_state_digest": require_nonempty_string(
            state.get("plan_state_digest"), "expected_plan_state_digest"
        ),
        "source_phase": require_nonempty_string(
            state.get("current_phase"), "source_phase"
        ),
        "target_phase": require_nonempty_string(target_phase, "target_phase"),
        "event_index": require_nonnegative_int(state.get("event_index"), "event_index")
        + 1,
        "artifact_digest": require_nonempty_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "plan_event_digest": "",
    }
    event["plan_event_digest"] = plan_event_digest(event)
    return event


def validate_plan_event_base(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if event.get("version") != EVENT_VERSION:
            errors.append("plan_event_version_invalid")
        if event.get("plan_id") != state.get("plan_id"):
            errors.append("plan_event_id_mismatch")
        if event.get("lineage_id") != state.get("lineage_id"):
            errors.append("plan_event_lineage_mismatch")
        if event.get("plan_event_digest") != plan_event_digest(event):
            errors.append("plan_event_digest_invalid")
        if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("plan_event_authority_escalation")
        source = str(event.get("source_phase", ""))
        if source != state.get("current_phase"):
            errors.append("plan_event_source_phase_stale")
        if event.get("target_phase") != next_phase(source):
            errors.append("plan_event_phase_order_invalid")
        if event.get("event_index") != int(state.get("event_index", -1)) + 1:
            errors.append("plan_event_index_invalid")
        if event.get("expected_plan_state_digest") != state.get("plan_state_digest"):
            errors.append("plan_event_state_digest_stale")
        if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
            errors.append("plan_event_time_regression")
        require_nonempty_string(event.get("artifact_digest"), "artifact_digest")
        require_mapping(event.get("payload"), "payload")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
