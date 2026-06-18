from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_multigeneration_kernel_v0_6 import (
    validate_multi_generation_state,
)
from runtime.kuuos_plan_os_multigeneration_types_v0_6 import (
    ACTIVE,
    HANDOVER,
    HOLD,
    state_digest as v06_state_digest,
)
from runtime.kuuos_plan_os_reentry_types_v0_7 import (
    ACCEPT_HANDOVER,
    BOUNDARY,
    DECISION_VERSION,
    EVENT_VERSION,
    NON_AUTHORITY,
    RECEIPT_VERSION,
    REENTRY_AUTHORIZED,
    REENTRY_KINDS,
    RESUME_HOLD,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    decision_digest,
    event_digest,
    receipt_digest,
    require_int,
    require_string,
    state_digest,
)

BOUND = "BOUND"
REENTERED = "REENTERED"


def build_reentry_controller_state(
    *, source_terminal_state: Mapping[str, Any], current_owner_id: str, now_ms: int
) -> dict[str, Any]:
    source_errors = validate_multi_generation_state(source_terminal_state)
    if source_errors:
        raise ValueError("v06_terminal_state_invalid:" + ";".join(source_errors))
    if source_terminal_state.get("status") not in {HOLD, HANDOVER}:
        raise ValueError("reentry_source_must_be_hold_or_handover")
    completed = int(source_terminal_state["completed_generations"])
    maximum = int(dict(source_terminal_state["policy"])["maximum_generations"])
    if completed >= maximum:
        raise ValueError("reentry_generation_capacity_exhausted")
    state = {
        "version": STATE_VERSION,
        "controller_id": "reentry:" + source_terminal_state["supervisor_id"],
        "supervisor_id": source_terminal_state["supervisor_id"],
        "lineage_id": source_terminal_state["lineage_id"],
        "mission_contract_digest": source_terminal_state["mission_contract_digest"],
        "policy_digest": source_terminal_state["policy_digest"],
        "source_terminal_status": source_terminal_state["status"],
        "source_terminal_state_digest": source_terminal_state[
            "multi_generation_supervisor_state_digest"
        ],
        "source_terminal_state": deepcopy(dict(source_terminal_state)),
        "current_owner_id": require_string(current_owner_id, "current_owner_id"),
        "status": BOUND,
        "event_index": 0,
        "processed_receipt_digests": [],
        "target_active_state": None,
        "created_at_ms": require_int(now_ms, "now_ms"),
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "reentry_controller_state_digest": "",
    }
    state["reentry_controller_state_digest"] = state_digest(state)
    return state


def validate_reentry_controller_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("reentry_controller_version_invalid")
        if state.get("reentry_controller_state_digest") != state_digest(state):
            errors.append("reentry_controller_digest_invalid")
        for field in (
            "controller_id",
            "supervisor_id",
            "lineage_id",
            "mission_contract_digest",
            "policy_digest",
            "source_terminal_state_digest",
            "current_owner_id",
        ):
            require_string(state.get(field), field)
        source = dict(state.get("source_terminal_state", {}))
        source_errors = validate_multi_generation_state(source)
        if source_errors:
            errors.extend(source_errors)
        if source.get("status") not in {HOLD, HANDOVER}:
            errors.append("reentry_source_status_invalid")
        if source.get("multi_generation_supervisor_state_digest") != state.get(
            "source_terminal_state_digest"
        ):
            errors.append("reentry_source_digest_binding_invalid")
        for field in ("supervisor_id", "lineage_id", "mission_contract_digest", "policy_digest"):
            if source.get(field) != state.get(field):
                errors.append(f"reentry_source_{field}_binding_invalid")
        status = state.get("status")
        if status not in {BOUND, REENTERED}:
            errors.append("reentry_controller_status_invalid")
        event_index = require_int(state.get("event_index"), "event_index")
        processed = list(state.get("processed_receipt_digests", []))
        if len(processed) != event_index or len(processed) != len(set(processed)):
            errors.append("reentry_receipt_consumption_invalid")
        target = state.get("target_active_state")
        if status == BOUND:
            if event_index != 0 or target is not None:
                errors.append("reentry_bound_state_mutated")
        if status == REENTERED:
            if event_index != 1 or not isinstance(target, dict):
                errors.append("reentry_target_state_required")
            else:
                target_errors = validate_multi_generation_state(target)
                if target_errors:
                    errors.extend(target_errors)
                if target.get("status") != ACTIVE:
                    errors.append("reentry_target_not_active")
                if target.get("next_generation_authorized") is not True:
                    errors.append("reentry_target_generation_not_authorized")
        for field, expected in {
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if state.get(field) != expected:
                errors.append(f"reentry_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("reentry_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("reentry_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_external_reentry_receipt(
    *,
    controller_state: Mapping[str, Any],
    kind: str,
    proposed_owner_id: str,
    delegated_by_owner_id: str,
    accepted_by_owner_id: str,
    authority_scope_digest: str,
    evidence_digest: str,
    issued_at_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    state_errors = validate_reentry_controller_state(controller_state)
    if state_errors:
        raise ValueError("reentry_controller_state_invalid:" + ";".join(state_errors))
    if controller_state.get("status") != BOUND:
        raise ValueError("reentry_controller_already_consumed")
    if kind not in REENTRY_KINDS:
        raise ValueError("reentry_kind_invalid")
    issued = require_int(issued_at_ms, "issued_at_ms")
    expires = require_int(expires_at_ms, "expires_at_ms")
    if expires <= issued:
        raise ValueError("reentry_receipt_expiry_invalid")
    receipt = {
        "version": RECEIPT_VERSION,
        "kind": kind,
        "controller_id": controller_state["controller_id"],
        "supervisor_id": controller_state["supervisor_id"],
        "lineage_id": controller_state["lineage_id"],
        "mission_contract_digest": controller_state["mission_contract_digest"],
        "policy_digest": controller_state["policy_digest"],
        "source_terminal_status": controller_state["source_terminal_status"],
        "source_terminal_state_digest": controller_state[
            "source_terminal_state_digest"
        ],
        "current_owner_id": controller_state["current_owner_id"],
        "proposed_owner_id": require_string(proposed_owner_id, "proposed_owner_id"),
        "delegated_by_owner_id": require_string(
            delegated_by_owner_id, "delegated_by_owner_id"
        ),
        "accepted_by_owner_id": require_string(
            accepted_by_owner_id, "accepted_by_owner_id"
        ),
        "authority_scope_digest": require_string(
            authority_scope_digest, "authority_scope_digest"
        ),
        "evidence_digest": require_string(evidence_digest, "evidence_digest"),
        "issued_at_ms": issued,
        "expires_at_ms": expires,
        "single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "external_reentry_receipt_digest": "",
    }
    receipt["external_reentry_receipt_digest"] = receipt_digest(receipt)
    return receipt


def validate_external_reentry_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("external_reentry_receipt_version_invalid")
        if receipt.get("external_reentry_receipt_digest") != receipt_digest(receipt):
            errors.append("external_reentry_receipt_digest_invalid")
        if receipt.get("kind") not in REENTRY_KINDS:
            errors.append("external_reentry_kind_invalid")
        for field in (
            "controller_id",
            "supervisor_id",
            "lineage_id",
            "mission_contract_digest",
            "policy_digest",
            "source_terminal_status",
            "source_terminal_state_digest",
            "current_owner_id",
            "proposed_owner_id",
            "delegated_by_owner_id",
            "accepted_by_owner_id",
            "authority_scope_digest",
            "evidence_digest",
        ):
            require_string(receipt.get(field), field)
        issued = require_int(receipt.get("issued_at_ms"), "issued_at_ms")
        expires = require_int(receipt.get("expires_at_ms"), "expires_at_ms")
        if expires <= issued:
            errors.append("external_reentry_expiry_invalid")
        if receipt.get("single_use") is not True:
            errors.append("external_reentry_single_use_required")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite"):
            if receipt.get(field) is not False:
                errors.append(f"external_reentry_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("external_reentry_non_authority_invalid")
        if dict(receipt.get("boundary", {})) != BOUNDARY:
            errors.append("external_reentry_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_reentry_decision(
    *, controller_state: Mapping[str, Any], receipt: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    state_errors = validate_reentry_controller_state(controller_state)
    if state_errors:
        raise ValueError("reentry_controller_state_invalid:" + ";".join(state_errors))
    receipt_errors = validate_external_reentry_receipt(receipt)
    if receipt_errors:
        raise ValueError("external_reentry_receipt_invalid:" + ";".join(receipt_errors))
    if controller_state.get("status") != BOUND:
        raise ValueError("reentry_controller_already_consumed")
    now = require_int(now_ms, "now_ms")
    if now < int(receipt["issued_at_ms"]) or now >= int(receipt["expires_at_ms"]):
        raise ValueError("external_reentry_receipt_not_current")
    for field in (
        "controller_id",
        "supervisor_id",
        "lineage_id",
        "mission_contract_digest",
        "policy_digest",
        "source_terminal_status",
        "source_terminal_state_digest",
        "current_owner_id",
    ):
        if receipt.get(field) != controller_state.get(field):
            raise ValueError(f"external_reentry_{field}_mismatch")
    kind = receipt["kind"]
    current = controller_state["current_owner_id"]
    proposed = receipt["proposed_owner_id"]
    if kind == RESUME_HOLD:
        if controller_state["source_terminal_status"] != HOLD:
            raise ValueError("hold_resume_requires_hold_state")
        if not (
            proposed == current
            and receipt["delegated_by_owner_id"] == current
            and receipt["accepted_by_owner_id"] == current
        ):
            raise ValueError("hold_resume_requires_same_owner")
    if kind == ACCEPT_HANDOVER:
        if controller_state["source_terminal_status"] != HANDOVER:
            raise ValueError("handover_acceptance_requires_handover_state")
        if proposed == current:
            raise ValueError("handover_requires_distinct_new_owner")
        if receipt["delegated_by_owner_id"] != current:
            raise ValueError("handover_outgoing_delegation_mismatch")
        if receipt["accepted_by_owner_id"] != proposed:
            raise ValueError("handover_incoming_acceptance_mismatch")
    decision = {
        "version": DECISION_VERSION,
        "controller_id": controller_state["controller_id"],
        "receipt_digest": receipt["external_reentry_receipt_digest"],
        "decision": REENTRY_AUTHORIZED,
        "kind": kind,
        "previous_owner_id": current,
        "next_owner_id": proposed,
        "source_terminal_state_digest": controller_state[
            "source_terminal_state_digest"
        ],
        "next_generation_authorized": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "decided_at_ms": now,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "reentry_decision_digest": "",
    }
    decision["reentry_decision_digest"] = decision_digest(decision)
    return decision


def build_reentry_event(
    *, controller_state: Mapping[str, Any], receipt: Mapping[str, Any], decision: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    if decision.get("receipt_digest") != receipt.get("external_reentry_receipt_digest"):
        raise ValueError("reentry_event_receipt_decision_mismatch")
    event = {
        "version": EVENT_VERSION,
        "controller_id": controller_state["controller_id"],
        "event_index": int(controller_state["event_index"]) + 1,
        "predecessor_state_digest": controller_state[
            "reentry_controller_state_digest"
        ],
        "receipt": deepcopy(dict(receipt)),
        "decision": deepcopy(dict(decision)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "reentry_event_digest": "",
    }
    event["reentry_event_digest"] = event_digest(event)
    return event


def apply_reentry_event(
    controller_state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_reentry_controller_state(controller_state)
    if state_errors:
        raise ValueError("reentry_controller_state_invalid:" + ";".join(state_errors))
    receipt = dict(event.get("receipt", {}))
    receipt_id = str(receipt.get("external_reentry_receipt_digest", ""))
    if receipt_id in set(controller_state.get("processed_receipt_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(dict(controller_state)), "errors": []}
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("reentry_event_version_invalid")
    if event.get("reentry_event_digest") != event_digest(event):
        errors.append("reentry_event_digest_invalid")
    if event.get("controller_id") != controller_state.get("controller_id"):
        errors.append("reentry_event_controller_mismatch")
    if event.get("event_index") != int(controller_state.get("event_index", -1)) + 1:
        errors.append("reentry_event_index_invalid")
    if event.get("predecessor_state_digest") != controller_state.get(
        "reentry_controller_state_digest"
    ):
        errors.append("reentry_event_predecessor_invalid")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(dict(controller_state)), "errors": errors}
    decision = dict(event.get("decision", {}))
    try:
        expected = build_reentry_decision(
            controller_state=controller_state,
            receipt=receipt,
            now_ms=int(decision.get("decided_at_ms", -1)),
        )
    except (TypeError, ValueError) as exc:
        return {"status": "REJECTED", "state": deepcopy(dict(controller_state)), "errors": [str(exc)]}
    if expected.get("reentry_decision_digest") != decision.get("reentry_decision_digest"):
        return {"status": "REJECTED", "state": deepcopy(dict(controller_state)), "errors": ["reentry_decision_not_canonical"]}
    target = deepcopy(dict(controller_state["source_terminal_state"]))
    target["status"] = ACTIVE
    target["terminal_reason"] = ""
    target["next_generation_authorized"] = True
    target["updated_at_ms"] = int(event["created_at_ms"])
    target["multi_generation_supervisor_state_digest"] = ""
    target["multi_generation_supervisor_state_digest"] = v06_state_digest(target)
    target_errors = validate_multi_generation_state(target)
    if target_errors:
        raise ValueError("reentry_target_state_invalid:" + ";".join(target_errors))
    next_state = deepcopy(dict(controller_state))
    next_state["status"] = REENTERED
    next_state["current_owner_id"] = decision["next_owner_id"]
    next_state["event_index"] = 1
    next_state["processed_receipt_digests"] = [receipt_id]
    next_state["target_active_state"] = target
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["reentry_controller_state_digest"] = ""
    next_state["reentry_controller_state_digest"] = state_digest(next_state)
    next_errors = validate_reentry_controller_state(next_state)
    if next_errors:
        raise ValueError("reentry_next_state_invalid:" + ";".join(next_errors))
    return {"status": "APPLIED", "state": next_state, "errors": []}
