from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_decision_os_plural_kernel_v0_2 import validate_plural_state
from runtime.kuuos_decision_os_wa_types_v0_3 import (
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    next_phase,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
    validate_wa_thresholds,
    validate_wa_weights,
    wa_event_digest,
    wa_state_digest,
)


def build_initial_wa_state(
    *,
    wa_id: str,
    source_plural_state: Mapping[str, Any],
    weights: Mapping[str, Any],
    thresholds: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    source_errors = validate_plural_state(source_plural_state)
    if source_errors:
        raise ValueError("invalid_source_plural_state:" + ";".join(source_errors))
    if source_plural_state.get("current_phase") != "commit":
        raise ValueError("source_plural_not_committed")
    source_option_ids = list(source_plural_state.get("source_option_ids", []))
    source_options = [deepcopy(dict(item)) for item in source_plural_state.get("source_options", [])]
    option_digest_by_id = {
        str(option["option_id"]): str(option["option_digest"])
        for option in source_options
    }
    state = {
        "version": STATE_VERSION,
        "wa_id": require_nonempty_string(wa_id, "wa_id"),
        "lineage_id": require_nonempty_string(
            source_plural_state.get("lineage_id"), "lineage_id"
        ),
        "source_plural_id": require_nonempty_string(
            source_plural_state.get("plural_id"), "source_plural_id"
        ),
        "source_plural_state_digest": require_nonempty_string(
            source_plural_state.get("plural_state_digest"),
            "source_plural_state_digest",
        ),
        "source_committed_plural_digest": require_nonempty_string(
            source_plural_state.get("latest_committed_plural_digest"),
            "source_committed_plural_digest",
        ),
        "source_plural_decision_basis_digest": require_nonempty_string(
            source_plural_state.get("plural_decision_basis_digest"),
            "source_plural_decision_basis_digest",
        ),
        "source_decision_basis_digest": require_nonempty_string(
            source_plural_state.get("source_decision_basis_digest"),
            "source_decision_basis_digest",
        ),
        "source_committed_decision_digest": require_nonempty_string(
            source_plural_state.get("source_committed_decision_digest"),
            "source_committed_decision_digest",
        ),
        "mission_contract_digest": require_nonempty_string(
            source_plural_state.get("mission_contract_digest"),
            "mission_contract_digest",
        ),
        "source_route": require_nonempty_string(
            source_plural_state.get("route"), "source_route"
        ),
        "source_selected_option_id": str(
            source_plural_state.get("selected_option_id", "")
        ),
        "source_option_ids": source_option_ids,
        "source_retained_alternative_ids": list(
            source_plural_state.get("retained_alternative_ids", [])
        ),
        "source_options_digest": require_nonempty_string(
            source_plural_state.get("source_options_digest"),
            "source_options_digest",
        ),
        "source_option_digest_by_id": option_digest_by_id,
        "source_stakeholder_registry_digest": require_nonempty_string(
            source_plural_state.get("stakeholder_registry_digest"),
            "source_stakeholder_registry_digest",
        ),
        "source_utility_records_digest": sha(source_plural_state.get("utility_records", [])),
        "source_veto_records_digest": sha(source_plural_state.get("veto_records", [])),
        "source_aggregate_records_digest": sha(source_plural_state.get("aggregate_records", [])),
        "source_appeal_history_digest": sha(source_plural_state.get("appeal_history", [])),
        "weights": validate_wa_weights(weights),
        "thresholds": validate_wa_thresholds(thresholds),
        "predecessor_wa_state_digest": "",
        "wa_state_digest": "",
        "current_phase": "bind",
        "event_index": 0,
        "wa_version": 0,
        "completed_wa_reviews": 0,
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "profiles": [],
        "wa_records": [],
        "false_harmony_records": [],
        "plurality": {
            "all_source_options_profiled": False,
            "retained_alternatives_preserved": False,
            "selected_identity_preserved": False,
            "stakeholder_sections_preserved": False,
            "veto_and_appeal_history_preserved": False,
            "silent_substitution_detected": False,
        },
        "route": "HOLD",
        "endorsed_option_ids": [],
        "review_option_ids": [],
        "wa_basis_digest": "",
        "pending_replan_activation": False,
        "latest_committed_wa_digest": "",
        "processed_event_digests": [],
        "event_history": [],
        "wa_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["wa_state_digest"] = wa_state_digest(state)
    return state


def validate_wa_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("wa_state_version_invalid")
        for field in (
            "wa_id",
            "lineage_id",
            "source_plural_id",
            "source_plural_state_digest",
            "source_committed_plural_digest",
            "source_plural_decision_basis_digest",
            "source_decision_basis_digest",
            "source_committed_decision_digest",
            "mission_contract_digest",
            "source_route",
            "source_options_digest",
            "source_stakeholder_registry_digest",
            "source_utility_records_digest",
            "source_veto_records_digest",
            "source_aggregate_records_digest",
            "source_appeal_history_digest",
        ):
            require_nonempty_string(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("wa_state_phase_invalid")
        for field in (
            "event_index",
            "wa_version",
            "completed_wa_reviews",
            "updated_at_ms",
        ):
            require_nonnegative_int(state.get(field), field)
        validate_wa_weights(require_mapping(state.get("weights"), "weights"))
        validate_wa_thresholds(
            require_mapping(state.get("thresholds"), "thresholds")
        )
        if state.get("route") not in ROUTES:
            errors.append("wa_state_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("wa_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("wa_state_boundary_invalid")
        if state.get("wa_state_digest") != wa_state_digest(state):
            errors.append("wa_state_digest_invalid")
        source_ids = list(state.get("source_option_ids", []))
        if len(source_ids) != len(set(source_ids)):
            errors.append("wa_source_option_duplicate")
        option_map = dict(state.get("source_option_digest_by_id", {}))
        if set(source_ids) != set(option_map):
            errors.append("wa_source_option_digest_map_mismatch")
        retained = list(state.get("source_retained_alternative_ids", []))
        if not set(retained).issubset(set(source_ids)):
            errors.append("wa_source_retained_unknown")
        selected = str(state.get("source_selected_option_id", ""))
        if selected and selected not in set(source_ids):
            errors.append("wa_source_selected_unknown")
        if state.get("source_route") == "CONSENSUS_CANDIDATE" and not selected:
            errors.append("wa_source_consensus_selected_missing")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("wa_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("wa_event_history_count_mismatch")
        profile_ids = [str(item.get("option_id", "")) for item in state.get("profiles", [])]
        if len(profile_ids) != len(set(profile_ids)):
            errors.append("wa_profile_option_duplicate")
        record_ids = [str(item.get("option_id", "")) for item in state.get("wa_records", [])]
        if len(record_ids) != len(set(record_ids)):
            errors.append("wa_record_option_duplicate")
        if state.get("route") == "ENDORSE" and not state.get(
            "endorsed_option_ids"
        ):
            errors.append("wa_endorsement_target_missing")
    except (TypeError, ValueError, KeyError) as exc:
        errors.append(str(exc))
    return errors


def build_wa_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "wa_id": require_nonempty_string(state.get("wa_id"), "wa_id"),
        "lineage_id": require_nonempty_string(
            state.get("lineage_id"), "lineage_id"
        ),
        "expected_wa_state_digest": require_nonempty_string(
            state.get("wa_state_digest"), "expected_wa_state_digest"
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
        "wa_event_digest": "",
    }
    event["wa_event_digest"] = wa_event_digest(event)
    return event


def validate_wa_event_base(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if event.get("version") != EVENT_VERSION:
            errors.append("wa_event_version_invalid")
        if event.get("wa_id") != state.get("wa_id"):
            errors.append("wa_event_id_mismatch")
        if event.get("lineage_id") != state.get("lineage_id"):
            errors.append("wa_event_lineage_mismatch")
        if event.get("wa_event_digest") != wa_event_digest(event):
            errors.append("wa_event_digest_invalid")
        if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("wa_event_authority_escalation")
        source = str(event.get("source_phase", ""))
        if source != state.get("current_phase"):
            errors.append("wa_event_source_phase_stale")
        if event.get("target_phase") != next_phase(source):
            errors.append("wa_event_phase_order_invalid")
        if event.get("event_index") != int(state.get("event_index", -1)) + 1:
            errors.append("wa_event_index_invalid")
        if event.get("expected_wa_state_digest") != state.get("wa_state_digest"):
            errors.append("wa_event_state_digest_stale")
        if int(event.get("created_at_ms", -1)) < int(
            state.get("updated_at_ms", 0)
        ):
            errors.append("wa_event_time_regression")
        require_nonempty_string(event.get("artifact_digest"), "artifact_digest")
        require_mapping(event.get("payload"), "payload")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
