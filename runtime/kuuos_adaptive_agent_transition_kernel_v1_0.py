from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_adaptive_agent_reference_types_v1_0 import (
    AUTHORITY_MODES,
    CONTROL_MODES,
    EVENT_KINDS,
    EVENT_VERSION,
    GLOBAL_BOUNDARY,
    MODULE_STATUSES,
    NON_AUTHORITY,
    RECOVERY_CONTRACTS,
    RECOVERY_DECISIONS,
    STATE_VERSION,
    TASK_STAGES,
    copy_global_boundary,
    copy_non_authority,
    event_digest,
    require_int,
    require_string,
    state_digest,
)


def build_initial_adaptive_state(
    *,
    owner_id: str,
    lineage_id: str,
    runtime_megamodel_digest: str,
) -> dict[str, Any]:
    state = {
        "version": STATE_VERSION,
        "sequence": 0,
        "task_stage": "BELIEF",
        "control_mode": "ACTIVE",
        "authority_mode": "UNBOUND",
        "module_status": "IDLE",
        "owner_id": require_string(owner_id, "owner_id"),
        "epoch_index": 0,
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "pre_recovery_lineage_id": "",
        "active_session_digest": "",
        "terminal_session_digests": [],
        "plan_digest": "",
        "authority_receipt_digest": "",
        "evidence_digest": "",
        "verification_digest": "",
        "observation_committed": False,
        "verification_committed": False,
        "recovery_decision": "CONTINUE",
        "requires_new_activation": False,
        "requires_new_session": False,
        "execution_allowed": False,
        "runtime_megamodel_digest": require_string(
            runtime_megamodel_digest, "runtime_megamodel_digest"
        ),
        "non_authority": copy_non_authority(),
        "global_boundary": copy_global_boundary(),
        "adaptive_control_state_digest": "",
    }
    state["adaptive_control_state_digest"] = state_digest(state)
    errors = validate_adaptive_state(state)
    if errors:
        raise ValueError("initial_adaptive_state_invalid:" + ";".join(errors))
    return state


def build_adaptive_event(
    *,
    kind: str,
    event_index: int,
    payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if kind not in EVENT_KINDS:
        raise ValueError("adaptive_event_kind_invalid")
    event = {
        "version": EVENT_VERSION,
        "kind": kind,
        "event_index": require_int(event_index, "event_index", minimum=1),
        "payload": deepcopy(dict(payload or {})),
        "adaptive_event_digest": "",
    }
    event["adaptive_event_digest"] = event_digest(event)
    errors = validate_adaptive_event(event)
    if errors:
        raise ValueError("adaptive_event_invalid:" + ";".join(errors))
    return event


def validate_adaptive_event(event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if event.get("version") != EVENT_VERSION:
            errors.append("adaptive_event_version_invalid")
        if event.get("kind") not in EVENT_KINDS:
            errors.append("adaptive_event_kind_invalid")
        require_int(event.get("event_index"), "event_index", minimum=1)
        if not isinstance(event.get("payload"), dict):
            errors.append("adaptive_event_payload_invalid")
        if event.get("adaptive_event_digest") != event_digest(event):
            errors.append("adaptive_event_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_adaptive_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("adaptive_state_version_invalid")
        require_int(state.get("sequence"), "sequence")
        if state.get("task_stage") not in TASK_STAGES:
            errors.append("adaptive_state_stage_invalid")
        if state.get("control_mode") not in CONTROL_MODES:
            errors.append("adaptive_state_control_mode_invalid")
        if state.get("authority_mode") not in AUTHORITY_MODES:
            errors.append("adaptive_state_authority_mode_invalid")
        if state.get("module_status") not in MODULE_STATUSES:
            errors.append("adaptive_state_module_status_invalid")
        require_string(state.get("owner_id"), "owner_id")
        require_int(state.get("epoch_index"), "epoch_index")
        require_string(state.get("lineage_id"), "lineage_id")
        require_string(
            state.get("runtime_megamodel_digest"),
            "runtime_megamodel_digest",
        )
        active_session = state.get("active_session_digest")
        if not isinstance(active_session, str):
            errors.append("adaptive_state_active_session_invalid")
        terminal_sessions = list(state.get("terminal_session_digests", []))
        if len(terminal_sessions) != len(set(terminal_sessions)):
            errors.append("adaptive_state_terminal_session_duplicate")
        if active_session and active_session in terminal_sessions:
            errors.append("adaptive_state_terminal_session_reactivated")
        if state.get("verification_committed") is True and state.get(
            "observation_committed"
        ) is not True:
            errors.append("adaptive_state_verification_without_observation")
        if state.get("execution_allowed") is True:
            if state.get("task_stage") != "ACT":
                errors.append("adaptive_state_execution_stage_invalid")
            if state.get("control_mode") != "ACTIVE":
                errors.append("adaptive_state_execution_control_invalid")
            if state.get("authority_mode") != "LEASED":
                errors.append("adaptive_state_execution_authority_invalid")
            if not active_session:
                errors.append("adaptive_state_execution_session_missing")
            if state.get("module_status") != "RUNNING":
                errors.append("adaptive_state_execution_module_invalid")
        if state.get("control_mode") in {
            "SUSPENDED",
            "RECOVERING",
            "TERMINATED",
        } and state.get("execution_allowed") is not False:
            errors.append("adaptive_state_inactive_mode_execution_invalid")
        if state.get("requires_new_session") is True and active_session:
            errors.append("adaptive_state_new_session_required_but_active")
        if state.get("control_mode") == "TERMINATED":
            if state.get("task_stage") != "TERMINAL":
                errors.append("adaptive_state_terminal_stage_invalid")
            if active_session:
                errors.append("adaptive_state_terminal_session_active")
        if state.get("recovery_decision") not in RECOVERY_DECISIONS:
            errors.append("adaptive_state_recovery_decision_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("adaptive_state_non_authority_invalid")
        if dict(state.get("global_boundary", {})) != GLOBAL_BOUNDARY:
            errors.append("adaptive_state_global_boundary_invalid")
        if state.get("adaptive_control_state_digest") != state_digest(state):
            errors.append("adaptive_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _terminalize_active_session(state: dict[str, Any]) -> None:
    active = state.get("active_session_digest", "")
    if active and active not in state["terminal_session_digests"]:
        state["terminal_session_digests"].append(active)
    state["active_session_digest"] = ""


def _recovery_authority_mode(decision: str) -> str:
    return {
        "RENEW": "RENEWAL_REVIEW",
        "ESCALATE": "ESCALATION",
        "REROTATE": "REROTATION",
    }.get(decision, "BOUND")


def apply_adaptive_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_adaptive_state(state)
    if state_errors:
        raise ValueError("adaptive_source_state_invalid:" + ";".join(state_errors))
    event_errors = validate_adaptive_event(event)
    if event_errors:
        raise ValueError("adaptive_event_invalid:" + ";".join(event_errors))
    if event.get("event_index") != int(state["sequence"]) + 1:
        raise ValueError("adaptive_event_index_mismatch")

    kind = str(event["kind"])
    payload = dict(event.get("payload", {}))
    next_state = deepcopy(dict(state))
    next_state["sequence"] = int(state["sequence"]) + 1
    next_state["adaptive_control_state_digest"] = ""

    if kind == "DECISION_COMMITTED":
        if state.get("task_stage") != "BELIEF" or state.get("control_mode") != "ACTIVE":
            raise ValueError("decision_transition_invalid")
        next_state["task_stage"] = "DECISION"
        next_state["module_status"] = "SUCCEEDED"

    elif kind == "PLAN_BOUND":
        if state.get("task_stage") not in {"DECISION", "LEARN"}:
            raise ValueError("plan_transition_invalid")
        next_state["task_stage"] = "PLAN"
        next_state["plan_digest"] = require_string(
            payload.get("plan_digest"), "plan_digest"
        )
        next_state["module_status"] = "SUCCEEDED"
        next_state["observation_committed"] = False
        next_state["verification_committed"] = False
        next_state["evidence_digest"] = ""
        next_state["verification_digest"] = ""

    elif kind == "AUTHORITY_BOUND":
        if state.get("task_stage") != "PLAN" or state.get("control_mode") != "ACTIVE":
            raise ValueError("authority_transition_invalid")
        next_state["authority_mode"] = "BOUND"
        next_state["authority_receipt_digest"] = require_string(
            payload.get("authority_receipt_digest"),
            "authority_receipt_digest",
        )

    elif kind == "LEASE_ACTIVATED":
        if state.get("task_stage") != "PLAN" or state.get("authority_mode") != "BOUND":
            raise ValueError("lease_transition_invalid")
        next_state["authority_mode"] = "LEASED"
        next_state["requires_new_activation"] = False

    elif kind == "SESSION_BOOTSTRAPPED":
        if state.get("task_stage") != "PLAN" or state.get("authority_mode") != "LEASED":
            raise ValueError("session_transition_invalid")
        session_digest = require_string(
            payload.get("session_digest"), "session_digest"
        )
        if session_digest in state.get("terminal_session_digests", []):
            raise ValueError("terminal_session_reactivation_forbidden")
        next_state["active_session_digest"] = session_digest
        next_state["requires_new_session"] = False
        next_state["module_status"] = "IDLE"

    elif kind == "ACT_AUTHORIZED":
        if (
            state.get("task_stage") != "PLAN"
            or state.get("authority_mode") != "LEASED"
            or state.get("control_mode") != "ACTIVE"
            or not state.get("active_session_digest")
        ):
            raise ValueError("act_transition_invalid")
        next_state["task_stage"] = "ACT"
        next_state["module_status"] = "RUNNING"
        next_state["execution_allowed"] = True

    elif kind == "EFFECT_RECORDED":
        if state.get("task_stage") != "ACT" or state.get("execution_allowed") is not True:
            raise ValueError("effect_transition_invalid")
        next_state["task_stage"] = "OBSERVE"
        next_state["module_status"] = "SUCCEEDED"
        next_state["execution_allowed"] = False

    elif kind == "OBSERVATION_COMMITTED":
        if state.get("task_stage") != "OBSERVE":
            raise ValueError("observation_transition_invalid")
        next_state["task_stage"] = "VERIFY"
        next_state["evidence_digest"] = require_string(
            payload.get("evidence_digest"), "evidence_digest"
        )
        next_state["observation_committed"] = True
        next_state["verification_committed"] = False
        next_state["verification_digest"] = ""

    elif kind in {"VERIFICATION_PASSED", "VERIFICATION_FAILED"}:
        if state.get("task_stage") != "VERIFY" or state.get(
            "observation_committed"
        ) is not True:
            raise ValueError("verification_transition_invalid")
        next_state["verification_digest"] = require_string(
            payload.get("verification_digest"), "verification_digest"
        )
        next_state["verification_committed"] = True
        if kind == "VERIFICATION_PASSED":
            next_state["task_stage"] = "LEARN"
            next_state["module_status"] = "SUCCEEDED"
        else:
            decision = str(payload.get("recovery_decision", "REVALIDATE"))
            if decision not in RECOVERY_DECISIONS or decision == "CONTINUE":
                raise ValueError("verification_failure_recovery_invalid")
            next_state["control_mode"] = "SUSPENDED"
            next_state["module_status"] = "FAILED"
            next_state["recovery_decision"] = decision
            next_state["execution_allowed"] = False
            _terminalize_active_session(next_state)

    elif kind == "LEARNING_COMMITTED":
        if state.get("task_stage") != "LEARN" or state.get(
            "verification_committed"
        ) is not True:
            raise ValueError("learning_transition_invalid")
        next_state["task_stage"] = "PLAN"
        next_state["plan_digest"] = require_string(
            payload.get("next_plan_digest"), "next_plan_digest"
        )
        next_state["module_status"] = "SUCCEEDED"
        next_state["evidence_digest"] = ""
        next_state["verification_digest"] = ""
        next_state["observation_committed"] = False
        next_state["verification_committed"] = False

    elif kind == "LEASE_ANOMALY":
        if state.get("control_mode") != "ACTIVE" or not state.get(
            "active_session_digest"
        ):
            raise ValueError("lease_anomaly_transition_invalid")
        decision = require_string(
            payload.get("recovery_decision"), "recovery_decision"
        )
        if decision not in RECOVERY_DECISIONS or decision == "CONTINUE":
            raise ValueError("lease_anomaly_recovery_invalid")
        next_state["control_mode"] = "SUSPENDED"
        next_state["module_status"] = "SUSPENDED"
        next_state["recovery_decision"] = decision
        next_state["execution_allowed"] = False
        _terminalize_active_session(next_state)

    elif kind == "RECOVERY_ROUTED":
        if state.get("control_mode") != "SUSPENDED":
            raise ValueError("recovery_route_transition_invalid")
        decision = require_string(
            payload.get("recovery_decision"), "recovery_decision"
        )
        if decision != state.get("recovery_decision"):
            raise ValueError("recovery_decision_mismatch")
        contract = RECOVERY_CONTRACTS[decision]
        if contract["requires_authority_receipt"]:
            next_state["authority_receipt_digest"] = require_string(
                payload.get("authority_receipt_digest"),
                "authority_receipt_digest",
            )
        if decision == "ABORT":
            next_state["task_stage"] = "TERMINAL"
            next_state["control_mode"] = "TERMINATED"
            next_state["module_status"] = "FAILED"
            next_state["authority_mode"] = "UNBOUND"
        else:
            next_state["control_mode"] = "RECOVERING"
            next_state["module_status"] = "BLOCKED"
            next_state["authority_mode"] = _recovery_authority_mode(decision)
            next_state["pre_recovery_lineage_id"] = state["lineage_id"]
            next_state["requires_new_activation"] = True
            next_state["requires_new_session"] = True
        next_state["execution_allowed"] = False

    elif kind == "RECOVERY_COMPLETED":
        if state.get("control_mode") != "RECOVERING":
            raise ValueError("recovery_completion_transition_invalid")
        decision = str(state.get("recovery_decision"))
        if decision == "ABORT":
            raise ValueError("aborted_recovery_cannot_complete")
        new_lineage = require_string(
            payload.get("new_lineage_id"), "new_lineage_id"
        )
        if new_lineage == state.get("pre_recovery_lineage_id") or new_lineage == state.get(
            "lineage_id"
        ):
            raise ValueError("fresh_recovery_lineage_required")
        next_state["lineage_id"] = new_lineage
        next_state["task_stage"] = "PLAN"
        next_state["control_mode"] = "ACTIVE"
        next_state["module_status"] = "IDLE"
        next_state["active_session_digest"] = ""
        next_state["requires_new_activation"] = True
        next_state["requires_new_session"] = True
        next_state["execution_allowed"] = False
        if decision == "REROTATE":
            new_epoch = require_int(
                payload.get("new_epoch_index"), "new_epoch_index", minimum=1
            )
            if new_epoch != int(state["epoch_index"]) + 1:
                raise ValueError("rerotation_epoch_successor_required")
            next_state["epoch_index"] = new_epoch
            next_state["authority_mode"] = "BOUND"
        else:
            result_mode = str(payload.get("authority_mode", "BOUND"))
            if result_mode not in {"BOUND", "LEASED"}:
                raise ValueError("recovery_authority_mode_invalid")
            next_state["authority_mode"] = result_mode

    elif kind == "ABORTED":
        _terminalize_active_session(next_state)
        next_state["task_stage"] = "TERMINAL"
        next_state["control_mode"] = "TERMINATED"
        next_state["module_status"] = "FAILED"
        next_state["authority_mode"] = "UNBOUND"
        next_state["recovery_decision"] = "ABORT"
        next_state["execution_allowed"] = False
        next_state["requires_new_activation"] = False
        next_state["requires_new_session"] = False

    else:
        raise ValueError("adaptive_event_unhandled")

    next_state["adaptive_control_state_digest"] = state_digest(next_state)
    next_errors = validate_adaptive_state(next_state)
    if next_errors:
        raise ValueError("adaptive_next_state_invalid:" + ";".join(next_errors))
    return next_state
