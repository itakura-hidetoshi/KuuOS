from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_mission_contract_types_v0_20 import (
    APPLY_RESULT_VERSION,
    DECISION_CLASSES,
    DECISION_VERSION,
    MISSION_STATES,
    NON_AUTHORITY_FLAGS,
    TERMINAL_STATES,
    _require_nonnegative_int,
    apply_result_digest,
    build_mission_contract,
    decision_digest,
    state_digest,
    validate_mission_contract,
    validate_resource_envelope,
)
from runtime.kuuos_mission_state_v0_20 import (
    build_initial_mission_state,
    validate_mission_command,
    validate_mission_evidence,
    validate_mission_state,
)


def _evidence_authorized(
    evidence: Mapping[str, Any], contract: Mapping[str, Any], role_field: str
) -> bool:
    policy = contract["evidence_policy"]
    return (
        evidence.get("evidence_level") in set(policy["authorized_evidence_levels"])
        and evidence.get("source_role") in set(policy[role_field])
        and float(evidence.get("confidence", 0.0))
        >= float(policy["minimum_confidence"])
    )


def evaluate_mission_lifecycle(
    *,
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
    now_ms: int,
    evidence: Mapping[str, Any] | None = None,
    command: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    errors = validate_mission_state(state, contract)
    if errors:
        raise ValueError(";".join(errors))
    now = _require_nonnegative_int(now_ms, "now_ms")
    if evidence is not None:
        evidence_errors = validate_mission_evidence(evidence, contract, state)
        if evidence_errors:
            raise ValueError(";".join(evidence_errors))
    if command is not None:
        command_errors = validate_mission_command(command, contract, state)
        if command_errors:
            raise ValueError(";".join(command_errors))
    current = str(state["lifecycle_state"])
    decision = "no_change"
    next_state = current
    reason = "mission_state_unchanged"

    if current in TERMINAL_STATES:
        reason = "mission_terminal"
    elif command is not None and command["command"] in {
        "terminate",
        "handover",
        "pause",
        "request_renewal",
    }:
        command_name = command["command"]
        mapping = {
            "terminate": ("terminate", "terminated"),
            "handover": ("handover", "handed_over"),
            "pause": ("pause", "paused"),
            "request_renewal": ("renewal_required", "renewal_required"),
        }
        decision, next_state = mapping[command_name]
        reason = f"explicit_command:{command_name}"
    elif evidence is not None and (
        evidence.get("invariant_breach")
        or evidence.get("prohibited_outcome_observed")
    ):
        if _evidence_authorized(evidence, contract, "invariant_roles"):
            decision = "terminate"
            next_state = "terminated"
            reason = "authorized_invariant_or_prohibited_outcome_evidence"
        else:
            decision = "pause"
            next_state = "paused"
            reason = "unconfirmed_invariant_or_prohibited_outcome_evidence"
    elif evidence is not None and evidence.get("failure_verified"):
        if _evidence_authorized(evidence, contract, "failure_roles"):
            if evidence.get("nonrecoverable"):
                decision, next_state = "terminate", "terminated"
                reason = "authorized_nonrecoverable_failure"
            else:
                decision, next_state = "handover", "handed_over"
                reason = "authorized_failure_handover"
        else:
            decision, next_state = "pause", "paused"
            reason = "failure_evidence_not_authorized"
    elif evidence is not None and evidence.get("success_verified"):
        if _evidence_authorized(evidence, contract, "completion_roles"):
            decision, next_state = "complete", "completed"
            reason = "authorized_success_evidence"
        else:
            decision, next_state = "pause", "paused"
            reason = "success_evidence_not_authorized"
    else:
        envelope = contract["resource_envelope"]
        usable_cost_limit = float(envelope["max_total_cost"]) - float(
            envelope["reserve_floor"]
        )
        if float(state["used_cost"]) >= usable_cost_limit:
            decision, next_state = "pause", "paused"
            reason = "resource_reserve_floor_reached"
        elif int(state["completed_cycles"]) >= int(
            envelope["max_cycles_before_renewal"]
        ):
            decision, next_state = "renewal_required", "renewal_required"
            reason = "cycle_renewal_boundary_reached"
        elif now >= int(contract["expires_at_ms"]):
            decision, next_state = "renewal_required", "renewal_required"
            reason = "mission_contract_expired"
        elif command is not None and command["command"] == "resume":
            if current != "paused":
                decision, next_state = "no_change", current
                reason = "resume_requires_paused_state"
            else:
                decision, next_state = "resume", "active"
                reason = "explicit_command:resume"
        elif current == "proposed" and now >= int(contract["valid_from_ms"]):
            decision, next_state = "continue", "active"
            reason = "mission_validity_started"
        elif current == "paused":
            decision, next_state = "no_change", "paused"
            reason = "mission_paused"
        elif current == "renewal_required":
            decision, next_state = "no_change", "renewal_required"
            reason = "renewal_authorization_required"
        else:
            decision, next_state = "continue", "active"
            reason = "mission_within_contract_bounds"

    packet = {
        "version": DECISION_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_state_digest": state["mission_state_digest"],
        "evaluated_at_ms": now,
        "decision": decision,
        "current_state": current,
        "next_state": next_state,
        "reason": reason,
        "command_digest": command.get("mission_command_digest", "")
        if command
        else "",
        "evidence_digest": evidence.get("mission_evidence_digest", "")
        if evidence
        else "",
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "mission_decision_digest": "",
    }
    packet["mission_decision_digest"] = decision_digest(packet)
    return packet


def validate_mission_decision(
    decision: Mapping[str, Any],
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
) -> list[str]:
    errors = validate_mission_state(state, contract)
    if errors:
        return ["state:" + item for item in errors]
    if decision.get("version") != DECISION_VERSION:
        errors.append("decision_version_invalid")
    if decision.get("mission_id") != contract.get("mission_id"):
        errors.append("decision_mission_mismatch")
    if decision.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("decision_contract_digest_mismatch")
    if decision.get("source_state_digest") != state.get("mission_state_digest"):
        errors.append("decision_source_state_stale")
    if decision.get("decision") not in DECISION_CLASSES:
        errors.append("decision_class_invalid")
    if decision.get("current_state") != state.get("lifecycle_state"):
        errors.append("decision_current_state_mismatch")
    if decision.get("next_state") not in MISSION_STATES:
        errors.append("decision_next_state_invalid")
    if dict(decision.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("decision_non_authority_invalid")
    if decision.get("mission_decision_digest") != decision_digest(decision):
        errors.append("mission_decision_digest_invalid")
    return errors


_ALLOWED_TRANSITIONS = {
    "proposed": {
        "proposed",
        "active",
        "paused",
        "renewal_required",
        "completed",
        "terminated",
        "handed_over",
    },
    "active": {
        "active",
        "paused",
        "renewal_required",
        "completed",
        "terminated",
        "handed_over",
    },
    "paused": {
        "paused",
        "active",
        "renewal_required",
        "completed",
        "terminated",
        "handed_over",
    },
    "renewal_required": {"renewal_required", "terminated", "handed_over"},
    "completed": {"completed"},
    "terminated": {"terminated"},
    "handed_over": {"handed_over"},
}


def apply_mission_decision(
    *,
    contract: Mapping[str, Any],
    state: Mapping[str, Any],
    decision: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_mission_decision(decision, contract, state)
    digest_value = str(decision.get("mission_decision_digest", ""))
    if digest_value in set(
        str(item) for item in state.get("processed_decision_digests", [])
    ):
        replay_result = {
            "version": APPLY_RESULT_VERSION,
            "status": "REPLAYED",
            "mission_id": contract["mission_id"],
            "decision_digest": digest_value,
            "previous_state_digest": state["mission_state_digest"],
            "result_state_digest": state["mission_state_digest"],
            "result_state": deepcopy(dict(state)),
            "apply_result_digest": "",
        }
        replay_result["apply_result_digest"] = apply_result_digest(replay_result)
        return replay_result
    if errors:
        raise ValueError(";".join(errors))
    current = str(state["lifecycle_state"])
    next_state = str(decision["next_state"])
    if next_state not in _ALLOWED_TRANSITIONS[current]:
        raise ValueError("mission_transition_forbidden")
    if decision["decision"] == "no_change" and next_state != current:
        raise ValueError("no_change_transition_invalid")
    result_state = deepcopy(dict(state))
    result_state["lifecycle_state"] = next_state
    result_state["transition_index"] = int(result_state["transition_index"]) + 1
    result_state["processed_decision_digests"] = list(
        result_state["processed_decision_digests"]
    ) + [digest_value]
    result_state["transition_history"] = list(
        result_state["transition_history"]
    ) + [
        {
            "transition_index": int(result_state["transition_index"]),
            "decision_digest": digest_value,
            "from_state": current,
            "to_state": next_state,
            "decision": decision["decision"],
            "reason": decision["reason"],
            "evaluated_at_ms": int(decision["evaluated_at_ms"]),
        }
    ]
    result_state["updated_at_ms"] = int(decision["evaluated_at_ms"])
    result_state["mission_state_digest"] = ""
    result_state["mission_state_digest"] = state_digest(result_state)
    status = "NO_CHANGE" if current == next_state else "APPLIED"
    result = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "mission_id": contract["mission_id"],
        "decision_digest": digest_value,
        "previous_state_digest": state["mission_state_digest"],
        "result_state_digest": result_state["mission_state_digest"],
        "result_state": result_state,
        "apply_result_digest": "",
    }
    result["apply_result_digest"] = apply_result_digest(result)
    return result


def build_successor_mission_contract(
    *,
    parent_contract: Mapping[str, Any],
    parent_state: Mapping[str, Any],
    renewal_command: Mapping[str, Any],
    created_at_ms: int,
    valid_from_ms: int,
    expires_at_ms: int,
    resource_envelope: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    errors = validate_mission_command(
        renewal_command, parent_contract, parent_state
    )
    if errors:
        raise ValueError(";".join(errors))
    if renewal_command.get("command") != "renew":
        raise ValueError("renewal_command_required")
    role = str(renewal_command.get("actor_role", ""))
    renewal_policy = parent_contract["renewal_policy"]
    if role not in set(renewal_policy["authorized_roles"]):
        raise ValueError("renewal_role_not_authorized")
    parent_revision = int(parent_contract["revision"])
    if parent_revision >= int(renewal_policy["max_renewals"]):
        raise ValueError("renewal_limit_reached")
    new_envelope = deepcopy(
        dict(resource_envelope or parent_contract["resource_envelope"])
    )
    new_errors = validate_resource_envelope(new_envelope)
    if new_errors:
        raise ValueError(";".join(new_errors))
    if not renewal_policy.get("allow_resource_increase", False):
        parent_envelope = parent_contract["resource_envelope"]
        for field in (
            "max_total_cost",
            "max_cycle_cost",
            "max_cycles_before_renewal",
            "max_active_goals",
            "max_goal_count",
        ):
            if float(new_envelope[field]) > float(parent_envelope[field]):
                raise ValueError("renewal_resource_increase_forbidden:" + field)
    return build_mission_contract(
        mission_id=str(parent_contract["mission_id"]),
        lineage_id=str(parent_contract["lineage_id"]),
        revision=parent_revision + 1,
        parent_contract_digest=str(parent_contract["mission_contract_digest"]),
        issuer_id=str(renewal_command["actor_id"]),
        issuer_role=role,
        governance_root_digest=str(parent_contract["governance_root_digest"]),
        purpose=str(parent_contract["purpose"]),
        success_criteria=list(parent_contract["success_criteria"]),
        failure_criteria=list(parent_contract["failure_criteria"]),
        invariants=list(parent_contract["invariants"]),
        prohibited_outcomes=list(parent_contract["prohibited_outcomes"]),
        resource_envelope=new_envelope,
        authority_scope=dict(parent_contract["authority_scope"]),
        renewal_policy=dict(parent_contract["renewal_policy"]),
        override_policy=dict(parent_contract["override_policy"]),
        evidence_policy=dict(parent_contract["evidence_policy"]),
        goal_policy=dict(parent_contract["goal_policy"]),
        created_at_ms=created_at_ms,
        valid_from_ms=valid_from_ms,
        expires_at_ms=expires_at_ms,
    )


def build_successor_mission_state(
    *,
    parent_state: Mapping[str, Any],
    successor_contract: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_mission_contract(successor_contract)
    if errors:
        raise ValueError(";".join(errors))
    if successor_contract.get("parent_contract_digest") != parent_state.get(
        "contract_digest"
    ):
        raise ValueError("successor_contract_parent_state_mismatch")
    if successor_contract.get("mission_id") != parent_state.get("mission_id"):
        raise ValueError("successor_mission_mismatch")
    state = build_initial_mission_state(successor_contract, now_ms=now_ms)
    state["predecessor_state_digest"] = str(parent_state["mission_state_digest"])
    state["mission_state_digest"] = ""
    state["mission_state_digest"] = state_digest(state)
    return state
