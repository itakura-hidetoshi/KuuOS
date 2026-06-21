from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_integrated_long_duration_operation_types_v0_27 import (
    APPLY_RESULT_VERSION,
    CONTRACT_VERSION,
    CONTROL_COMMANDS,
    CONTROL_VERSION,
    CYCLE_ROUTES,
    CYCLE_VERSION,
    EVENT_VERSION,
    LOWER_COMPONENTS,
    NON_AUTHORITY_FLAGS,
    OPERATION_MODES,
    RECOVERY_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    apply_result_digest,
    contract_digest,
    control_digest,
    copy_boundary,
    copy_non_authority,
    cycle_digest,
    event_digest,
    exact_string_map,
    recovery_digest,
    require_bool,
    require_nonnegative_int,
    require_positive_int,
    require_string,
    state_digest,
)


def build_integrated_operation_contract(
    *,
    contract_id: str,
    mission_id: str,
    lineage_id: str,
    lower_contract_digests: Mapping[str, str],
    initial_host_license_digest: str,
    max_cycle_cost: int,
    max_cycle_steps: int,
    max_cycle_duration_ms: int,
    max_lease_cycles: int,
    max_lease_cost: int,
    initial_lease_id: str,
    initial_lease_cycles: int,
    initial_lease_cost: int,
    initial_lease_expires_at_ms: int,
    user_control_policy_digest: str,
    recovery_policy_digest: str,
    audit_policy_digest: str,
    created_at_ms: int,
) -> dict[str, Any]:
    created = require_nonnegative_int(created_at_ms, "created_at_ms")
    max_cycles = require_positive_int(max_lease_cycles, "max_lease_cycles")
    max_cost = require_positive_int(max_lease_cost, "max_lease_cost")
    lease_cycles = require_positive_int(initial_lease_cycles, "initial_lease_cycles")
    lease_cost = require_positive_int(initial_lease_cost, "initial_lease_cost")
    if lease_cycles > max_cycles:
        raise ValueError("initial_lease_cycles_above_contract_cap")
    if lease_cost > max_cost:
        raise ValueError("initial_lease_cost_above_contract_cap")
    expiry = require_positive_int(
        initial_lease_expires_at_ms, "initial_lease_expires_at_ms"
    )
    if expiry <= created:
        raise ValueError("initial_lease_expiry_invalid")
    packet = {
        "version": CONTRACT_VERSION,
        "contract_id": require_string(contract_id, "contract_id"),
        "mission_id": require_string(mission_id, "mission_id"),
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "lower_contract_digests": exact_string_map(
            lower_contract_digests, LOWER_COMPONENTS, "lower_contract_digests"
        ),
        "initial_host_license_digest": require_string(
            initial_host_license_digest, "initial_host_license_digest"
        ),
        "max_cycle_cost": require_positive_int(max_cycle_cost, "max_cycle_cost"),
        "max_cycle_steps": require_positive_int(max_cycle_steps, "max_cycle_steps"),
        "max_cycle_duration_ms": require_positive_int(
            max_cycle_duration_ms, "max_cycle_duration_ms"
        ),
        "max_lease_cycles": max_cycles,
        "max_lease_cost": max_cost,
        "initial_lease_id": require_string(initial_lease_id, "initial_lease_id"),
        "initial_lease_cycles": lease_cycles,
        "initial_lease_cost": lease_cost,
        "initial_lease_expires_at_ms": expiry,
        "user_control_policy_digest": require_string(
            user_control_policy_digest, "user_control_policy_digest"
        ),
        "recovery_policy_digest": require_string(
            recovery_policy_digest, "recovery_policy_digest"
        ),
        "audit_policy_digest": require_string(
            audit_policy_digest, "audit_policy_digest"
        ),
        "external_renewal_required": True,
        "automatic_renewal": False,
        "finite_cycle_contract": True,
        "finite_lease_contract": True,
        "created_at_ms": created,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "integrated_operation_contract_digest": "",
    }
    packet["integrated_operation_contract_digest"] = contract_digest(packet)
    errors = validate_contract(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_contract(contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if contract.get("version") != CONTRACT_VERSION:
            errors.append("integrated_contract_version_invalid")
        for field in (
            "contract_id",
            "mission_id",
            "lineage_id",
            "initial_host_license_digest",
            "initial_lease_id",
            "user_control_policy_digest",
            "recovery_policy_digest",
            "audit_policy_digest",
        ):
            require_string(contract.get(field), field)
        exact_string_map(
            contract.get("lower_contract_digests"),
            LOWER_COMPONENTS,
            "lower_contract_digests",
        )
        for field in (
            "max_cycle_cost",
            "max_cycle_steps",
            "max_cycle_duration_ms",
            "max_lease_cycles",
            "max_lease_cost",
            "initial_lease_cycles",
            "initial_lease_cost",
            "initial_lease_expires_at_ms",
        ):
            require_positive_int(contract.get(field), field)
        if int(contract["initial_lease_cycles"]) > int(contract["max_lease_cycles"]):
            errors.append("integrated_initial_cycles_above_cap")
        if int(contract["initial_lease_cost"]) > int(contract["max_lease_cost"]):
            errors.append("integrated_initial_cost_above_cap")
        if int(contract["initial_lease_expires_at_ms"]) <= int(
            contract.get("created_at_ms", -1)
        ):
            errors.append("integrated_initial_expiry_invalid")
        require_nonnegative_int(contract.get("created_at_ms"), "created_at_ms")
        if contract.get("external_renewal_required") is not True:
            errors.append("integrated_external_renewal_required")
        if contract.get("automatic_renewal") is not False:
            errors.append("integrated_automatic_renewal_forbidden")
        if contract.get("finite_cycle_contract") is not True:
            errors.append("integrated_finite_cycle_contract_required")
        if contract.get("finite_lease_contract") is not True:
            errors.append("integrated_finite_lease_contract_required")
        if dict(contract.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("integrated_contract_authority_expansion")
        if dict(contract.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("integrated_contract_boundary_invalid")
        if contract.get("integrated_operation_contract_digest") != contract_digest(
            contract
        ):
            errors.append("integrated_contract_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_state(
    *, contract: Mapping[str, Any], initialized_at_ms: int
) -> dict[str, Any]:
    errors = validate_contract(contract)
    if errors:
        raise ValueError("contract_invalid:" + ";".join(errors))
    now = require_nonnegative_int(initialized_at_ms, "initialized_at_ms")
    if now >= int(contract["initial_lease_expires_at_ms"]):
        raise ValueError("initial_state_after_lease_expiry")
    state = {
        "version": STATE_VERSION,
        "contract": deepcopy(dict(contract)),
        "contract_digest": contract["integrated_operation_contract_digest"],
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "mode": "ACTIVE",
        "mode_reason_digest": "",
        "cycle_index": 0,
        "completed_cycles": 0,
        "lease_sequence": 0,
        "lease_id": contract["initial_lease_id"],
        "lease_cycles_remaining": contract["initial_lease_cycles"],
        "lease_cost_remaining": contract["initial_lease_cost"],
        "lease_expires_at_ms": contract["initial_lease_expires_at_ms"],
        "host_license_digest": contract["initial_host_license_digest"],
        "fresh_host_license_required": False,
        "process_epoch": 0,
        "host_epoch": 0,
        "latest_checkpoint_digest": contract["integrated_operation_contract_digest"],
        "latest_cycle_receipt_digest": "",
        "cycle_summaries": [],
        "processed_event_digests": [],
        "event_history": [],
        "event_index": 0,
        "updated_at_ms": now,
        "foreground_user_control_available": True,
        "termination_reachable": True,
        "handover_reachable": True,
        "automatic_renewal_performed": False,
        "automatic_resume_performed": False,
        "history_append_only": True,
        "audit_preserved": True,
        "provenance_preserved": True,
        "memory_root_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "integrated_operation_state_digest": "",
    }
    state["integrated_operation_state_digest"] = state_digest(state)
    state_errors = validate_state(state)
    if state_errors:
        raise ValueError("initial_state_invalid:" + ";".join(state_errors))
    return state


def validate_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("integrated_state_version_invalid")
        contract = state.get("contract")
        if not isinstance(contract, Mapping):
            errors.append("integrated_state_contract_missing")
        else:
            errors.extend("contract:" + item for item in validate_contract(contract))
            if state.get("contract_digest") != contract.get(
                "integrated_operation_contract_digest"
            ):
                errors.append("integrated_state_contract_digest_mismatch")
        if state.get("mode") not in OPERATION_MODES:
            errors.append("integrated_state_mode_invalid")
        for field in (
            "cycle_index",
            "completed_cycles",
            "lease_sequence",
            "lease_cycles_remaining",
            "lease_cost_remaining",
            "lease_expires_at_ms",
            "process_epoch",
            "host_epoch",
            "event_index",
            "updated_at_ms",
        ):
            require_nonnegative_int(state.get(field), field)
        if int(state.get("cycle_index", -1)) != int(
            state.get("completed_cycles", -2)
        ):
            errors.append("integrated_cycle_index_mismatch")
        for field in (
            "fresh_host_license_required",
            "foreground_user_control_available",
            "termination_reachable",
            "handover_reachable",
            "automatic_renewal_performed",
            "automatic_resume_performed",
            "history_append_only",
            "audit_preserved",
            "provenance_preserved",
            "memory_root_overwrite",
        ):
            require_bool(state.get(field), field)
        if state.get("foreground_user_control_available") is not True:
            errors.append("integrated_foreground_control_missing")
        if state.get("termination_reachable") is not True:
            errors.append("integrated_termination_not_reachable")
        if state.get("handover_reachable") is not True:
            errors.append("integrated_handover_not_reachable")
        if state.get("automatic_renewal_performed") is not False:
            errors.append("integrated_automatic_renewal_forbidden")
        if state.get("automatic_resume_performed") is not False:
            errors.append("integrated_automatic_resume_forbidden")
        if state.get("history_append_only") is not True:
            errors.append("integrated_history_append_only_required")
        if state.get("audit_preserved") is not True:
            errors.append("integrated_audit_preservation_required")
        if state.get("provenance_preserved") is not True:
            errors.append("integrated_provenance_preservation_required")
        if state.get("memory_root_overwrite") is not False:
            errors.append("integrated_memory_overwrite_forbidden")
        for field in ("cycle_summaries", "processed_event_digests", "event_history"):
            if not isinstance(state.get(field), list):
                errors.append(f"integrated_{field}_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("integrated_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("integrated_event_history_count_mismatch")
        if len(list(state.get("cycle_summaries", []))) != int(
            state.get("completed_cycles", -1)
        ):
            errors.append("integrated_cycle_summary_count_mismatch")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("integrated_state_authority_expansion")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("integrated_state_boundary_invalid")
        if state.get("integrated_operation_state_digest") != state_digest(state):
            errors.append("integrated_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_cycle_receipt(
    *,
    state: Mapping[str, Any],
    cycle_id: str,
    lower_cycle_receipt_digests: Mapping[str, str],
    cycle_authorization_digest: str,
    host_license_digest: str,
    cycle_cost: int,
    cycle_steps: int,
    started_at_ms: int,
    completed_at_ms: int,
    route: str,
    checkpoint_digest: str,
) -> dict[str, Any]:
    errors = validate_state(state)
    if errors:
        raise ValueError("state_invalid:" + ";".join(errors))
    if state.get("mode") != "ACTIVE":
        raise ValueError("cycle_requires_active_mode")
    if state.get("fresh_host_license_required") is not False:
        raise ValueError("cycle_requires_fresh_host_license")
    normalized_route = require_string(route, "route")
    if normalized_route not in CYCLE_ROUTES:
        raise ValueError("cycle_route_invalid")
    cost = require_positive_int(cycle_cost, "cycle_cost")
    steps = require_positive_int(cycle_steps, "cycle_steps")
    started = require_nonnegative_int(started_at_ms, "started_at_ms")
    completed = require_nonnegative_int(completed_at_ms, "completed_at_ms")
    if started < int(state["updated_at_ms"]):
        raise ValueError("cycle_start_before_state_time")
    if completed <= started:
        raise ValueError("cycle_completion_time_invalid")
    contract = state["contract"]
    if cost > int(contract["max_cycle_cost"]):
        raise ValueError("cycle_cost_above_per_cycle_bound")
    if cost > int(state["lease_cost_remaining"]):
        raise ValueError("cycle_cost_above_lease_remaining")
    if steps > int(contract["max_cycle_steps"]):
        raise ValueError("cycle_steps_above_per_cycle_bound")
    if completed - started > int(contract["max_cycle_duration_ms"]):
        raise ValueError("cycle_duration_above_per_cycle_bound")
    if int(state["lease_cycles_remaining"]) < 1:
        raise ValueError("cycle_lease_quota_exhausted")
    if completed >= int(state["lease_expires_at_ms"]):
        raise ValueError("cycle_completed_after_lease_expiry")
    if host_license_digest != state["host_license_digest"]:
        raise ValueError("cycle_host_license_mismatch")
    packet = {
        "version": CYCLE_VERSION,
        "cycle_id": require_string(cycle_id, "cycle_id"),
        "mission_id": state["mission_id"],
        "lineage_id": state["lineage_id"],
        "source_state_digest": state["integrated_operation_state_digest"],
        "cycle_number": int(state["completed_cycles"]) + 1,
        "lease_id": state["lease_id"],
        "lease_sequence": state["lease_sequence"],
        "lower_cycle_receipt_digests": exact_string_map(
            lower_cycle_receipt_digests,
            LOWER_COMPONENTS,
            "lower_cycle_receipt_digests",
        ),
        "cycle_authorization_digest": require_string(
            cycle_authorization_digest, "cycle_authorization_digest"
        ),
        "host_license_digest": require_string(
            host_license_digest, "host_license_digest"
        ),
        "cycle_cost": cost,
        "cycle_steps": steps,
        "started_at_ms": started,
        "completed_at_ms": completed,
        "route": normalized_route,
        "checkpoint_digest": require_string(
            checkpoint_digest, "checkpoint_digest"
        ),
        "fresh_cycle_authority": True,
        "finite_cycle_cost": True,
        "finite_cycle_steps": True,
        "finite_cycle_duration": True,
        "lower_receipts_canonical": True,
        "verification_is_truth": False,
        "learning_is_permission": False,
        "wake_event_is_permission": False,
        "change_review_is_deployment": False,
        "user_control_observed": True,
        "memory_root_overwrite": False,
        "non_authority": copy_non_authority(),
        "integrated_cycle_receipt_digest": "",
    }
    packet["integrated_cycle_receipt_digest"] = cycle_digest(packet)
    return packet


def validate_cycle_receipt(
    receipt: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != CYCLE_VERSION:
            errors.append("integrated_cycle_version_invalid")
        if receipt.get("source_state_digest") != state.get(
            "integrated_operation_state_digest"
        ):
            errors.append("integrated_cycle_source_state_mismatch")
        if receipt.get("mission_id") != state.get("mission_id"):
            errors.append("integrated_cycle_mission_mismatch")
        if receipt.get("lineage_id") != state.get("lineage_id"):
            errors.append("integrated_cycle_lineage_mismatch")
        if receipt.get("cycle_number") != int(state.get("completed_cycles", -1)) + 1:
            errors.append("integrated_cycle_number_invalid")
        if receipt.get("lease_id") != state.get("lease_id"):
            errors.append("integrated_cycle_lease_id_mismatch")
        if receipt.get("lease_sequence") != state.get("lease_sequence"):
            errors.append("integrated_cycle_lease_sequence_mismatch")
        exact_string_map(
            receipt.get("lower_cycle_receipt_digests"),
            LOWER_COMPONENTS,
            "lower_cycle_receipt_digests",
        )
        for field in (
            "cycle_id",
            "cycle_authorization_digest",
            "host_license_digest",
            "checkpoint_digest",
        ):
            require_string(receipt.get(field), field)
        cost = require_positive_int(receipt.get("cycle_cost"), "cycle_cost")
        steps = require_positive_int(receipt.get("cycle_steps"), "cycle_steps")
        started = require_nonnegative_int(receipt.get("started_at_ms"), "started_at_ms")
        completed = require_nonnegative_int(
            receipt.get("completed_at_ms"), "completed_at_ms"
        )
        contract = state["contract"]
        if cost > int(contract["max_cycle_cost"]):
            errors.append("integrated_cycle_cost_bound_invalid")
        if cost > int(state["lease_cost_remaining"]):
            errors.append("integrated_cycle_lease_cost_invalid")
        if steps > int(contract["max_cycle_steps"]):
            errors.append("integrated_cycle_step_bound_invalid")
        if completed <= started:
            errors.append("integrated_cycle_time_invalid")
        if completed - started > int(contract["max_cycle_duration_ms"]):
            errors.append("integrated_cycle_duration_bound_invalid")
        if completed >= int(state["lease_expires_at_ms"]):
            errors.append("integrated_cycle_lease_expired")
        if receipt.get("host_license_digest") != state.get("host_license_digest"):
            errors.append("integrated_cycle_host_license_mismatch")
        if receipt.get("route") not in CYCLE_ROUTES:
            errors.append("integrated_cycle_route_invalid")
        for field in (
            "fresh_cycle_authority",
            "finite_cycle_cost",
            "finite_cycle_steps",
            "finite_cycle_duration",
            "lower_receipts_canonical",
            "user_control_observed",
        ):
            if receipt.get(field) is not True:
                errors.append(f"integrated_cycle_{field}_required")
        for field in (
            "verification_is_truth",
            "learning_is_permission",
            "wake_event_is_permission",
            "change_review_is_deployment",
            "memory_root_overwrite",
        ):
            if receipt.get(field) is not False:
                errors.append(f"integrated_cycle_{field}_forbidden")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("integrated_cycle_authority_expansion")
        if receipt.get("integrated_cycle_receipt_digest") != cycle_digest(receipt):
            errors.append("integrated_cycle_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_control_event(
    *,
    state: Mapping[str, Any],
    command: str,
    command_id: str,
    external_authority_digest: str,
    reason_digest: str,
    payload: Mapping[str, Any],
    issued_at_ms: int,
) -> dict[str, Any]:
    normalized = require_string(command, "command")
    if normalized not in CONTROL_COMMANDS:
        raise ValueError("integrated_control_command_invalid")
    packet = {
        "version": CONTROL_VERSION,
        "command_id": require_string(command_id, "command_id"),
        "command": normalized,
        "mission_id": state["mission_id"],
        "source_state_digest": state["integrated_operation_state_digest"],
        "external_authority_digest": require_string(
            external_authority_digest, "external_authority_digest"
        ),
        "reason_digest": require_string(reason_digest, "reason_digest"),
        "payload": deepcopy(dict(payload)),
        "direct_effect": False,
        "automatic_resume": False,
        "issued_at_ms": require_nonnegative_int(issued_at_ms, "issued_at_ms"),
        "integrated_control_event_digest": "",
    }
    packet["integrated_control_event_digest"] = control_digest(packet)
    return packet


def build_recovery_receipt(
    *,
    state: Mapping[str, Any],
    recovery_kind: str,
    ledger_root_digest: str,
    checkpoint_digest: str,
    new_host_license_digest: str = "",
    recovered_at_ms: int,
) -> dict[str, Any]:
    if recovery_kind not in {"process_restart", "host_restart", "host_rebind"}:
        raise ValueError("integrated_recovery_kind_invalid")
    host_license = str(new_host_license_digest)
    if recovery_kind == "host_rebind":
        require_string(host_license, "new_host_license_digest")
    elif host_license:
        raise ValueError("integrated_unexpected_host_license")
    packet = {
        "version": RECOVERY_VERSION,
        "recovery_kind": recovery_kind,
        "mission_id": state["mission_id"],
        "source_state_digest": state["integrated_operation_state_digest"],
        "ledger_root_digest": require_string(
            ledger_root_digest, "ledger_root_digest"
        ),
        "checkpoint_digest": require_string(
            checkpoint_digest, "checkpoint_digest"
        ),
        "new_host_license_digest": host_license,
        "ledger_replay_verified": True,
        "checkpoint_verified": checkpoint_digest
        == state["latest_checkpoint_digest"],
        "automatic_resume": False,
        "recovered_at_ms": require_nonnegative_int(
            recovered_at_ms, "recovered_at_ms"
        ),
        "integrated_recovery_receipt_digest": "",
    }
    packet["integrated_recovery_receipt_digest"] = recovery_digest(packet)
    return packet


def build_event(
    *,
    state: Mapping[str, Any],
    event_kind: str,
    payload: Mapping[str, Any],
    created_at_ms: int,
) -> dict[str, Any]:
    if event_kind not in {"cycle", "control", "recovery"}:
        raise ValueError("integrated_event_kind_invalid")
    packet = {
        "version": EVENT_VERSION,
        "mission_id": state["mission_id"],
        "expected_state_digest": state["integrated_operation_state_digest"],
        "event_index": int(state["event_index"]) + 1,
        "event_kind": event_kind,
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(
            created_at_ms, "created_at_ms"
        ),
        "integrated_operation_event_digest": "",
    }
    packet["integrated_operation_event_digest"] = event_digest(packet)
    return packet


def _apply_cycle(state: dict[str, Any], receipt: Mapping[str, Any]) -> None:
    errors = validate_cycle_receipt(receipt, state)
    if errors:
        raise ValueError("cycle_invalid:" + ";".join(errors))
    cost = int(receipt["cycle_cost"])
    state["completed_cycles"] += 1
    state["cycle_index"] = state["completed_cycles"]
    state["lease_cycles_remaining"] -= 1
    state["lease_cost_remaining"] -= cost
    state["latest_checkpoint_digest"] = receipt["checkpoint_digest"]
    state["latest_cycle_receipt_digest"] = receipt[
        "integrated_cycle_receipt_digest"
    ]
    state["cycle_summaries"] = list(state["cycle_summaries"]) + [
        {
            "cycle_number": receipt["cycle_number"],
            "cycle_id": receipt["cycle_id"],
            "lease_sequence": receipt["lease_sequence"],
            "cycle_cost": cost,
            "cycle_steps": receipt["cycle_steps"],
            "route": receipt["route"],
            "checkpoint_digest": receipt["checkpoint_digest"],
            "integrated_cycle_receipt_digest": receipt[
                "integrated_cycle_receipt_digest"
            ],
        }
    ]
    route = receipt["route"]
    if route == "PAUSE":
        state["mode"] = "PAUSED"
    elif route == "RENEWAL_REQUIRED":
        state["mode"] = "RENEWAL_REQUIRED"
    elif route == "TERMINATE":
        state["mode"] = "TERMINATED"
    elif route == "HANDOVER":
        state["mode"] = "HANDED_OVER"
    elif (
        state["lease_cycles_remaining"] == 0
        or state["lease_cost_remaining"] < int(state["contract"]["max_cycle_cost"])
    ):
        state["mode"] = "RENEWAL_REQUIRED"
        state["mode_reason_digest"] = receipt["integrated_cycle_receipt_digest"]


def _apply_control(state: dict[str, Any], command: Mapping[str, Any], now_ms: int) -> None:
    if command.get("version") != CONTROL_VERSION:
        raise ValueError("control_version_invalid")
    if command.get("source_state_digest") != state[
        "integrated_operation_state_digest"
    ]:
        raise ValueError("control_state_stale")
    if command.get("integrated_control_event_digest") != control_digest(command):
        raise ValueError("control_digest_invalid")
    if command.get("direct_effect") is not False:
        raise ValueError("control_direct_effect_forbidden")
    normalized = str(command.get("command", ""))
    if normalized not in CONTROL_COMMANDS:
        raise ValueError("control_command_invalid")
    mode = state["mode"]
    if mode in {"TERMINATED", "HANDED_OVER"}:
        raise ValueError("terminal_mode_rejects_control")
    if normalized == "pause":
        state["mode"] = "PAUSED"
    elif normalized == "resume":
        if mode != "PAUSED":
            raise ValueError("resume_requires_paused_mode")
        if state["fresh_host_license_required"] is True:
            raise ValueError("resume_requires_host_rebind")
        if now_ms >= int(state["lease_expires_at_ms"]):
            raise ValueError("resume_requires_valid_lease")
        if state["lease_cycles_remaining"] < 1:
            raise ValueError("resume_requires_cycle_quota")
        if state["lease_cost_remaining"] < int(state["contract"]["max_cycle_cost"]):
            raise ValueError("resume_requires_cost_quota")
        state["mode"] = "ACTIVE"
    elif normalized == "terminate":
        state["mode"] = "TERMINATED"
    elif normalized == "handover":
        require_string(state.get("latest_checkpoint_digest"), "latest_checkpoint_digest")
        state["mode"] = "HANDED_OVER"
    elif normalized == "request_renewal":
        state["mode"] = "RENEWAL_REQUIRED"
    elif normalized == "renew":
        if mode != "RENEWAL_REQUIRED":
            raise ValueError("renew_requires_renewal_mode")
        payload = command.get("payload")
        if not isinstance(payload, Mapping):
            raise ValueError("renew_payload_required")
        new_cycles = require_positive_int(
            payload.get("lease_cycles"), "lease_cycles"
        )
        new_cost = require_positive_int(payload.get("lease_cost"), "lease_cost")
        new_expiry = require_positive_int(
            payload.get("lease_expires_at_ms"), "lease_expires_at_ms"
        )
        if new_cycles > int(state["contract"]["max_lease_cycles"]):
            raise ValueError("renew_cycles_above_contract_cap")
        if new_cost > int(state["contract"]["max_lease_cost"]):
            raise ValueError("renew_cost_above_contract_cap")
        if new_expiry <= now_ms:
            raise ValueError("renew_expiry_invalid")
        require_string(payload.get("renewal_receipt_digest"), "renewal_receipt_digest")
        state["lease_sequence"] += 1
        state["lease_id"] = require_string(payload.get("lease_id"), "lease_id")
        state["lease_cycles_remaining"] = new_cycles
        state["lease_cost_remaining"] = new_cost
        state["lease_expires_at_ms"] = new_expiry
        state["mode"] = "PAUSED"
    state["mode_reason_digest"] = command["reason_digest"]


def _apply_recovery(state: dict[str, Any], receipt: Mapping[str, Any]) -> None:
    if receipt.get("version") != RECOVERY_VERSION:
        raise ValueError("recovery_version_invalid")
    if receipt.get("source_state_digest") != state[
        "integrated_operation_state_digest"
    ]:
        raise ValueError("recovery_state_stale")
    if receipt.get("integrated_recovery_receipt_digest") != recovery_digest(receipt):
        raise ValueError("recovery_digest_invalid")
    if receipt.get("ledger_replay_verified") is not True:
        raise ValueError("recovery_ledger_replay_required")
    if receipt.get("checkpoint_verified") is not True:
        raise ValueError("recovery_checkpoint_mismatch")
    kind = receipt.get("recovery_kind")
    if kind == "process_restart":
        state["process_epoch"] += 1
        if state["mode"] not in {"TERMINATED", "HANDED_OVER"}:
            state["mode"] = "PAUSED"
    elif kind == "host_restart":
        state["host_epoch"] += 1
        state["fresh_host_license_required"] = True
        if state["mode"] not in {"TERMINATED", "HANDED_OVER"}:
            state["mode"] = "PAUSED"
    elif kind == "host_rebind":
        if state["fresh_host_license_required"] is not True:
            raise ValueError("host_rebind_not_required")
        state["host_license_digest"] = require_string(
            receipt.get("new_host_license_digest"), "new_host_license_digest"
        )
        state["fresh_host_license_required"] = False
        state["mode"] = "PAUSED"
    else:
        raise ValueError("recovery_kind_invalid")
    state["mode_reason_digest"] = receipt["integrated_recovery_receipt_digest"]


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
        "integrated_operation_event_digest": event_id,
        "predecessor_state_digest": predecessor,
        "result_state_digest": state["integrated_operation_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "integrated_operation_apply_result_digest": "",
    }
    packet["integrated_operation_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_state(state)
    if state_errors:
        raise ValueError("state_invalid:" + ";".join(state_errors))
    event_id = str(event.get("integrated_operation_event_digest", ""))
    predecessor = state["integrated_operation_state_digest"]
    if event_id in set(state["processed_event_digests"]):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("integrated_event_version_invalid")
    if event.get("mission_id") != state.get("mission_id"):
        errors.append("integrated_event_mission_mismatch")
    if event.get("expected_state_digest") != predecessor:
        errors.append("integrated_event_state_stale")
    if event.get("event_index") != int(state["event_index"]) + 1:
        errors.append("integrated_event_index_invalid")
    if int(event.get("created_at_ms", -1)) < int(state["updated_at_ms"]):
        errors.append("integrated_event_time_regression")
    if event.get("event_kind") not in {"cycle", "control", "recovery"}:
        errors.append("integrated_event_kind_invalid")
    if event.get("integrated_operation_event_digest") != event_digest(event):
        errors.append("integrated_event_digest_invalid")
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=["integrated_event_payload_invalid"],
        )
    next_state = deepcopy(dict(state))
    try:
        if event["event_kind"] == "cycle":
            _apply_cycle(next_state, payload)
        elif event["event_kind"] == "control":
            _apply_control(next_state, payload, int(event["created_at_ms"]))
        else:
            _apply_recovery(next_state, payload)
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_index"] += 1
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": next_state["event_index"],
            "event_kind": event["event_kind"],
            "event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
            "mode": next_state["mode"],
            "completed_cycles": next_state["completed_cycles"],
        }
    ]
    next_state["integrated_operation_state_digest"] = ""
    next_state["integrated_operation_state_digest"] = state_digest(next_state)
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
    "build_control_event",
    "build_cycle_receipt",
    "build_event",
    "build_initial_state",
    "build_integrated_operation_contract",
    "build_recovery_receipt",
    "validate_contract",
    "validate_cycle_receipt",
    "validate_state",
]
