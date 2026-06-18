from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import (
    EVENT_VERSION,
    NEXT_PHASE,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    event_digest,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    state_digest,
)


def append_unique(existing: Sequence[str], incoming: Sequence[str]) -> list[str]:
    result = list(existing)
    seen = set(result)
    for item in incoming:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def build_initial_belief_state(
    *,
    belief_id: str,
    lineage_id: str,
    claim: str,
    claim_digest: str,
    hypothesis_space_digest: str,
    source_memory_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    state = {
        "version": STATE_VERSION,
        "belief_id": require_nonempty_string(belief_id, "belief_id"),
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "claim": require_nonempty_string(claim, "claim"),
        "claim_digest": require_nonempty_string(claim_digest, "claim_digest"),
        "hypothesis_space_digest": require_nonempty_string(
            hypothesis_space_digest, "hypothesis_space_digest"
        ),
        "source_memory_digest": require_nonempty_string(
            source_memory_digest, "source_memory_digest"
        ),
        "predecessor_belief_state_digest": "",
        "belief_state_digest": "",
        "current_phase": "propose",
        "event_index": 0,
        "belief_version": 0,
        "completed_revisions": 0,
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "context": {},
        "evidence_digests": [],
        "observation_digests": [],
        "verification_receipt_digests": [],
        "causal_support_digests": [],
        "counterevidence_digests": [],
        "contradiction_digests": [],
        "alternative_hypothesis_digests": [],
        "unresolved_residual_digests": [],
        "resolved_challenge_receipts": [],
        "credal_state": {
            "lower_probability": 0.0,
            "upper_probability": 1.0,
            "central_estimate": None,
            "conflict_index": 0.0,
            "ignorance_width": 1.0,
        },
        "uncertainty": {
            "epistemic": 1.0,
            "aleatory": 0.0,
            "contextual": 1.0,
            "temporal": 1.0,
            "model": 1.0,
            "observer": 1.0,
            "process_history": 1.0,
        },
        "qi_process": {
            "process_tensor_digest": "",
            "history_window_digest": "",
            "roles": [],
            "flow_phase": "unobserved",
            "authority_source": False,
        },
        "two_truths": {
            "samvrti_operationally_usable": False,
            "paramartha_non_reified": True,
            "two_truths_separated": True,
        },
        "middle_way": {
            "reification_risk": 0.0,
            "nihilistic_erasure_risk": 0.0,
            "premature_closure_risk": 0.0,
            "responsibility_abandonment_risk": 0.0,
            "repairability": 1.0,
        },
        "route": "CANDIDATE",
        "reasoning_license": False,
        "planning_support_license": False,
        "pending_replan_activation": False,
        "latest_committed_belief_digest": "",
        "active_belief_snapshot_digest": "",
        "processed_event_digests": [],
        "event_history": [],
        "revision_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["belief_state_digest"] = state_digest(state)
    return state


def validate_belief_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("state_version_invalid")
        for field in (
            "belief_id",
            "lineage_id",
            "claim",
            "claim_digest",
            "hypothesis_space_digest",
            "source_memory_digest",
        ):
            require_nonempty_string(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("state_phase_invalid")
        for field in ("event_index", "belief_version", "completed_revisions", "updated_at_ms"):
            require_nonnegative_int(state.get(field), field)
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("state_boundary_invalid")
        if state.get("route") not in ROUTES:
            errors.append("state_route_invalid")
        if state.get("belief_state_digest") != state_digest(state):
            errors.append("state_digest_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("processed_event_digest_duplicate")
        if len(list(state.get("event_history", []))) != int(state.get("event_index", -1)):
            errors.append("event_history_count_mismatch")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_belief_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "belief_id": require_nonempty_string(state.get("belief_id"), "belief_id"),
        "lineage_id": require_nonempty_string(state.get("lineage_id"), "lineage_id"),
        "expected_belief_state_digest": require_nonempty_string(
            state.get("belief_state_digest"), "expected_belief_state_digest"
        ),
        "source_phase": require_nonempty_string(
            state.get("current_phase"), "source_phase"
        ),
        "target_phase": require_nonempty_string(target_phase, "target_phase"),
        "event_index": require_nonnegative_int(state.get("event_index"), "event_index") + 1,
        "artifact_digest": require_nonempty_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "belief_event_digest": "",
    }
    event["belief_event_digest"] = event_digest(event)
    return event


def validate_event_base(state: Mapping[str, Any], event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if event.get("version") != EVENT_VERSION:
            errors.append("event_version_invalid")
        if event.get("belief_id") != state.get("belief_id"):
            errors.append("event_belief_id_mismatch")
        if event.get("lineage_id") != state.get("lineage_id"):
            errors.append("event_lineage_id_mismatch")
        if event.get("belief_event_digest") != event_digest(event):
            errors.append("event_digest_invalid")
        if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("event_authority_escalation")
        source = event.get("source_phase")
        if source != state.get("current_phase"):
            errors.append("event_source_phase_stale")
        if source not in NEXT_PHASE or event.get("target_phase") != NEXT_PHASE.get(source):
            errors.append("event_phase_order_invalid")
        if event.get("event_index") != int(state.get("event_index", -1)) + 1:
            errors.append("event_index_invalid")
        if event.get("expected_belief_state_digest") != state.get("belief_state_digest"):
            errors.append("event_state_digest_stale")
        if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
            errors.append("event_time_regression")
        require_nonempty_string(event.get("artifact_digest"), "artifact_digest")
        require_mapping(event.get("payload"), "payload")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
