from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_transactional_effect_types_v0_24 import (
    FINAL_RECEIPT_VERSION,
    final_receipt_digest,
)
from runtime.kuuos_event_wakeup_control_resource_types_v0_25 import (
    APPLY_RESULT_VERSION,
    CONTROL_COMMANDS,
    CONTROL_COMMAND_VERSION,
    CONTROL_MODES,
    EVENT_VERSION,
    MODEL_TIERS,
    MUTATING_CONTROL_COMMANDS,
    NON_AUTHORITY_FLAGS,
    REQUIRED_BOUNDARY,
    RESOURCE_DECISION_VERSION,
    RESOURCE_ENVELOPE_VERSION,
    RESOURCE_FIELDS,
    RESOURCE_ROUTES,
    STATE_VERSION,
    STATUS_VERSION,
    TRIGGER_CLASSES,
    TRIGGER_VERSION,
    WAKEUP_ROUTES,
    WAKEUP_VERSION,
    apply_result_digest,
    control_command_digest,
    copy_boundary,
    copy_non_authority,
    event_digest,
    require_bool,
    require_nonnegative_int,
    require_positive_int,
    require_string,
    resource_decision_digest,
    resource_envelope_digest,
    state_digest,
    status_digest,
    trigger_digest,
    unique_strings,
    wakeup_digest,
)

TIER_SCALE = {"small": 40, "standard": 70, "advanced": 100}


def _resource_map(value: Any, name: str) -> dict[str, int]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_mapping_required")
    result: dict[str, int] = {}
    for field in RESOURCE_FIELDS:
        result[field] = require_nonnegative_int(value.get(field), f"{name}_{field}")
    if set(value) != set(RESOURCE_FIELDS):
        raise ValueError(f"{name}_fields_invalid")
    return result


def _scaled_resources(request: Mapping[str, int], tier: str) -> dict[str, int]:
    scale = TIER_SCALE[tier]
    return {
        field: max(1, (int(request[field]) * scale + 99) // 100)
        if int(request[field]) > 0
        else 0
        for field in RESOURCE_FIELDS
    }


def _receipt_static_valid(receipt: Mapping[str, Any]) -> bool:
    return (
        receipt.get("version") == FINAL_RECEIPT_VERSION
        and receipt.get("transaction_final_receipt_digest")
        == final_receipt_digest(receipt)
        and receipt.get("append_only_commit") is True
        and receipt.get("lower_receipts_remain_canonical") is True
        and receipt.get("commit_grants_execution_authority") is False
        and receipt.get("commit_grants_final_authority") is False
    )


def build_resource_envelope(
    *,
    envelope_id: str,
    mission_id: str,
    authorized_by_digest: str,
    allowed_model_tiers: list[str],
    preferred_model_tier: str,
    governance_caps: Mapping[str, int],
    hard_limits: Mapping[str, int],
    reserve_floors: Mapping[str, int],
    remaining: Mapping[str, int],
    max_cycles: int,
    remaining_cycles: int,
    renewable: bool,
    expires_at_ms: int,
) -> dict[str, Any]:
    tiers = unique_strings(allowed_model_tiers, "allowed_model_tiers")
    if any(tier not in MODEL_TIERS for tier in tiers):
        raise ValueError("resource_model_tier_invalid")
    preferred = require_string(preferred_model_tier, "preferred_model_tier")
    if preferred not in tiers:
        raise ValueError("resource_preferred_tier_not_allowed")
    caps = _resource_map(governance_caps, "governance_caps")
    limits = _resource_map(hard_limits, "hard_limits")
    floors = _resource_map(reserve_floors, "reserve_floors")
    available = _resource_map(remaining, "remaining")
    for field in RESOURCE_FIELDS:
        if limits[field] > caps[field]:
            raise ValueError(f"resource_{field}_limit_above_governance_cap")
        if floors[field] > limits[field]:
            raise ValueError(f"resource_{field}_floor_above_limit")
        if available[field] > limits[field]:
            raise ValueError(f"resource_{field}_remaining_above_limit")
    maximum_cycles = require_positive_int(max_cycles, "max_cycles")
    cycles = require_nonnegative_int(remaining_cycles, "remaining_cycles")
    if cycles > maximum_cycles:
        raise ValueError("remaining_cycles_above_max_cycles")
    packet = {
        "version": RESOURCE_ENVELOPE_VERSION,
        "envelope_id": require_string(envelope_id, "envelope_id"),
        "mission_id": require_string(mission_id, "mission_id"),
        "authorized_by_digest": require_string(
            authorized_by_digest, "authorized_by_digest"
        ),
        "allowed_model_tiers": tiers,
        "preferred_model_tier": preferred,
        "governance_caps": caps,
        "hard_limits": limits,
        "reserve_floors": floors,
        "remaining": available,
        "max_cycles": maximum_cycles,
        "remaining_cycles": cycles,
        "renewable": require_bool(renewable, "renewable"),
        "expires_at_ms": require_positive_int(expires_at_ms, "expires_at_ms"),
        "finite_envelope": True,
        "self_increase_allowed": False,
        "model_self_escalation_allowed": False,
        "resource_envelope_digest": "",
    }
    packet["resource_envelope_digest"] = resource_envelope_digest(packet)
    errors = validate_resource_envelope(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_resource_envelope(envelope: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if envelope.get("version") != RESOURCE_ENVELOPE_VERSION:
            errors.append("resource_envelope_version_invalid")
        for field in ("envelope_id", "mission_id", "authorized_by_digest"):
            require_string(envelope.get(field), field)
        tiers = unique_strings(envelope.get("allowed_model_tiers"), "allowed_model_tiers")
        if any(tier not in MODEL_TIERS for tier in tiers):
            errors.append("resource_model_tier_invalid")
        if envelope.get("preferred_model_tier") not in tiers:
            errors.append("resource_preferred_tier_not_allowed")
        caps = _resource_map(envelope.get("governance_caps"), "governance_caps")
        limits = _resource_map(envelope.get("hard_limits"), "hard_limits")
        floors = _resource_map(envelope.get("reserve_floors"), "reserve_floors")
        remaining = _resource_map(envelope.get("remaining"), "remaining")
        for field in RESOURCE_FIELDS:
            if limits[field] > caps[field]:
                errors.append(f"resource_{field}_limit_above_cap")
            if floors[field] > limits[field]:
                errors.append(f"resource_{field}_floor_above_limit")
            if remaining[field] > limits[field]:
                errors.append(f"resource_{field}_remaining_above_limit")
        maximum = require_positive_int(envelope.get("max_cycles"), "max_cycles")
        current = require_nonnegative_int(
            envelope.get("remaining_cycles"), "remaining_cycles"
        )
        if current > maximum:
            errors.append("resource_remaining_cycles_above_max")
        require_bool(envelope.get("renewable"), "renewable")
        require_positive_int(envelope.get("expires_at_ms"), "expires_at_ms")
        if envelope.get("finite_envelope") is not True:
            errors.append("resource_finite_envelope_required")
        if envelope.get("self_increase_allowed") is not False:
            errors.append("resource_self_increase_forbidden")
        if envelope.get("model_self_escalation_allowed") is not False:
            errors.append("resource_model_self_escalation_forbidden")
        if envelope.get("resource_envelope_digest") != resource_envelope_digest(
            envelope
        ):
            errors.append("resource_envelope_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_trigger_event(
    *,
    trigger_id: str,
    trigger_class: str,
    source_id: str,
    source_event_digest: str,
    mission_id: str,
    condition_digest: str,
    condition_satisfied: bool,
    requested_resources: Mapping[str, int],
    requested_model_tier: str,
    cycle_duration_ms: int,
    due_at_ms: int,
    observed_at_ms: int,
) -> dict[str, Any]:
    trigger_type = require_string(trigger_class, "trigger_class")
    if trigger_type not in TRIGGER_CLASSES:
        raise ValueError("trigger_class_invalid")
    tier = require_string(requested_model_tier, "requested_model_tier")
    if tier not in MODEL_TIERS:
        raise ValueError("trigger_model_tier_invalid")
    due = require_nonnegative_int(due_at_ms, "due_at_ms")
    observed = require_nonnegative_int(observed_at_ms, "observed_at_ms")
    if observed < due:
        raise ValueError("trigger_not_due")
    packet = {
        "version": TRIGGER_VERSION,
        "trigger_id": require_string(trigger_id, "trigger_id"),
        "trigger_class": trigger_type,
        "source_id": require_string(source_id, "source_id"),
        "source_event_digest": require_string(
            source_event_digest, "source_event_digest"
        ),
        "mission_id": require_string(mission_id, "mission_id"),
        "condition_digest": require_string(condition_digest, "condition_digest"),
        "condition_satisfied": require_bool(
            condition_satisfied, "condition_satisfied"
        ),
        "requested_resources": _resource_map(
            requested_resources, "requested_resources"
        ),
        "requested_model_tier": tier,
        "cycle_duration_ms": require_positive_int(
            cycle_duration_ms, "cycle_duration_ms"
        ),
        "due_at_ms": due,
        "observed_at_ms": observed,
        "external_trigger_surface": True,
        "hidden_daemon_invocation": False,
        "trigger_grants_execution_authority": False,
        "trigger_event_digest": "",
    }
    packet["trigger_event_digest"] = trigger_digest(packet)
    errors = validate_trigger_event(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_trigger_event(trigger: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if trigger.get("version") != TRIGGER_VERSION:
            errors.append("trigger_version_invalid")
        for field in (
            "trigger_id",
            "source_id",
            "source_event_digest",
            "mission_id",
            "condition_digest",
        ):
            require_string(trigger.get(field), field)
        if trigger.get("trigger_class") not in TRIGGER_CLASSES:
            errors.append("trigger_class_invalid")
        require_bool(trigger.get("condition_satisfied"), "condition_satisfied")
        _resource_map(trigger.get("requested_resources"), "requested_resources")
        if trigger.get("requested_model_tier") not in MODEL_TIERS:
            errors.append("trigger_model_tier_invalid")
        require_positive_int(trigger.get("cycle_duration_ms"), "cycle_duration_ms")
        due = require_nonnegative_int(trigger.get("due_at_ms"), "due_at_ms")
        observed = require_nonnegative_int(
            trigger.get("observed_at_ms"), "observed_at_ms"
        )
        if observed < due:
            errors.append("trigger_not_due")
        if trigger.get("external_trigger_surface") is not True:
            errors.append("trigger_external_surface_required")
        if trigger.get("hidden_daemon_invocation") is not False:
            errors.append("trigger_hidden_daemon_forbidden")
        if trigger.get("trigger_grants_execution_authority") is not False:
            errors.append("trigger_execution_authority_forbidden")
        if trigger.get("trigger_event_digest") != trigger_digest(trigger):
            errors.append("trigger_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_control_command(
    *,
    command_id: str,
    command: str,
    mission_id: str,
    principal_id: str,
    principal_authority_digest: str,
    expected_state_digest: str,
    reason_digest: str,
    payload: Mapping[str, Any],
    mission_control_authority: bool,
    permission_authority: bool,
    budget_authority: bool,
    issued_at_ms: int,
) -> dict[str, Any]:
    normalized = require_string(command, "command")
    if normalized not in CONTROL_COMMANDS:
        raise ValueError("control_command_invalid")
    packet = {
        "version": CONTROL_COMMAND_VERSION,
        "command_id": require_string(command_id, "command_id"),
        "command": normalized,
        "mission_id": require_string(mission_id, "mission_id"),
        "principal_id": require_string(principal_id, "principal_id"),
        "principal_authority_digest": require_string(
            principal_authority_digest, "principal_authority_digest"
        ),
        "expected_state_digest": require_string(
            expected_state_digest, "expected_state_digest"
        ),
        "reason_digest": require_string(reason_digest, "reason_digest"),
        "payload": deepcopy(dict(payload)),
        "mission_control_authority": require_bool(
            mission_control_authority, "mission_control_authority"
        ),
        "permission_authority": require_bool(
            permission_authority, "permission_authority"
        ),
        "budget_authority": require_bool(budget_authority, "budget_authority"),
        "read_only": normalized in {"inspect", "explain"},
        "direct_execution": False,
        "direct_plan_activation": False,
        "direct_world_rewrite": False,
        "issued_at_ms": require_nonnegative_int(issued_at_ms, "issued_at_ms"),
        "control_command_digest": "",
    }
    packet["control_command_digest"] = control_command_digest(packet)
    errors = validate_control_command(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_control_command(command: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if command.get("version") != CONTROL_COMMAND_VERSION:
            errors.append("control_command_version_invalid")
        for field in (
            "command_id",
            "mission_id",
            "principal_id",
            "principal_authority_digest",
            "expected_state_digest",
            "reason_digest",
        ):
            require_string(command.get(field), field)
        normalized = command.get("command")
        if normalized not in CONTROL_COMMANDS:
            errors.append("control_command_invalid")
        if not isinstance(command.get("payload"), Mapping):
            errors.append("control_command_payload_invalid")
        for field in (
            "mission_control_authority",
            "permission_authority",
            "budget_authority",
            "read_only",
            "direct_execution",
            "direct_plan_activation",
            "direct_world_rewrite",
        ):
            require_bool(command.get(field), field)
        if command.get("read_only") is not (normalized in {"inspect", "explain"}):
            errors.append("control_command_read_only_flag_invalid")
        if command.get("direct_execution") is not False:
            errors.append("control_command_direct_execution_forbidden")
        if command.get("direct_plan_activation") is not False:
            errors.append("control_command_direct_plan_activation_forbidden")
        if command.get("direct_world_rewrite") is not False:
            errors.append("control_command_direct_world_rewrite_forbidden")
        require_nonnegative_int(command.get("issued_at_ms"), "issued_at_ms")
        if command.get("control_command_digest") != control_command_digest(command):
            errors.append("control_command_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_state(
    *,
    mission_id: str,
    lineage_id: str,
    source_transaction_final_receipt: Mapping[str, Any],
    resource_envelope: Mapping[str, Any],
    initialized_at_ms: int,
) -> dict[str, Any]:
    if not _receipt_static_valid(source_transaction_final_receipt):
        raise ValueError("source_transaction_final_receipt_invalid")
    resource_errors = validate_resource_envelope(resource_envelope)
    if resource_errors:
        raise ValueError("resource_envelope_invalid:" + ";".join(resource_errors))
    mission = require_string(mission_id, "mission_id")
    if resource_envelope.get("mission_id") != mission:
        raise ValueError("resource_envelope_mission_mismatch")
    state = {
        "version": STATE_VERSION,
        "mission_id": mission,
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "source_transaction_final_receipt": deepcopy(
            dict(source_transaction_final_receipt)
        ),
        "source_transaction_final_receipt_digest": source_transaction_final_receipt[
            "transaction_final_receipt_digest"
        ],
        "control_mode": "ACTIVE",
        "control_reason_digest": "",
        "mission_revision": 0,
        "constraint_revision": 0,
        "priority": 0,
        "force_replan_required": False,
        "permission_approval_digests": [],
        "dead_letter_trigger_digests": [],
        "resource_envelope": deepcopy(dict(resource_envelope)),
        "resource_envelope_digest": resource_envelope["resource_envelope_digest"],
        "pending_cycle_ids": [],
        "wakeup_proposals": {},
        "processed_trigger_digests": [],
        "processed_control_command_digests": [],
        "event_history": [],
        "event_index": 0,
        "completed_wakeup_count": 0,
        "latest_wakeup_route": "",
        "latest_resource_route": "",
        "latest_status_snapshot": {},
        "latest_status_snapshot_digest": "",
        "updated_at_ms": require_nonnegative_int(
            initialized_at_ms, "initialized_at_ms"
        ),
        "conversation_model_running_as_daemon": False,
        "foreground_user_control_available": True,
        "queue_is_running": False,
        "running_is_verified": False,
        "append_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "event_wakeup_state_digest": "",
    }
    state["event_wakeup_state_digest"] = state_digest(state)
    errors = validate_state(state)
    if errors:
        raise ValueError("initial_state_invalid:" + ";".join(errors))
    return state


def validate_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("event_wakeup_state_version_invalid")
        for field in (
            "mission_id",
            "lineage_id",
            "source_transaction_final_receipt_digest",
            "resource_envelope_digest",
        ):
            require_string(state.get(field), field)
        receipt = state.get("source_transaction_final_receipt")
        if not isinstance(receipt, Mapping) or not _receipt_static_valid(receipt):
            errors.append("event_wakeup_source_transaction_receipt_invalid")
        elif state.get("source_transaction_final_receipt_digest") != receipt.get(
            "transaction_final_receipt_digest"
        ):
            errors.append("event_wakeup_source_receipt_digest_mismatch")
        envelope = state.get("resource_envelope")
        if not isinstance(envelope, Mapping):
            errors.append("event_wakeup_resource_envelope_missing")
        else:
            errors.extend(
                "resource:" + item for item in validate_resource_envelope(envelope)
            )
            if state.get("resource_envelope_digest") != envelope.get(
                "resource_envelope_digest"
            ):
                errors.append("event_wakeup_resource_digest_mismatch")
        if state.get("control_mode") not in CONTROL_MODES:
            errors.append("event_wakeup_control_mode_invalid")
        for field in (
            "mission_revision",
            "constraint_revision",
            "event_index",
            "completed_wakeup_count",
            "updated_at_ms",
        ):
            require_nonnegative_int(state.get(field), field)
        if not isinstance(state.get("priority"), int) or isinstance(
            state.get("priority"), bool
        ):
            errors.append("event_wakeup_priority_invalid")
        for field in (
            "force_replan_required",
            "conversation_model_running_as_daemon",
            "foreground_user_control_available",
            "queue_is_running",
            "running_is_verified",
            "append_only",
            "memory_overwrite",
        ):
            require_bool(state.get(field), field)
        if state.get("conversation_model_running_as_daemon") is not False:
            errors.append("event_wakeup_hidden_daemon_forbidden")
        if state.get("foreground_user_control_available") is not True:
            errors.append("event_wakeup_foreground_control_required")
        if state.get("queue_is_running") is not False:
            errors.append("event_wakeup_queue_running_collapse_forbidden")
        if state.get("running_is_verified") is not False:
            errors.append("event_wakeup_running_verified_collapse_forbidden")
        if state.get("append_only") is not True:
            errors.append("event_wakeup_append_only_required")
        if state.get("memory_overwrite") is not False:
            errors.append("event_wakeup_memory_overwrite_forbidden")
        for field in (
            "pending_cycle_ids",
            "permission_approval_digests",
            "dead_letter_trigger_digests",
            "processed_trigger_digests",
            "processed_control_command_digests",
            "event_history",
        ):
            if not isinstance(state.get(field), list):
                errors.append(f"event_wakeup_{field}_invalid")
        if not isinstance(state.get("wakeup_proposals"), Mapping):
            errors.append("event_wakeup_proposals_invalid")
        for field in (
            "processed_trigger_digests",
            "processed_control_command_digests",
            "pending_cycle_ids",
            "permission_approval_digests",
        ):
            values = list(state.get(field, []))
            if len(values) != len(set(values)):
                errors.append(f"event_wakeup_{field}_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("event_wakeup_event_history_count_mismatch")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("event_wakeup_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("event_wakeup_boundary_invalid")
        if state.get("event_wakeup_state_digest") != state_digest(state):
            errors.append("event_wakeup_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def evaluate_resource_admission(
    *, state: Mapping[str, Any], trigger: Mapping[str, Any], evaluated_at_ms: int
) -> dict[str, Any]:
    state_errors = validate_state(state)
    trigger_errors = validate_trigger_event(trigger)
    if state_errors:
        raise ValueError("state_invalid:" + ";".join(state_errors))
    if trigger_errors:
        raise ValueError("trigger_invalid:" + ";".join(trigger_errors))
    if trigger.get("mission_id") != state.get("mission_id"):
        raise ValueError("trigger_mission_mismatch")
    mode = state["control_mode"]
    route_by_mode = {
        "PAUSED": "REJECT_CONTROL_PAUSED",
        "CANCELLED": "REJECT_CONTROL_CANCELLED",
        "HANDOVER": "REJECT_HANDOVER",
        "AWAITING_RENEWAL": "RENEWAL_REQUIRED",
    }
    selected_tier = str(trigger["requested_model_tier"])
    requested = _resource_map(trigger["requested_resources"], "requested_resources")
    reserved = dict(requested)
    shortfalls: list[str] = []
    envelope = state["resource_envelope"]
    route = route_by_mode.get(mode, "")
    if not route and trigger.get("condition_satisfied") is not True:
        route = "PAUSE_RESOURCE_EXHAUSTED"
        shortfalls.append("trigger_condition_unsatisfied")
    if not route and int(envelope["remaining_cycles"]) < 1:
        route = "RENEWAL_REQUIRED" if envelope["renewable"] else "PAUSE_RESOURCE_EXHAUSTED"
        shortfalls.append("cycle_budget_exhausted")
    if not route and int(evaluated_at_ms) >= int(envelope["expires_at_ms"]):
        route = "RENEWAL_REQUIRED" if envelope["renewable"] else "PAUSE_RESOURCE_EXHAUSTED"
        shortfalls.append("resource_envelope_expired")
    if not route:
        candidate_tiers = [
            tier
            for tier in MODEL_TIERS
            if tier in envelope["allowed_model_tiers"]
            and MODEL_TIERS.index(tier) <= MODEL_TIERS.index(selected_tier)
        ]
        candidate_tiers.sort(key=lambda tier: MODEL_TIERS.index(tier), reverse=True)
        admitted: tuple[str, dict[str, int]] | None = None
        for tier in candidate_tiers:
            scaled = _scaled_resources(requested, tier)
            if all(
                int(envelope["remaining"][field]) - scaled[field]
                >= int(envelope["reserve_floors"][field])
                for field in RESOURCE_FIELDS
            ):
                admitted = (tier, scaled)
                break
        if admitted is None:
            route = "RENEWAL_REQUIRED" if envelope["renewable"] else "PAUSE_RESOURCE_EXHAUSTED"
            for field in RESOURCE_FIELDS:
                if int(envelope["remaining"][field]) - requested[field] < int(
                    envelope["reserve_floors"][field]
                ):
                    shortfalls.append(field)
        else:
            selected_tier, reserved = admitted
            route = (
                "ADMIT"
                if selected_tier == trigger["requested_model_tier"]
                else "DEGRADE_MODEL"
            )
    packet = {
        "version": RESOURCE_DECISION_VERSION,
        "mission_id": state["mission_id"],
        "source_state_digest": state["event_wakeup_state_digest"],
        "trigger_event_digest": trigger["trigger_event_digest"],
        "resource_envelope_digest": state["resource_envelope_digest"],
        "route": route,
        "requested_model_tier": trigger["requested_model_tier"],
        "selected_model_tier": selected_tier,
        "requested_resources": requested,
        "reserved_resources": reserved if route in {"ADMIT", "DEGRADE_MODEL"} else {field: 0 for field in RESOURCE_FIELDS},
        "shortfall_fields": sorted(set(shortfalls)),
        "new_cycle_license_required": route in {"ADMIT", "DEGRADE_MODEL"},
        "budget_self_increase_performed": False,
        "model_self_escalation_performed": False,
        "evaluated_at_ms": require_nonnegative_int(evaluated_at_ms, "evaluated_at_ms"),
        "non_authority": copy_non_authority(),
        "resource_decision_digest": "",
    }
    packet["resource_decision_digest"] = resource_decision_digest(packet)
    return packet


def build_wakeup_proposal(
    *,
    state: Mapping[str, Any],
    trigger: Mapping[str, Any],
    resource_decision: Mapping[str, Any],
    proposed_at_ms: int,
) -> dict[str, Any]:
    route_map = {
        "ADMIT": "WAKEUP_PROPOSED",
        "DEGRADE_MODEL": "WAKEUP_DEGRADED",
        "RENEWAL_REQUIRED": "WAKEUP_BLOCKED_RENEWAL",
        "PAUSE_RESOURCE_EXHAUSTED": "WAKEUP_BLOCKED_RENEWAL",
        "REJECT_CONTROL_PAUSED": "WAKEUP_BLOCKED_PAUSED",
        "REJECT_CONTROL_CANCELLED": "WAKEUP_BLOCKED_CANCELLED",
        "REJECT_HANDOVER": "WAKEUP_BLOCKED_HANDOVER",
    }
    route = route_map[str(resource_decision["route"])]
    admitted = route in {"WAKEUP_PROPOSED", "WAKEUP_DEGRADED"}
    cycle_id = (
        f"{state['mission_id']}:cycle:{int(state['completed_wakeup_count']) + 1}:"
        f"{trigger['trigger_id']}"
        if admitted
        else ""
    )
    packet = {
        "version": WAKEUP_VERSION,
        "mission_id": state["mission_id"],
        "lineage_id": state["lineage_id"],
        "source_state_digest": state["event_wakeup_state_digest"],
        "source_transaction_final_receipt_digest": state[
            "source_transaction_final_receipt_digest"
        ],
        "trigger_event_digest": trigger["trigger_event_digest"],
        "resource_decision_digest": resource_decision[
            "resource_decision_digest"
        ],
        "route": route,
        "new_cycle_id": cycle_id,
        "selected_model_tier": resource_decision["selected_model_tier"],
        "reserved_resources": deepcopy(resource_decision["reserved_resources"]),
        "cycle_duration_ms": trigger["cycle_duration_ms"],
        "new_bounded_cycle": admitted,
        "fresh_plan_required": admitted,
        "fresh_cycle_license_required": admitted,
        "fresh_actos_authorization_required": admitted,
        "inherited_execution_authority": False,
        "queue_entry_only": admitted,
        "running": False,
        "verified": False,
        "conversation_model_daemon_started": False,
        "proposed_at_ms": require_nonnegative_int(proposed_at_ms, "proposed_at_ms"),
        "non_authority": copy_non_authority(),
        "wakeup_proposal_digest": "",
    }
    packet["wakeup_proposal_digest"] = wakeup_digest(packet)
    return packet


def build_event(
    *,
    state: Mapping[str, Any],
    event_kind: str,
    payload: Mapping[str, Any],
    created_at_ms: int,
) -> dict[str, Any]:
    if event_kind not in {"trigger", "control"}:
        raise ValueError("event_kind_invalid")
    packet = {
        "version": EVENT_VERSION,
        "mission_id": state["mission_id"],
        "expected_state_digest": state["event_wakeup_state_digest"],
        "event_index": int(state["event_index"]) + 1,
        "event_kind": event_kind,
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "event_wakeup_event_digest": "",
    }
    packet["event_wakeup_event_digest"] = event_digest(packet)
    return packet


def _valid_actions(state: Mapping[str, Any]) -> list[str]:
    mode = state["control_mode"]
    if mode == "CANCELLED":
        return ["inspect", "explain", "handover"]
    if mode == "HANDOVER":
        return ["inspect", "explain"]
    if mode in {"PAUSED", "AWAITING_RENEWAL"}:
        return [
            "inspect",
            "explain",
            "resume",
            "cancel",
            "increase_budget",
            "revise_mission",
            "revise_constraint",
            "handover",
        ]
    return sorted(CONTROL_COMMANDS)


def build_status_snapshot(
    *, state: Mapping[str, Any], reason_digest: str, observed_at_ms: int
) -> dict[str, Any]:
    mode = state["control_mode"]
    worker_state = {
        "ACTIVE": "QUEUED" if state["pending_cycle_ids"] else "IDLE",
        "PAUSED": "PAUSED",
        "CANCELLED": "CANCELLED",
        "HANDOVER": "HANDOVER",
        "AWAITING_RENEWAL": "AWAITING_RENEWAL",
    }[mode]
    next_condition = {
        "ACTIVE": "external_trigger_or_user_command",
        "PAUSED": "authorized_resume",
        "CANCELLED": "none_terminal",
        "HANDOVER": "external_owner_acceptance",
        "AWAITING_RENEWAL": "authorized_budget_renewal_then_resume",
    }[mode]
    packet = {
        "version": STATUS_VERSION,
        "mission_id": state["mission_id"],
        "source_state_digest": state["event_wakeup_state_digest"],
        "state": mode,
        "reason_digest": require_string(reason_digest, "reason_digest"),
        "completed_work": {
            "source_transaction_committed": True,
            "wakeup_proposals_created": state["completed_wakeup_count"],
            "events_applied": state["event_index"],
        },
        "checkpoint": {
            "source_transaction_final_receipt_digest": state[
                "source_transaction_final_receipt_digest"
            ],
            "latest_wakeup_route": state["latest_wakeup_route"],
            "latest_resource_route": state["latest_resource_route"],
            "pending_cycle_ids": list(state["pending_cycle_ids"]),
        },
        "next_condition": next_condition,
        "resource_state": deepcopy(dict(state["resource_envelope"])),
        "worker_state": worker_state,
        "valid_user_actions": _valid_actions(state),
        "foreground_channel_available": True,
        "status_grants_execution_authority": False,
        "observed_at_ms": require_nonnegative_int(observed_at_ms, "observed_at_ms"),
        "status_snapshot_digest": "",
    }
    packet["status_snapshot_digest"] = status_digest(packet)
    return packet


def _resource_increase(
    envelope: Mapping[str, Any], payload: Mapping[str, Any]
) -> dict[str, Any]:
    hard_increase = _resource_map(payload.get("hard_limit_increase"), "hard_limit_increase")
    replenishment = _resource_map(payload.get("remaining_replenishment"), "remaining_replenishment")
    result = deepcopy(dict(envelope))
    for field in RESOURCE_FIELDS:
        new_limit = int(result["hard_limits"][field]) + hard_increase[field]
        if new_limit > int(result["governance_caps"][field]):
            raise ValueError(f"budget_{field}_increase_above_governance_cap")
        new_remaining = int(result["remaining"][field]) + replenishment[field]
        if new_remaining > new_limit:
            raise ValueError(f"budget_{field}_replenishment_above_new_limit")
        result["hard_limits"][field] = new_limit
        result["remaining"][field] = new_remaining
    cycle_increase = require_nonnegative_int(
        payload.get("cycle_limit_increase"), "cycle_limit_increase"
    )
    cycle_replenishment = require_nonnegative_int(
        payload.get("cycle_replenishment"), "cycle_replenishment"
    )
    new_max_cycles = int(result["max_cycles"]) + cycle_increase
    new_remaining_cycles = int(result["remaining_cycles"]) + cycle_replenishment
    if new_remaining_cycles > new_max_cycles:
        raise ValueError("cycle_replenishment_above_new_limit")
    result["max_cycles"] = new_max_cycles
    result["remaining_cycles"] = new_remaining_cycles
    result["authorized_by_digest"] = require_string(
        payload.get("new_authorization_digest"), "new_authorization_digest"
    )
    result["resource_envelope_digest"] = ""
    result["resource_envelope_digest"] = resource_envelope_digest(result)
    errors = validate_resource_envelope(result)
    if errors:
        raise ValueError("resource_increase_invalid:" + ";".join(errors))
    return result


def _apply_control(state: dict[str, Any], command: Mapping[str, Any]) -> None:
    normalized = str(command["command"])
    payload = command["payload"]
    if normalized in {"inspect", "explain"}:
        raise ValueError("read_only_command_must_use_status_endpoint")
    if command.get("mission_control_authority") is not True:
        raise ValueError("control_command_mission_authority_required")
    mode = state["control_mode"]
    if mode == "CANCELLED" and normalized != "handover":
        raise ValueError("cancelled_state_is_terminal")
    if mode == "HANDOVER":
        raise ValueError("handover_state_is_terminal")
    if normalized == "pause":
        state["control_mode"] = "PAUSED"
        state["control_reason_digest"] = command["reason_digest"]
    elif normalized == "resume":
        if mode not in {"PAUSED", "AWAITING_RENEWAL"}:
            raise ValueError("resume_requires_paused_or_renewal_state")
        envelope = state["resource_envelope"]
        if int(envelope["remaining_cycles"]) < 1:
            raise ValueError("resume_cycle_budget_unavailable")
        if any(
            int(envelope["remaining"][field]) <= int(envelope["reserve_floors"][field])
            for field in RESOURCE_FIELDS
        ):
            raise ValueError("resume_resource_floor_not_restored")
        state["control_mode"] = "ACTIVE"
        state["control_reason_digest"] = command["reason_digest"]
    elif normalized == "cancel":
        state["control_mode"] = "CANCELLED"
        state["control_reason_digest"] = command["reason_digest"]
        state["pending_cycle_ids"] = []
    elif normalized == "handover":
        state["control_mode"] = "HANDOVER"
        state["control_reason_digest"] = command["reason_digest"]
        state["pending_cycle_ids"] = []
    elif normalized == "reprioritize":
        priority = payload.get("priority")
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise ValueError("reprioritize_priority_int_required")
        state["priority"] = priority
    elif normalized == "revise_mission":
        require_string(payload.get("mission_revision_digest"), "mission_revision_digest")
        state["mission_revision"] += 1
        state["force_replan_required"] = True
    elif normalized == "revise_constraint":
        require_string(
            payload.get("constraint_revision_digest"), "constraint_revision_digest"
        )
        state["constraint_revision"] += 1
        state["force_replan_required"] = True
    elif normalized == "approve_permission":
        if command.get("permission_authority") is not True:
            raise ValueError("permission_authority_required")
        approval = require_string(
            payload.get("permission_approval_digest"),
            "permission_approval_digest",
        )
        if approval not in state["permission_approval_digests"]:
            state["permission_approval_digests"] = list(
                state["permission_approval_digests"]
            ) + [approval]
    elif normalized == "increase_budget":
        if command.get("budget_authority") is not True:
            raise ValueError("budget_authority_required")
        state["resource_envelope"] = _resource_increase(
            state["resource_envelope"], payload
        )
        state["resource_envelope_digest"] = state["resource_envelope"][
            "resource_envelope_digest"
        ]
    elif normalized == "force_replan":
        state["force_replan_required"] = True
    elif normalized == "release_dead_letter":
        digest = require_string(
            payload.get("trigger_event_digest"), "trigger_event_digest"
        )
        state["dead_letter_trigger_digests"] = [
            item for item in state["dead_letter_trigger_digests"] if item != digest
        ]
    else:
        raise ValueError("control_command_not_implemented")


def _apply_trigger(state: dict[str, Any], trigger: Mapping[str, Any], now_ms: int) -> None:
    decision = evaluate_resource_admission(
        state=state, trigger=trigger, evaluated_at_ms=now_ms
    )
    proposal = build_wakeup_proposal(
        state=state,
        trigger=trigger,
        resource_decision=decision,
        proposed_at_ms=now_ms,
    )
    trigger_id = trigger["trigger_event_digest"]
    state["latest_resource_route"] = decision["route"]
    state["latest_wakeup_route"] = proposal["route"]
    state["wakeup_proposals"] = dict(state["wakeup_proposals"])
    state["wakeup_proposals"][proposal["wakeup_proposal_digest"]] = proposal
    if proposal["new_bounded_cycle"] is True:
        envelope = deepcopy(dict(state["resource_envelope"]))
        for field in RESOURCE_FIELDS:
            envelope["remaining"][field] = int(envelope["remaining"][field]) - int(
                proposal["reserved_resources"][field]
            )
        envelope["remaining_cycles"] = int(envelope["remaining_cycles"]) - 1
        envelope["resource_envelope_digest"] = ""
        envelope["resource_envelope_digest"] = resource_envelope_digest(envelope)
        state["resource_envelope"] = envelope
        state["resource_envelope_digest"] = envelope["resource_envelope_digest"]
        state["pending_cycle_ids"] = list(state["pending_cycle_ids"]) + [
            proposal["new_cycle_id"]
        ]
        state["completed_wakeup_count"] += 1
    else:
        state["dead_letter_trigger_digests"] = list(
            state["dead_letter_trigger_digests"]
        ) + [trigger_id]
        if decision["route"] in {"RENEWAL_REQUIRED", "PAUSE_RESOURCE_EXHAUSTED"}:
            state["control_mode"] = "AWAITING_RENEWAL"
            state["control_reason_digest"] = decision["resource_decision_digest"]


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: list[str],
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "event_wakeup_event_digest": event_id,
        "predecessor_state_digest": predecessor,
        "result_state_digest": state["event_wakeup_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "event_wakeup_apply_result_digest": "",
    }
    packet["event_wakeup_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_state(state)
    if state_errors:
        raise ValueError("state_invalid:" + ";".join(state_errors))
    event_id = str(event.get("event_wakeup_event_digest", ""))
    predecessor = state["event_wakeup_state_digest"]
    if event.get("event_kind") == "trigger":
        payload_id = str(event.get("payload", {}).get("trigger_event_digest", ""))
        if payload_id in set(state["processed_trigger_digests"]):
            return _result(
                status="REPLAYED",
                state=state,
                event_id=event_id,
                predecessor=predecessor,
                errors=[],
            )
    if event.get("event_kind") == "control":
        payload_id = str(event.get("payload", {}).get("control_command_digest", ""))
        if payload_id in set(state["processed_control_command_digests"]):
            return _result(
                status="REPLAYED",
                state=state,
                event_id=event_id,
                predecessor=predecessor,
                errors=[],
            )
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("event_version_invalid")
    if event.get("mission_id") != state.get("mission_id"):
        errors.append("event_mission_mismatch")
    if event.get("expected_state_digest") != predecessor:
        errors.append("event_state_digest_stale")
    if event.get("event_index") != int(state["event_index"]) + 1:
        errors.append("event_index_invalid")
    if int(event.get("created_at_ms", -1)) < int(state["updated_at_ms"]):
        errors.append("event_time_regression")
    if event.get("event_kind") not in {"trigger", "control"}:
        errors.append("event_kind_invalid")
    if event.get("event_wakeup_event_digest") != event_digest(event):
        errors.append("event_digest_invalid")
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    next_state = deepcopy(dict(state))
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=["event_payload_invalid"],
        )
    try:
        if event["event_kind"] == "trigger":
            payload_errors = validate_trigger_event(payload)
            if payload_errors:
                raise ValueError("trigger_invalid:" + ";".join(payload_errors))
            if payload.get("mission_id") != state.get("mission_id"):
                raise ValueError("trigger_mission_mismatch")
            _apply_trigger(next_state, payload, int(event["created_at_ms"]))
            next_state["processed_trigger_digests"] = list(
                next_state["processed_trigger_digests"]
            ) + [payload["trigger_event_digest"]]
            payload_digest = payload["trigger_event_digest"]
        else:
            payload_errors = validate_control_command(payload)
            if payload_errors:
                raise ValueError("control_invalid:" + ";".join(payload_errors))
            if payload.get("mission_id") != state.get("mission_id"):
                raise ValueError("control_mission_mismatch")
            if payload.get("expected_state_digest") != predecessor:
                raise ValueError("control_state_digest_stale")
            _apply_control(next_state, payload)
            next_state["processed_control_command_digests"] = list(
                next_state["processed_control_command_digests"]
            ) + [payload["control_command_digest"]]
            payload_digest = payload["control_command_digest"]
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["event_index"] += 1
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": next_state["event_index"],
            "event_kind": event["event_kind"],
            "payload_digest": payload_digest,
            "event_wakeup_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    status = build_status_snapshot(
        state={
            **next_state,
            "event_wakeup_state_digest": state_digest(
                {**next_state, "event_wakeup_state_digest": ""}
            ),
        },
        reason_digest=(
            next_state["control_reason_digest"]
            or payload_digest
        ),
        observed_at_ms=int(event["created_at_ms"]),
    )
    next_state["latest_status_snapshot"] = status
    next_state["latest_status_snapshot_digest"] = status["status_snapshot_digest"]
    next_state["event_wakeup_state_digest"] = ""
    next_state["event_wakeup_state_digest"] = state_digest(next_state)
    next_errors = validate_state(next_state)
    if next_errors:
        raise ValueError("next_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


__all__ = [
    "apply_event",
    "build_control_command",
    "build_event",
    "build_initial_state",
    "build_resource_envelope",
    "build_status_snapshot",
    "build_trigger_event",
    "build_wakeup_proposal",
    "evaluate_resource_admission",
    "validate_control_command",
    "validate_resource_envelope",
    "validate_state",
    "validate_trigger_event",
]
