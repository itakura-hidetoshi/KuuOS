from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_host_adapter_license_v0_17 import validate_host_license
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    BLOCKED as HOST_BLOCKED,
    NON_AUTHORITY_FLAGS as HOST_NON_AUTHORITY,
    PROJECTION_VERSION,
    READY as HOST_READY,
    RECEIPT_VERSION,
    REPLAYED as HOST_REPLAYED,
    TICK_VERSION,
    license_digest,
    projection_digest,
    receipt_digest,
    tick_digest,
)
from runtime.kuuos_cooperative_host_adapter_v0_17 import run_host_tick
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state
from runtime.kuuos_plan_os_types_v0_1 import (
    ACTIVATION_RECEIPT_VERSION as PLAN_ACTIVATION_VERSION,
    plan_activation_receipt_digest,
)
from runtime.kuuos_act_os_types_v0_1 import (
    APPLY_RESULT_VERSION,
    AUTHORIZATION_VERSION,
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    STATE_VERSION,
    apply_result_digest,
    authorization_digest,
    copy_boundary,
    copy_non_authority,
    event_digest,
    next_phase,
    require_bool,
    require_int,
    require_string,
    state_digest,
)


def _selected_step(plan_state: Mapping[str, Any], step_id: str) -> dict[str, Any]:
    for raw in plan_state.get("steps", []):
        if str(raw.get("step_id", "")) == step_id:
            return deepcopy(dict(raw))
    raise ValueError("act_selected_plan_step_not_found")


def build_initial_act_state(
    *,
    act_id: str,
    plan_state: Mapping[str, Any],
    plan_activation_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_plan_state(plan_state)
    if errors:
        raise ValueError("invalid_source_plan_state:" + ";".join(errors))
    if plan_state.get("current_phase") != "commit":
        raise ValueError("source_plan_not_committed")
    if plan_state.get("route") != "PLAN_CANDIDATE":
        raise ValueError("source_plan_not_effect_candidate")
    if plan_activation_receipt.get("version") != PLAN_ACTIVATION_VERSION:
        raise ValueError("plan_activation_version_invalid")
    if plan_activation_receipt.get("plan_activation_receipt_digest") != plan_activation_receipt_digest(
        plan_activation_receipt
    ):
        raise ValueError("plan_activation_digest_invalid")
    bindings = {
        "plan_state_digest": plan_state.get("plan_state_digest"),
        "committed_plan_digest": plan_state.get("latest_committed_plan_digest"),
        "plan_basis_digest": plan_state.get("plan_basis_digest"),
    }
    for field, expected in bindings.items():
        if plan_activation_receipt.get(field) != expected:
            raise ValueError(f"plan_activation_{field}_mismatch")
    if plan_activation_receipt.get("route") != "PLAN_CANDIDATE":
        raise ValueError("plan_activation_route_invalid")
    if plan_activation_receipt.get("mission_cycle_phase") != "plan":
        raise ValueError("plan_activation_phase_invalid")
    if plan_activation_receipt.get("plan_not_execution") is not True:
        raise ValueError("plan_activation_nonexecution_required")
    if plan_activation_receipt.get("host_license_granted") is not False:
        raise ValueError("plan_activation_must_not_grant_license")

    state = {
        "version": STATE_VERSION,
        "act_id": require_string(act_id, "act_id"),
        "lineage_id": require_string(plan_state.get("lineage_id"), "lineage_id"),
        "source_plan_id": require_string(plan_state.get("plan_id"), "source_plan_id"),
        "source_plan_state_digest": require_string(plan_state.get("plan_state_digest"), "source_plan_state_digest"),
        "source_committed_plan_digest": require_string(
            plan_state.get("latest_committed_plan_digest"), "source_committed_plan_digest"
        ),
        "source_plan_basis_digest": require_string(plan_state.get("plan_basis_digest"), "source_plan_basis_digest"),
        "plan_activation_receipt_digest": require_string(
            plan_activation_receipt.get("plan_activation_receipt_digest"),
            "plan_activation_receipt_digest",
        ),
        "source_wa_basis_digest": require_string(plan_state.get("source_wa_basis_digest"), "source_wa_basis_digest"),
        "mission_contract_digest": require_string(plan_state.get("mission_contract_digest"), "mission_contract_digest"),
        "current_phase": "bind",
        "route": "PENDING",
        "event_index": 0,
        "act_version": 0,
        "committed_records": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "predecessor_act_state_digest": "",
        "act_state_digest": "",
        "selected_step": {},
        "selected_step_id": "",
        "selected_step_digest": "",
        "operation_id": "",
        "operation_input_digest": "",
        "step_authorization": {},
        "step_authorization_digest": "",
        "host_license": {},
        "host_license_digest": "",
        "host_projection": {},
        "host_projection_digest": "",
        "host_tick": {},
        "host_tick_digest": "",
        "host_receipt": {},
        "host_receipt_digest": "",
        "host_invocation_digest": "",
        "source_supervisor_bundle_digest": "",
        "result_supervisor_bundle_digest": "",
        "completed_step_ids": [],
        "blockers": [],
        "effect_recorded": False,
        "observation_required": False,
        "verification_required": False,
        "expected_observation_digest": "",
        "verification_criterion_digest": "",
        "automatic_truth_promotion": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "processed_event_digests": [],
        "event_history": [],
        "record_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["act_state_digest"] = state_digest(state)
    return state


def validate_act_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("act_state_version_invalid")
        for field in (
            "act_id",
            "lineage_id",
            "source_plan_id",
            "source_plan_state_digest",
            "source_committed_plan_digest",
            "source_plan_basis_digest",
            "plan_activation_receipt_digest",
            "source_wa_basis_digest",
            "mission_contract_digest",
        ):
            require_string(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("act_state_phase_invalid")
        if state.get("route") not in ROUTES:
            errors.append("act_state_route_invalid")
        for field in ("event_index", "act_version", "committed_records", "updated_at_ms"):
            require_int(state.get(field), field)
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("act_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("act_state_boundary_invalid")
        if state.get("act_state_digest") != state_digest(state):
            errors.append("act_state_digest_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("act_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(state.get("event_index", -1)):
            errors.append("act_event_history_count_mismatch")
        if state.get("effect_recorded") is True:
            if state.get("route") != "EFFECT_RECORDED":
                errors.append("act_effect_route_mismatch")
            if state.get("observation_required") is not True:
                errors.append("act_observation_debt_missing")
            if state.get("verification_required") is not True:
                errors.append("act_verification_debt_missing")
        if state.get("automatic_truth_promotion") is not False:
            errors.append("act_truth_promotion_forbidden")
        if state.get("automatic_plan_completion") is not False:
            errors.append("act_plan_completion_forbidden")
        if state.get("automatic_rollback") is not False:
            errors.append("act_automatic_rollback_forbidden")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_act_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "act_id": require_string(state.get("act_id"), "act_id"),
        "lineage_id": require_string(state.get("lineage_id"), "lineage_id"),
        "expected_act_state_digest": require_string(state.get("act_state_digest"), "expected_act_state_digest"),
        "source_phase": require_string(state.get("current_phase"), "source_phase"),
        "target_phase": require_string(target_phase, "target_phase"),
        "event_index": require_int(state.get("event_index"), "event_index") + 1,
        "artifact_digest": require_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "act_event_digest": "",
    }
    event["act_event_digest"] = event_digest(event)
    return event


def build_step_authorization(
    *,
    state: Mapping[str, Any],
    authorization_id: str,
    operation_id: str,
    operation_input_digest: str,
    act_phase_receipt_digest: str,
    invocation_id: str,
    source_supervisor_bundle_digest: str,
    host_job_id: str,
    host_step_id: str,
    host_license: Mapping[str, Any],
    human_approval_receipt_digest: str = "",
    human_approver_id: str = "",
    issued_at_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "select":
        raise ValueError("act_authorization_requires_selected_step")
    selected = dict(state.get("selected_step", {}))
    if not selected:
        raise ValueError("act_selected_step_missing")
    issued = require_int(issued_at_ms, "issued_at_ms")
    expires = require_int(expires_at_ms, "expires_at_ms")
    if expires <= issued:
        raise ValueError("act_authorization_expiry_invalid")
    if selected.get("requires_human_review") is True:
        require_string(human_approval_receipt_digest, "human_approval_receipt_digest")
        require_string(human_approver_id, "human_approver_id")
    packet = {
        "version": AUTHORIZATION_VERSION,
        "authorization_id": require_string(authorization_id, "authorization_id"),
        "act_id": state["act_id"],
        "source_plan_state_digest": state["source_plan_state_digest"],
        "source_committed_plan_digest": state["source_committed_plan_digest"],
        "source_plan_basis_digest": state["source_plan_basis_digest"],
        "plan_activation_receipt_digest": state["plan_activation_receipt_digest"],
        "selected_step_id": state["selected_step_id"],
        "selected_step_digest": state["selected_step_digest"],
        "operation_id": require_string(operation_id, "operation_id"),
        "operation_input_digest": require_string(operation_input_digest, "operation_input_digest"),
        "act_phase_receipt_digest": require_string(act_phase_receipt_digest, "act_phase_receipt_digest"),
        "invocation_id": require_string(invocation_id, "invocation_id"),
        "source_supervisor_bundle_digest": require_string(
            source_supervisor_bundle_digest, "source_supervisor_bundle_digest"
        ),
        "host_job_id": require_string(host_job_id, "host_job_id"),
        "host_step_id": require_string(host_step_id, "host_step_id"),
        "host_license_digest": require_string(host_license.get("host_license_digest"), "host_license_digest"),
        "human_approval_receipt_digest": str(human_approval_receipt_digest),
        "human_approver_id": str(human_approver_id),
        "issued_at_ms": issued,
        "expires_at_ms": expires,
        "single_use": True,
        "authorization_does_not_widen_license": True,
        "non_authority": copy_non_authority(),
        "step_authorization_digest": "",
    }
    packet["step_authorization_digest"] = authorization_digest(packet)
    return packet


def _validate_event_base(state: Mapping[str, Any], event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("act_event_version_invalid")
    if event.get("act_id") != state.get("act_id"):
        errors.append("act_event_id_mismatch")
    if event.get("lineage_id") != state.get("lineage_id"):
        errors.append("act_event_lineage_mismatch")
    if event.get("act_event_digest") != event_digest(event):
        errors.append("act_event_digest_invalid")
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("act_event_authority_escalation")
    source = str(event.get("source_phase", ""))
    if source != state.get("current_phase"):
        errors.append("act_event_source_phase_stale")
    if event.get("target_phase") != next_phase(source):
        errors.append("act_event_phase_order_invalid")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("act_event_index_invalid")
    if event.get("expected_act_state_digest") != state.get("act_state_digest"):
        errors.append("act_event_state_digest_stale")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("act_event_time_regression")
    return errors


def _validate_authorization(
    state: Mapping[str, Any], authorization: Mapping[str, Any], host_license: Mapping[str, Any], now_ms: int
) -> None:
    if authorization.get("version") != AUTHORIZATION_VERSION:
        raise ValueError("step_authorization_version_invalid")
    if authorization.get("step_authorization_digest") != authorization_digest(authorization):
        raise ValueError("step_authorization_digest_invalid")
    bindings = {
        "act_id": state["act_id"],
        "source_plan_state_digest": state["source_plan_state_digest"],
        "source_committed_plan_digest": state["source_committed_plan_digest"],
        "source_plan_basis_digest": state["source_plan_basis_digest"],
        "plan_activation_receipt_digest": state["plan_activation_receipt_digest"],
        "selected_step_id": state["selected_step_id"],
        "selected_step_digest": state["selected_step_digest"],
        "operation_id": state["operation_id"],
        "operation_input_digest": state["operation_input_digest"],
    }
    for field, expected in bindings.items():
        if authorization.get(field) != expected:
            raise ValueError(f"step_authorization_{field}_mismatch")
    if authorization.get("single_use") is not True:
        raise ValueError("step_authorization_single_use_required")
    if authorization.get("authorization_does_not_widen_license") is not True:
        raise ValueError("step_authorization_license_widening_forbidden")
    now = require_int(now_ms, "now_ms")
    if int(authorization.get("issued_at_ms", -1)) > now:
        raise ValueError("step_authorization_not_yet_valid")
    if int(authorization.get("expires_at_ms", 0)) <= now:
        raise ValueError("step_authorization_expired")
    if state["selected_step"].get("requires_human_review") is True:
        require_string(authorization.get("human_approval_receipt_digest"), "human_approval_receipt_digest")
        require_string(authorization.get("human_approver_id"), "human_approver_id")
    license_errors = validate_host_license(host_license, now_ms=now)
    if license_errors:
        raise ValueError(";".join(license_errors))
    if authorization.get("host_license_digest") != host_license.get("host_license_digest"):
        raise ValueError("step_authorization_host_license_mismatch")
    if host_license.get("host_license_digest") != license_digest(host_license):
        raise ValueError("host_license_digest_invalid")
    if state["operation_id"] not in {str(item) for item in host_license.get("operation_allowlist", [])}:
        raise ValueError("act_operation_not_host_licensed")


def _apply_payload(state: dict[str, Any], phase: str, payload: Mapping[str, Any], now_ms: int) -> None:
    if phase == "select":
        step_id = require_string(payload.get("selected_step_id"), "selected_step_id")
        plan_state = payload.get("plan_state")
        if not isinstance(plan_state, Mapping):
            raise ValueError("source_plan_state_required")
        if plan_state.get("plan_state_digest") != state["source_plan_state_digest"]:
            raise ValueError("source_plan_state_digest_mismatch")
        step = _selected_step(plan_state, step_id)
        if step.get("step_class") != "act_candidate" or step.get("effectful") is not True:
            raise ValueError("selected_step_not_effectful_act_candidate")
        if not step.get("stop_condition_digests"):
            raise ValueError("selected_step_stop_conditions_missing")
        state["selected_step"] = step
        state["selected_step_id"] = step_id
        state["selected_step_digest"] = require_string(step.get("step_digest"), "selected_step_digest")
        state["operation_id"] = require_string(payload.get("operation_id"), "operation_id")
        state["operation_input_digest"] = require_string(
            payload.get("operation_input_digest"), "operation_input_digest"
        )
        state["expected_observation_digest"] = require_string(
            step.get("expected_observation_digest"), "expected_observation_digest"
        )
        state["verification_criterion_digest"] = require_string(
            step.get("verification_criterion_digest"), "verification_criterion_digest"
        )
        return

    if phase == "authorize":
        authorization = payload.get("step_authorization")
        host_license = payload.get("host_license")
        if not isinstance(authorization, Mapping) or not isinstance(host_license, Mapping):
            raise ValueError("authorization_and_host_license_required")
        _validate_authorization(state, authorization, host_license, now_ms)
        state["step_authorization"] = deepcopy(dict(authorization))
        state["step_authorization_digest"] = authorization["step_authorization_digest"]
        state["host_license"] = deepcopy(dict(host_license))
        state["host_license_digest"] = host_license["host_license_digest"]
        state["source_supervisor_bundle_digest"] = authorization[
            "source_supervisor_bundle_digest"
        ]
        return

    if phase == "project":
        projection = payload.get("host_projection")
        if not isinstance(projection, Mapping):
            raise ValueError("host_projection_required")
        if projection.get("version") != PROJECTION_VERSION:
            raise ValueError("host_projection_version_invalid")
        if projection.get("projection_digest") != projection_digest(projection):
            raise ValueError("host_projection_digest_invalid")
        authorization = state["step_authorization"]
        checks = {
            "source_supervisor_bundle_digest": authorization["source_supervisor_bundle_digest"],
            "selected_job_id": authorization["host_job_id"],
            "selected_step_id": authorization["host_step_id"],
            "selected_operation_id": state["operation_id"],
        }
        for field, expected in checks.items():
            if projection.get(field) != expected:
                raise ValueError(f"host_projection_{field}_mismatch")
        if projection.get("adapter_state") != "work_ready":
            raise ValueError("host_projection_not_work_ready")
        state["host_projection"] = deepcopy(dict(projection))
        state["host_projection_digest"] = projection["projection_digest"]
        return

    if phase == "invoke":
        host_tick = payload.get("host_tick")
        if not isinstance(host_tick, Mapping):
            raise ValueError("host_tick_required")
        if host_tick.get("version") != TICK_VERSION:
            raise ValueError("host_tick_version_invalid")
        if host_tick.get("host_tick_digest") != tick_digest(host_tick):
            raise ValueError("host_tick_digest_invalid")
        receipt = host_tick.get("receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("host_receipt_required")
        if receipt.get("version") != RECEIPT_VERSION:
            raise ValueError("host_receipt_version_invalid")
        if receipt.get("host_receipt_digest") != receipt_digest(receipt):
            raise ValueError("host_receipt_digest_invalid")
        if receipt.get("projection_digest") != state["host_projection_digest"]:
            raise ValueError("host_receipt_projection_mismatch")
        if receipt.get("source_supervisor_bundle_digest") != state[
            "source_supervisor_bundle_digest"
        ]:
            raise ValueError("host_receipt_source_bundle_mismatch")
        if receipt.get("job_id") != state["step_authorization"]["host_job_id"]:
            raise ValueError("host_receipt_job_mismatch")
        for field, expected in HOST_NON_AUTHORITY.items():
            if receipt.get(field) != expected or host_tick.get(field) != expected:
                raise ValueError("lower_host_authority_escalation")
        if receipt.get("one_job_claimed_at_most") is not True:
            raise ValueError("host_receipt_job_bound_invalid")
        if receipt.get("one_bounded_slice_run_at_most") is not True:
            raise ValueError("host_receipt_slice_bound_invalid")
        state["host_tick"] = deepcopy(dict(host_tick))
        state["host_tick_digest"] = host_tick["host_tick_digest"]
        state["host_receipt"] = deepcopy(dict(receipt))
        state["host_receipt_digest"] = receipt["host_receipt_digest"]
        state["host_invocation_digest"] = require_string(
            receipt.get("invocation_digest"), "host_invocation_digest"
        )
        state["result_supervisor_bundle_digest"] = str(
            receipt.get("result_supervisor_bundle_digest", "")
        )
        state["completed_step_ids"] = list(receipt.get("completed_step_ids_in_slice", []))
        state["blockers"] = list(receipt.get("blockers", []))
        return

    if phase == "verify":
        require_string(payload.get("verification_receipt_digest"), "verification_receipt_digest")
        receipt = state["host_receipt"]
        status = receipt.get("status")
        if status == HOST_READY:
            expected_host_step = state["step_authorization"]["host_step_id"]
            if expected_host_step not in set(state["completed_step_ids"]):
                raise ValueError("authorized_host_step_not_completed")
            if not state["result_supervisor_bundle_digest"]:
                raise ValueError("result_supervisor_bundle_digest_missing")
            state["route"] = "EFFECT_RECORDED"
            state["effect_recorded"] = True
            state["observation_required"] = True
            state["verification_required"] = True
        elif status == HOST_BLOCKED:
            state["route"] = "BLOCKED"
            state["effect_recorded"] = False
        elif status == HOST_REPLAYED:
            state["route"] = "REPLAYED"
            state["effect_recorded"] = False
            state["observation_required"] = True
            state["verification_required"] = True
        else:
            raise ValueError("host_receipt_status_invalid")
        state["act_verification_receipt_digest"] = payload["verification_receipt_digest"]
        return

    if phase == "commit":
        required = {
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_plan_completion": False,
            "automatic_rollback": False,
            "lower_host_receipt_canonical": True,
            "source_lineage_preserved": True,
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"act_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("act_commit_authority_escalation")
        if state["route"] == "PENDING":
            raise ValueError("act_route_not_resolved")
        return

    raise ValueError("act_target_phase_unsupported")


def _result(
    *, status: str, state: Mapping[str, Any], event_id: str, predecessor: str, errors: list[str]
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "act_event_digest": event_id,
        "predecessor_act_state_digest": predecessor,
        "result_act_state_digest": state["act_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "act_apply_result_digest": "",
    }
    packet["act_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_act_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_act_state(state)
    if state_errors:
        raise ValueError("invalid_act_state:" + ";".join(state_errors))
    event_id = str(event.get("act_event_digest", ""))
    predecessor = str(state["act_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED", state=state, event_id=event_id, predecessor=predecessor, errors=[]
        )
    errors = _validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED", state=state, event_id=event_id, predecessor=predecessor, errors=errors
        )
    next_state = deepcopy(dict(state))
    phase = str(event["target_phase"])
    try:
        _apply_payload(next_state, phase, dict(event.get("payload", {})), int(event["created_at_ms"]))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_act_state_digest"] = predecessor
    next_state["current_phase"] = phase
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(next_state["processed_event_digests"]) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": phase,
            "artifact_digest": event["artifact_digest"],
            "act_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if phase == "commit":
        next_state["act_version"] += 1
        next_state["committed_records"] += 1
        next_state["record_summaries"] = list(next_state["record_summaries"]) + [
            {
                "act_version": next_state["act_version"],
                "route": next_state["route"],
                "selected_step_id": next_state["selected_step_id"],
                "operation_id": next_state["operation_id"],
                "host_invocation_digest": next_state["host_invocation_digest"],
                "host_receipt_digest": next_state["host_receipt_digest"],
                "effect_recorded": next_state["effect_recorded"],
                "observation_required": next_state["observation_required"],
                "verification_required": next_state["verification_required"],
            }
        ]
    next_state["act_state_digest"] = ""
    next_state["act_state_digest"] = state_digest(next_state)
    next_errors = validate_act_state(next_state)
    if next_errors:
        raise ValueError("next_act_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED", state=next_state, event_id=event_id, predecessor=predecessor, errors=[]
    )


def build_authorized_invoke_event(
    *,
    state: Mapping[str, Any],
    supervisor_bundle: Mapping[str, Any],
    worker_id: str,
    now_ms: int,
    supervisor_policy: Mapping[str, Any],
    registry: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = validate_act_state(state)
    if errors:
        raise ValueError("invalid_act_state:" + ";".join(errors))
    if state.get("current_phase") != "project":
        raise ValueError("act_invoke_requires_project_phase")
    if supervisor_bundle.get("supervisor_bundle_digest") != bundle_digest(supervisor_bundle):
        raise ValueError("supervisor_bundle_digest_invalid")
    if supervisor_bundle.get("supervisor_bundle_digest") != state[
        "source_supervisor_bundle_digest"
    ]:
        raise ValueError("supervisor_bundle_authorization_mismatch")
    authorization = state["step_authorization"]
    tick = run_host_tick(
        supervisor_bundle=supervisor_bundle,
        projection=state["host_projection"],
        host_license=state["host_license"],
        worker_id=require_string(worker_id, "worker_id"),
        invocation_id=authorization["invocation_id"],
        now_ms=require_int(now_ms, "now_ms"),
        supervisor_policy=supervisor_policy,
        registry=registry,
    )
    event = build_act_event(
        state=state,
        target_phase="invoke",
        artifact_digest=sha(
            {
                "host_tick_digest": tick.get("host_tick_digest", ""),
                "authorization_digest": state["step_authorization_digest"],
            }
        ),
        payload={"host_tick": tick},
        now_ms=now_ms,
    )
    return event, tick
