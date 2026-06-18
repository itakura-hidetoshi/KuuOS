from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_mission_contract_types_v0_20 import (
    COMMAND_VERSION,
    EVIDENCE_LEVELS,
    EVIDENCE_VERSION,
    MISSION_COMMANDS,
    MISSION_STATES,
    NON_AUTHORITY_FLAGS,
    STATE_VERSION,
    _require_finite_number,
    _require_nonempty_string,
    _require_nonnegative_int,
    _require_unique_strings,
    command_digest,
    evidence_digest,
    state_digest,
    validate_mission_contract,
)


def build_initial_mission_state(
    contract: Mapping[str, Any], *, now_ms: int
) -> dict[str, Any]:
    errors = validate_mission_contract(contract)
    if errors:
        raise ValueError(";".join(errors))
    now = _require_nonnegative_int(now_ms, "now_ms")
    lifecycle_state = "proposed" if now < int(contract["valid_from_ms"]) else "active"
    state = {
        "version": STATE_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "contract_revision": int(contract["revision"]),
        "predecessor_state_digest": "",
        "lifecycle_state": lifecycle_state,
        "used_cost": 0.0,
        "completed_cycles": 0,
        "transition_index": 0,
        "processed_decision_digests": [],
        "transition_history": [],
        "updated_at_ms": now,
        "mission_state_digest": "",
    }
    state["mission_state_digest"] = state_digest(state)
    return state


def validate_mission_state(
    state: Mapping[str, Any], contract: Mapping[str, Any]
) -> list[str]:
    errors = validate_mission_contract(contract)
    if errors:
        return ["contract:" + item for item in errors]
    if state.get("version") != STATE_VERSION:
        errors.append("state_version_invalid")
    if state.get("mission_id") != contract.get("mission_id"):
        errors.append("state_mission_mismatch")
    if state.get("lineage_id") != contract.get("lineage_id"):
        errors.append("state_lineage_mismatch")
    if state.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("state_contract_digest_mismatch")
    if int(state.get("contract_revision", -1)) != int(contract.get("revision", -2)):
        errors.append("state_contract_revision_mismatch")
    if state.get("lifecycle_state") not in MISSION_STATES:
        errors.append("state_lifecycle_invalid")
    try:
        used_cost = _require_finite_number(
            state.get("used_cost"), "used_cost", minimum=0.0
        )
        _require_nonnegative_int(state.get("completed_cycles"), "completed_cycles")
        transition_index = _require_nonnegative_int(
            state.get("transition_index"), "transition_index"
        )
        _require_nonnegative_int(state.get("updated_at_ms"), "updated_at_ms")
        if used_cost < 0:
            errors.append("used_cost_negative")
        history = state.get("transition_history")
        processed = state.get("processed_decision_digests")
        if not isinstance(history, list):
            errors.append("transition_history_invalid")
        elif len(history) != transition_index:
            errors.append("transition_index_mismatch")
        if not isinstance(processed, list):
            errors.append("processed_decisions_invalid")
        elif len(processed) != len(set(str(item) for item in processed)):
            errors.append("processed_decisions_duplicate")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    if state.get("mission_state_digest") != state_digest(state):
        errors.append("mission_state_digest_invalid")
    return errors


def record_mission_usage(
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    *,
    cost: float,
    completed_cycles: int = 1,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_mission_state(state, contract)
    if errors:
        raise ValueError(";".join(errors))
    increment_cost = _require_finite_number(cost, "cost", minimum=0.0)
    increment_cycles = _require_nonnegative_int(
        completed_cycles, "completed_cycles"
    )
    result = deepcopy(dict(state))
    result["used_cost"] = float(result["used_cost"]) + increment_cost
    result["completed_cycles"] = int(result["completed_cycles"]) + increment_cycles
    result["updated_at_ms"] = _require_nonnegative_int(now_ms, "now_ms")
    result["mission_state_digest"] = ""
    result["mission_state_digest"] = state_digest(result)
    return result


def build_mission_command(
    *,
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
    actor_id: str,
    actor_role: str,
    command: str,
    reason: str,
    issued_at_ms: int,
    payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    errors = validate_mission_state(state, contract)
    if errors:
        raise ValueError(";".join(errors))
    role = _require_nonempty_string(actor_role, "actor_role")
    command_name = _require_nonempty_string(command, "command")
    if command_name not in MISSION_COMMANDS:
        raise ValueError("mission_command_unknown")
    allowed = contract["override_policy"]["role_commands"].get(role, [])
    if command_name not in allowed:
        raise ValueError("mission_command_role_not_authorized")
    packet = {
        "version": COMMAND_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_state_digest": state["mission_state_digest"],
        "actor_id": _require_nonempty_string(actor_id, "actor_id"),
        "actor_role": role,
        "command": command_name,
        "reason": _require_nonempty_string(reason, "reason"),
        "issued_at_ms": _require_nonnegative_int(issued_at_ms, "issued_at_ms"),
        "payload": deepcopy(dict(payload or {})),
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "mission_command_digest": "",
    }
    packet["mission_command_digest"] = command_digest(packet)
    return packet


def validate_mission_command(
    command: Mapping[str, Any],
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
) -> list[str]:
    errors = validate_mission_state(state, contract)
    if errors:
        return ["state:" + item for item in errors]
    if command.get("version") != COMMAND_VERSION:
        errors.append("command_version_invalid")
    if command.get("mission_id") != contract.get("mission_id"):
        errors.append("command_mission_mismatch")
    if command.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("command_contract_digest_mismatch")
    if command.get("source_state_digest") != state.get("mission_state_digest"):
        errors.append("command_source_state_stale")
    command_name = str(command.get("command", ""))
    if command_name not in MISSION_COMMANDS:
        errors.append("command_unknown")
    role = str(command.get("actor_role", ""))
    if command_name not in contract.get("override_policy", {}).get(
        "role_commands", {}
    ).get(role, []):
        errors.append("command_role_not_authorized")
    if not str(command.get("actor_id", "")).strip():
        errors.append("command_actor_missing")
    if not str(command.get("reason", "")).strip():
        errors.append("command_reason_missing")
    if dict(command.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("command_non_authority_invalid")
    if command.get("mission_command_digest") != command_digest(command):
        errors.append("mission_command_digest_invalid")
    return errors


def build_mission_evidence(
    *,
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
    source_id: str,
    source_role: str,
    evidence_level: str,
    observed_at_ms: int,
    confidence: float,
    success_verified: bool = False,
    failure_verified: bool = False,
    invariant_breach: bool = False,
    prohibited_outcome_observed: bool = False,
    nonrecoverable: bool = False,
    external_handover_required: bool = False,
    evidence_refs: Sequence[str] = (),
) -> dict[str, Any]:
    errors = validate_mission_state(state, contract)
    if errors:
        raise ValueError(";".join(errors))
    level = _require_nonempty_string(evidence_level, "evidence_level")
    if level not in EVIDENCE_LEVELS:
        raise ValueError("evidence_level_invalid")
    confidence_value = _require_finite_number(
        confidence, "confidence", minimum=0.0
    )
    if confidence_value > 1.0:
        raise ValueError("confidence_above_one")
    if success_verified and failure_verified:
        raise ValueError("evidence_success_failure_conflict")
    packet = {
        "version": EVIDENCE_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_state_digest": state["mission_state_digest"],
        "source_id": _require_nonempty_string(source_id, "source_id"),
        "source_role": _require_nonempty_string(source_role, "source_role"),
        "evidence_level": level,
        "observed_at_ms": _require_nonnegative_int(
            observed_at_ms, "observed_at_ms"
        ),
        "confidence": confidence_value,
        "success_verified": bool(success_verified),
        "failure_verified": bool(failure_verified),
        "invariant_breach": bool(invariant_breach),
        "prohibited_outcome_observed": bool(prohibited_outcome_observed),
        "nonrecoverable": bool(nonrecoverable),
        "external_handover_required": bool(external_handover_required),
        "evidence_refs": _require_unique_strings(
            evidence_refs, "evidence_refs", allow_empty=True
        ),
        "mission_evidence_digest": "",
    }
    packet["mission_evidence_digest"] = evidence_digest(packet)
    return packet


def validate_mission_evidence(
    evidence: Mapping[str, Any],
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
) -> list[str]:
    errors = validate_mission_state(state, contract)
    if errors:
        return ["state:" + item for item in errors]
    if evidence.get("version") != EVIDENCE_VERSION:
        errors.append("evidence_version_invalid")
    if evidence.get("mission_id") != contract.get("mission_id"):
        errors.append("evidence_mission_mismatch")
    if evidence.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("evidence_contract_digest_mismatch")
    if evidence.get("source_state_digest") != state.get("mission_state_digest"):
        errors.append("evidence_source_state_stale")
    if evidence.get("evidence_level") not in EVIDENCE_LEVELS:
        errors.append("evidence_level_invalid")
    try:
        confidence = _require_finite_number(
            evidence.get("confidence"), "confidence", minimum=0.0
        )
        if confidence > 1.0:
            errors.append("confidence_above_one")
    except ValueError as exc:
        errors.append(str(exc))
    if evidence.get("success_verified") and evidence.get("failure_verified"):
        errors.append("evidence_success_failure_conflict")
    if not str(evidence.get("source_id", "")).strip() or not str(
        evidence.get("source_role", "")
    ).strip():
        errors.append("evidence_source_missing")
    if evidence.get("mission_evidence_digest") != evidence_digest(evidence):
        errors.append("mission_evidence_digest_invalid")
    return errors
